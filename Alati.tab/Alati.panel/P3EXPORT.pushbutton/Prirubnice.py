# This Python file uses the following encoding: utf-8
class P3Prirubnica():
    def __init__(self, TipPrirubnice, Duzina):
        self.TipPrirubnice=TipPrirubnice
        self.Duzina=Duzina

    def __str__(self):
        s=self.TipPrirubnice +' : '+ str(self.Duzina)
        return s

# CITAC KONEKTORA JE FUKNCIJA KOJA CITA I PRETVARA PROCITANU VREDNOST IZ REVITA U JEDINICI FEET I PRETVARA U MILIMETRE. TAKO RADI ZA SVAKU VRSTU PROFILA
def CitacKonektoraS(Konektor): 
    '''
    OVA FUNKCIJA CITA DIMENZIJE KONEKTORA, I PRAVI OBJEKTE KLASE P3Prirubnica, SA TIPOM 'S' I DIMENZIJOM.
    '''    
    P1=[P3Prirubnica('S',Konektor.Width*304.8-2) for i in range(2)] 
    P2=[P3Prirubnica('S',Konektor.Height*304.8-2) for i in range(2)]
    return P1+P2    
def CitacKonektoraB(Konektor): 
    '''
    OVA FUNKCIJA CITA DIMENZIJE KONEKTORA, I PRAVI OBJEKTE KLASE P3Prirubnica, SA TIPOM 'B' I DIMENZIJOM.-spojnica
    '''    
    if (Konektor.Width*304.8)>(Konektor.Height*304.8):
        B1=[P3Prirubnica('B',Konektor.Width*304.8+23+40)]
        B2=[P3Prirubnica('B',Konektor.Height*304.8+11+40)]
    else:
        B1=[P3Prirubnica('B',Konektor.Width*304.8+11+40)]
        B2=[P3Prirubnica('B',Konektor.Height*304.8+23+40)]
    return B1+B2  
def CitacKonektoraU_UBOD(Konektor):
    '''
    OVA FUNKCIJA CITA DIMENZIJE KONEKTORA, I PRAVI OBJEKTE KLASE P3Prirubnica, SA TIPOM 'U-UBOD' I DIMENZIJOM.
    '''  
    P1=[P3Prirubnica('U',Konektor.Width*304.8+100-2) for i in range(2)] 
    P2=[P3Prirubnica('U',Konektor.Height*304.8-2) for i in range(2)] 
    return P1+P2  
def CitacKonektoraU(Konektor):
    '''
    OVA FUNKCIJA CITA DIMENZIJE KONEKTORA, I PRAVI OBJEKTE KLASE P3Prirubnica, SA TIPOM 'U' I DIMENZIJOM.
    '''  
    P1=[P3Prirubnica('U',Konektor.Width*304.8-2) for i in range(2)] 
    P2=[P3Prirubnica('U',Konektor.Height*304.8-2) for i in range(2)] 
    return P1+P2   
def CitacKonektoraF(Konektor):
    '''
    OVA FUNKCIJA CITA DIMENZIJE KONEKTORA, I PRAVI OBJEKTE KLASE P3Prirubnica, SA TIPOM 'F' I DIMENZIJOM.
    '''  
    P1=[P3Prirubnica('F',Konektor.Width*304.8-2) for i in range(2)] 
    P2=[P3Prirubnica('F',Konektor.Height*304.8-2) for i in range(2)] 
    return P1+P2   
def CitacKonektoraF_UBOD(Konektor):
    '''
    OVA FUNKCIJA CITA DIMENZIJE KONEKTORA, I PRAVI OBJEKTE KLASE P3Prirubnica, SA TIPOM 'F-UBOD' I DIMENZIJOM.
    '''  
    P1=[P3Prirubnica('F',Konektor.Width*304.8+100-2) for i in range(2)] 
    P2=[P3Prirubnica('F',Konektor.Height*304.8-2) for i in range(2)] 
    return P1+P2   
    
def NadjiPrirubnice(element):
    '''
    OVA FUNNKCIJA NA ULAZU OCEKUJE REVIT ELEMENT, A NA IZLAZU DOBIJA LISTU PRIRUBNICA , SVAKU POJEDINACNO (TIP,DUZINA)
    '''
    from  Autodesk.Revit.DB import BuiltInParameter
    from  Autodesk.Revit.DB import PartType
    doc=__revit__.ActiveUIDocument.Document 
    dozvoljenaKategorija=['Duct Fittings',  'Duct Accessories', 'Air Terminals', 'Ducts','Mechanical Equipment']
    konektori=[]
    Nekonektovani=[]
    #ISPITUJE SE ELEMENT NA ULAZU FUNKCIJE KOJE JE KATEGORIJE - U ZAVISNOSTI OD KATEGORIJE DRUGACIJE SE CITA KOJI SU KONEKTORI
    if element.Category.Name=='Duct Fittings': 
        k=element.MEPModel.ConnectorManager.Connectors		
        TipElementa=doc.GetElement(element.GetTypeId())
        KODelementa=TipElementa.GetParameters('P3 - Code')[0].AsInteger() # Ne treba Try jer je na ulazu element koji sigurno ima vrednost P3Code-a
        if KODelementa == 843:       #Ukoliko je Cap element funkcije ovim se prekida i vraca praznu listu nastavku programa . 
            return []   
    elif element.Category.Name=='Ducts':
        k=element.ConnectorManager.Connectors
        dozvoljenaKategorija=dozvoljenaKategorija[0:3]
        KODelementa=None
    else: 
        print('Kategorija elementa nije dobra')
        exit(1)
    for ElKon in k:
        if ElKon.IsConnected:
            konektori.append(ElKon)
        else:
            Nekonektovani.append(ElKon)
    if len(Nekonektovani) != 0:  #AKO JE LISTA NEKONEKTOVANIH KONEKTORA VECA OD 0 , FUNKCIJA VRACA FALSE I PREKIDA SE ZA TAJ ELEMENT.
        return False
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
                            PRIRUBNICElista.extend(CitacKonektoraB(Kon))
                        elif paramF == 812 and Par.GetMEPConnectorInfo().IsPrimary:  # U ovom slucaju se uzima konektovani konektor cipelice (PAR) jer konektor uboda cita dimenziju kanala a ne otvora od cipelice
                            PRIRUBNICElista.extend(CitacKonektoraU_UBOD(Par))   # OTVOR U KANALU ZA UBOD CIPELICE  -uvecava se za 100
                        elif model == 'P3-TAP' and Par.GetMEPConnectorInfo().IsPrimary:
                            PRIRUBNICElista.extend(CitacKonektoraU(Par))   # OTVOR U KANALU ZA Direktan UBOD -MAGI UBOD
                        elif paramF ==812 and not Par.GetMEPConnectorInfo().IsPrimary:
                            PRIRUBNICElista.extend(CitacKonektoraS(Kon))
                            PRIRUBNICElista.extend(CitacKonektoraB(Kon))
                        elif model == 'P3-TAP'and not Par.GetMEPConnectorInfo().IsPrimary:
                            PRIRUBNICElista.extend(CitacKonektoraF(Kon))
                        elif paramF ==843:
                            UklonjeniKonektori.append(Kon) # ODSTRANJUJE SE KONEKTOR KOJI PRIPADA END CAP-u ili CEPU JER NA NJEGA NE IDE PRIRUBNICA
                        elif Par.Owner.MEPModel.PartType == PartType.Union or paramF:
                            PRIRUBNICElista.extend(CitacKonektoraS(Kon))
                            PRIRUBNICElista.extend(CitacKonektoraB(Kon))
                elif Par.Owner.Category.Name == 'Ducts':
                    if KODelementa == 812 and Kon.GetMEPConnectorInfo().IsPrimary:   #ako je primaran konektor elementa onda je ubod u kanal , u svakom drugom slucaju ako je P3 kanal onda je  S
                        PRIRUBNICElista.extend(CitacKonektoraF_UBOD(Kon))     #UBOD CIPELICE U KANAL- uvecava se za 100
                    elif model == 'P3 - Rectangular':
                        PRIRUBNICElista.extend(CitacKonektoraS(Kon))
                        PRIRUBNICElista.extend(CitacKonektoraB(Kon))
                elif Par.Owner.Category.Name == 'Duct Accessories':
                    try:
                        paramDA=Par.Owner.GetParameters('TK_SetTipPrirubnice')[0].AsString()
                        if paramDA.upper()=='U':
                            PRIRUBNICElista.extend(CitacKonektoraU(Kon))
                        elif paramDA.upper()=='F':
                            PRIRUBNICElista.extend(CitacKonektoraF(Kon))
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

if __name__=='__main__':   #TEST PROGRAM KOJI TESTIRA FUNKCIJU NadjiPrirubnice NA POJEDINACNOM ELEMENTU A ZATIM PRAVI PRIRPREMLJENU LISTU ZA IZLAZ I ISPIS.

    def PrebrojUnikate(lista):
        '''
    OVA FUNKCIJA TRAZI UNIKATE I PREBROJAVA IH.VRACA DICTIONARY UNIKATA I NJIHOVOG BROJA
        '''
        Unikati={}
        for i in lista:
            if i in Unikati:
                Unikati[i]+=1
            else:
                Unikati[i]=1

        return Unikati

    PrirubniceS=[]
    PrirubniceU=[]
    PrirubniceF=[]
    PrirubniceB=[]
    try:
        p=NadjiPrirubnice(a)
        for j in p:  #PRIRUBNICE SE RAYVRSTAVAJU PO TIPU U PRIRPADAJUCE LISTE
            if j.TipPrirubnice == 'S':
                PrirubniceS.append(int(j.Duzina))
            elif j.TipPrirubnice == 'U':
                PrirubniceU.append(int(j.Duzina))
            elif j.TipPrirubnice == 'F':
                PrirubniceF.append(int(j.Duzina))  
            elif j.TipPrirubnice == 'B':
                PrirubniceB.append(int(j.Duzina)) 
                
        #PRAVE SE LISTE STRINGOVA NASLOVA KOLONA, PO DVA ELEMENTA DA BI SE UPISALO U EKSEL U DVA REDA
        stringSlist=[['TIP PROFILA : ','U172P2'],['dužina (mm)','kom.']]
        unikatiSdict=PrebrojUnikate(PrirubniceS)
        stringUlist=[['TIP PROFILA : ','U172P1'],['dužina (mm)','kom.']]
        unikatiUdict=PrebrojUnikate(PrirubniceU)
        stringFlist=[['TIP PROFILA : ','F - dostavlja TERMOVENT'],['dužina (mm)','kom.']]
        unikatiFdict=PrebrojUnikate(PrirubniceF)
        stringBlist=[['TIP PROFILA : ','U172P3'],['dužina (mm)','kom.']]
        unikatiBdict=PrebrojUnikate(PrirubniceB)

        #AKO JE JEDNA OD LISTA PRAZNA ,ONDA SE NI NASLOV NE ISPISUJE
        if len(PrirubniceS) != 0:
            listaS=stringSlist+[[i,unikatiSdict[i]] for i in unikatiSdict]
        else:
            listaS=[]
        if len(PrirubniceU) != 0:
            listaU=stringUlist+[[i,unikatiUdict[i]] for i in unikatiUdict]
        else:
            listaU=[]
        if len(PrirubniceF) != 0:
            listaF=stringFlist+[[i,unikatiFdict[i]] for i in unikatiFdict]
        else:
            listaF=[]
        if len(PrirubniceB) != 0:
            listaB=stringBlist+[[i,unikatiBdict[i]] for i in unikatiBdict]
        else:
            listaB=[]

        listaZaEksport=listaU+listaS+listaF+listaB    #LISTA NAPRAVLJENA DA BI SE U OVAKVOM FORMATU PROSLEDILA FUNKCIJI ZA UPIS U EKSEL

        print('S')
        print(unikatiSdict)
        print('U')
        print(unikatiUdict)
        print('F')
        print(unikatiFdict)
        print('B')
        print(unikatiBdict)

    except:
        print('Елемент: ID(' + str(a.Id) +') није добро повезан (СТАВИТИ ЧЕП АКО ЈЕ ОСТАЈЕ НЕПОВЕЗАН)' )


