
def pickobjects(self, sender, event):    #PROMENITI DA BUDE SELEKCIJA ALI SA  FILTEROM KATEGORIJE
    '''
    DOGADJAJ PRITISKOM NA DUGME IZABERI IZ MODELA
    '''
    for c in self.Controls:
        c.Enabled = False
    try:
        from  Autodesk.Revit.UI import Selection
        uidoc=__revit__.ActiveUIDocument
        doc=__revit__.ActiveUIDocument.Document
        sel = uidoc.Selection.PickObjects(Selection.ObjectType.Element,'')
        self.selelem = [doc.GetElement(s.ElementId) for s in sel]
        sender.Tag = (self.selelem)
        self.BringToFront()
    except:
        print('NIJE MOGUC PRISTUP REVITU A')
    for c in self.Controls:
        c.Enabled = True
    
def KolektorSistema():
    '''
    IZ REVITA VRSI SAKUPLJANJE SVIH POSTOJECIH KANALSKIH SISTEMA I NA IZLAZ DAJE DICTIONARY IMENA SISTEMA I SISTEMA
    '''
    imenaSistema={}
    try:
        from  Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
        doc=__revit__.ActiveUIDocument.Document
        KolSis=FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DuctSystem).WhereElementIsNotElementType()
        for sistem in KolSis:	
            if not sistem:
                print('NE POSTOJI NI JEDAN SISTEM' )
            else:
                imenaSistema[sistem.Name]=sistem
        return imenaSistema
    except:
        print('NIJE MOGUC PRISTUP REVITU B')
        return False

def KolektorP3Schedula():
    '''
    IZ REVITA VRSI SAKUPLJANJE SVIH POSTOJECIH SCHEDULA I NA IZLAZ DAJE DICTIONARY IMENA SCHEDULA i SCHEDULA
    '''
    Dozvoljeni=['P3 - Duct Fitting Schedule - Code 802','P3 - Duct Fitting Schedule - Code 803','P3 - Duct Fitting Schedule - Code 804','P3 - Duct Fitting Schedule - Code 827','P3 - Duct Fitting Schedule - Code 843','P3 - Duct Fitting Schedule - Code 847','P3 - Duct Fitting Schedule - Code 853','P3 - Duct Fitting Schedule - Code 854','P3 - Rectangular Duct Schedule','P3 - Duct Fitting Schedule - All']
    imenaSchedula={}
    try:
        from  Autodesk.Revit.DB import FilteredElementCollector,ViewSchedule
        doc=__revit__.ActiveUIDocument.Document
        KolSCH=FilteredElementCollector(doc).OfClass(ViewSchedule)
        for schedule in KolSCH:	
            if not schedule:
                print('NE POSTOJI NI JEDAN SCHEDULE' )
            elif schedule.Name in Dozvoljeni:
                imenaSchedula[schedule.Name]=schedule
        return imenaSchedula
    except:
        print('NIJE MOGUC PRISTUP REVITU C')
        return False

def PretvoriJedinicu(RevitParametar):
    '''
    FUNKCIJA PRETVARA RADIJANE U UGAO ILI FITE U MILIMETRE.
    NA ULAZU POTREBNO DOVESTI Autodesk.Revit.DB.ParameterType.HVACDuctSize ili Angle
    '''
    try:
        import math
        from  Autodesk.Revit.DB import ParameterType
        if RevitParametar.Definition.ParameterType == ParameterType.HVACDuctSize :
            V=RevitParametar.AsDouble()*304.8
        elif RevitParametar.Definition.ParameterType == ParameterType.Length :
            V=RevitParametar.AsDouble()*304.8
        elif RevitParametar.Definition.ParameterType == ParameterType.Angle :
            V=RevitParametar.AsDouble()*180/math.pi
        if round(V,3).is_integer():
            return str(int(round(V,3)))
        else:
            return str(round(V,3))
    except TypeError:  
        return 'GRESKA U PRETVARANJU'


def Prirubnice(element):
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
    KonElementi={}
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
    
    prirubnice={'S': konS,'U':konU,'F':konF}

    return prirubnice
