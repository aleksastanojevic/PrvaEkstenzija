class P3Prirubnica():
    def __init__(self, TipPrirubnice, Duzina):
        self.TipPrirubnice=TipPrirubnice
        self.Duzina=Duzina

    def __str__(self):
        s=self.TipPrirubnice + ' : ' + self.Duzina
        return s

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
    UklonjeniKonektori=[]
    konS=[]
    konU=[]
    konF=[]
    for Kon in konektori:  #PROLAZI SE KROZ SVAKI KONEKTOR ELEMENTA
        for Par in Kon.AllRefs:  #PROLAZI SE KROZ SVE UPARENE KONEKTORE TOG KONEKTORA (MOZE BITI VISE KONEKTORA KONEKTOVANO NA OVAJ KONEKTOR npr. IZOLACIJA)
            if Par.Owner.Category.Name in dozvoljenaKategorija:  # ISPITUJE SE DA LI JE KONEKTOVANI ELEMENT U DOZVOLJENIM KATEGORIJAMA
                tip=doc.GetElement(Par.Owner.GetTypeId())
                model=tip.get_Parameter(BuiltInParameter.ALL_MODEL_MODEL).AsString()
                if Par.Owner.Category.Name == 'Duct Fittings':
                    try:
                        paramF=tip.GetParameters('P3 - Code')[0].AsInteger()
                    except:
                        paramF=None
                    finally:
                        if KODelementa == 812 and not Kon.GetMEPConnectorInfo().IsPrimary:
                            konS.append(Kon)
                        elif (paramF ==812 or model == 'P3-TAP') and Par.GetMEPConnectorInfo().IsPrimary:
                            konU.append(Kon)   # OTVOR U KANALU ZA UBOD CIPELICE- TREBA PROCITATI IZ FAMILIJE PRAVU DIMENZIJU
                        elif paramF ==812 and not Par.GetMEPConnectorInfo().IsPrimary:
                            konS.append(Kon)
                        elif model == 'P3-TAP'and not Par.GetMEPConnectorInfo().IsPrimary:
                            konF.append(Kon)
                        elif paramF ==843:
                            UklonjeniKonektori.append(Kon) # ODSTRANJUJE SE KONEKTOR KOJI PRIPADA END CAP-u ili CEPU JER NA NJEGA NE IDE PRIRUBNICA
                        elif paramF:
                            konS.append(Kon)
                        elif Par.Owner.MEPModel.PartType == PartType.Union:
                            konS.append(Kon)

                elif Par.Owner.Category.Name == 'Ducts':
                    if KODelementa == 812 and Kon.GetMEPConnectorInfo().IsPrimary:   #ako je primaran konektor elementa onda je ubod u kanal , u svakom drugom slucaju ako je P3 kanal onda je  S
                        konF.append(Kon)          #UBOD CIPELICE U KANAL- DIMENZIJA NIJE DOBRA VEC SE POSEBNO CITA IZ FAMILIJE
                    elif model == 'P3 - Rectangular':
                        konS.append(Kon)

                elif Par.Owner.Category.Name == 'Duct Accessories':
                    try:
                        paramDA=Par.Owner.GetParameters('TK_SetTipPrirubnice')[0].AsString()
                        if KODelementa == 812 and not Kon.GetMEPConnectorInfo().IsPrimary:
                            konU.append(Kon)
                        elif paramDA.upper()=='U':
                            konU.append(Kon)
                        elif paramDA.upper()=='F':
                            konF.append(Kon)
                        else:
                            pass
                    except:
                        konU.append(Kon)
                elif Par.Owner.Category.Name == 'Air Terminals':
                    konF.append(Kon)

                elif Par.Owner.Category.Name == 'Mechanical Equipment':
                    konU.append(Kon)
                else:
                    print('KATEGORIJA KONEKTOVANOG ELEMENTA NIJE DOZVOLJENA')
                    exit(1)
    
    # for i in konS:
    #     P=P3Prirubnica('S',i.Width)


    prirubnice={'S': konS,'U':konU,'F':konF}

    return prirubnice
