element=a
from  Autodesk.Revit.DB import BuiltInParameter

dozvoljenaKategorija=['Duct Fittings',  'Duct Accessories', 'Air Terminals', 'Ducts','Mechanical Equipment']
#ISPITUJE SE ELEMENT NA ULAZU FUNKCIJE KOJE JE KATEGORIJE - U ZAVISNOSTI OD KATEGORIJE DRUGACIJE SE CITA KOJI SU KONEKTORI
if element.Category.Name=='Duct Fittings': 
    k=element.MEPModel.ConnectorManager.Connectors		
elif element.Category.Name=='Ducts':
    k=element.ConnectorManager.Connectors
    dozvoljenaKategorija=dozvoljenaKategorija[0:3]
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
			# KonElementi[Par.Owner.Category.Name]=[Par.Owner]   # U RECNIK SE DODAJU SVI KONEKTOVANI ELEMENTI PO KATEGORIJI NA ULAZNI ELEMENT 
			tip=doc.GetElement(Par.Owner.GetTypeId())
			model=tip.get_Parameter(BuiltInParameter.ALL_MODEL_MODEL).AsString()
			if Par.Owner.Category.Name == 'Duct Fittings':
				try:
					paramF=tip.GetParameters('P3 - Code')[0].AsInteger()
				except:
					paramF=None
				finally:
					if (paramF ==812 or model == 'P3-TAP') and Par.GetMEPConnectorInfo().IsPrimary:
						konU.append(Kon)
					elif paramF ==812 and not Par.GetMEPConnectorInfo().IsPrimary:
						konS.append(Kon)
					elif model == 'P3-TAP'and not Par.GetMEPConnectorInfo().IsPrimary:
						konF.append(Kon)
					elif paramF ==843:
						UklonjeniKonektori.append(Kon) # ODSTRANJUJE SE KONEKTOR KOJI PRIPADA END CAP-u ili CEPU JER NA NJEGA NE IDE PRIRUBNICA
					elif paramF:
						konS.append(Kon)

			if Par.Owner.Category.Name == 'Ducts':
				if model == 'P3 - Rectangular':
					konS.append(Kon)

			if Par.Owner.Category.Name == 'Duct Accessories':
				try:
					paramDA=Par.Owner.GetParameters('TK_SetTipPrirubnice')[0].AsString()
					if paramDA.upper()=='U':
						konU.append(Kon)
					elif paramDA.upper()=='F':
						konF.append(Kon)
					else:
						pass
				except:
					konU.append(Kon)
			if Par.Owner.Category.Name == 'Air Terminals':
				konF.append(Kon)

			if Par.Owner.Category.Name == 'Mechanical Equipment':
				konU.append(Kon)

			# W=Kon.Width*304.8
			# H=Kon.Height*304.8
			# print(str(W) + '/'+  str(H))
			
# print(Elementi)
# print(konektori)
print(konS)
print(konU)
print(konF)
print(UklonjeniKonektori)

# def ProveraFitinga(fiting):
