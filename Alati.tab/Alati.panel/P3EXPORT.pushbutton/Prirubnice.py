class P3Prirubnica():
    def __init__(self, TipPrirubnice, Duzina):
        self.TipPrirubnice=TipPrirubnice
        self.Duzina=Duzina

    def __str__(self):
        s=self.TipPrirubnice +' : '+ str(self.Duzina)
        return s


def CitacKonektoraS(Konektor):
    P1=[P3Prirubnica('S',Konektor.Width*304.8) for i in range(2)] 
    P2=[P3Prirubnica('S',Konektor.Height*304.8) for i in range(2)] 
    return P1+P2      
def CitacKonektoraU_UBOD(Konektor):
    P1=[P3Prirubnica('U',Konektor.Width*304.8+100) for i in range(2)] 
    P2=[P3Prirubnica('U',Konektor.Height*304.8) for i in range(2)] 
    return P1+P2  
def CitacKonektoraU(Konektor):
    P1=[P3Prirubnica('U',Konektor.Width*304.8) for i in range(2)] 
    P2=[P3Prirubnica('U',Konektor.Height*304.8) for i in range(2)] 
    return P1+P2   
def CitacKonektoraF(Konektor):
    P1=[P3Prirubnica('F',Konektor.Width*304.8) for i in range(2)] 
    P2=[P3Prirubnica('F',Konektor.Height*304.8) for i in range(2)] 
    return P1+P2   
def CitacKonektoraF_UBOD(Konektor):
    P1=[P3Prirubnica('F',Konektor.Width*304.8+100) for i in range(2)] 
    P2=[P3Prirubnica('F',Konektor.Height*304.8) for i in range(2)] 
    return P1+P2   
def NadjiPrirubnice(element):
    from  Autodesk.Revit.DB import BuiltInParameter
    from  Autodesk.Revit.DB import PartType
    doc=__revit__.ActiveUIDocument.Document 
    dozvoljenaKategorija=['Duct Fittings',  'Duct Accessories', 'Air Terminals', 'Ducts','Mechanical Equipment']
    #ISPITUJE SE ELEMENT NA ULAZU FUNKCIJE KOJE JE KATEGORIJE - U ZAVISNOSTI OD KATEGORIJE DRUGACIJE SE CITA KOJI SU KONEKTORI
    if element.Category.Name=='Duct Fittings': 
        k=element.MEPModel.ConnectorManager.Connectors		
        TipElementa=doc.GetElement(element.GetTypeId())
        KODelementa=TipElementa.GetParameters('P3 - Code')[0].AsInteger() # Ne treba Try jer je na ulazu element koji sigurno ima vrednost P3Code-a
    elif element.Category.Name=='Ducts':
        k=element.ConnectorManager.Connectors
        dozvoljenaKategorija=dozvoljenaKategorija[0:3]
        KODelementa=None
    else: 
        print('Kategorija elementa nije dobra')
        exit(1)
    konektori=[ElKon for ElKon in k if ElKon.IsConnected]
    PRIRUBNICElista=[]
    UklonjeniKonektori=[]
    for Kon in konektori:  #PROLAZI SE KROZ SVAKI KONEKTOR ELEMENTA
        for Par in Kon.AllRefs:  #PROLAZI SE KROZ SVE UPARENE KONEKTORE TOG KONEKTORA (MOZE BITI VISE KONEKTORA KONEKTOVANO NA OVAJ KONEKTOR npr. IZOLACIJA)
            if Par.Owner.Category.Name in dozvoljenaKategorija:  # ISPITUJE SE DA LI JE KONEKTOVANI ELEMENT U DOZVOLJENIM KATEGORIJAMA
                tip=doc.GetElement(Par.Owner.GetTypeId())     #CITA SE TIP KONEKTOVANOG FITINGA
                model=tip.get_Parameter(BuiltInParameter.ALL_MODEL_MODEL).AsString()  #CITA SE MODEL TIPA KONEKTOVANOG FITINGA
                if Par.Owner.Category.Name == 'Duct Fittings':
                    try:
                        paramF=tip.GetParameters('P3 - Code')[0].AsInteger()
                    except:
                        paramF=None
                    finally:
                        if KODelementa == 812 and not Kon.GetMEPConnectorInfo().IsPrimary:
                            PRIRUBNICElista.extend(CitacKonektoraS(Kon))
                        elif paramF ==812 and Par.GetMEPConnectorInfo().IsPrimary:
                            PRIRUBNICElista.extend(CitacKonektoraU_UBOD(Kon))   # OTVOR U KANALU ZA UBOD CIPELICE  -uvecava se za 100
                        elif model == 'P3-TAP' and Par.GetMEPConnectorInfo().IsPrimary:
                            PRIRUBNICElista.extend(CitacKonektoraU(Kon))   # OTVOR U KANALU ZA Direktan UBOD -MAGI UBOD
                        elif paramF ==812 and not Par.GetMEPConnectorInfo().IsPrimary:
                            PRIRUBNICElista.extend(CitacKonektoraS(Kon))
                        elif model == 'P3-TAP'and not Par.GetMEPConnectorInfo().IsPrimary:
                            PRIRUBNICElista.extend(CitacKonektoraF(Kon))
                        elif paramF ==843:
                            UklonjeniKonektori.append(Kon) # ODSTRANJUJE SE KONEKTOR KOJI PRIPADA END CAP-u ili CEPU JER NA NJEGA NE IDE PRIRUBNICA
                        elif Par.Owner.MEPModel.PartType == PartType.Union or paramF:
                            PRIRUBNICElista.extend(CitacKonektoraS(Kon))
                elif Par.Owner.Category.Name == 'Ducts':
                    if KODelementa == 812 and Kon.GetMEPConnectorInfo().IsPrimary:   #ako je primaran konektor elementa onda je ubod u kanal , u svakom drugom slucaju ako je P3 kanal onda je  S
                        PRIRUBNICElista.extend(CitacKonektoraF_UBOD(Kon))     #UBOD CIPELICE U KANAL- uvecava se za 100
                    elif model == 'P3 - Rectangular':
                        PRIRUBNICElista.extend(CitacKonektoraS(Kon))
                elif Par.Owner.Category.Name == 'Duct Accessories':
                    try:
                        paramDA=Par.Owner.GetParameters('TK_SetTipPrirubnice')[0].AsString()
                        if KODelementa == 812 and not Kon.GetMEPConnectorInfo().IsPrimary:
                            PRIRUBNICElista.extend(CitacKonektoraU(Kon))    #PROVERITI !!!!!
                        elif paramDA.upper()=='U':
                            PRIRUBNICElista.extend(CitacKonektoraU(Kon))
                        elif paramDA.upper()=='F':
                            PRIRUBNICElista.extend(CitacKonektoraF(Kon))
                        else:
                            pass
                    except:
                        PRIRUBNICElista.extend(CitacKonektoraU(Kon)) 
                elif Par.Owner.Category.Name == 'Air Terminals':
                    PRIRUBNICElista.extend(CitacKonektoraF(Kon))

                elif Par.Owner.Category.Name == 'Mechanical Equipment':
                    PRIRUBNICElista.extend(CitacKonektoraU(Kon))
                else:
                    print('KATEGORIJA KONEKTOVANOG ELEMENTA NIJE DOZVOLJENA')
                    exit(1)


    return PRIRUBNICElista

if __name__=='__main__':
    p=NadjiPrirubnice(a)
    print(p)
