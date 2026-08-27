# -*- coding: utf-8 -*-
__title__ = "Import SAT & Connectors"
__doc__ = "Select an OMWATER SAT + JSON export folder to automatically import geometry and construct Revit Pipe Connectors."

import os
import json
import clr

# Load Revit API
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *

# Load pyRevit UI helpers if available
try:
    from pyrevit import forms
    has_pyrevit = True
except ImportError:
    has_pyrevit = False

doc = __revit__.ActiveUIDocument.Document

def run_import():
    # 1. Select the JSON file
    json_path = None
    if has_pyrevit:
        json_path = forms.pick_file(file_ext="json", title="Select OMWATER Revit Contract JSON File")
    else:
        # Fallback to auto-detecting the latest export in WT3D_Project
        export_batch_dir = r"D:\WT3D_Project\1_Exports_Batch"
        if os.path.exists(export_batch_dir):
            json_files = []
            for root, dirs, files in os.walk(export_batch_dir):
                for f in files:
                    if f.endswith(".json"):
                        full_p = os.path.join(root, f)
                        json_files.append((full_p, os.path.getmtime(full_p)))
            if json_files:
                # Sort by modification time descending (latest first)
                json_files.sort(key=lambda x: x[1], reverse=True)
                json_path = json_files[0][0]
                print("Auto-detected latest export: {}".format(json_path))
    
    if not json_path or not os.path.exists(json_path):
        print("No valid JSON file selected.")
        return

    folder_path = os.path.dirname(json_path)
    base_name = os.path.basename(json_path).replace(".json", "")
    sat_path = os.path.join(folder_path, base_name + ".sat")

    if not os.path.exists(sat_path):
        print("Corresponding SAT file not found: {}".format(sat_path))
        return

    # 2. Read the JSON Configuration
    with open(json_path, 'r') as f:
        config = json.load(f)

    # Validate schema
    if "inlet" not in config or "outlet" not in config:
        print("Invalid OMWATER contract schema.")
        return

    # Convert mm to Feet (Internal Revit Database Units)
    dn_in = config['dn_in'] / 304.8
    dn_out = config['dn_out'] / 304.8

    inlet_pos = XYZ(config['inlet']['position'][0] / 304.8, config['inlet']['position'][1] / 304.8, config['inlet']['position'][2] / 304.8)
    outlet_pos = XYZ(config['outlet']['position'][0] / 304.8, config['outlet']['position'][1] / 304.8, config['outlet']['position'][2] / 304.8)

    # 3. Process Import within a Revit Transaction
    t = Transaction(doc, "Import OMWATER SAT and Build Connectors")
    t.Start()

    try:
        sat_options = SATImportOptions()
        sat_options.Unit = ImportUnit.Millimeter
        
        active_view = doc.ActiveView
        import_id = doc.Import(sat_path, sat_options, active_view)
        import_element = doc.GetElement(import_id)

        # 4. Traverse Geometry to find mating faces closest to the json coordinates
        geom_options = Options()
        geom_options.ComputeReferences = True
        geom_element = import_element.get_Geometry(geom_options)

        inlet_face_ref = None
        outlet_face_ref = None
        min_dist_in = 999.0
        min_dist_out = 999.0

        for geom_obj in geom_element:
            if isinstance(geom_obj, GeometryInstance):
                for inst_obj in geom_obj.GetInstanceGeometry():
                    if isinstance(inst_obj, Solid):
                        for face in inst_obj.Faces:
                            face_center = face.Evaluate(UV(0.5, 0.5))
                            dist_in = face_center.DistanceTo(inlet_pos)
                            dist_out = face_center.DistanceTo(outlet_pos)
                            
                            if dist_in < min_dist_in:
                                min_dist_in = dist_in
                                inlet_face_ref = face.Reference
                                
                            if dist_out < min_dist_out:
                                min_dist_out = dist_out
                                outlet_face_ref = face.Reference

        # 5. Create native Revit Pipe Connectors on the identified faces
        if inlet_face_ref and outlet_face_ref:
            inlet_conn = doc.FamilyCreate.NewPipeConnector(inlet_face_ref, SystemClassification.HydronicSupply)
            inlet_conn.FlowDirection = FlowDirectionType.In
            inlet_conn.GetParameters("Diameter")[0].Set(dn_in)
            
            outlet_conn = doc.FamilyCreate.NewPipeConnector(outlet_face_ref, SystemClassification.HydronicReturn)
            outlet_conn.FlowDirection = FlowDirectionType.Out
            outlet_conn.GetParameters("Diameter")[0].Set(dn_out)
            
            print("Successfully imported {} and placed 2 Connectors.".format(base_name))
        else:
            print("Failed to locate appropriate geometric faces for connectors.")
            
        t.Commit()
    except Exception as ex:
        t.RollBack()
        print("Error during import: {}".format(str(ex)))

if __name__ == "__main__":
    run_import()
