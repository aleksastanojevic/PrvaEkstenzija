# This Python file uses the following encoding: utf-8
from DodatneFunkcije import PretvoriJedinicu
class P3Posao:
    def __init__(self,*args):
        self.SysRef=args[0]
        self.SysDes=args[1]
        self.ClName=args[2]
        self.Add=args[3]
        self.Tel=args[4]
        self.DateOrder=args[5]
        self.DateOrder2=args[6]
        self.Notes=args[7]

    def __str__(self):
        s=self.__class__.__name__ +'>>>' +' Ref:'+self.SysRef+ ' Des:'+self.SysDes + ' Date:'+self.DateOrder
        return s
    def CODE(self):
        l=[self.SysRef,self.SysDes,self.ClName,self.Add,self.Tel,self.DateOrder,self.DateOrder2,self.Notes]
        s='\n'.join(l)
        return s

def NapraviNoviPosao(UnosOPoslu):
    NoviPosao=P3Posao(*UnosOPoslu)
    return NoviPosao
##### ##### ##### ##### KLASA P3!!!!!!
class P3:
    def __init__(self,DebMat, Mark,ElId):
        self.DebMat=DebMat
        self.Mark=Mark
        self.ElId=ElId

    def povrsina(self):
        doc=__revit__.ActiveUIDocument.Document
        sel=doc.GetElement(self.ElId)
        P=sel.GetParameters('P3_Sup_S.app')[0].AsValueString()
        return P

    def materijal(self):
        M=int(self.debMat)
        return M

    def Selektuj(self):
        elementIdList = List[ElementId]()
        elementIdList.Add(self.ElId)
        sel = SetElementIds(elementIdList)
        return sel

class P3802(P3):
    cutDef_01='0'
    LineDef='0'
    LineType_012='1'
    def __init__(self,DebMat, Mark,ElId ,**kwargs):
        P3.__init__(self,DebMat, Mark,ElId)
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.RedniBroj=None
        self.Prirubnice=[]

        if int(float(self.P3_Radius_Internal)) == 1:  #Ako je unutrasnji radijus 1 , onda je radijus 0
            self.P3_Radius_Internal='0'
		    
    def __str__(self):
        s =self.__class__.__name__ + '>>>' +' A:'+self.P3_AWidth_1 +' M:'+ self.P3_MWidth_2 + ' B:'+self.P3_BDepth \
            +' Angle:'+ self.P3_Angle + ' Mark:'+self.Mark+' ID:'+ self.ElId
        return s

    def CODE(self):
        s='*\n'+ '802\n' +  str(self.RedniBroj) + '\n' + '1\n' + '11\n' 
        l=[self.P3_AWidth_1 ,self.P3_BDepth ,self.P3_MWidth_2 ,self.P3_Radius_Internal ,self.P3_Radius_External ,self.P3_ELine_1 ,self.P3_FLine_2 ,\
            self.P3_Angle ,self.P3_R1D ,self.P3_R2D ,self.P3_R3D ,self.P3_R4D ,self.cutDef_01 ,self.LineDef ,self.LineType_012]
        s+= (',').join(l)+'\n' 
        s+='0,0,0,0,0,0,0,0,0,0,0,0\n'
        if self.Mark == None:
            s+='\n'
        else:
            s+= self.Mark+'\n'
        return s

def NapraviP3802(Elementi):
    '''
    Funkcija od Elemenata na unosu pravi elemente klase P3802 i popunjava ga parametrima iz modela,kao i nephodnim parametrima za softver BRAVO i prirubnicama
    '''
    doc=__revit__.ActiveUIDocument.Document
    from  Autodesk.Revit.DB import BuiltInParameter
    parametri802=['P3 - A Width_1','P3 - B Depth','P3 - M Width_2','P3 - Radius_Internal','P3 - Radius_External','P3 - E Line_1','P3 - F Line_2',\
        'P3 - Angle','P3 - R1D','P3 - R2D','P3 - R3D','P3 - R4D']
    listaKolena=[]
    for element in Elementi:
        debljinaMaterijala=element.get_Parameter(BuiltInParameter.RBS_REFERENCE_INSULATION_THICKNESS).AsInteger()
        Mark=element.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).AsString()
        ElId=element.Id
        parametri={}
        for j in parametri802:
            parametri[j.replace(' ','').replace('-','_')]=PretvoriJedinicu(element.GetParameters(j)[0])
        koleno=P3802(debljinaMaterijala, Mark,ElId,**parametri)
        listaKolena.append(koleno)
    return listaKolena
##### ##### ##### ##### KLASA P3803 T RACVA!!!!!!
class P3803(P3):
    RD1_Lf='0'
    RD2_Lf='0'
    RD3_Lf='0'
    RD4_Lf='0'
    RD1_Rg='0'
    RD2_Rg='0'
    RD3_Rg='0'
    RD4_Rg='0'
    LineDef='0'
    cutDef_01='0'
    LineType_012='1'
    BuildType_1_2='2'
    def __init__(self,DebMat, Mark,ElId ,**kwargs):
        P3.__init__(self,DebMat, Mark,ElId)
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.RedniBroj=None
        self.Prirubnice=[]
		    
    def __str__(self):
        s =self.__class__.__name__ +'>>>' +' A:'+self.P3_AWidth_1 +' M:'+ self.P3_MWidth_2 +' P:'+ self.P3_PWidth_3 +\
            ' B:'+self.P3_BDepth +' Mark:'+ self.Mark +' ID:'+ self.ElId
        return s

    def CODE(self):
        s='*\n'+ '803\n' +  str(self.RedniBroj) + '\n' + '1\n' + '11\n' 
        l=[self.P3_AWidth_1 ,self.P3_BDepth ,self.P3_MWidth_2 ,self.P3_PWidth_3,self.P3_RRadius_1,self.P3_SRadius_2,self.P3_ZShift,self.P3_ELine_1 \
            ,self.P3_FLine_2 ,self.P3_GLine_3,self.P3_KLine_4,self.P3_LLine_5,self.P3_Angle ,self.RD1_Lf,self.RD2_Lf ,self.RD3_Lf ,self.RD4_Lf \
                ,self.RD1_Rg,self.RD2_Rg,self.RD3_Rg,self.RD4_Rg ,self.LineDef ,self.cutDef_01 ,self.LineType_012,self.BuildType_1_2]
        s+= (',').join(l)+'\n' 
        s+='0,0,0,0,0,0,0,0,0,0,0,0\n'
        if self.Mark == None:
            s+='\n'
        else:
            s+= self.Mark+'\n'
        return s

def NapraviP3803(Elementi):
    '''
    Funkcija od Elemenata na unosu pravi elemente klase P3803 i popunjava ga parametrima iz modela,kao i nephodnim parametrima za softver BRAVO i prirubnicama
    '''
    doc=__revit__.ActiveUIDocument.Document
    from  Autodesk.Revit.DB import BuiltInParameter
    parametri803=['P3 - A Width_1','P3 - B Depth','P3 - M Width_2','P3 - P Width_3','P3 - R Radius_1','P3 - S Radius_2','P3 - Z Shift','P3 - E Line_1',\
        'P3 - F Line_2','P3 - G Line_3','P3 - K Line_4','P3 - L Line_5','P3 - Angle']
    listaTracvi=[]
    for element in Elementi:
        debljinaMaterijala=element.get_Parameter(BuiltInParameter.RBS_REFERENCE_INSULATION_THICKNESS).AsInteger()
        Mark=element.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).AsString()
        ElId=element.Id
        parametri={}
        for j in parametri803:
            parametri[j.replace(' ','').replace('-','_')]=PretvoriJedinicu(element.GetParameters(j)[0])
        Tracva=P3803(debljinaMaterijala, Mark,ElId,**parametri)
        listaTracvi.append(Tracva)
    return listaTracvi

##### ##### ##### ##### KLASA P3847 REDUKCIJA!!!!!!
class P3847(P3):
    LineType_012='1'
    def __init__(self,DebMat, Mark,ElId ,**kwargs):
        P3.__init__(self,DebMat, Mark,ElId)
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.RedniBroj=None
        self.Prirubnice=[]
		     
    def __str__(self):
        s =self.__class__.__name__ +'>>>' +' A:'+self.P3_AWidth_1 +' B:'+ self.P3_BDepth_1+' M:'+ self.P3_MWidth_2 +\
            ' N:'+ self.P3_NDepth_2+' H: '+ self.P3_HHeight+' Mark:'+ self.Mark +' ID:'+ self.ElId
        return s

    def povrsina(self):
        doc=__revit__.ActiveUIDocument.Document
        sel=doc.GetElement(self.ElId)
        P1=sel.GetParameters('P3_Sup_S.app')[0].AsValueString()
        P2=sel.GetParameters('P3_Sup_S.app2')[0].AsValueString()
        P3=sel.GetParameters('P3_Sup_S.app3')[0].AsValueString()
        return P1+P2+P3

    def CODE(self):
        s='*\n'+ '847\n' +  str(self.RedniBroj) + '\n' + '1\n' + '11\n' 
        l=[self.P3_AWidth_1,self.P3_BDepth_1,self.P3_MWidth_2,self.P3_NDepth_2,self.P3_HHeight,self.P3_ELine_1,self.P3_FLine_2,self.P3_MisalignmentX\
            ,self.P3_MisalignmentY,self.P3_ShiftX1,self.P3_ShiftX2,self.P3_ShiftY1,self.P3_ShiftY2,self.P3_Addition_1,self.P3_Addition_2,self.P3_Addition_3,self.P3_Addition_4\
                ,self.P3_Right_Angle,self.P3_Left_Angle,self.LineType_012]
        s+= (',').join(l)+'\n' 
        s+='0,0,0,0,0,0,0,0,0,0,0,0\n'
        if self.Mark == None:
            s+='\n'
        else:
            s+= self.Mark+'\n'
        return s    

def NapraviP3847(Elementi):
    '''
    Funkcija od Elemenata na unosu pravi elemente klase P3847 i popunjava ga parametrima iz modela,kao i nephodnim parametrima za softver BRAVO i prirubnicama
    '''
    doc=__revit__.ActiveUIDocument.Document
    from  Autodesk.Revit.DB import BuiltInParameter
    parametri847=['P3 - A Width_1','P3 - B Depth_1','P3 - M Width_2','P3 - N Depth_2','P3 - H Height','P3 - E Line_1','P3 - F Line_2','P3 - MisalignmentX'\
        ,'P3 - MisalignmentY','P3 - ShiftX1','P3 - ShiftX2','P3 - ShiftY1','P3 - ShiftY2','P3 - Addition_1','P3 - Addition_2','P3 - Addition_3','P3 - Addition_4'\
            ,'P3 - Right_Angle','P3 - Left_Angle']
    listaRedukcija=[]
    for element in Elementi:
        debljinaMaterijala=element.get_Parameter(BuiltInParameter.RBS_REFERENCE_INSULATION_THICKNESS).AsInteger()
        Mark=element.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).AsString()
        ElId=element.Id
        parametri={}
        for j in parametri847:
            parametri[j.replace(' ','').replace('-','_')]=PretvoriJedinicu(element.GetParameters(j)[0])
        Redukcija=P3847(debljinaMaterijala, Mark,ElId,**parametri)
        listaRedukcija.append(Redukcija)
    return listaRedukcija
##### ##### ##### ##### KLASA P3812 TAP/CIPELA!!!!!!
class P3812(P3):
    ductType_012='1'
    LineType_012='1'
    def __init__(self,DebMat, Mark,ElId ,**kwargs):
        P3.__init__(self,DebMat, Mark,ElId)
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.RedniBroj=None
        self.Prirubnice=[]
		    
    def __str__(self):
        s =self.__class__.__name__ +'>>>' +' A:'+self.P3_Awidth +' b:'+ self.P3_Sup_b+' a:'+ self.P3_Sup_a +\
            ' H:'+ self.Hheight+' Mark:'+ self.Mark +' ID:'+ self.ElId
        return s

    def CODE(self):
        s='*\n'+ '812\n' +  str(self.RedniBroj) + '\n' + '1\n' + '11\n' 
        l=[self.P3_Awidth,self.P3_Sup_b,self.P3_Sup_a,self.Hheight,self.Lunghezzastaccolineare,self.Lunghezzastaccolineare,self.RRadius\
            ,self.SRadius,self.Angle,self.ductType_012,self.LineType_012]
        s+= (',').join(l)+'\n' 
        s+='0,0,0,0,0,0,0,0,0,0,0,0\n'
        if self.Mark == None:
            s+='\n'
        else:
            s+= self.Mark+'\n'
        return s    

def NapraviP3812(Elementi):
    '''
    Funkcija od Elemenata na unosu pravi elemente klase P3812 i popunjava ga parametrima iz modela,kao i nephodnim parametrima za softver BRAVO i prirubnicama
    '''
    doc=__revit__.ActiveUIDocument.Document
    from  Autodesk.Revit.DB import BuiltInParameter
    parametri812=['P3_A width','P3_Sup_b','P3_Sup_a','H height','Lunghezza stacco lineare','Lunghezza stacco lineare','R Radius','S Radius','Angle']
    listaCipela=[]
    for element in Elementi:
        debljinaMaterijala=element.get_Parameter(BuiltInParameter.RBS_REFERENCE_INSULATION_THICKNESS).AsInteger()
        Mark=element.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).AsString()
        ElId=element.Id
        parametri={}
        for j in parametri812:
            parametri[j.replace(' ','').replace('-','_')]=PretvoriJedinicu(element.GetParameters(j)[0])
        Cipela=P3812(debljinaMaterijala, Mark,ElId,**parametri)
        listaCipela.append(Cipela)
    return listaCipela
##### ##### ##### ##### KLASA P3827 LASTIN REP!!!!!!
class P3827(P3):
    cutDef_01='0'
    LineDef='0'
    LineType_012='1'
    def __init__(self,DebMat, Mark,ElId ,**kwargs):
        P3.__init__(self,DebMat, Mark,ElId)
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.RedniBroj=None
        self.Prirubnice=[]
		    
    def __str__(self):
        s =self.__class__.__name__ +'>>>' +' P:'+self.P3_PWidth_1 +' M:'+ self.P3_MWidth_4 +' N:'+self.P3_NWidth_3 +' B:'+ self.P3_BDepth+\
            ' Mark:'+ self.Mark +' ID:'+ self.ElId
        return s

    def CODE(self):
        s='*\n'+ '827\n' +  str(self.RedniBroj) + '\n' + '1\n' + '11\n' 
        l=[self.P3_PWidth_1,self.P3_OWidth_2,self.P3_BDepth,self.P3_NWidth_3,self.P3_Angle_Dx,self.P3_RRadius_1,self.P3_SRadius_2,self.P3_ELine_1,self.P3_GLine_3,\
            self.P3_FLine_2,self.P3_MWidth_4,self.P3_Angle_Sx,self.P3_TRadius_3,self.P3_URadius_4,self.P3_HLine_4,self.P3_LLine_6,self.P3_ILine_5,self.P3_R1D_Sx,\
                self.P3_R2D_Sx,self.P3_R3D_Sx,self.P3_R4D_Sx,self.P3_R1D_Dx,self.P3_R2D_Dx,self.P3_R3D_Dx,self.P3_R4D_Dx,self.cutDef_01,self.LineDef,self.LineType_012]
        s+= (',').join(l)+'\n' 
        s+='0,0,0,0,0,0,0,0,0,0,0,0\n'
        if self.Mark == None:
            s+='\n'
        else:
            s+= self.Mark+'\n'
        return s

def NapraviP3827(Elementi):
    '''
    Funkcija od Elemenata na unosu pravi elemente klase P3827 i popunjava ga parametrima iz modela,kao i nephodnim parametrima za softver BRAVO i prirubnicama
    '''
    doc=__revit__.ActiveUIDocument.Document
    from  Autodesk.Revit.DB import BuiltInParameter
    parametri827=['P3 - P Width_1','P3 - O Width_2','P3 - B Depth','P3 - N Width_3','P3 - Angle_Dx','P3 - R Radius_1','P3 - S Radius_2','P3 - E Line_1','P3 - G Line_3',\
        'P3 - F Line_2','P3 - M Width_4','P3 - Angle_Sx','P3 - T Radius_3','P3 - U Radius_4','P3 - H Line_4','P3 - L Line_6','P3 - I Line_5','P3 - R1D_Sx',\
            'P3 - R2D_Sx','P3 - R3D_Sx','P3 - R4D_Sx','P3 - R1D_Dx','P3 - R2D_Dx','P3 - R3D_Dx','P3 - R4D_Dx']
    listaLastinRep=[]
    for element in Elementi:
        debljinaMaterijala=element.get_Parameter(BuiltInParameter.RBS_REFERENCE_INSULATION_THICKNESS).AsInteger()
        Mark=element.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).AsString()
        ElId=element.Id
        parametri={}
        for j in parametri827:
            parametri[j.replace(' ','').replace('-','_')]=PretvoriJedinicu(element.GetParameters(j)[0])
        LastinRep=P3827(debljinaMaterijala, Mark,ElId,**parametri)
        listaLastinRep.append(LastinRep)
    return listaLastinRep

##### ##### ##### ##### KLASA P3827 ČEP-END CAP!!!!!!
class P3843(P3):
    holeNew='-1'
    def __init__(self,DebMat, Mark,ElId ,**kwargs):
        P3.__init__(self,DebMat, Mark,ElId)
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.RedniBroj=None
        self.Prirubnice=[]
		    
    def __str__(self):
        s =self.__class__.__name__ +'>>>' +' A:'+self.P3_Sup_a +' B:'+self.P3_Sup_b +' Mark:'+ self.Mark +' ID:'+ self.ElId
        return s

    def CODE(self):
        s='*\n'+ '843\n' +  str(self.RedniBroj) + '\n' + '1\n' + '11\n' 
        l=[self.P3_Sup_a,self.P3_Sup_b,self.cut90_45,self.holeDimension,self.holeDimension2,self.holeCenterX,self.holeCenterY,self.holeNew]
        s+= (',').join(l)+'\n' 
        s+='0,0,0,0,0,0,0,0,0,0,0,0\n'
        if self.Mark == None:
            s+='\n'
        else:
            s+= self.Mark+'\n'
        return s

def NapraviP3843(Elementi):
    '''
    Funkcija od Elemenata na unosu pravi elemente klase P3843 i popunjava ga parametrima iz modela,kao i nephodnim parametrima za softver BRAVO i prirubnicama
    '''
    doc=__revit__.ActiveUIDocument.Document
    from  Autodesk.Revit.DB import BuiltInParameter
    parametri843=['P3_Sup_a','P3_Sup_b','cut90/45','holeDimension','holeDimension2','holeCenterX','holeCenterY']
    listaCepova=[]
    for element in Elementi:
        debljinaMaterijala=element.get_Parameter(BuiltInParameter.RBS_REFERENCE_INSULATION_THICKNESS).AsInteger()
        Mark=element.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).AsString()
        ElId=element.Id
        parametri={}
        for j in parametri843:
            try:
                parametri[j.replace(' ','').replace('-','_').replace('/','_')]=PretvoriJedinicu(element.GetParameters(j)[0])
            except:
                parametri[j.replace(' ','').replace('-','_').replace('/','_')]='0'
        Cep=P3843(debljinaMaterijala, Mark,ElId,**parametri)
        listaCepova.append(Cep)
    return listaCepova

##### ##### ##### ##### KLASA P3853 RACVA-SKRETANJE-PROLAZ-Redukcija!!!!!!
class P3853(P3):
    cutDef_01='0'
    LineDef='0'
    LineType_012='1'
    def __init__(self,DebMat, Mark,ElId ,**kwargs):
        P3.__init__(self,DebMat, Mark,ElId)
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.RedniBroj=None
        self.Prirubnice=[]
		    
    def __str__(self):
        s =self.__class__.__name__ +'>>>' +' C:'+ self.P3_CWidth_1 +' B:'+  self.P3_BDepth +\
            ' M:'+ self.P3_MWidth_2+ ' P:'+  self.P3_PWidth_3 +' Mark:'+ self.Mark +' ID:'+ self.ElId
        return s

    def CODE(self):
        s='*\n'+ '853\n' +  str(self.RedniBroj) + '\n' + '1\n' + '11\n' 
        l=[self.P3_CWidth_1,self.P3_AWidth_2,self.P3_BDepth,self.P3_MWidth_2,self.P3_PWidth_3,self.P3_ELine_1,self.P3_FLine_2,self.P3_GLine_3,\
            self.P3_RadiusInt,self.P3_RadiusExt,self.P3_Angle,self.P3_HHeight,self.P3_LHeight_1,self.P3_R1D,self.P3_R2D,self.P3_R3D,self.P3_R4D,\
                self.cutDef_01,self.P3_Bending_Angle,self.LineDef,self.LineType_012]
        s+= (',').join(l)+'\n' 
        s+='0,0,0,0,0,0,0,0,0,0,0,0\n'
        if self.Mark == None:
            s+='\n'
        else:
            s+= self.Mark+'\n'
        return s

def NapraviP3853(Elementi):
    '''
    Funkcija od Elemenata na unosu pravi elemente klase P3853 i popunjava ga parametrima iz modela,kao i nephodnim parametrima za softver BRAVO i prirubnicama
    '''
    doc=__revit__.ActiveUIDocument.Document
    from  Autodesk.Revit.DB import BuiltInParameter
    parametri853=['P3 - C Width_1','P3 - A Width_2','P3 - B Depth','P3 - M Width_2','P3 - P Width_3','P3 - E Line_1','P3 - F Line_2','P3 - G Line_3','P3 - RadiusInt'\
        ,'P3 - RadiusExt','P3 - Angle','P3 - H Height','P3 - L Height_1','P3 - R1D','P3 - R2D','P3 - R3D','P3 - R4D','P3 - Bending_Angle']
    listaRacviRedukcija=[]
    for element in Elementi:
        debljinaMaterijala=element.get_Parameter(BuiltInParameter.RBS_REFERENCE_INSULATION_THICKNESS).AsInteger()
        Mark=element.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).AsString()
        ElId=element.Id
        parametri={}
        for j in parametri853:
            parametri[j.replace(' ','').replace('-','_')]=PretvoriJedinicu(element.GetParameters(j)[0])
        RacvaRedukcija=P3853(debljinaMaterijala, Mark,ElId,**parametri)
        listaRacviRedukcija.append(RacvaRedukcija)
    return listaRacviRedukcija


##### ##### ##### ##### KLASA P3801 PRAVOUGAONI KANAL!!!!!!
class P3801(P3):
    ductType_1234=None  #ako je kanal iz jednog dela onda je 1.Moze biti i 2,3,4
    cutOption=None  #da li se seče ili ne
    def __init__ (self,DebMat, Mark,ElId ,**kwargs):
        P3.__init__(self,DebMat, Mark,ElId)
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.RedniBroj=None
        self.Prirubnice=[]
        
        Obim=(float(self.P3_Width)+float(self.P3_Height))*2
        if Obim<=3960 and (float(self.P3_Length))<=1200:
            self.ductType_1234='1'
            self.cutOption='1'
        else:
            self.ductType_1234='4'
            self.cutOption='0'
        
    def __str__(self):
        s =self.__class__.__name__ +'>>>' +' W:'+self.P3_Width +' H:'+self.P3_Height+' L:'+self.P3_Length+' Mark:'+self.Mark +' ID:'+ self.ElId
        return s

    def CODE(self):
        s='*\n'+ '801\n' + str(self.RedniBroj) + '\n' + '1\n' + '11\n' 
        l=[self.P3_Width,self.P3_Height,self.P3_Length,self.ductType_1234,self.cutOption]
        s+= (',').join(l)+ ',0,0,0,0,0,0'+'\n' 
        s+='0,0,0,0,0,0,0,0,0,0,0,0\n'
        if self.Mark == None:
            s+='\n'
        else:
            s+= self.Mark+'\n'
        return s

def NapraviP3801(Elementi):
    '''
    Funkcija od Elemenata na unosu pravi elemente klase P3801 i popunjava ga parametrima iz modela,kao i nephodnim parametrima za softver BRAVO i prirubnicama
    '''
    doc=__revit__.ActiveUIDocument.Document
    from  Autodesk.Revit.DB import BuiltInParameter
    parametri801=['Width','Height','Length']
    listaKanala=[]
    for element in Elementi:
        debljinaMaterijala=element.get_Parameter(BuiltInParameter.RBS_REFERENCE_INSULATION_THICKNESS).AsInteger()
        Mark=element.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).AsString()
        ElId=element.Id
        parametri={}
        for j in parametri801:
            parametri['P3_'+j]=PretvoriJedinicu(element.GetParameters(j)[0])
        Kanal=P3801(debljinaMaterijala, Mark,ElId,**parametri)
        listaKanala.append(Kanal)
    return listaKanala