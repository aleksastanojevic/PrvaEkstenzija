# This Python file uses the following encoding: utf-8
import clr
clr.AddReference("System.Windows.Forms")
import System.Windows.Forms as WF
import os
import subprocess
from datetime import datetime
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import *
from P3CODE import NapraviNoviPosao, NapraviP3802 , NapraviP3803, NapraviP3847, NapraviP3812,NapraviP3827,NapraviP3843
from Windows_Forma import FormaPrograma
from WindowsFormaJobInfo import FormaProgramaJob
clr.AddReference('RevitAPIUI')

uidoc=__revit__.ActiveUIDocument
doc=__revit__.ActiveUIDocument.Document

if __name__ == '__main__': #GLAVNI PROGRAM
    KOD=''
    pokrenutUI=FormaPrograma() #pokretanje prvog UI prozora
    #CITANJE IZLAZNIH PARAMETARA PRVOG UI-a
    Opcija = pokrenutUI[0]
    ListaOdabira = pokrenutUI[1]
    ListaSistema = pokrenutUI[3]
    ListaSchedula = pokrenutUI[2]
    StatusUI1 = pokrenutUI[4]
    #PRAVLJANJE JEDINSTVENE LISTE ELEMENATA NAKON ODABIRA OPCIJE RADIO DUGMETA
    Elementi=[]
    DozCat=['Ducts','Duct Fittings']
    if Opcija == 1: 
        OdabraniSistem=ListaSistema[ListaOdabira[0]]
        [Elementi.append(element)for element in OdabraniSistem.DuctNetwork if element.Category.Name in DozCat]
    elif Opcija == 2:
        [Elementi.append(element) for element in ListaOdabira if element.Category.Name in DozCat]
    elif Opcija ==3:
        OdabraniScheduli = [ListaSchedula[sch] for sch in ListaOdabira]
        for sch in OdabraniScheduli:
            [Elementi.append(i) for i in FilteredElementCollector(doc,sch.Id) if i.Category.Name in DozCat ]
    DictKodova={801 :[], 802 :[],803:[],804:[],827:[],843:[],847:[],853:[],854:[],812:[]} #Kreira se dictionary po kodu elemenata i zatim se sortira u odredjenu listu unutar vrednosti kljuca()REVIT ELEMENATA
    for fiting in Elementi:
        tip=doc.GetElement(fiting.GetTypeId())  # GetElement Type
        paramF=tip.GetParameters('P3 - Code') #traži parametre prema imenu i kreira listu.Ako je jedan nađen, svakako je lista pa je potrebno uzeti element na indeksu 0
        paramD=tip.get_Parameter(BuiltInParameter.ALL_MODEL_MODEL).AsString()
        if paramF:
            P3Code=paramF[0].AsInteger()
            for kod in DictKodova:
                if P3Code == kod:
                    DictKodova[kod].append(fiting)
        if paramD and paramD=='P3 - Rectangular' and fiting.Category.Name=='Ducts':
            DictKodova[801].append(fiting)
    #PRAVLJANJE JEDINSTVENE LISTE DEFAULT VREDNOSTI ZA PODATKE O POSLU
    if StatusUI1:  
        SysRef=Elementi[0].LookupParameter('System Name').AsString()
        SysDes=SysRef + ' Ducting System'
        ClName = doc.ProjectInformation.ClientName
        Add = doc.ProjectInformation.Address
        Tel = '-'
        vreme = datetime.now()
        DateOrder = vreme.strftime("%d/%m/%Y")
        Notes= '\n\n'
        ListaDefaultVrednosti=[SysRef,SysDes,ClName,Add,Tel,DateOrder,DateOrder,Notes]  
        #POKRETANJE DRUGOG UI PROGRAMA ZA UNOS PODATAKA O POSLU I UNOS DEFAULT VREDNOSTI
        pokrenutUI2=FormaProgramaJob(ListaDefaultVrednosti)
        StatusUI2=pokrenutUI2[0]
        UnosOPoslu=pokrenutUI2[1]
    if StatusUI1 and StatusUI2:  #PROGRAM SE MOZE POKRENUTI-Status predtavlja dugme dalje na prvom i drugom UI
        Posao=NapraviNoviPosao(UnosOPoslu)
        KOD+=Posao.CODE()
        RedniBroj=0  # Redni broj pocinje od 0 i ide kroz sve elemente jednog posla
        Kolena=NapraviP3802(DictKodova[802])
        for k in Kolena:
            k.RedniBroj=RedniBroj
            RedniBroj+=1
            KOD+=k.CODE()
            # print(k.CODE())
        TRacve=NapraviP3803(DictKodova[803])
        for t in TRacve:
            t.RedniBroj=RedniBroj
            RedniBroj+=1
            KOD+=t.CODE()
            # print(t.CODE())
        Redukcije=NapraviP3847(DictKodova[847])
        for r in Redukcije:
            r.RedniBroj=RedniBroj
            RedniBroj+=1
            KOD+=r.CODE()
            # print(r.CODE())
        Cipele=NapraviP3812(DictKodova[812])
        for c in Cipele:
            c.RedniBroj=RedniBroj
            RedniBroj+=1
            KOD+=c.CODE()
            # print(c.CODE())    
        LastinRep=NapraviP3827(DictKodova[827])
        for lr in LastinRep:
            lr.RedniBroj=RedniBroj
            RedniBroj+=1
            KOD+=lr.CODE()
            # print(lr.CODE())    
        Cep=NapraviP3843(DictKodova[843])
        for c in Cep:
            c.RedniBroj=RedniBroj
            RedniBroj+=1
            KOD+=c.CODE()
            # print(c.CODE())  
        
        WF.MessageBox.Show(" УСПЕШНО ЈЕ НАПИСАН КОД !")
        imeFajla=SysRef+'.BRV'
        lokacijaCuvanja=os.path.expanduser("~\\Desktop\\"+imeFajla) # CITA HOMEPATH I DODAJE DEKSTOP I IME FAJLA.BRV
        with open(lokacijaCuvanja,'w') as f:
            f.write(KOD)
        subprocess.Popen('explorer /select ,'+lokacijaCuvanja , shell=True) # Otvara Windows Explorer sa selektovanim fajlom
        # print(KOD)


        

