# This Python file uses the following encoding: utf-8
import os, sys
import clr
clr.AddReference("System.IO")
clr.AddReference("System.Drawing")
clr.AddReference("System.Reflection")
clr.AddReference("System.Threading")
clr.AddReference("System.Windows.Forms")

import System
import System.IO
from System.Drawing import Color, Icon ,Font, FontStyle, Point, Size, FontFamily, Image,Bitmap
from System.Windows.Forms import (Application, Button,PictureBox, TextBox, Label, FormBorderStyle)
                  
class ProzorJ(System.Windows.Forms.Form):
    def __init__(self):
        self.Opcija=None
        self.izabrano=None
        self.izlaz=[]
        #Konstruktor FORME
        self.Text="P3-О ПОСЛУ"
        self.Font= Font(FontFamily("Arial"),8.0, FontStyle.Regular)
        self.ClientSize=Size(500,600)
        self.HelpButton = True
        self.FormBorderStyle = FormBorderStyle.FixedDialog #fiksira velicinu forme
        self.MaximizeBox = False
        self.MinimizeBox = False
        #Kreiranje NASLOVA
        self.naslov = Label()
        self.naslov.Text = "ПОДАЦИ О ПОСЛУ :"
        self.naslov.Font= Font(FontFamily("Arial"),16.0, FontStyle.Bold)
        self.naslov.Location = Point(10,20)
        self.naslov.Height = 25
        self.naslov.Width = 500
        self.CenterToScreen()  
        #Kreiranje 
        self.pov = Label()
        self.pov.Text = "Површина канала :"
        self.pov.Font= Font(FontFamily("Arial"),12.0, FontStyle.Regular)
        self.pov.Location = Point(45,50)
        self.pov.Height = 25
        self.pov.Width = 500
        self.CenterToScreen()  
        #kreiranje dugmeta1
        self.dugme1=Button()
        self.dugme1.Location=Point(380,500)
        self.dugme1.Size=Size(100,45)
        self.dugme1.Text="НАПРАВИ .BRV"
        self.dugme1.BackColor=Color.FromName('White')
        self.dugme1.Click+=self.pritisnutoDugme
        #kreiranje dugmeta2
        self.dugme2=Button()
        self.dugme2.Location=Point(280,500)
        self.dugme2.Size=Size(100,45)
        self.dugme2.Text="ИЗАЂИ"
        self.dugme2.BackColor=Color.FromName('White')
        self.dugme2.Click+=self.pritisnutoCancel
        #######################################
        #KREIRANJE UNOSA INFORMACIJA O POSLU
        listaLabela=['Reference*','Description*','Customer Name*','Address','Telephone','Order Date','Order Date','Notes']
        self.listaInputa=[None]*len(listaLabela)
        y=80
        for i in range(len(listaLabela)):
            naslov=Label()
            naslov.Text=listaLabela[i]
            naslov.Location=Point(40,y)
            self.Controls.Add(naslov)
            self.listaInputa[i] = listaLabela[i]
            self.listaInputa[i] = TextBox()
            if i == 7:
                self.listaInputa[i].Multiline  = True
                self.listaInputa[i].Height=50
            else:
                self.listaInputa[i].Multiline  = False
            self.listaInputa[i].Width=310
            self.listaInputa[i].Location=Point(170,y)
            self.Controls.Add(self.listaInputa[i])
            y+=45
        # LOGO
        self.Velicina=110
        self.LogoPutanja=sys.path[0]+'\T1.png' # nalazi se putanja fajla koji se izvrsava a zatim se dodaje ime LOGO-a.
        self.ima=Image.FromFile(self.LogoPutanja) # pravi se .net Image
        self.bmp=Bitmap(self.ima,self.Velicina,self.Velicina) # pravi se Bitmap(mapa piksela) od slike u odredjenoj velicini
        self.logo = PictureBox() # Pravi se picture Box
        self.logo.Size=Size(self.Velicina,self.Velicina) #definise se velicina Picture Boxa
        self.logo.Location = Point(20,450)
        self.logo.Image=self.bmp #dodaje se slika Bitmap Picture Boxu
        #THUMBNAIL
        self.thumb=Bitmap(self.ima,64,64) #kreira se Bitmap slika u 64x64 formatu za thumbnail
        self.thumb.MakeTransparent()
        self.icon = Icon.FromHandle(self.thumb.GetHicon()) #pravi se ikonica od slike64x64
        self.Icon = self.icon # postavljamo ikonicu na formu 
        #DODAVANJE DUGMADI I GRUPA NA FORMU
        # self.AcceptButton = self.dugme1
        self.CancelButton = self.dugme2
        self.Controls.Add(self.naslov)
        self.Controls.Add(self.pov)
        self.Controls.Add(self.dugme1)
        self.Controls.Add(self.dugme2)
        self.Controls.Add(self.logo)
        ##############################

    def pritisnutoDugme(self,sender,args):
        '''
        DOGADJAJ NA STISNUTO DUGME 'DALJE'  
        '''
        praznaPolja=0
        for i in range(3):
            if len(self.listaInputa[i].Text)==0:
                praznaPolja+=1
        if praznaPolja>0:
            PraznoPoljeGreska = System.Windows.Forms.ErrorProvider()
            PraznoPoljeGreska.SetError(sender, 'ПОЉА СА (*) СУ ОБАВЕЗНА')
        else:
            self.izlaz=[i.Text for i in self.listaInputa]
            self.Status = True
            self.Close()
    
    def pritisnutoCancel(self,sender,args):
        '''
        DOGADJAJ NA STISNUTO IZADJI DUGME

        '''
        self.Status = False
        self.Close()
            
def FormaProgramaJob(ulaz,Pov): 
    '''
    Kreiranje funkcije u kojoj se kreira objekat klase ProzorJ i dodeljuju stavke za popunjavanje
    (ulaz-->Lista ulaznih default textova za UI2)
    '''
    FormaJ=ProzorJ()
    FormaJ.Status=None   
    for i in range(len(ulaz)):
        FormaJ.listaInputa[i].Text = ulaz[i]
    FormaJ.pov.Text=Pov
    Application.EnableVisualStyles()    
    Application.Run(FormaJ)          

    return FormaJ.Status,FormaJ.izlaz
    

if __name__=='__main__':   #ZA TESTIRANJE-NIJE GLAVNI PROGRAM
    ulaz=['A','V','l','r','k','V','s','\n '] 
    POV='Површина P3 канала је: 233'
    a=FormaProgramaJob(ulaz,POV)
    print(a[0])
    print(a[1][1])


    

    

