# This Python file uses the following encoding: utf-8
from Autodesk.Revit.DB import *
from System.Collections.Generic import List
import Autodesk.Revit.DB as DB
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from Autodesk.Revit.DB.Mechanical import Duct
from pyrevit import forms

from FunkcijePrefabrikacije import PrefabrikovanjeElemenata

if __name__ == '__main__': #GLAVNI PROGRAM - OVDE TREBA ANALIZIRATI KANALE I POZIVATI FUNKCIJU ZA DELJENJE KANALA NA DUZINE I DODAVANJE FITTINGA

        count = 1
        try:
            SelektovaniKanali = [el for el in FilteredElementCollector(doc, uidoc.Selection.GetElementIds()).OfClass(Duct).ToElements() if el.DuctType.GetParameters('Model')[0].AsString()=='P3 - Rectangular']
            
        except:
            forms.alert("ODABIR JE PRAZAN! IZABERI P3 ELEMENTE ZA PREFABRIKACIJU")
            SelektovaniKanali = []
        finally:
            Prefabrikovani=PrefabrikovanjeElemenata(SelektovaniKanali)

            