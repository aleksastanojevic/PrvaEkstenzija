
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
    Dozvoljeni=['P3 - Duct Fitting Schedule - Code 802','P3 - Duct Fitting Schedule - Code 803','P3 - Duct Fitting Schedule - Code 804','P3 - Duct Fitting Schedule - Code 827','P3 - Duct Fitting Schedule - Code 843','P3 - Duct Fitting Schedule - Code 847','P3 - Duct Fitting Schedule - Code 853','P3 - Duct Fitting Schedule - Code 854','P3 - Rectangular Duct Schedule','P3 - Duct Fitting Schedule - All','P3 - Duct Fitting Schedule - Code 812']
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
    NA ULAZU POTREBNO DOVESTI Autodesk.Revit.DB.ParameterType.HVACDuctSize ili Angle . Postoje dva koda u zavisnosti od verzije Revita.
    '''

    uidoc = __revit__.ActiveUIDocument
    if uidoc.Document.Application.VersionNumber <2023:
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

    else:

        try:
            import math
            from  Autodesk.Revit.DB import Definition
            if RevitParametar.Definition.GetDataType().TypeId.Contains('ductSize') :
                V=RevitParametar.AsDouble()*304.8
            elif RevitParametar.Definition.GetDataType().TypeId.Contains('length') :
                V=RevitParametar.AsDouble()*304.8
            elif RevitParametar.Definition.GetDataType().TypeId.Contains('angle') :
                V=RevitParametar.AsDouble()*180/math.pi
            if round(V,3).is_integer():
                return str(int(round(V,3)))
            else:
                return str(round(V,3))
        except TypeError:  
            return 'GRESKA U PRETVARANJU'

def PrebrojUnikate(lista):
        '''
        FUNKCIJA PREBROJAVA UNIKATE IZ LISTE NA ULAZU I VRACA DICTIONARY UNKATA I BROJA PONAVLJANJA
        '''
        Unikati={}
        for i in lista:
            if i in Unikati:
                Unikati[i]+=1
            else:
                Unikati[i]=1

        return Unikati