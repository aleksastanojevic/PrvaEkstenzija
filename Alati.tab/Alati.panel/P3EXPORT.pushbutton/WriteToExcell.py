
import clr
import os

clr.AddReference('Microsoft.Office.Interop.Excel')
from Microsoft.Office.Interop import Excel

lokacijaCuvanja=os.path.expanduser("~\\Desktop\\"+ 'Aleksa.xlsx')

ex=Excel.ApplicationClass()

ex.Visible=True
# ex.DisplayAlerts = False
xlbook = ex.Workbooks.Add()

xlsheet= ex.Worksheets['PRIRUBNICE']
xlbook.ActiveSheet

xlbook.SaveAs(lokacijaCuvanja)


