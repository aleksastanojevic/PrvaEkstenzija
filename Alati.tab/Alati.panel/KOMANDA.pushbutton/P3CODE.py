# This Python file uses the following encoding: utf-8
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
##### ##### ##### ##### KLASA P3802 KOLENO!!!!!!
class P3802:
    cutDef_01='0'
    LineDef='0'
    LineType_012='1'
    def __init__(self,DebMat, Mark,ElId ,**kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.DebMat=DebMat
        self.Mark=Mark
        self.RedniBroj=None
        self.ElId=ElId
        self.Prirubnice=[]
		    
    def __str__(self):
        s =self.__class__.__name__ + '>>>' +' A:'+str(self.P3_AWidth_1) +' M:'+ str(self.P3_MWidth_2) + ' B:'+str(self.P3_BDepth) +' Angle:'+ str(self.P3_Angle) + ' Mark:'+str( self.Mark) +' ID:'+ str(self.ElId)
        return s

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

    def CODE(self):
        s='* \n'+ '802\n' +  str(self.RedniBroj) + '\n' + '1 \n' + '11\n' 
        l=[self.P3_AWidth_1 ,self.P3_BDepth ,self.P3_MWidth_2 ,self.P3_Radius_Internal ,self.P3_Radius_External ,self.P3_ELine_1 ,self.P3_FLine_2 ,\
			str(int(float(self.P3_Angle.replace('\xb0' , '')))) ,self.P3_R1D \
				 ,self.P3_R2D ,self.P3_R3D ,self.P3_R4D ,self.cutDef_01 ,self.LineDef ,self.LineType_012]
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
            parametri[j.replace(' ','').replace('-','_')]=element.GetParameters(j)[0].AsValueString()
        koleno=P3802(debljinaMaterijala, Mark,ElId,**parametri)
        listaKolena.append(koleno)
    return listaKolena
##### ##### ##### ##### KLASA P3803 KOLENO!!!!!!
class P3803:
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
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.DebMat=DebMat
        self.Mark=Mark
        self.RedniBroj=None
        self.ElId=ElId
        self.Prirubnice=[]
		    
    def __str__(self):
        s =self.__class__.__name__ +'>>>' +' A:'+str(self.P3_AWidth_1) +' M:'+ str(self.P3_MWidth_2) +' P:'+ str(self.P3_PWidth_3) +' B:'+str(self.P3_BDepth) +' Mark:'+str( self.Mark) +' ID:'+ str(self.ElId)
        return s

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

    def CODE(self):
        s='* \n'+ '803\n' +  str(self.RedniBroj) + '\n' + '1 \n' + '11\n' 
        l=[self.P3_AWidth_1 ,self.P3_BDepth ,self.P3_MWidth_2 ,self.P3_PWidth_3,self.P3_RRadius_1,self.P3_SRadius_2,self.P3_ZShift,self.P3_ELine_1 ,self.P3_FLine_2 ,self.P3_GLine_3,self.P3_KLine_4,self.P3_LLine_5 \
            ,str(int(float(self.P3_Angle.replace('\xb0' , '')))) ,self.RD1_Lf,self.RD2_Lf ,self.RD3_Lf ,self.RD4_Lf ,self.RD1_Rg,self.RD2_Rg,self.RD3_Rg,self.RD4_Rg ,self.LineDef ,self.cutDef_01 ,self.LineType_012,self.BuildType_1_2]
        s+= (',').join(l)+'\n' 
        s+='0,0,0,0,0,0,0,0,0,0,0,0\n'
        if self.Mark == None:
            s+='\n'
        else:
            s+= self.Mark+'\n'
        return s

def NapraviP3803(Elementi):
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
            parametri[j.replace(' ','').replace('-','_')]=element.GetParameters(j)[0].AsValueString()
        Tracva=P3803(debljinaMaterijala, Mark,ElId,**parametri)
        listaTracvi.append(Tracva)
    return listaTracvi

##### ##### ##### ##### KLASA P3847 REDUKCIJA!!!!!!
class P3847:
    LineType_012='1'
    def __init__(self,DebMat, Mark,ElId ,**kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.DebMat=DebMat
        self.Mark=Mark
        self.RedniBroj=None
        self.ElId=ElId
        self.Prirubnice=[]
		    
    def __str__(self):
        s =self.__class__.__name__ +'>>>' +' A:'+str(self.P3_AWidth_1) +' B:'+str(self.P3_BDepth_1)+' M:'+ str(self.P3_MWidth_2) +\
            ' N:'+ str(self.P3_NDepth_2)+' H: '+ str(self.P3_HHeight)+' Mark:'+str( self.Mark) +' ID:'+ str(self.ElId)
        return s

    def povrsina(self):
        doc=__revit__.ActiveUIDocument.Document
        sel=doc.GetElement(self.ElId)
        P1=sel.GetParameters('P3_Sup_S.app')[0].AsValueString()
        P2=sel.GetParameters('P3_Sup_S.app2')[0].AsValueString()
        P3=sel.GetParameters('P3_Sup_S.app3')[0].AsValueString()
        return P1+P2+P3

    def materijal(self):
        M=int(self.debMat)
        return M

    def Selektuj(self):
        elementIdList = List[ElementId]()
        elementIdList.Add(self.ElId)
        sel = SetElementIds(elementIdList)
        return sel

    def CODE(self):
        s='* \n'+ '847\n' +  str(self.RedniBroj) + '\n' + '1 \n' + '11\n' 
        l=[self.P3_AWidth_1,self.P3_BDepth_1,self.P3_MWidth_2,self.P3_NDepth_2,self.P3_HHeight,self.P3_ELine_1,self.P3_FLine_2,self.P3_MisalignmentX\
            ,self.P3_MisalignmentY,self.P3_ShiftX1,self.P3_ShiftX2,self.P3_ShiftY1,self.P3_ShiftY2,self.P3_Addition_1,self.P3_Addition_2,self.P3_Addition_3,self.P3_Addition_4\
                ,str(int(float(self.P3_Right_Angle.replace('\xb0' , '')))),str(int(float(self.P3_Left_Angle.replace('\xb0' , '')))),self.LineType_012]
        s+= (',').join(l)+'\n' 
        s+='0,0,0,0,0,0,0,0,0,0,0,0\n'
        if self.Mark == None:
            s+='\n'
        else:
            s+= self.Mark+'\n'
        return s    

def NapraviP3847(Elementi):
    doc=__revit__.ActiveUIDocument.Document
    from  Autodesk.Revit.DB import BuiltInParameter
    parametri847=['P3 - A Width_1','P3 - B Depth_1','P3 - M Width_2','P3 - N Depth_2','P3 - H Height','P3 - E Line_1','P3 - F Line_2','P3 - MisalignmentX','P3 - MisalignmentY','P3 - ShiftX1','P3 - ShiftX2',\
        'P3 - ShiftY1','P3 - ShiftY2','P3 - Addition_1','P3 - Addition_2','P3 - Addition_3','P3 - Addition_4','P3 - Right_Angle','P3 - Left_Angle']
    listaRedukcija=[]
    for element in Elementi:
        debljinaMaterijala=element.get_Parameter(BuiltInParameter.RBS_REFERENCE_INSULATION_THICKNESS).AsInteger()
        Mark=element.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).AsString()
        ElId=element.Id
        parametri={}
        for j in parametri847:
            parametri[j.replace(' ','').replace('-','_')]=element.GetParameters(j)[0].AsValueString()
        Redukcija=P3847(debljinaMaterijala, Mark,ElId,**parametri)
        listaRedukcija.append(Redukcija)
    return listaRedukcija
##### ##### ##### ##### KLASA P3812 TAP/CIPELA!!!!!!
class P3812:
    ductType_012='1'
    LineType_012='1'
    def __init__(self,DebMat, Mark,ElId ,**kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.DebMat=DebMat
        self.Mark=Mark
        self.RedniBroj=None
        self.ElId=ElId
        self.Prirubnice=[]
		    
    def __str__(self):
        s =self.__class__.__name__ +'>>>' +' A:'+str(self.P3_Awidth) +' b:'+str(self.P3_Sup_b)+' a:'+ str(self.P3_Sup_a) +\
            ' H:'+ str(self.Hheight)+' Mark:'+str( self.Mark) +' ID:'+ str(self.ElId)
        return s

    def povrsina(self):
        doc=__revit__.ActiveUIDocument.Document
        sel=doc.GetElement(self.ElId)
        P1=sel.GetParameters('P3_Sup_S.app')[0].AsValueString()
        return P1

    def materijal(self):
        M=int(self.debMat)
        return M

    def Selektuj(self):
        elementIdList = List[ElementId]()
        elementIdList.Add(self.ElId)
        sel = SetElementIds(elementIdList)
        return sel

    def CODE(self):
        s='* \n'+ '812\n' +  str(self.RedniBroj) + '\n' + '1 \n' + '11\n' 
        l=[self.P3_Awidth,self.P3_Sup_b,self.P3_Sup_a,self.Hheight,self.Lunghezzastaccolineare,self.Lunghezzastaccolineare,str(int(float(self.RRadius.replace('\xb0' , ''))))\
            ,str(int(float(self.SRadius.replace('\xb0' , '')))),str(int(float(self.Angle.replace('\xb0' , '')))),self.ductType_012,self.LineType_012]
        s+= (',').join(l)+'\n' 
        s+='0,0,0,0,0,0,0,0,0,0,0,0\n'
        if self.Mark == None:
            s+='\n'
        else:
            s+= self.Mark+'\n'
        return s    

def NapraviP3812(Elementi):
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
            parametri[j.replace(' ','').replace('-','_')]=element.GetParameters(j)[0].AsValueString()
        Cipela=P3812(debljinaMaterijala, Mark,ElId,**parametri)
        listaCipela.append(Cipela)
    return listaCipela
##### ##### ##### ##### KLASA P3827 LASTIN REP!!!!!!
class P3827:
    cutDef_01='0'
    LineDef='0'
    LineType_012='1'
    def __init__(self,DebMat, Mark,ElId ,**kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.DebMat=DebMat
        self.Mark=Mark
        self.RedniBroj=None
        self.ElId=ElId
        self.Prirubnice=[]
		    
    def __str__(self):
        s =self.__class__.__name__ +'>>>' +' A:'+str(self.P3_PWidth_1) +' M:'+ str(self.P3_OWidth_2) +' P:'+ str(self.P3_BDepth) +' B:'+str(self.P3_NWidth_3) +' Mark:'+str( self.Mark) +' ID:'+ str(self.ElId)
        return s

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

    def CODE(self):
        s='* \n'+ '803\n' +  str(self.RedniBroj) + '\n' + '1 \n' + '11\n' 
        l=[self.P3_PWidth_1,self.P3_OWidth_2,self.P3_BDepth,self.P3_NWidth_3,str(int(float(self.P3_Angle_Dx.replace('\xb0' , '')))),self.P3_RRadius_1,self.P3_SRadius_2,self.P3_ELine_1,self.P3_GLine_3,\
            self.P3_FLine_2,self.P3_MWidth_4,str(int(float(self.P3_Angle_Sx.replace('\xb0' , '')))),self.P3_TRadius_3,self.P3_URadius_4,self.P3_HLine_4,self.P3_LLine_6,self.P3_ILine_5,self.P3_R1D_Sx,\
                self.P3_R2D_Sx,self.P3_R3D_Sx,self.P3_R4D_Sx,self.P3_R1D_Dx,self.P3_R2D_Dx,self.P3_R3D_Dx,self.P3_R4D_Dx]
        s+= (',').join(l)+'\n' 
        s+='0,0,0,0,0,0,0,0,0,0,0,0\n'
        if self.Mark == None:
            s+='\n'
        else:
            s+= self.Mark+'\n'
        return s

def NapraviP3827(Elementi):
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
            parametri[j.replace(' ','').replace('-','_')]=element.GetParameters(j)[0].AsValueString()
        LastinRep=P3803(debljinaMaterijala, Mark,ElId,**parametri)
        listaLastinRep.append(LastinRep)
    return listaLastinRep
