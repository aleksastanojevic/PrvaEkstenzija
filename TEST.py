import clr

clr.AddReference(r"C:\Program Files\Autodesk\Revit 2024\RevitAPI.dll")
clr.AddReference(r"C:\Program Files\Autodesk\Revit 2024\RevitUIAPI.dll")

from pyrevit import DB, UI
from pyrevit import PyRevitException, PyRevitIOError

# pyrevit module has global instance of the
# _HostAppPostableCommand and _ExecutorParams classes already created
# import and use them like below
from pyrevit import HOST_APP
from pyrevit import EXEC_PARAMS



from Autodesk import Revit
from Autodesk.Revit import *

#from Autodesk.Revit import DB, UI

#docptr = __revit__.OpenAndActivateDocument(rvt_file_path)

doc= __revit__.ActiveUIDocument



#from System.Runtime.InteropServices import Marshal


#doc = uiapp.ActiveUIDocument.Document


