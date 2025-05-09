# This Python file uses the following encoding: utf-8
from Autodesk.Revit.DB import *
from System.Collections.Generic import List
import Autodesk.Revit.DB as DB
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from Autodesk.Revit.DB.Mechanical import Duct
from pyrevit import forms
from DodatneFunkcijePrefabSplit import SortedPoints,placeFittingAndLength
from SpajanjeKanalaSaUbodom import SpojKanalaIuboda
from KratkiKanaliFunkcije import KratakKanal_DodatakNaFiting

###--------------------SETUJE TRANSAKCIJI OPCIJE DA NE IZBACUJE UPOZORENJA -OVAJ TIP TRANSAKCIJE SE RADI DA BISMO IZBEGLI WARNING PORUKU U PROMENITI TIPA KANALA
class AutoAcceptWarnings(DB.IFailuresPreprocessor):
    def PreprocessFailures(self, failuresAccessor):
        # Get all failure messages
        failures = failuresAccessor.GetFailureMessages()
        for failure in failures:
            failuresAccessor.DeleteWarning(failure)
        return DB.FailureProcessingResult.Continue  # Continue the transaction and "click OK"
###--------------------SETUJE TRANSAKCIJI OPCIJE DA NE IZBACUJE UPOZORENJA

def GenericDuctSplitAndPrefab(duct,familytype,DTtapfamtype,splitl=1210.5):
    '''FUNKCIJA ZA DELJENJE KANALA NA STANDARDNE DELOVE I DODAVANJE FITTINGA IZABRANOG TIPA
    -duct: kanal koji se deli
    -familytype: tip standardne familije koja se dodaje
    -splitl: duzina deljenja kanala    
    ''' 
    from Autodesk.Revit.DB import Line
    import math
    endIsConnected,startIsConnected = False,False     
    endrefconn,startrefconn=None,None  
    ListOfPoints=[]
    ductline = duct.Location.Curve
    ductStartPoint = ductline.GetEndPoint(0)
    ductEndPoint = ductline.GetEndPoint(1)
    pravac=ductline.Direction
    DL=Line.CreateBound(ductStartPoint,ductEndPoint)
    duzina=ductline.Length*304.8
    minduzina=400
    TAPSCons={}

    '''
    for conn in duct.ConnectorManager.Connectors:  
        if conn.ConnectorType == ConnectorType.Curve:
            for Cconn in conn.AllRefs:
                if Cconn.ConnectorType != ConnectorType.Logical and Cconn.Owner.Id.IntegerValue != duct.Id.IntegerValue:
                    TAPSCons[Cconn]=[Cconn.Origin,Cconn.Width,DL.Project(Cconn.Origin).Parameter]##TREBA DODATI KRUZNI UBOD ili vise uboda razlicitih oblika
                    #TAPSConsPriv[Cconn]=[Cconn.Origin,Cconn.Width,DL.Project(Cconn.Origin).Parameter]

                '''
    for conn in duct.ConnectorManager.Connectors:  
        if conn.ConnectorType == ConnectorType.Curve:
            for Cconn in conn.AllRefs:
                if Cconn.ConnectorType == ConnectorType.Logical and Cconn.Owner.Id.IntegerValue == duct.Id.IntegerValue :
                    continue
                if Cconn.Shape==ConnectorProfileType.Round:
                    TAPSCons[Cconn]=[Cconn.Origin,(Cconn.Radius)*2,DL.Project(Cconn.Origin).Parameter]##TREBA DODATI KRUZNI UBOD ili vise uboda razlicitih oblika
                elif Cconn.Shape==ConnectorProfileType.Rectangular or Cconn.Shape==ConnectorProfileType.Oval:
                    dp=abs(pravac.DotProduct(Cconn.CoordinateSystem.BasisX))
                    
                    if dp>=1:
                        TAPSCons[Cconn]=[Cconn.Origin,Cconn.Width,DL.Project(Cconn.Origin).Parameter]
                    elif dp==0:
                        TAPSCons[Cconn]=[Cconn.Origin,Cconn.Height,DL.Project(Cconn.Origin).Parameter]
                    else:
                        d=math.sqrt((Cconn.Width)*2+(Cconn.Height)*2)
                        TAPSCons[Cconn]=[Cconn.Origin,d,DL.Project(Cconn.Origin).Parameter]
                    
        elif conn.Origin.DistanceTo(ductEndPoint) < 5/304.8 and conn.IsConnected:
            endIsConnected = True
            for refconn in conn.AllRefs:
                    if refconn.ConnectorType != ConnectorType.Logical and refconn.Owner.Id.IntegerValue != duct.Id.IntegerValue:
                        endrefconn = refconn  #OVO JE Konektor koji je povezan sa konektorom na kraju kanala
        elif conn.Origin.DistanceTo(ductStartPoint) < 5/304.8 and conn.IsConnected:
                startIsConnected = True
                for refconn in conn.AllRefs:
                    if refconn.ConnectorType != ConnectorType.Logical and refconn.Owner.Id.IntegerValue != duct.Id.IntegerValue:
                        startrefconn = refconn  #OVO JE Konektor koji je povezan sa konektorom na pocetku kanala
        else :
            continue
###OVAJ DEO KODA PROVERA INICIJALNE KONEKTOVANE ELEMENTE I PROVERAVA DA LI SU IZ P3 PORODICE JER TO MENJA PREDLOG TRACAKA PODELE KANALA. AKO SU OBA P3 ONDA SE MALI DODATAK PRERASPDELJUJE NA NJIH
    print(TAPSCons)
    PrikljuceniKonektori=[]
    try:   
        StartFamilyOwner=startrefconn.Owner
        PrikljuceniKonektori.append(startrefconn)
        StartP3code=StartFamilyOwner.Symbol.GetParameters('P3 - Code')[0].AsInteger()
    except:
        StartP3code=None
        StartFamilyOwner=None
    try:   
        EndFamilyOwner=endrefconn.Owner
        PrikljuceniKonektori.append(endrefconn)
        EndP3code=EndFamilyOwner.Symbol.GetParameters('P3 - Code')[0].AsInteger()
    except:
        EndP3code=None
        EndFamilyOwner=None
#####################################################################################
    #OVDE DODATI ANALIZU PRIKLJUCENIH KOMADA 
    ###########################################
    if duzina<=splitl:
        tacke=[]
    if duzina<duzina//splitl*splitl+400 and duzina>splitl and not StartP3code and not EndP3code: #ako je duzina manja od delitelja i veca od 400 i nije povezan sa nicim na pocetku i kraju
        tacke=[pravac.Multiply(i/304.8) for i in xrange(minduzina,duzina,splitl)]
    else:
        tacke=[pravac.Multiply(i/304.8) for i in xrange(splitl,duzina,splitl)]

    ###--------ANALIZA TACAKA I POZICIJA UBODA I ADAPTACIJA --------------
    TAPSConsSortedTuple =sorted(TAPSCons.items(), key=lambda item: item[1][2])
    nedozvoljenaDistanca=[(tap[1][2]-tap[1][1]/2-0.5,tap[1][2]+tap[1][1]/2+0.5) for tap in TAPSConsSortedTuple]
    ##############################################-DEO KODA ODGOVORAN ZA PRAVLJENJE SPLIT TACAKA ZA DELJENJE-#########################################
    def is_valid(p):
        '''FUNKCIJA PROVERAVA DA LI JE INPUT BROJ U OPSEGU DVA BOJA JEDNE TUPLE  (start <= p < end) '''
        return 0 <= p <= duzina/304.8 and all(not (start <= p < end) for start, end in nedozvoljenaDistanca)
    #### NAREDNI DEO KODA POSTAVLJA TACKE DA OBILAZI LISTU TAPOVA ######
    Nt=[]
    tacka=0
    pomeraj=0
    while tacka<duzina/304.8:
        tacka+=splitl/304.8
        if tacka>duzina/304.8:
            break
        Validna=is_valid(tacka)
        while not Validna :
            tacka-=0.0164041995
            Validna=is_valid(tacka)
            pomeraj+=0.0164041995
        Nt.append(tacka)
    # NACI I POKUSATI DOTERATI DEONICU DA IMA STO VISE CELIH KOMADA KANALA I DA PRVA I POSLEDNJA BUDU OSTACI DODELJIVI FITINZIMA
    Nt.insert(0,0)
    Nt.append(duzina/304.8)

    for p,point in enumerate(Nt[::-1]):
        if p==0 or p==len(Nt)-1:
            continue
        distanca=Nt[len(Nt)-p]-Nt[len(Nt)-p-1]
        while distanca<=splitl/304.8:
            if is_valid(point):
                point-=0.0164041995  
                distanca=Nt[len(Nt)-p]-point
            else:
                break
        if (((splitl-10)/304.8<distanca<(splitl+10)/304.8)):
            Nt[len(Nt)-p-1]=point
        else:
            continue

    Nt.pop(0)
    Nt.pop(len(Nt)-1)
##############################################-DEO KODA ODGOVORAN ZA PRAVLJENJE SPLIT TACAKA ZA DELJENJE-######################################### 
    tacke=[pravac.Multiply(i) for i in Nt]
    tacke.append(pravac.Multiply(duzina/304.8))    #dodavanje kraja
    ListOfPoints=[ductStartPoint.Add(tacka) for tacka in tacke ]
    pointlist = SortedPoints(ListOfPoints,ductStartPoint)#sort the points from start of duct to end of duct
    newFittings = []
    NewFittingsDuctsTaps={}
    NewFittingsDucts=[]
    NewFittingsDuctsSHORT=[]
    tempStartPoint = ductStartPoint
    lineDirection = ductline.Direction

    for i,p in enumerate(pointlist):		
        DtLine=Line.CreateBound(tempStartPoint, p)    #pravi liniju izmedju dve tacke
        LLenPola=DtLine.Length/2                      #sredina linije
        point=DtLine.Evaluate(LLenPola,False)         #tacka na sredini linije
        tempL=p.DistanceTo(tempStartPoint)             #duzina linije izmedju dve tacke tj. duzina kanala
        output = placeFittingAndLength(duct,point,familytype,lineDirection,tempL,"P3 - TotalLength") 
        newfitting = output.keys()[0]  #vraca novi fitting
        newFittings.append(newfitting)
        fittingpoints = output.values()[0] #vraca tacke konektora fittinga
        doc.Regenerate()
        ####----------------######
        ######### SVE UBODE KOJI SE UBADAJU U OVAJ SEKTOR IZMEDJU TACAKA(KANAL) STAVLJA U NewFittingsDuctsTaps DICTIONARY KAKO BI KASNIJE MOGAO DA PROMENI TIP I DODELI UBODE U FAMILIJI KANALA  
        if len(TAPSCons)!=0:       #proverava da li ima uboda
            a=DtLine.GetEndPoint(0)
            IntersectionA=DtLine.Project(a).Parameter   #projekcija tacke A na liniju
            b=DtLine.GetEndPoint(1)
            IntersectionB=DtLine.Project(b).Parameter   #projekcija tacke B na liniju
            DtLine.MakeUnbound() # Skidamo granice krivoj Tako da moze u sledecem koraku da da Parametar van granica pocetne i krajnje tacke
            for tapConn in TAPSCons: #prolazi kroz sve Tapove i proverava da li su u opsegu tacke A i B
                Intersection=DtLine.Project(tapConn.Origin).Parameter
                if IntersectionA<Intersection<IntersectionB: #proverava da li je ubod u opsegu tacke A i B (AKO JE UBOD NA OVOM KANALU)
                    if newfitting in NewFittingsDuctsTaps:  
                        NewFittingsDuctsTaps[newfitting].append(tapConn.Owner)   #ukoliko je dodat vec u listu dodaje sledeci ubod
                    else:
                        NewFittingsDuctsTaps[newfitting]=[tapConn.Owner]      #dodaje novi ubod u listu
                    newfitting.ChangeTypeId(DTtapfamtype.Id)   # PROMENA TIPA
                else:
                    if tempL*304.8<=minduzina-5:
                        NewFittingsDuctsSHORT.append(newfitting) #dodaje fitting u listu samo ako je manji od 400mm
                    else:
                        NewFittingsDucts.append(newfitting)
        else:             
            if tempL*304.8<=minduzina-5:
                NewFittingsDuctsSHORT.append(newfitting) #dodaje fitting u listu samo ako je manji od 400mm
            else:
                NewFittingsDucts.append(newfitting)
        ######### SVE UBODE KOJI SE UBADAJU U OVAJ SEKTOR IZMEDJU TACAKA(KANAL) STAVLJA U NewFittingsDuctsTaps DICTIONARY KAKO BI KASNIJE MOGAO DA PROMENI TIP I DODELI UBODE U FAMILIJI KANALA 
        tempPoints = SortedPoints(fittingpoints,ductStartPoint) #sortira tacke konektora fittinga u odnosu na pocetnu tacku kanala
        tempStartPoint=tempPoints[1] #nova pocetna tacka je druga tacka konektora fittinga
        if i != 0:
            fittingconns1 = newFittings[i-1].MEPModel.ConnectorManager.Connectors
            fittingconns2 = newFittings[i].MEPModel.ConnectorManager.Connectors
            for conn in fittingconns2:
                for DuctFitConn in fittingconns1:
                    if DuctFitConn.Origin.DistanceTo(conn.Origin) < 5/304.8:    #ako su konektori blizu povezi ih
                        DuctFitConn.ConnectTo(conn)
                        break
    
    doc.Delete(duct.Id)        #brise originalni kanal koji je podeljen     
    doc.Regenerate()       
    if startIsConnected:    # ukoliko je kanal bio povezan sa necim na pocetku sada povezi prvi fitting sa tim
        for conn in newFittings[0].MEPModel.ConnectorManager.Connectors:
            if conn.Origin.DistanceTo(startrefconn.Origin) < 5/304.8:  ##proverava da li je konektor blizu
                startrefconn.ConnectTo(conn) # povezivanje konektora
                break 
    
    if endIsConnected: # ukoliko je kanal bio povezan sa necim na kraju sada povezi poslednji fitting sa tim
        for conn in newFittings[-1].MEPModel.ConnectorManager.Connectors:
            if conn.Origin.DistanceTo(endrefconn.Origin) < 5/304.8: ##proverava da li je konektor blizu
                endrefconn.ConnectTo(conn)  # povezivanje konektora
                break
    
    return NewFittingsDuctsTaps, NewFittingsDucts, NewFittingsDuctsSHORT #vraca listu fittinga i listu ductova koji su dodati u funkciji placeFittingAndLength

def PrefabrikovanjeElemenata(SelektovaniKanali):
    '''OVA FUNKCIJA SE POKRECE NA LISTU SELEKTOVANIH P3 Duct KANALA I PREFABRIKUJE IH U DuctFitting ELEMENTE
    -Selektovani Kanali- INPUT SELEKCIJE IZ REVITA'''
    Tipovi=FilteredElementCollector(doc).WhereElementIsElementType()
    for i in Tipovi:
        if i.FamilyName=='P3 - Straight Duct' :
            DTfamtype=i
        elif i.FamilyName=='P3 - Straight Duct-Tap Alt' :
            DTtapfamtype=i
            break
    Tr=Transaction(doc, "P3 - PREFABRICATION")  #--TRANSAKCIJA
    Tr.Start()   #--TRANSAKCIJA
    options = Tr.GetFailureHandlingOptions() # Get the current failure handling options 
    options = options.SetFailuresPreprocessor(AutoAcceptWarnings())  # Set the preprocessor
    Tr.SetFailureHandlingOptions(options) # Set the new options to the transaction

    count=0
    maxelements=len(SelektovaniKanali) # maximalan broj elemenata
    with forms.ProgressBar(title='P3 - PREFABRICATION PROGRESS : No Of Elements: '+str(maxelements), cancellable=True) as pb:
        for kanal in SelektovaniKanali: #--prolazi kroz sve selektovane kanale  
            if pb.cancelled:
                Tr.RollBack() #--TRANSAKCIJA
                uidoc.Selection.SetElementIds(List[ElementId]())  # --brisanje selekcije kako ne bi ostali selektovani elementi nakon zavrsetka
            count += 1
            pb.update_progress(count,maxelements) # --progres bar

            SubTrPrefab=SubTransaction(doc)    # U SUBTRANSAKICIJI SE MENJA TIP KANALA U KANAL SA TAPOVIMA ### PROBLEM JE BIO DA PORED REDUKCIJE PROMENI TIP. ZATO SE MENJA POD SUBTRANSAKCIJOM
            SubTrPrefab.Start()
            try:
                NewPrefabFittings=GenericDuctSplitAndPrefab(kanal,DTfamtype,DTtapfamtype,1210.5)  #--poziva funkciju za deljenje kanala i dodavanje fittinga
                SubTrPrefab.Commit()
            except:
                SubTrPrefab.RollBack()
                Tr.RollBack()

            PrefabDucts=NewPrefabFittings[1]  
            PrefabDuctsTaps=NewPrefabFittings[0]
            PrefabDuctsShort=NewPrefabFittings[2]
            for f,fitting in enumerate(PrefabDuctsTaps):  #--prolazi kroz sve fittinge i dodaje im tapove
                selekcijaZaSpajanjeTapa=PrefabDuctsTaps[fitting]  # selekcija kanala i uboda koji treba spojiti   (FORMA DICT-a [Kanal]-ubodi)
                selekcijaZaSpajanjeTapa.append(fitting) #--dodaje fitting u selekciju
                for spoj in selekcijaZaSpajanjeTapa:
                    SubTrUbod=SubTransaction(doc) 
                    SubTrUbod.Start()
                    try:
                        spoj=SpojKanalaIuboda(selekcijaZaSpajanjeTapa) #--poziva funkciju za spajanje kanala i uboda
                        SubTrUbod.Commit()
                    except:
                        SubTrUbod.RollBack()
            for s,short in enumerate(PrefabDuctsShort):      
                SubTr=SubTransaction(doc)
                SubTr.Start()
                try:
                    KratakUFiting=KratakKanal_DodatakNaFiting(short)
                    SubTr.Commit()
                    doc.Regenerate()
                except:
                    SubTr.RollBack()
        else:
            Tr.Commit()
            uidoc.Selection.SetElementIds(List[ElementId]()) # --brisanje selekcije kako ne bi ostali selektovani elementi nakon zavrsetka
            return 

if __name__ == '__main__': #GLAVNI PROGRAM - OVDE TREBA ANALIZIRATI KANALE I POZIVATI FUNKCIJU ZA DELJENJE KANALA NA DUZINE I DODAVANJE FITTINGA
        from Autodesk.Revit.DB.Mechanical import Duct
        from pyrevit import forms
        count = 1
        try:
            SelektovaniKanali = [el for el in FilteredElementCollector(doc, uidoc.Selection.GetElementIds()).OfClass(Duct).ToElements()]
            Prefabrikovani=PrefabrikovanjeElemenata(SelektovaniKanali)
        except:
            forms.alert("ODABIR JE PRAZAN! IZABERI ELEMENTE ZA PREFABRIKACIJU")
            SelektovaniKanali = []



            