# This Python file uses the following encoding: utf-8
import codecs
import sys
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
from P3CODE import NapraviNoviPosao, NapraviP3802, NapraviP3803, NapraviP3847, NapraviP3812, NapraviP3827, NapraviP3843, NapraviP3853, NapraviP3801, NapraviP3813, NapraviP3828, NapraviP3823, NapraviP3826
from Prirubnice import NadjiPrirubnice
from Windows_Forma import FormaPrograma
from WindowsFormaJobInfo import FormaProgramaJob
from DodatneFunkcije import PrebrojUnikate
from WriteToExcell import ExcelExport

clr.AddReference('RevitAPIUI')
uidoc=__revit__.ActiveUIDocument
doc=__revit__.ActiveUIDocument.Document

if __name__ == '__main__': #GLAVNI PROGRAM
    KOD=''
    PrirubniceS=[]
    PrirubniceU=[]
    PrirubniceF=[]
    PrirubniceB=[]
    NekonektovaniEl=[]
    povrsinaP3kanala=0
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
        try:
            OdabraniSistem=ListaSistema[ListaOdabira[0]]
            [Elementi.append(element)for element in OdabraniSistem.DuctNetwork if element.Category.Name in DozCat]
            if len(Elementi)==0:
                WF.MessageBox.Show(" У СИСТЕМУ НЕМА КАНАЛСКИХ ЕЛЕМЕНАТА !", '  УПС  ')
                sys.exit(1)
        except:
            WF.MessageBox.Show(" НЕМА СИСТЕМА У ПРОЈЕКТУ", '  УПС  ')
            sys.exit(1)
    elif Opcija == 2:
        [Elementi.append(element) for element in ListaOdabira if element.Category.Name in DozCat]
    elif Opcija ==3:
        try:
            OdabraniScheduli = [ListaSchedula[sch] for sch in ListaOdabira]
            for sch in OdabraniScheduli:
                [Elementi.append(i) for i in FilteredElementCollector(doc,sch.Id) if i.Category.Name in DozCat ]
        except:
            if len(Elementi)==0:
                WF.MessageBox.Show(" НЕМА КАНАЛСКИХ ЕЛЕМЕНАТА У ОДАБРАНИМ 'SCHEDULE-има !", '  УПС  ')
                sys.exit(3)
    DictKodova={801 :[], 802 :[],803:[],804:[],827:[],843:[],847:[],853:[],854:[],812:[],813:[],828:[],823:[],826:[]} #Kreira se dictionary po kodu elemenata i zatim se sortira u odredjenu listu unutar vrednosti kljuca()REVIT ELEMENATA
    for fiting in Elementi:
        tip=doc.GetElement(fiting.GetTypeId())  # GetElement Type
        paramF=tip.GetParameters('P3 - Code') #traži parametre prema imenu i kreira listu.Ako je jedan nađen, svakako je lista pa je potrebno uzeti element na indeksu 0
        paramD=tip.get_Parameter(BuiltInParameter.ALL_MODEL_MODEL).AsString()
        if paramF:
            P3Code=paramF[0].AsInteger()
            for kod in DictKodova:
                if P3Code == kod:
                    DictKodova[kod].append(fiting)
                    try:
                        paramA=fiting.GetParameters('P3_Sup_S.app')[0].AsDouble()/10.76389999
                        paramA2=fiting.GetParameters('P3_Sup_S.app2')[0].AsDouble()/10.76389999
                        paramA3=fiting.GetParameters('P3_Sup_S.app3')[0].AsDouble()/10.76389999
                        povrsinaP3kanala+=paramA+paramA2+paramA3 
                    except:
                        paramA=fiting.GetParameters('P3_Sup_S.app')[0].AsDouble()/10.76389999
                        povrsinaP3kanala+=paramA 
        if paramD and paramD=='P3 - Rectangular' and fiting.Category.Name=='Ducts':
            DictKodova[801].append(fiting)
            paramA=fiting.GetParameters('Area')[0].AsDouble()/10.76389999
            povrsinaP3kanala+=paramA
        POV='Површина селектованих P3 канала је: '+ str(round(povrsinaP3kanala))+ str(' m2')
    #WF.MessageBox.Show('Површина селектованих P3 канала је: '+ str(povrsinaP3kanala), 'ПОВРШИНА КАНАЛА')
    if StatusUI1:  
        #PROVERA DA LI IMA ELEMENATA U JEDINSTVENOM RECNIKU ELEMENATA
        nula=0
        for i in DictKodova:
            if len(DictKodova[i])==0:
                nula+=1
        if nula==len(DictKodova):
            WF.MessageBox.Show(" НЕМА 'P3' КАНАЛСКИХ ЕЛЕМЕНАТА ", 'УПС')
            sys.exit('')
        #PRAVLJANJE JEDINSTVENE LISTE DEFAULT VREDNOSTI ZA PODATKE O POSLU
        try:
            SysRef=Elementi[0].LookupParameter('System Name').AsString()
        except:
            SysRef='NEPOZNATO'
        try:
            SysDes=SysRef + ' Ducting System'
        except:
            SysDes='NEPOZNATO'
        ClName = doc.ProjectInformation.ClientName
        Add = doc.ProjectInformation.Address
        Tel = '-'
        vreme = datetime.now()
        DateOrder = vreme.strftime("%d/%m/%Y")
        Notes= '\n\n'
        ListaDefaultVrednosti=[SysRef,SysDes,ClName,Add,Tel,DateOrder,DateOrder,Notes]  
        #POKRETANJE DRUGOG UI PROGRAMA ZA UNOS PODATAKA O POSLU I UNOS DEFAULT VREDNOSTI
        pokrenutUI2=FormaProgramaJob(ListaDefaultVrednosti,POV)
        StatusUI2=pokrenutUI2[0]
        UnosOPoslu=pokrenutUI2[1]
        
    if StatusUI1 and StatusUI2:  #PROGRAM SE MOZE POKRENUTI-Status predstavlja dugme dalje na prvom i drugom UI
        Kolena=NapraviP3802(DictKodova[802])
        TRacve=NapraviP3803(DictKodova[803])
        Redukcije=NapraviP3847(DictKodova[847])
        Cipele=NapraviP3812(DictKodova[812])
        LastinRep=NapraviP3827(DictKodova[827])
        Cep=NapraviP3843(DictKodova[843])
        RacvaRedukcije=NapraviP3853(DictKodova[853])  # 813:[],828:[],823:[],826:[]

        Pantalone=NapraviP3813(DictKodova[813])  
        ProstaRacva=NapraviP3828(DictKodova[828])      
        RedukcionoKoleno=NapraviP3823(DictKodova[823]) 
        KrstRacva=NapraviP3826(DictKodova[826]) 

        Kanali=NapraviP3801(DictKodova[801])

        P3Elementi = Kolena + TRacve + Redukcije + Cipele + LastinRep + Cep + RacvaRedukcije + Pantalone + ProstaRacva + RedukcionoKoleno + KrstRacva + Kanali

        Posao=NapraviNoviPosao(UnosOPoslu)
        KOD+=Posao.CODE()
        RedniBroj=1  # Redni broj pocinje od 1 i ide kroz sve elemente jednog posla
        for P3 in P3Elementi:
            P3.RedniBroj=RedniBroj
            RedniBroj+=1
            KOD+=P3.CODE()  #METODOM CODE SE PRAVI KOD ZA SVAKI ELEMENT
            EL=doc.GetElement(P3.ElId)
            try:
                PR=NadjiPrirubnice(EL)  #OVOM METODOM SE ZA ODREDJENI ELEMENT TRAZE PRIRUBNICE I SORTIRAJU U PRIPADAJUCE LISTE
                P3.Prirubnice=PR
                for j in P3.Prirubnice:
                    if j.TipPrirubnice == 'S':
                        PrirubniceS.append(int(j.Duzina))
                    elif j.TipPrirubnice == 'U':
                        PrirubniceU.append(int(j.Duzina))
                    elif j.TipPrirubnice == 'F':
                        PrirubniceF.append(int(j.Duzina)) 
                    elif j.TipPrirubnice == 'B':
                        PrirubniceB.append(int(j.Duzina))   
            except:
                NekonektovaniEl.append(P3.ElId.IntegerValue)    #UKOLIKO IMA ELEMENATA KOJI NISU KONEKTOVANI PROGRAM VRACA LISTU SA ID ELEMENATA

        #U ovom delu koda se saklupljaju unikati, broj unikata prirubnica i sprema se lista u predodredjenom formatu za upis u Eksel a zatim upis
        stringSlist=[['TIP PROFILA : ','U172P2'],['dužina (mm)','kom.']]
        unikatiSdict=PrebrojUnikate(PrirubniceS)
        stringUlist=[['TIP PROFILA : ','U172P1'],['dužina (mm)','kom.']]
        unikatiUdict=PrebrojUnikate(PrirubniceU)
        stringFlist=[['TIP PROFILA : ','F - dostavlja TERMOVENT'],['dužina (mm)','kom.']]
        unikatiFdict=PrebrojUnikate(PrirubniceF)
        stringBlist=[['TIP PROFILA : ','U172P3'],['dužina (mm)','kom.']]
        unikatiBdict=PrebrojUnikate(PrirubniceB)
        SysRef=UnosOPoslu[0] #SysRef se prepisuje vrednoscu upisanom u UI upitniku

        #WF.MessageBox.Show(SysRef)
        if len(NekonektovaniEl) == 0:
            if len(PrirubniceS) != 0:
                listaS=stringSlist+[[i,unikatiSdict[i]] for i in unikatiSdict]
            else:
                listaS=[]
            if len(PrirubniceU) != 0:
                listaU=stringUlist+[[i,unikatiUdict[i]] for i in unikatiUdict]
            else:
                listaU=[]
            if len(PrirubniceF) != 0:
                listaF=stringFlist+[[i,unikatiFdict[i]] for i in unikatiFdict]
            else:
                listaF=[]
            if len(PrirubniceB) != 0:
                listaB=stringBlist+[[i,unikatiBdict[i]] for i in unikatiBdict]
            else:
                listaB=[]
                
            listaZaEksport=listaU+listaS+listaF+listaB
            try:
                eksel=ExcelExport(SysRef, listaZaEksport)   #METODA ExcelExport EKPORTUJE TACNOI PRIPREMLJENU LISTU U DVA REDA U EKSEL SHEET
                WF.MessageBox.Show(" УСПЕШНО ЈЕ НАПИСАНА СПЕЦИФИКАЦИЈА ПРИРУБНИЦА !",' УСПЕХ ')
            except:
                WF.MessageBox.Show('ПРОБЛЕМ ПРИ ЕКСПОРТУ У ЕКСЕЛ !',' УПС ')
        else:
            WF.MessageBox.Show('НИЈЕ МОГУЋ ЕКСПОРТ У EXCEL ! \nЕлементи: IDs :' + str(NekonektovaniEl) + ' нису добро повезани! \n(СТАВИТИ ЧЕП АКО ЕЛЕМЕНТ ОСТАЈЕ НЕПОВЕЗАН)' ,' УПС ')

        #UPIS .BRV fajla   
        
        imeFajla=SysRef+'.BRV'
        lokacijaCuvanja=os.path.expanduser("~\\Desktop\\"+imeFajla) # CITA HOMEPATH I DODAJE DEKSTOP I IME FAJLA.BRV
        try:
            with codecs.open(lokacijaCuvanja,'w', 'utf-8') as f:   #ZA PYTHON 3 (with open(lokacijaCuvanja,'w', encoding='utf-8') as f:)
                f.write(KOD)
                WF.MessageBox.Show(" УСПЕШНО ЈЕ НАПИСАН .BRV КОД !",' УСПЕХ ')
                subprocess.Popen('explorer /select ,'+lokacijaCuvanja , shell=True) # Otvara Windows Explorer sa selektovanim fajlom
        except:
            WF.MessageBox.Show(" ПРОБЛЕМ ПРИ УПИСИВАЊУ У ДАТОТЕКУ !",' УПС ')







