
import clr
import os

clr.AddReference('Microsoft.Office.Interop.Excel, Version=15.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel
from System.Runtime.InteropServices import Marshal

lokacijaCuvanja=os.path.expanduser("~\\Desktop\\"+ 'Aleksa.xlsx')

with open(lokacijaCuvanja,'w',) as f:
	print('NEW FILE')
	


excelApp=Excel.ApplicationClass()
excelApp.Visible=True
excelApp.DisplayAlerts = False

xlbook = excelApp.Workbooks.Open('asdasd')
# xlsheet=xlbook.Worksheets['Sheet1']
ws=xlbook.Worksheets[1]

xlsheet= excelApp.Worksheets['PRIRUBNICE']
xlbook.ActiveSheet

xlbook.SaveAs(lokacijaCuvanja)
Marshal.ReleaseComObject(ws)