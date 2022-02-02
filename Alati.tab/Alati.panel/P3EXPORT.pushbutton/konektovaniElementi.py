def KonEl(element):
	elementIdList = List[ElementId]()	
	Elementi=[]
	dozvoljenaKategorija=['Duct Fittings',  'Duct Accessories', 'Air Terminals', 'Ducts','Mechanical Equipment']

	if element.Category.Name=='Duct Fittings':
		k=element.MEPModel.ConnectorManager.Connectors		
	elif element.Category.Name=='Ducts':
		k=element.ConnectorManager.Connectors
		dozvoljenaKategorija=dozvoljenaKategorija[0:3]
	else: 
		print('Kategorija elementa nije dobra')
		exit(1)

	konektori=[konektor for konektor in k if konektor.IsConnected]
	SetKonektora=[konektovan.AllRefs for konektovan in konektori]
	for Set in SetKonektora:
		for konektor in Set:
			if konektor.Owner.Category.Name in dozvoljenaKategorija:
				Elementi.append(konektor)
				elementIdList.Add(konektor.Owner.Id)
	

	sel = uidoc.Selection.SetElementIds(elementIdList)

	return Elementi
	
	
b=KonEl(a)


#VEZBA
con=a.MEPModel.ConnectorManager.Connectors
konektori=[]
for i in con:
	konektori.append(i)
kon=konektori[0]
