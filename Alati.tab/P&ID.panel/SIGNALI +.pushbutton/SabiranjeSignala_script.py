# This Python file uses the following encoding: utf-8
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *
import clr
import sys
clr.AddReference("RevitServices")
clr.AddReference("RevitAPI")
clr.AddReference("System.Windows.Forms")
import System.Windows.Forms as WF

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

def SignalIn(tag,traka):
	tg=tag.TagHeadPosition.Add(XYZ(100,100,0))
	
	l=int(traka.GetParameters('Weight')[0].AsValueString())/304.8
	sp=traka.Location.Point.Add(XYZ(100,99.985,0)) #ovo radim da bih izbegao vrednosti manje od nule. 
	ep=sp.Add(XYZ(l,15/304.8,0))
	return (sp.X<=tg.X<=ep.X and sp.Y<=tg.Y<=ep.Y)
if __name__ == '__main__': #GLAVNI PROGRAM
    view=uidoc.ActiveGraphicalView.Id
    collectorTagova=FilteredElementCollector(doc,view).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_DetailComponentTags)
    collectorItema=FilteredElementCollector(doc,view).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_DetailComponents)
    familyName='SIGNALI'
    trake=[item for item in collectorItema if item.Symbol.FamilyName==familyName]
    t=Transaction(doc, "SABIRANJE SIGNALA")
    ListaParametara=['MC AI','MC AO','MC DI','MC DO']
    #ListaParametaraTrake={}
    for traka in trake:
        BMS={}
        [BMS.setdefault(param, 0) for param in ListaParametara]
        EMS={}
        [EMS.setdefault(param, 0) for param in ListaParametara]
        Comm={}
        [Comm.setdefault(param, 0) for param in ListaParametara]
        for tag in collectorTagova:
            if SignalIn(tag,traka):
                if tag.Name == 'SIGNAL TAG-BMS':
                    el=doc.GetElement(tag.GetTaggedElementIds()[0].HostElementId)
                    for param in ListaParametara:
                        BMS.setdefault(param,0)
                        try:
                            Value=int(el.GetParameters(param)[0].AsValueString())
                        except:
                            continue
                        else:
                            BMS[param]+=Value

                if tag.Name == 'SIGNAL TAG-EMS':
                    el=doc.GetElement(tag.GetTaggedElementIds()[0].HostElementId)
                    for param in ListaParametara:
                        EMS.setdefault(param,0)
                        try:
                            Value=int(el.GetParameters(param)[0].AsValueString())
                        except:
                            continue
                        else:
                            EMS[param]+=Value

                if (tag.Name=='SIGNAL TAG-Comm-Modbus' or tag.Name=='SIGNAL TAG-Comm-Profibus' or tag.Name=='SIGNAL TAG-Comm-Profinet'):
                    el=doc.GetElement(tag.GetTaggedElementIds()[0].HostElementId)
                    for param in ListaParametara:
                        Comm.setdefault(param,0)
                        try:
                            Value=int(el.GetParameters(param)[0].AsValueString())
                        except:
                            continue
                        else:
                            Comm[param]+=Value

        PARAMETARMAP={'BMS AI':BMS['MC AI'],'BMS AO':BMS['MC AO'],'BMS DI':BMS['MC DI'],'BMS DO':BMS['MC DO'],'EMS AI':EMS['MC AI'],'EMS AO':EMS['MC AO'],'EMS DI':EMS['MC DI'],'EMS DO':EMS['MC DO'],'Comm AI':Comm['MC AI'],'Comm AO':Comm['MC AO'],'Comm DI':Comm['MC DI'],'Comm DO':Comm['MC DO']}
        t.Start()
        for SetPar in PARAMETARMAP: 
            try:
                traka.GetParameters(SetPar)[0].Set(str(PARAMETARMAP[SetPar]))
            except:
                continue

        doc.Regenerate()
        uidoc.RefreshActiveView()
        t.Commit()
            
WF.MessageBox.Show('СИГНАЛИ СУ САБРАНИ НА ЦЕЛОМ ПОГЛЕДУ',' УСПЕШНО ')
