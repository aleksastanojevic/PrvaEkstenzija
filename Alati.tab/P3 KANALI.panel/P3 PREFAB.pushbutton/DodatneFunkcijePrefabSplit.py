####OVAJ FAJL POSTOJI TAKODJE I U DRUGIM ALATIMA ALI JE BLAGO PREPRAVLJEN KAKO BI RADIO U PREFABRICATION TOOL-u. NE MESATI SA 'OBICNIM SPLIT' ALATOM ####
def SortedPoints(fittingspoints,ductStartPoint):
	sortedpoints = sorted(fittingspoints, key=lambda x: measure(ductStartPoint, x))
	return sortedpoints

def ConnectElements(duct, fitting):
	import RevitServices
	ductconns = duct.ConnectorManager.Connectors
	fittingconns = fitting.MEPModel.ConnectorManager.Connectors
	for conn in fittingconns:
		for ductconn in ductconns:
			result = ductconn.Origin.IsAlmostEqualTo(conn.Origin)
			if result:
				ductconn.ConnectTo(conn)
				break
	return result

def IsParallel(dir1,dir2):
	if dir1.Normalize().IsAlmostEqualTo(dir2.Normalize()):
		return True
	if dir1.Normalize().Negate().IsAlmostEqualTo(dir2.Normalize()):
		return True
	return False
	
def measure(startpoint, point):
	return startpoint.DistanceTo(point)
	
def copyElement(element, oldloc, loc):
	doc = __revit__.ActiveUIDocument.Document

	import RevitServices
	from System.Collections.Generic import List
	from Autodesk.Revit.DB import XYZ
	from Autodesk.Revit.DB import ElementId
	from Autodesk.Revit.DB import ElementTransformUtils

	elementlist = List[ElementId]()
	elementlist.Add(element.Id)
	OffsetZ = (oldloc.Z - loc.Z)*-1
	OffsetX = (oldloc.X - loc.X)*-1
	OffsetY = (oldloc.Y - loc.Y)*-1
	direction = XYZ(OffsetX,OffsetY,OffsetZ)
	newelementId = ElementTransformUtils.CopyElements(doc,elementlist,direction)
	newelement = doc.GetElement(newelementId[0])
	return newelement

def GetDirection(faminstance):
	for c in faminstance.MEPModel.ConnectorManager.Connectors:
		conn = c
		break
	return conn.CoordinateSystem.BasisZ

def GetClosestDirection(faminstance, lineDirection):
	from Autodesk.Revit.DB import XYZ

	conndir = None
	flat_linedir = XYZ(lineDirection.X,lineDirection.Y,0).Normalize()
	for conn in faminstance.MEPModel.ConnectorManager.Connectors:
		conndir = conn.CoordinateSystem.BasisZ
		if flat_linedir.IsAlmostEqualTo(conndir):
			return conndir
	return conndir

#global variables for rotating new families
from Autodesk.Revit.DB import XYZ
tempfamtype = None
xAxis = XYZ(1,0,0)
def placeFittingAndLength(duct,point,familytype,lineDirection,Length,LengthParamName):
	doc = __revit__.ActiveUIDocument.Document
	from Autodesk.Revit.DB import *
	toggle = False
	isVertical = False
	global tempfamtype
	if tempfamtype == None:
		tempfamtype = familytype
		toggle = True
	elif tempfamtype != familytype:
		toggle = True
		tempfamtype = familytype
	level = duct.ReferenceLevel
	width = 4
	height = 4
	radius = 2
	round = False
	connectors = duct.ConnectorManager.Connectors
	for c in connectors:
		if c.ConnectorType != ConnectorType.End:
			continue
		shape = c.Shape
		if shape == ConnectorProfileType.Round:
			radius = c.Radius
			round = True	
			break
		elif shape == ConnectorProfileType.Rectangular or shape == ConnectorProfileType.Oval:
			if abs(lineDirection.Z) == 1:
				isVertical = True
				yDir = c.CoordinateSystem.BasisY
			width = c.Width
			height = c.Height
			break
	
	point = XYZ(point.X,point.Y,point.Z-level.Elevation)
	newfam = doc.Create.NewFamilyInstance(point,familytype,level,Structure.StructuralType.NonStructural)
	newfam.GetParameters(LengthParamName)[0].Set(Length)
	doc.Regenerate()
	transform = newfam.GetTransform()
	axis = Line.CreateUnbound(transform.Origin, transform.BasisZ)
	global xAxis
	if toggle:
		xAxis = GetDirection(newfam)
	zAxis = XYZ(0,0,1)
	
	if isVertical:
		angle = xAxis.AngleOnPlaneTo(yDir,zAxis)
	else:
		angle = xAxis.AngleOnPlaneTo(lineDirection,zAxis)
	
	ElementTransformUtils.RotateElement(doc,newfam.Id,axis,angle)
	doc.Regenerate()
	
	if lineDirection.Z != 0:
		newAxis = GetClosestDirection(newfam,lineDirection)
		yAxis = newAxis.CrossProduct(zAxis)
		angle2 = newAxis.AngleOnPlaneTo(lineDirection,yAxis)
		axis2 = Line.CreateUnbound(transform.Origin, yAxis)
		ElementTransformUtils.RotateElement(doc,newfam.Id,axis2,angle2)
		
	result = {}
	connpoints = []
	famconns = newfam.MEPModel.ConnectorManager.Connectors
	
	if round:
		for conn in famconns:
			if IsParallel(lineDirection,conn.CoordinateSystem.BasisZ) == False:
				continue
			if conn.Shape != shape:
				continue
			conn.Radius = radius
			connpoints.append(conn.Origin)
	else:
		for conn in famconns:
			if IsParallel(lineDirection,conn.CoordinateSystem.BasisZ) == False:
				continue
			if conn.Shape != shape:
				continue
			conn.Width = width
			conn.Height = height
			connpoints.append(conn.Origin)

	result[newfam] = connpoints
	return result


	