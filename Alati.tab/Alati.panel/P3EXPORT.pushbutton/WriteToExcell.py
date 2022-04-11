import clr
import os

clr.AddReference('Microsoft.Office.Interop.Excel, Version=15.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel
from System.Runtime.InteropServices import Marshal

lokacijaCuvanja=os.path.expanduser("~\\Desktop\\"+ 'PRIRUBNICE.xlsx')

exApp = Excel.ApplicationClass()   
exApp.Visible = True
exApp.DisplayAlerts = False   
xlbook=exApp.Workbooks.Add()
xlsheet=xlbook.Worksheets[1]
xlsheet2=xlbook.Worksheets.Add()


xlsheet.Name='PRIRUBNICE'
xlsheet2.Name='DODATNO'

xlsheet.Cells[8, 2].Value = "Salary"

#print(xlbook.Name)
#print(xlsheet.Name)

xlbook.SaveAs(lokacijaCuvanja)
xlbook.Close()
exApp.Quit()

Marshal.ReleaseComObject(exApp)
Marshal.ReleaseComObject(xlbook)
Marshal.ReleaseComObject(xlsheet)
