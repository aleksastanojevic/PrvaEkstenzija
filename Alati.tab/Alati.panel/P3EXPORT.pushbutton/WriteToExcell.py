def ExcelExport(imeSistema,lista):
    import clr
    import os
    clr.AddReference('Microsoft.Office.Interop.Excel, Version=15.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c') #referencira se Interop.Excel it CLR modula
    from Microsoft.Office.Interop import Excel      
    from System.Runtime.InteropServices import Marshal  #potreban kako bi se uklonio COM objekat koji ostaje nakon gasenja EXCEL aplikacije u Task manageru i yauyima RAM
    imeFajla=imeSistema+' PRIRUBNICE.xlsx'
    lokacijaCuvanja=os.path.expanduser("~\\Desktop\\"+ str(imeFajla)) 
    exApp = Excel.ApplicationClass()     #Pravi se novi objekat klase Excel Aplikacije  
    exApp.Visible = True
    exApp.DisplayAlerts = False   
    xlbook=exApp.Workbooks.Add()        # U Excel applikaciju se dodaje novi Workbook (Book1.xlsx)
    xlsheet=xlbook.Worksheets[1]        # Ovim postupkom vec postojeci Sheet1 u novokreiranom Workbook-u selektujemo i dodajemo ga varijabli xlsheet da bi se na njemu vrsile dalje operacije
    # xlsheet2=xlbook.Worksheets.Add()
    xlsheet.Name=' PRIRUBNICE'          # Menja se ime sheeta
    # xlsheet2.Name='DODATNO'
    
    y=1
    for i in lista:
        x=1
        for j in i:
            xlsheet.Cells[y, x].Value = j  
            x+=1      # xlsheet.Cells f-ja pristupa celijama sheeta i dodaje im vrednost 
        y+=1

    xlbook.SaveAs(lokacijaCuvanja)    # Snima se na zeljenu lokaciju
    xlbook.Close()                    # Gasi se workbook
    exApp.Quit()                      # Napusta se eksel aplikacija

    Marshal.ReleaseComObject(exApp)  #Ceo modul Marshal modul sluzi da otpusti objecte COM Object i skida Excel sa task manager liste
    Marshal.ReleaseComObject(xlbook)
    Marshal.ReleaseComObject(xlsheet)

if __name__ == '__main__':   #TEST PROGRAM YA UPIS U EKSEL
    excel=ExcelExport('AHU76-R',[['a','b'],['c','d'],['e','f']])

