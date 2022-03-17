import clr 
import os
clr.AddReference('Microsoft.Office.Interop.Excel')
from Microsoft.Office.Interop import Excell

lokacijaCuvanja=os.path.expanduser("~\\Desktop\\"+ 'Aleksa.xlsx')

ex=Excell.ApplicationClass()
ex.Visible=True
ex.DisplayAlerts = False

workbook=ex.Workbooks.Open(lokacijaCuvanja)



