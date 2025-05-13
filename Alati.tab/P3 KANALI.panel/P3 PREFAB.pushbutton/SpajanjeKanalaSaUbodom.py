import math
import Autodesk.Revit.DB as DB

class AutoAcceptWarnings(DB.IFailuresPreprocessor):
    def PreprocessFailures(self, failuresAccessor):        
        failures = failuresAccessor.GetFailureMessages()# Get all failure messages
        for failure in failures:
            failuresAccessor.DeleteWarning(failure)
        return DB.FailureProcessingResult.Continue  # Continue the transaction and "click OK"

def SpojKanalaIuboda(selekcija):
	import clr
	import clr
	clr.AddReference("RevitAPI")
	clr.AddReference("RevitNodes")
	import Revit
	clr.ImportExtensions(Revit.Elements)
	clr.ImportExtensions(Revit.GeometryConversion)
	doc = __revit__.ActiveUIDocument.Document
	from Autodesk.Revit.DB import Line
	DUCT=[el for el in selekcija if el.Symbol.FamilyName=='P3 - Straight Duct-Tap Alt'][0]
	TAPS=[tel for tel in selekcija if not tel.Symbol.FamilyName=='P3 - Straight Duct-Tap Alt']  #Sve sto nije kanal je Tap 
	nTaps=len(TAPS)
	print('POCELA JE FUNKCIJA SPOJ KANALAiUBODA',nTaps,'SELEKCIJA:',selekcija)
	for i in DUCT.MEPModel.ConnectorManager.Connectors:
		if i.GetMEPConnectorInfo().IsPrimary:
			PconnO=i.Origin
			PconnC=i
		elif i.GetMEPConnectorInfo().IsSecondary:
			LconnO=i.Origin
			LconnC=i

	DuctLine=Line.CreateBound(PconnO,LconnO)
	DuctDir=DuctLine.Direction
	RightVector=PconnC.CoordinateSystem.BasisX	
	TapsConnectors=[]
	for j,tap in enumerate(TAPS):
		for cc in tap.MEPModel.ConnectorManager.Connectors:
			if cc.GetMEPConnectorInfo().IsPrimary:
				PtapConnO=cc.Origin
				PtapConnC=cc
		IntersectionPoint=DuctLine.Project(PtapConnO).XYZPoint
		ShortestLine=Line.CreateBound(IntersectionPoint,PtapConnO)
		ShortestLineDir=ShortestLine.Direction
		TapOrientationAngleRAD=ShortestLineDir.AngleOnPlaneTo(RightVector,DuctDir)
		TapOrientationAngleDEG=math.degrees(TapOrientationAngleRAD)
		NormalizedAngleDEG=(90*round(TapOrientationAngleDEG/90))
		NormalizedAngleRAD=math.radians(NormalizedAngleDEG)
		DiffAngleRAD=TapOrientationAngleRAD-NormalizedAngleRAD
		X=DuctLine.Project(PtapConnO).Parameter
		Y=math.sin(DiffAngleRAD)*ShortestLine.Length	
		A=NormalizedAngleRAD
		
		sTa='TapAngle'+str(j+1)
		sTx='TapX'+str(j+1)
		sTy='TapY'+str(j+1)
		sTvis='TapVis'+str(j+1)
		
		Ta=DUCT.GetParameters(sTa)[0].Set(A)
		Tx=DUCT.GetParameters(sTx)[0].Set(X)
		Ty=DUCT.GetParameters(sTy)[0].Set(Y)
		Tv=DUCT.GetParameters(sTvis)[0].Set(1)
		doc.Regenerate()
		TapsConnectors.append(PtapConnC)

	DuctConnectors=[]
	for i in DUCT.MEPModel.ConnectorManager.Connectors:
		if i.GetMEPConnectorInfo().IsPrimary or i.GetMEPConnectorInfo().IsSecondary or i.IsConnected:
			continue
		DuctConnectors.append(i)
	
	for tc in TapsConnectors:
		for c in DuctConnectors:
			if tc.Origin.DistanceTo(c.Origin)< 5/304.8:
				tc.ConnectTo(c)
			else:
				continue
		
	return	True

if __name__=='__main__': #ZA TESTIRANJE-NIJE GLAVNI PROGRAM

	Tr=Transaction(doc, "TAP kanala ")
	Tr.Start() 
	options = Tr.GetFailureHandlingOptions()
	options = options.SetFailuresPreprocessor(AutoAcceptWarnings())  # Attach custom failure handler
	Tr.SetFailureHandlingOptions(options)
	try:
		SPOJ=SpojKanalaIuboda(s)
	except:
		print('PROBLEM')
	Tr.Commit()


