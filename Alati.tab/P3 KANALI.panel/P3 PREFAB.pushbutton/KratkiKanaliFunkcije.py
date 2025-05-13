def KratakKanal_DodatakNaFiting(ShortDuct):
    ''' Funkcija kratak kanal na ulazu brise i njegovu duzinu dodaje na jedan ili oba spojena fitinga u zavisnosto od uslova.
    - ShortDuct je instanca kratkog kanala koji je kategorije DUCT FITTING .
    OVA FUNKCIJA MORA BITI IZVRSENA UNUTAR TRANSAKCIJE''' 

    from Autodesk.Revit.DB import ConnectorType, Domain, Line, XYZ #--IMPORTOVANJE NEOPHODNIH MODULA
    doc = __revit__.ActiveUIDocument.Document #--AKTIVNI DOKUMENT
    Konektori=[] #--KONEKTORI KANALA
    PrikljuceniKonektori=[] #--PRIKLJUCENI KONEKTORI FITINGA
    PrikljuceniP3Konektori=[]
    BrP3KonIz=0    # Broj konektora koji su iz P3 porodice i Podlozni su promeni
    DictP3Kodova={802:['P3 - E Line_1','P3 - F Line_2'],
                  823:['P3 - E Line_1','P3 - F Line_2'],
                  847:['P3 - E Line_1','P3 - F Line_2'],
                  813:[],  #PANTALONE NE MOGU JER NEMAJU INDIVIDUALNE PARAMETRE ZA POMERANJE
                  828:['P3 - E Line_1','P3 - F Line_2','P3 - G Line_3'],
                  812:['P3 - E Line_1'],
                  803:['P3 - E Line_1','P3 - F Line_2','P3 - L Line_5'],
                  826:['P3 - F Line2_Lt','P3 - I Line_Rt'],
                  827:['P3 - I Line_5','P3 - F Line_2'],
                  843:[],
                  801:[]}
    
    for conn in ShortDuct.MEPModel.ConnectorManager.Connectors: 
        Konektori.append(conn)   
        for Cconn in conn.AllRefs:
            if Cconn.ConnectorType == ConnectorType.End and Cconn.Domain ==Domain.DomainHvac and Cconn.Owner.Id!= ShortDuct.Id:
                PrikljuceniKonektori.append(Cconn)  #--DODAVANJE PRIKLJUCENIH KONEKTORA FITINGA KAKO BISMO KASNIJE MOGU DA IH SPOJIMO
                try:
                    P3Code=Cconn.Owner.Symbol.GetParameters('P3 - Code')[0].AsInteger()
                    if P3Code in DictP3Kodova.keys() and len(DictP3Kodova[P3Code])>0: #--U SLUCAJU DA JE KONEKTOR U DICTU i DA IMA PROMENLJIVE PARAMETRE
                        PrikljuceniP3Konektori.append(Cconn)
                except:
                    P3Code=None
                    pass

    Dir=Line.CreateBound(Konektori[0].Origin, Konektori[1].Origin).Direction #--DIREKCIJA KONEKTORA
    Distanca=Konektori[0].Origin.DistanceTo(Konektori[1].Origin)
    ParametriZaPromenu=[]
    for konektor in PrikljuceniP3Konektori:   #ITERACIJA KROZ SVE PRIKLJUCENE P3 KONEKTORE
        TrenutniP3Code=konektor.Owner.Symbol.GetParameters('P3 - Code')[0].AsInteger()
        ValidniP3ProduziviParametri=[konektor.Owner.GetParameters(param)[0] for param in DictP3Kodova[TrenutniP3Code] if param] #--VALIDNI PARAMETRI KOJI SU P3 - PRODUZIVI
        try:
            doc.Delete(ShortDuct.Id) #--BRISANJE KRATKOG KANALA
        except:
            pass
        StaraVrednostKonektora=konektor.Origin #--STARA VREDNOST DISTANCE KONEKTORA PRE BRISANJA KRATKOG KANALA
        StaraPozicijaKonektovanogFitinga=konektor.Owner.Location.Point
        for param in ValidniP3ProduziviParametri:
            ParamValue=param.AsDouble() #--VREDNOST PARAMETRA KOJI SE ZOVE P3 - PRODUZIVI
            param.Set(ParamValue+Distanca)  #--SETOVANJE VREDNOSTI PARAMETRA KOJI SE ZOVE P3 - PRODUZIVI sa NOVOM VREDNOSTI
            doc.Regenerate() #--REGENERACIJA DOKUMENTA
            try:
                PravacPomeraja=Line.CreateBound(StaraVrednostKonektora, konektor.Origin).Direction #--PRAVIMO LINIJU KOJA POVEZUJE STARU I NOVU VREDNOST KONEKTORA
            except:
                PravacPomeraja=XYZ(0,0,0)
            if not StaraVrednostKonektora.IsAlmostEqualTo(konektor.Origin) and ( Dir.CrossProduct(PravacPomeraja).IsAlmostEqualTo(XYZ(0,0,0))) and (StaraPozicijaKonektovanogFitinga.IsAlmostEqualTo(konektor.Owner.Location.Point)): #--U SLUCAJU DA JE KONEKTOR PROMENJEN I DA JE U PRAVCU KANALA
                ParametriZaPromenu.append(param)
                param.Set(ParamValue)
                BrP3KonIz+=1
                break
            else:
                param.Set(ParamValue)  #--SETOVANJE VREDNOSTI PARAMETRA KOJI SE ZOVE P3 - PRODUZIVI NA STARU VREDNOST

    if BrP3KonIz==0:
        return False
    elif BrP3KonIz==2:
        Distanca=Distanca/2

    doc.Regenerate()
    for paramN in ParametriZaPromenu:
        PrethodnaVrednost=paramN.AsDouble()
        paramN.Set(PrethodnaVrednost+Distanca)
    if len(PrikljuceniKonektori)==2:  #--U SLUCAJU DA SU DVA FITINGA PRIKLJUCENA NA KRAJEVE KRATKOG KANALA VRSI SE SPAJANJE ISTIH. U SUPROTNOM SE NE SPAJAJU
        PrikljuceniKonektori[0].ConnectTo(PrikljuceniKonektori[1]) 
    return True

if __name__ == '__main__': 
    # Ova funkcija se poziva samo kada se koristi kao samostalan skript.
    # U tom slucaju, ShortDuct je instanca kratkog kanala koji je kategorije DUCT FITTING .
    # KratakKanal_DodatakNaFiting(ShortDuct)
    from Autodesk.Revit.DB import *
    doc = __revit__.ActiveUIDocument.Document
    selektovanoU_revitu=[doc.GetElement(id) for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    Tr=Transaction(doc, "P3 - SPLIT DUCTS")  #--TRANSAKCIJA
    Tr.Start()   #--TRANSAKCIJA
    for ss in selektovanoU_revitu:
        SubTr=SubTransaction(doc)
        SubTr.Start()
        KratakUFiting=KratakKanal_DodatakNaFiting(selektovanoU_revitu[0])
        if KratakUFiting:
            SubTr.Commit()
        else:
            SubTr.RollBack()
    Tr.Commit()

