import sys
import FreeCAD
import Import

def wash_step(file_path):
    doc_name = "WashDoc"
    doc = FreeCAD.newDocument(doc_name)
    try:
        # Import the STEP file (containing Autodesk Inventor metadata)
        Import.insert(file_path, doc_name)
        
        # Get all imported objects
        objs = doc.Objects
        if objs:
            # Overwrite the original file with FreeCAD's neutral metadata format
            Import.export(objs, file_path)
            print("Successfully washed and neutralized metadata for: " + file_path)
    except Exception as e:
        print("Washing Error: " + str(e))
    finally:
        FreeCAD.closeDocument(doc_name)

if __name__ == '__main__':
    # Target file is the last argument provided via FreeCADCmd
    if len(sys.argv) > 1:
        target_file = sys.argv[-1]
        wash_step(target_file)
