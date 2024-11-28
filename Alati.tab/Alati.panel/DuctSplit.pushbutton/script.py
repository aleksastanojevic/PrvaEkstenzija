# This Python file uses the following encoding: utf-8
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *
import clr
import math
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)
from System.Collections.Generic import List
from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.UI import UIApplication
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

#from DodatneFunkcijeSplit import SortedPoints, ConnectElements, IsParallel, measure, copyElement, GetDirection, GetClosestDirection, placeFitting

SveNoveTacke=[]

selektovanoU_revitu=[doc.GetElement(id) for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]

for el in selektovanoU_revitu:
    noveTacke=[]
    l=el.Location.Curve
    pocetna=l.Origin
    pravac=l.Direction
    splitl=round(3000) #OVDE DEFINISATI DUZINU DELJENJA
    duzina=round(l.Length*304.8)
    tacke=[pravac.Multiply(i/304.8) for i in xrange(splitl,duzina,splitl)]
    for tacka in tacke:
        novaTacka=pocetna.Add(tacka)
        noveTacke.append(novaTacka)
    SveNoveTacke.append(noveTacke)


famtype = []
Tipovi=FilteredElementCollector(doc).WhereElementIsElementType()
for i in Tipovi:
    if i.FamilyName=='M_Rectangular Union' :
        famtype.append(i)

ducts = selektovanoU_revitu
points = SveNoveTacke
print(ducts)
print(points[0])
ftl = len(famtype)
ductsout = []
fittingsout = []
combilist = []

t=Transaction(doc, "Transaction")
t.Start()

for typ in famtype:
    if typ.IsActive == False:
        typ.Activate()
        doc.Regenerate()
t.Commit()

t=Transaction(doc, "Add new fitting")
t.Start()
for i,duct in enumerate(ducts):
    ListOfPoints = [x for x in points[i]]
    familytype = famtype[i%ftl]
    #create duct location line
    ductline = duct.Location.Curve
    ductStartPoint = ductline.GetEndPoint(0)
    ductEndPoint = ductline.GetEndPoint(1)
    #get end connector to reconnect later
    endIsConnected = False
    endrefconn = None
    for ductconn in duct.ConnectorManager.Connectors:
        if ductconn.Origin.DistanceTo(ductEndPoint) < 5/304.8:
            if ductconn.IsConnected:
                endIsConnected = True
                for refconn in ductconn.AllRefs:
                    if refconn.ConnectorType != ConnectorType.Logical and refconn.Owner.Id.IntegerValue != duct.Id.IntegerValue:
                        endrefconn = refconn
    
            #sort the points from start of duct to end of duct
    pointlist = SortedPoints(ListOfPoints,ductStartPoint)
    ductlist = []
    newFittings = []
    ductlist.append(duct)

    tempStartPoint = None
    tempEndPoint = None
    lineDirection = ductline.Direction
	
    for i,p in enumerate(pointlist):		
        output = placeFitting(duct,p,familytype,lineDirection)
        print(p)
        print(duct.Location.Curve.GetEndPoint(0),duct.Location.Curve.GetEndPoint(1))
        #print(output)
        newfitting = output.keys()[0]
        newFittings.append(newfitting)
        fittingpoints = output.values()[0]
        tempPoints = SortedPoints(fittingpoints,ductStartPoint)
        #print(tempPoints)
        
        if i == 0:
            tempEndPoint = tempPoints[0]
            tempStartPoint = tempPoints[1]			
            newduct = copyElement(duct,ductStartPoint,tempStartPoint)	
            duct.Location.Curve = Line.CreateBound(ductStartPoint,tempEndPoint)
            ductlist.append(newduct)
            combilist.append([duct,newfitting])
            combilist.append([newduct,newfitting])
        else:
            combilist.append([newduct,newfitting])
            tempEndPoint = tempPoints[0]
            newduct = copyElement(duct,ductStartPoint,tempStartPoint)
            ductlist[-1].Location.Curve = Line.CreateBound(tempStartPoint,tempEndPoint)
            tempStartPoint = tempPoints[1]
            ductlist.append(newduct)
            combilist.append([newduct,newfitting])
    
    newline = Line.CreateBound(tempStartPoint,ductEndPoint)
    ductlist[-1].Location.Curve = newline
    ductsout.append(ductlist)
    fittingsout.append(newFittings)
    doc.Regenerate()
    
    if endIsConnected:
        for conn in ductlist[-1].ConnectorManager.Connectors:
            if conn.Origin.DistanceTo(ductEndPoint) < 5/304.8:
                endrefconn.ConnectTo(conn)
            
    for combi in combilist:
        ConnectElements(combi[0],combi[1])

t.Commit()

OUT= [ductsout,fittingsout]
print(OUT)

