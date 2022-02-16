element=a

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
Elementi={}
konU=[]
konF=[]
konS=[]
for Kon in konektori:  #PROLAZI SE KROZ SVAKI KONEKTOR ELEMENTA
	for Par in Kon.AllRefs:  #PROLAZI SE KROZ SVE UPARENE KONEKTORE TOG KONEKTORA (MOZE BITI VISE KONEKTORA KONEKTOVANO NA OVAJ KONEKTOR npr. IZOLACIJA)
		if Par.Owner.Category.Name in dozvoljenaKategorija:  # ISPITUJE SE DA LI JE KONEKTOVANI ELEMENT U DOZVOLJENIM KATEGORIJAMA
			# Elementi[Par.Owner.Category.Name]=[Par.Owner]   # U RECNIK SE DODAJU SVI KONEKTOVANI ELEMENTI PO KATEGORIJI NA ULAZNI ELEMENT 
			if Par.Owner.Category.Name == 'Duct Fittings':
				try:
					tip=doc.GetElement(Par.Owner.GetTypeId())  # GetElement Type
					paramF=tip.GetParameters('P3 - Code')
					konS.append(Kon)
				except:
					pass
			if Par.Owner.Category.Name == 'Ducts':
				try:
					paramD=tip.get_Parameter(BuiltInParameter.ALL_MODEL_MODEL).AsString()
					if paramD=='P3 - Rectangular':
						konS.append(Kon)
				except:
					pass
			if Par.Owner.Category.Name == 'Duct Accessories':
				try:
					paramDA=Par.Owner.GetParameters('TK_SetTipPrirubnice').AsString()
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


			# W=Kon.Width*304.8
			# H=Kon.Height*304.8
			# print(str(W) + '/'+  str(H))
			
# print(Elementi)
# print(konektori)
print(konS)
print(konU)
print(konF)

# def ProveraFitinga(fiting):
