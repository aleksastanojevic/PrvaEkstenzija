# Import Revit API modules
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

# Get the active Revit document and active view
uiapp = __revit__.ActiveUIDocument
doc = uiapp.Document
view = doc.ActiveView

# Check if the active view is a schedule view
if isinstance(view, ViewSchedule):
    # Start a transaction to modify the document
    t = Transaction(doc, "Insert Row into Schedule")
    t.Start()

    try:
        # Access the schedule's table data
        tableData = view.GetTableData()
        sectionData = tableData.GetSectionData(SectionType.Body)

        # Insert a new row at the end of the schedule
        noviRed=sectionData.InsertRow(sectionData.LastRowNumber + 1)

        t.Commit()
        print(noviRed)
        print("Row inserted successfully.")
    except Exception as e:
        t.RollBack()
        print("Failed to insert row: {}".format(e))
else:
    print("The active view is not a schedule view.")

viewid=2866399

allKeys = FilteredElementCollector(doc).WhereElementIsNotElementType()
a=[]
for i in allKeys:
	try:
		if i.get_Parameter(BuiltInParameter.REF_TABLE_ELEM_NAME).AsString() and i.OwnerViewId.IntegerValue== viewid :
			a.append(i)
			#print(i)
			#print(i.get_Parameter(BuiltInParameter.REF_TABLE_ELEM_NAME).AsString())
	except:
		pass
		
el=a[len(a)]	
print(el.get_Parameter(BuiltInParameter.REF_TABLE_ELEM_NAME).AsString())
param=el.GetParameters(str('Model'))[0]
print(param)

t = Transaction(doc, 'Parameter Set')
t.Start()

try:
	param.Set(str('STANOJEVIC'))
	t.Commit()
except:
	t.RollBack()
