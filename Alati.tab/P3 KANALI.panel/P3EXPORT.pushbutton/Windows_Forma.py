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
from System.Drawing import Color, Icon ,Font, FontStyle, Point, Size, FontFamily, Image,Bitmap, Graphics
from System.Windows.Forms import (Application,  Button, CheckBox,PictureBox,Form, Panel, RadioButton, ComboBox, GroupBox, Label, CheckedListBox, CheckState, FormBorderStyle)

class Prozor(Form):
    def __init__(self):
        self.Opcija=None
        self.izabrano=None
        self.izlaz=[]
        #Konstruktor FORME
        self.Text="P3-ИЗВОЗ У ПРОГРАМ BRAVO"
        self.Font= Font(FontFamily("Arial"),8.0, FontStyle.Regular)
        self.ClientSize=Size(500,650)
        self.HelpButton = True
        self.FormBorderStyle = FormBorderStyle.FixedDialog #fiksira velicinu forme
        self.MaximizeBox = False
        self.MinimizeBox = False
        #Kreiranje NASLOVA
        self.naslov = Label()
        self.naslov.Text = "ИЗАБЕРИ МЕТОДУ ОДАБИРА ЕЛЕМЕНАТА :"
        self.naslov.Font= Font(FontFamily("Arial"),16.0, FontStyle.Bold)
        self.naslov.Location = Point(10,20)
        self.naslov.Height = 25
        self.naslov.Width = 500
        self.CenterToScreen()  
        #kreiranje dugmeta1
        self.dugme1=Button()
        self.dugme1.Location=Point(350,550)
        self.dugme1.Size=Size(100,45)
        self.dugme1.Text="ДАЉЕ"
        self.dugme1.BackColor=Color.FromName('White')
        self.dugme1.Click+=self.pritisnutoDugme
        #kreiranje dugmeta2
        self.dugme2=Button()
        self.dugme2.Location=Point(250,550)
        self.dugme2.Size=Size(100,45)
        self.dugme2.Text="ИЗАЂИ"
        self.dugme2.BackColor=Color.FromName('White')
        self.dugme2.Click+=self.pritisnutoCancel
        #######################################
        #kreiranje Padajuce liste Sistema
        self.PadajucaLista=ComboBox()
        self.PadajucaLista.Location = Point(35, 130)
        self.PadajucaLista.DropDownWidth= 140
        self.PadajucaLista.Width= 140
        self.PadajucaLista.Enabled=True
        #kreiranje Radio dugmeta 
        self.radio1=RadioButton()
        self.radio1.Text='ИЗАБЕРИ СИСТЕМ'
        self.radio1.Location = Point(45, 20)
        self.radio1.Width = 130
        self.radio1.Checked = True
        self.radio1.CheckedChanged+=self.radioDugme_PromenaCekiranja
        #kreiranje GRUPE1
        self.Grupa1=GroupBox()
        self.Grupa1.Location=Point(40,50)
        self.Grupa1.Size=Size(200,200)
        self.Grupa1.Controls.Add(self.radio1)
        self.Grupa1.Controls.Add(self.PadajucaLista)
        ##########################################
        #kreiranje PADAJUCE LISTE 2
        self.Sel=Button()
        self.Sel.Location = Point(40,120)
        self.Sel.Text = 'ИЗАБЕРИ ИЗ МОДЕЛА'
        self.Sel.BackColor=Color.FromName('White')
        self.Sel.Height = 40
        self.Sel.Width = 120
        self.Sel.Enabled= False
        self.Sel.Click += self.pickobjects
        #kreiranje Radio dugmeta 2
        self.radio2=RadioButton()
        self.radio2.Text='ОДРЕДИ ЕЛЕМЕНТЕ'
        self.radio2.Location = Point(45, 20)
        self.radio2.Width = 135
        self.radio2.Checked = False
        self.radio2.CheckedChanged+=self.radioDugme_PromenaCekiranja
        #kreiranje GRUPE2
        self.Grupa2=GroupBox()
        self.Grupa2.Location=Point(250,50)
        self.Grupa2.Size=Size(200,200)
        self.Grupa2.Controls.Add(self.radio2)
        self.Grupa2.Controls.Add(self.Sel)
        ############################################
        #kreiranje PADAJUCE LISTE 3
        self.PadajucaLista3= CheckedListBox()
        self.PadajucaLista3.HorizontalScrollbar= True
        self.PadajucaLista3.Location = Point(5, 5)
        self.PadajucaLista3.Width=390
        self.PadajucaLista3.Height=160
        self.PadajucaLista3.CheckOnClick = True
        self.PadajucaLista3.Enabled=False 
        #kreiranje Radio dugmeta 3
        self.radio3=RadioButton()
        self.radio3.Text='ИЗАБЕРИ SCHEDULE'
        self.radio3.Location = Point(150, 20)
        self.radio3.Width = 145
        self.radio3.Checked = False
        self.radio3.CheckedChanged+=self.radioDugme_PromenaCekiranja
        self.Panel3= Panel()
        self.Panel3.Location=Point(5, 45)
        self.Panel3.BackColor=Color.FromName('White')
        self.Panel3.Size=Size(400,180)
        self.radioSelectAll = RadioButton()
        self.radioSelectAll.Checked= True
        self.radioSelectAll.Enabled= False
        self.radioSelectAll.Location = Point(280, 157)
        self.radioSelectAll.Text= 'Све'
        self.radioSelectAll.Width=50
        self.radioSelectAll.CheckedChanged+=self.selectAll
        self.radioSelectNone=RadioButton()
        self.radioSelectNone.Checked= False
        self.radioSelectNone.Enabled= False
        self.radioSelectNone.Location = Point(340, 157)
        self.radioSelectNone.Text= 'Ништа'
        self.radioSelectNone.Width=60
        self.radioSelectNone.CheckedChanged+=self.selectNone
        self.Panel3.Controls.Add(self.PadajucaLista3)
        self.Panel3.Controls.Add(self.radioSelectAll)
        self.Panel3.Controls.Add(self.radioSelectNone)
        #kreiranje GRUPE3
        self.Grupa3=GroupBox()
        self.Grupa3.Location=Point(40,250)
        self.Grupa3.Size=Size(410,230)
        self.Grupa3.Controls.Add(self.radio3)
        self.Grupa3.Controls.Add(self.Panel3)
        #############################################
        # LOGO
        self.Velicina=110
        self.LogoPutanja=sys.path[0]+'\T1.png' # nalazi se putanja fajla koji se izvrsava a zatim se dodaje ime LOGO-a.
        self.ima=Image.FromFile(self.LogoPutanja) # pravi se .net Image
        self.bmp=Bitmap(self.ima,self.Velicina,self.Velicina) # pravi se Bitmap(mapa piksela) od slike u odredjenoj velicini
        self.logo = PictureBox() # Pravi se picture Box
        self.logo.Size=Size(self.Velicina,self.Velicina) #definise se velicina Picture Boxa
        self.logo.Location = Point(45,510)
        self.logo.Image=self.bmp #dodaje se slika Bitmap Picture Boxu
        #THUMBNAIL
        self.thumb=Bitmap(self.ima,64,64) #kreira se Bitmap slika u 64x64 formatu za thumbnail
        self.thumb.MakeTransparent()
        self.icon = Icon.FromHandle(self.thumb.GetHicon()) #pravi se ikonica od slike64x64
        self.Icon = self.icon # postavljamo ikonicu na formu 

        #DODAVANJE DUGMADI I GRUPA NA FORMU
        self.AcceptButton = self.dugme1
        self.CancelButton = self.dugme2
        self.Controls.Add(self.naslov)
        self.Controls.Add(self.dugme1)
        self.Controls.Add(self.dugme2)
        self.Controls.Add(self.Grupa1)
        self.Controls.Add(self.Grupa2)
        self.Controls.Add(self.Grupa3)
        self.Controls.Add(self.logo)
        ##############################
    # Dogadjaj se ucitava iz DodatneFunkcije.py zato sto radi sa metodama iz RevitAPI-ja

    from DodatneFunkcije import pickobjects 


    def selectAll(self,sender,args):
        '''
        Select all dogadjaj
        '''
        if sender.Checked:
            for i in range(0,self.PadajucaLista3.Items.Count):
                self.PadajucaLista3.SetItemChecked(i,True )
        else:
            pass

    def selectNone(self,sender,args):
        '''
        Select None dogadjaj
        '''
        if sender.Checked:
            for i in range(0,self.PadajucaLista3.Items.Count):
                self.PadajucaLista3.SetItemChecked(i,False )
        else:
            pass
        
    def pritisnutoDugme(self,sender,args):
        '''
        DOGADJAJ NA STISNUTO DUGME 'DALJE'  
        '''
        import System.Windows.Forms as WF
        if self.radio1.Checked:
            self.Opcija=1
            self.izlaz.append(self.PadajucaLista.SelectedItem)
            self.Status = True
            self.Close()
        elif self.radio2.Checked:
            self.Opcija=2
            try: 
                self.izlaz=self.selelem
                if len(self.izlaz)==0:
                    SelekcijaProblem = System.Windows.Forms.ErrorProvider()
                    SelekcijaProblem.SetError(sender, " НИШТА НИЈЕ ИЗАБРАНО  ! !")
                else:
                    self.Status = True
                    self.Close()
            except:
                SelekcijaProblem = System.Windows.Forms.ErrorProvider()
                SelekcijaProblem.SetError(sender, " ПРИТИСНИ ИЗАБЕРИ ИЗ МОДЕЛА ! !")
        elif self.radio3.Checked:
            self.Opcija=3
            for i in range(0,self.PadajucaLista3.CheckedItems.Count):
                self.izlaz.append(self.PadajucaLista3.CheckedItems[i])
            if len(self.izlaz)==0:
                SchProblem = System.Windows.Forms.ErrorProvider()
                SchProblem.SetError(sender, " НИШТА НИЈЕ ИЗАБРАНО  ! !")
            else:
                self.Status = True
                self.Close()
        else:
            pass

    def pritisnutoCancel(self,sender,args):
        '''
        DOGADJAJ NA STISNUTO IZADJI DUGME

        '''
        self.Status = False
        self.Close()

    def radioDugme_PromenaCekiranja(self,sender,args):
        '''
        PRITISKOM NA RADIO DUGME SE AKTIVIRA NJEMU ODGOVARAJUCA OPCIJA
    
        '''
        if (sender == self.radio1 and sender.Checked) :
            self.radioSelectAll.Checked = True
            self.radioSelectAll.Enabled = False
            self.radioSelectNone.Enabled = False
            self.Sel.Enabled = False
            self.radio3.Checked = False
            self.radio2.Checked = False
            self.PadajucaLista.Enabled = True
            self.PadajucaLista3.Enabled = False
        elif (sender == self.radio2 and sender.Checked) :
            self.radioSelectAll.Checked = True
            self.radioSelectAll.Enabled = False
            self.radioSelectNone.Enabled = False
            self.radio1.Checked = False
            self.radio3.Checked = False
            self.PadajucaLista.Enabled = False
            self.Sel.Enabled = True
            self.PadajucaLista3.Enabled = False
        elif (sender == self.radio3 and sender.Checked):
            self.radioSelectAll.Enabled = True
            self.radioSelectAll.Enabled = True
            self.radioSelectNone.Enabled = True
            self.radio1.Checked = False
            self.radio2.Checked = False
            self.PadajucaLista.Enabled = False
            self.Sel.Enabled = False
            self.PadajucaLista3.Enabled = True
        else:
            pass
            
def FormaPrograma():      #Kreiranje funkcije u kojoj se kreira objekat klase Prozor i dodeljuju stavke za odabir
    Forma=Prozor()
    Forma.Status=None     # Funkcija FormaPrograma ocekuje Forma.Status, ali ako korisnik iskljuci program na X onda se Status ne definise. Ovim korakom se dodeljuje None dok program ne promeni status u True ili False
    ######  UCITAVANJE LISTE SISTEMA IZ REVITA
    try:
        from DodatneFunkcije import KolektorSistema
        from DodatneFunkcije import KolektorP3Schedula
    except:
        print('Nedostaje modul DodatneFunkcije.py')
    
    if KolektorSistema(): #popunjava se lista sistema Forme
        ListaSistema=KolektorSistema()
        [Forma.PadajucaLista.Items.Add(sis) for sis in ListaSistema]
        Forma.PadajucaLista.SelectedIndex=0
    else:
        Forma.PadajucaLista.Text='НЕМА СИСТЕМА'  
        ListaSistema=None
    ######  UCITAVANJE LISTE SCHEDULE-a IZ REVITA
    
    if KolektorP3Schedula():  #popunjava se lista schedule-a Forme
        ListaSchedula=KolektorP3Schedula()  
        [Forma.PadajucaLista3.Items.Add(sch, CheckState.Checked) for sch in ListaSchedula]
    else:
        Forma.PadajucaLista3.Text='Нема - P3 Schedule-а'
        ListaSchedula=None
    Application.EnableVisualStyles()    
    Application.Run(Forma)
    # print(Forma.izlaz)
    
    return Forma.Opcija, Forma.izlaz, ListaSchedula, ListaSistema,Forma.Status

if __name__=='__main__': #ZA TESTIRANJE-NIJE GLAVNI PROGRAM
    pokrenutUI=FormaPrograma()
    
    
        