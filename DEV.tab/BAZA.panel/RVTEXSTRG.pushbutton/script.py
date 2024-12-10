from System import String
from System import Guid
import System.Collections.Generic
from Autodesk.Revit.Attributes import *
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.ExtensibleStorage import *
from Autodesk.Revit.DB.ExtensibleStorage import Schema
from Autodesk.Revit.DB.ExtensibleStorage import Entity
#from Autodesk.Revit.DB import FieldType


uiapp = __revit__.ActiveUIDocument
doc = uiapp.Document
view = doc.ActiveView

#SAMO UPISIVANJE-SCHEMA VEC POSTOJI

selektovanoU_revitu=[doc.GetElement(id) for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
s0=selektovanoU_revitu[0]
schema_guid = Guid('061a4c59-b31b-47ee-87df-412c1113c7be')



schema_guid1=Guid( '4142a05d-4095-4108-a86a-27180e33a2c8')




schema = Schema.Lookup(schema_guid)
print(schema)
entity=Entity(schema)
fieldID=schema.GetField('EliD')
entity.Set(fieldID, 'ALEKSA JE USPEO')

t = Transaction(doc, "Insert Row into Schedule")
t.Start()

s0.SetEntity(entity)
print('USPEH')
t.Commit()



'''
PRAVLJENJE SCHEME I UPISIVANJE
schemaGuid=doc.CreationGUID.NewGuid()
schemaBuilder =SchemaBuilder(schemaGuid)
schemaBuilder.SetReadAccessLevel(AccessLevel.Public)
schemaBuilder.SetWriteAccessLevel(AccessLevel.Public)
schemaBuilder.SetSchemaName("LINKPID")
schemaBuilder.SetDocumentation("LINK PIDa i MODELa")
fieldBuilder = schemaBuilder.AddSimpleField("EliD", String)
schema=schemaBuilder.Finish()


entity=Entity(schema)
fieldID=schema.GetField('EliD')
entity.Set(fieldID, 'ALEKSA')


t = Transaction(doc, "Insert Row into Schedule")
t.Start()

s0.SetEntity(entity)

t.Commit()
'''
#READING
'''
schema_guid1=Guid( '4142a05d-4095-4108-a86a-27180e33a2c8')
from Autodesk.Revit.DB.ExtensibleStorage import Schema
from Autodesk.Revit.DB.ExtensibleStorage import Field
from System import Guid
from System import String


schema_guid = Guid('061a4c59-b31b-47ee-87df-412c1113c7be')
schema = Schema.Lookup(schema_guid)
field=schema.GetField("EliD")
ent=s0.GetEntity(schema)
VALUE=ent.Get[String](field)
print(VALUE)

'''