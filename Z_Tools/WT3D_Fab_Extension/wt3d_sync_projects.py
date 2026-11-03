#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
WT3D FAB EXTENSION - AUTO-SYNC PROJECTS TO EXTENSION DB (V3.6.6)
===============================================================
Tự động quét D:\INVENTOR_DATA\01_PROJECTS và cập nhật lại
toàn bộ category "00_Projects_Skid_Systems" trong content.js.

CÁCH DÙNG:
  1. Thêm thư mục project mới vào D:\INVENTOR_DATA\01_PROJECTS
  2. Chạy: python wt3d_sync_projects.py  (hoặc double-click SYNC_PROJECTS_1CLICK.bat)
  3. Reload extension trong Chrome/Edge

QUY TẮC:
  - 100% titles <= 85 ký tự (chuẩn Fab Marketplace)
  - 100% đúng 25 tags SEO kỹ thuật
  - Tự động quét tìm ảnh Hero Renders trong 06_Renders_and_Media
  - Tự động quét tìm file Universal CAD ZIP trong 01_Marketplace_Upload_Package
  - Loại trừ dự án không phải CAD (PROJECT_ARES_AQUA_MARS_2026)
"""
import sys, io, os, re, glob, shutil, zipfile
sys.dont_write_bytecode = True

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============================================================
# CẤU HÌNH ĐƯỜNG DẪN
# ============================================================
PROJECTS_DIR   = r'D:\INVENTOR_DATA\01_PROJECTS'
CONTENT_JS     = r'D:\WT3D_Project\Z_Tools\WT3D_Fab_Extension\content.js'
CONTENT_JS2    = r'D:\WT3D_Project\industrial-3d-models\Z_Tools\WT3D_Fab_Extension\content.js'
MANIFEST_PATH  = r'D:\WT3D_Project\Z_Tools\WT3D_Fab_Extension\manifest.json'
MANIFEST_PATH2 = r'D:\WT3D_Project\industrial-3d-models\Z_Tools\WT3D_Fab_Extension\manifest.json'

BEGIN_MARKER = '  // ##BEGIN_PROJECTS_SKID_SYSTEMS##'
END_MARKER   = '  // ##END_PROJECTS_SKID_SYSTEMS##'
CATEGORY_KEY = '"00_Projects_Skid_Systems"'

EXCLUDE_DIRS = {'PROJECT_ARES_AQUA_MARS_2026'}

# ============================================================
# MASTER METADATA CURATION (11 SKID PROJECTS)
# ============================================================
PROJECTS_METADATA = {
    'Industrial_RO_Pretreatment_Skid_20m3h_Dual_Cartridge_Softener_UF': {
        'title': "Industrial RO Pretreatment Skid 20m3h Cartridge Softener UF CAD",
        'personal_price': 299.99,
        'professional_price': 599.99,
        'tags': [
            "industrial",
            "water",
            "treatment",
            "skid",
            "assembly",
            "pretreatment",
            "ro",
            "osmosis",
            "ultrafiltration",
            "softener",
            "cartridge",
            "filter",
            "membrane",
            "frp",
            "stainless",
            "steel",
            "vessel",
            "cad",
            "step",
            "fbx",
            "piping",
            "valve",
            "pump",
            "mechanical",
            "engineering",
        ],
        'description': "INDUSTRIAL WATER TREATMENT 3D CAD MODEL\n\nNeed an industrial water-treatment skid without modeling every vessel, valve, fitting and pipe from scratch?\nThis detailed CAD asset provides a practical starting point for industrial water-treatment layouts, proposal and concept visualization, training content and 3D presentations.\n\nSYSTEM OVERVIEW:\n- System: Industrial RO Pretreatment Skid\n- Reference System Capacity: ~20 m³/h\n- Configuration: Dual Cartridge Filtration + Water Softening + Ultrafiltration\n\nThe model represents a pretreatment arrangement including major equipment, piping, valves, fittings, instrumentation and structural components as shown in the preview images.\n\nMAIN EQUIPMENT:\n- Dual 7 x 40\" SUS304 cartridge filter housings with bypass piping\n- Dual FRP 2472 water softener vessels\n- Automatic multiport control valves and brine tank\n- Dual hollow-fiber UF membrane modules\n- uPVC process piping, manifolds, isolation valves and pressure gauges\n- SUS304 support frame with caster wheels\n\nINCLUDED FILE FORMATS:\n- STEP (.stp) — CAD exchange\n- FBX (.fbx) — DCC and real-time visualization\n- Blender (.blend) — Native 3D scene\n- OBJ (.obj + .mtl) — Universal mesh exchange\n- GLTF / GLB (.glb) — Web 3D and AR/VR\n- STL (.stl), SAT (.sat), IGES (.igs)\n- 2D Drawing Sheets (.dwg, .pdf, .png)\n\nSUITABLE FOR:\n- Industrial water-treatment visualization and plant layout planning\n- Conceptual GA and layout development\n- Proposal and concept visualization\n- Technical presentations, training and educational content\n- Animation, Unreal Engine, Unity, Blender and real-time 3D workflows\n\nIMPORTANT INFORMATION:\nThis product is a 3D digital asset intended primarily for visualization, reference, layout development, presentations and related design workflows. It is not a manufacturer-certified model, engineering calculation, construction document, fabrication drawing, process design, or performance guarantee.\nDimensions, component specifications, connections, clearances, materials and other technical details may differ from actual equipment or later manufacturer revisions. Verify all critical information against current manufacturer documentation and project requirements before procurement, fabrication, installation or construction.\nThe purchaser is responsible for evaluating the asset's suitability for their intended use and for carrying out any project-specific engineering verification that may be required.\n\nAssembly created and prepared by WaterTreatment3D."
    },
    'SKID_Pre_Cartridge_Filter_2x7x40In_SS304_20m3h': {
        'title': "Dual 7x40 Stainless Cartridge Filter Skid 20m3h Pre-RO CAD Model",
        'personal_price': 159.99,
        'professional_price': 299.99,
        'tags': [
            "filter",
            "cartridge",
            "skid",
            "stainless",
            "pretreatment",
            "water",
            "treatment",
            "purification",
            "industrial",
            "piping",
            "valve",
            "gauge",
            "step",
            "fbx",
            "cad",
            "assembly",
            "mechanical",
            "engineering",
            "factory",
            "plant",
            "equipment",
            "pvc",
            "clean",
            "ro",
            "solid",
        ],
        'description': "INDUSTRIAL WATER TREATMENT 3D CAD MODEL\n\nNeed an industrial water-treatment skid without modeling every vessel, valve, fitting and pipe from scratch?\nThis detailed CAD asset provides a practical starting point for industrial water-treatment layouts, proposal and concept visualization, training content and 3D presentations.\n\nSYSTEM OVERVIEW:\n- System: Dual 7x40\" Stainless Cartridge Filter Skid\n- Reference System Capacity: ~20 m³/h\n- Configuration: Dual Parallel 7-Element 40-Inch Housings with Manual Bypass\n\nThe model represents a cartridge filtration skid arrangement including major equipment, piping, valves, fittings, instrumentation and structural components as shown in the preview images.\n\nMAIN EQUIPMENT:\n- Dual SUS304 7-element 40\" cartridge filter housings\n- uPVC main manifold headers and branch piping\n- Manual bypass line for maintenance isolation\n- Isolation valves, sampling ports, pressure gauges and air vent fittings\n- SUS304 skid support frame with caster wheels\n\nINCLUDED FILE FORMATS:\n- STEP (.stp) — CAD exchange\n- FBX (.fbx) — DCC and real-time visualization\n- Blender (.blend) — Native 3D scene\n- OBJ (.obj + .mtl) — Universal mesh exchange\n- GLTF / GLB (.glb) — Web 3D and AR/VR\n- STL (.stl), SAT (.sat), IGES (.igs)\n- 2D Drawing Sheets (.dwg, .pdf, .png)\n\nSUITABLE FOR:\n- Industrial water-treatment visualization and plant layout planning\n- Conceptual GA and layout development\n- Proposal and concept visualization\n- Technical presentations, training and educational content\n- Animation, Unreal Engine, Unity, Blender and real-time 3D workflows\n\nIMPORTANT INFORMATION:\nThis product is a 3D digital asset intended primarily for visualization, reference, layout development, presentations and related design workflows. It is not a manufacturer-certified model, engineering calculation, construction document, fabrication drawing, process design, or performance guarantee.\nDimensions, component specifications, connections, clearances, materials and other technical details may differ from actual equipment or later manufacturer revisions. Verify all critical information against current manufacturer documentation and project requirements before procurement, fabrication, installation or construction.\nThe purchaser is responsible for evaluating the asset's suitability for their intended use and for carrying out any project-specific engineering verification that may be required.\n\nAssembly created and prepared by WaterTreatment3D."
    },
    'SKID_Ultrafiltration_UF_Dual_10000L_Outside_In_20m3h': {
        'title': "Dual 10000L Outside-In UF Membrane Skid 20m3h Pre-RO 3D CAD Model",
        'personal_price': 249.99,
        'professional_price': 449.99,
        'tags': [
            "ultrafiltration",
            "membrane",
            "uf",
            "skid",
            "water",
            "filtration",
            "treatment",
            "purification",
            "industrial",
            "pvdf",
            "filter",
            "pretreatment",
            "step",
            "fbx",
            "cad",
            "assembly",
            "mechanical",
            "engineering",
            "piping",
            "valve",
            "stainless",
            "factory",
            "plant",
            "clean",
            "solid",
        ],
        'description': "INDUSTRIAL WATER TREATMENT 3D CAD MODEL\n\nNeed an industrial water-treatment skid without modeling every vessel, valve, fitting and pipe from scratch?\nThis detailed CAD asset provides a practical starting point for industrial water-treatment layouts, proposal and concept visualization, training content and 3D presentations.\n\nSYSTEM OVERVIEW:\n- System: Dual Outside-In UF Membrane Skid\n- Reference System Capacity: ~20 m³/h (Dual ~10,000 L/h class modules)\n- Configuration: Dual Hollow-Fiber Ultrafiltration Train\n\nThe model represents a ultrafiltration skid arrangement including major equipment, piping, valves, fittings, instrumentation and structural components as shown in the preview images.\n\nMAIN EQUIPMENT:\n- Dual hollow-fiber UF membrane modules\n- uPVC feed, permeate, concentrate and backwash manifolds\n- Actuated process valves and manual isolation valves\n- Pressure gauges, check valves and sampling ports\n- SUS304 support frame with caster wheels\n\nINCLUDED FILE FORMATS:\n- STEP (.stp) — CAD exchange\n- FBX (.fbx) — DCC and real-time visualization\n- Blender (.blend) — Native 3D scene\n- OBJ (.obj + .mtl) — Universal mesh exchange\n- GLTF / GLB (.glb) — Web 3D and AR/VR\n- STL (.stl), SAT (.sat), IGES (.igs)\n- 2D Drawing Sheets (.dwg, .pdf, .png)\n\nSUITABLE FOR:\n- Industrial water-treatment visualization and plant layout planning\n- Conceptual GA and layout development\n- Proposal and concept visualization\n- Technical presentations, training and educational content\n- Animation, Unreal Engine, Unity, Blender and real-time 3D workflows\n\nIMPORTANT INFORMATION:\nThis product is a 3D digital asset intended primarily for visualization, reference, layout development, presentations and related design workflows. It is not a manufacturer-certified model, engineering calculation, construction document, fabrication drawing, process design, or performance guarantee.\nDimensions, component specifications, connections, clearances, materials and other technical details may differ from actual equipment or later manufacturer revisions. Verify all critical information against current manufacturer documentation and project requirements before procurement, fabrication, installation or construction.\nThe purchaser is responsible for evaluating the asset's suitability for their intended use and for carrying out any project-specific engineering verification that may be required.\n\nAssembly created and prepared by WaterTreatment3D."
    },
    'Water_Softener_Dual_FRP2472_Runxin_N74A3_500L_Tank_20m3h': {
        'title': "Dual FRP 2472 Water Softener System 20m3h with 500L Brine Tank CAD",
        'personal_price': 224.99,
        'professional_price': 399.99,
        'tags': [
            "softener",
            "frp",
            "duplex",
            "autovalve",
            "brine",
            "water",
            "treatment",
            "filtration",
            "skid",
            "industrial",
            "resin",
            "purification",
            "vessel",
            "tank",
            "step",
            "fbx",
            "cad",
            "assembly",
            "mechanical",
            "engineering",
            "piping",
            "valve",
            "stainless",
            "factory",
            "solid",
        ],
        'description': "INDUSTRIAL WATER TREATMENT 3D CAD MODEL\n\nNeed an industrial water-treatment skid without modeling every vessel, valve, fitting and pipe from scratch?\nThis detailed CAD asset provides a practical starting point for industrial water-treatment layouts, proposal and concept visualization, training content and 3D presentations.\n\nSYSTEM OVERVIEW:\n- System: Dual FRP 2472 Water Softener System\n- Reference System Capacity: ~20 m³/h\n- Configuration: Duplex Alternating Water Softener Vessels + ~500L Brine Tank\n\nThe model represents a duplex water softening arrangement including major equipment, piping, valves, fittings, instrumentation and structural components as shown in the preview images.\n\nMAIN EQUIPMENT:\n- Dual FRP 2472 water softener pressure vessels\n- Automatic multiport control valves\n- PE brine tank with brine line connection\n- Duplex uPVC piping manifold with bypass line and isolation ball valves\n- Structural base support channel frame\n\nINCLUDED FILE FORMATS:\n- STEP (.stp) — CAD exchange\n- FBX (.fbx) — DCC and real-time visualization\n- Blender (.blend) — Native 3D scene\n- OBJ (.obj + .mtl) — Universal mesh exchange\n- GLTF / GLB (.glb) — Web 3D and AR/VR\n- STL (.stl), SAT (.sat), IGES (.igs)\n- 2D Drawing Sheets (.dwg, .pdf, .png)\n\nSUITABLE FOR:\n- Industrial water-treatment visualization and plant layout planning\n- Conceptual GA and layout development\n- Proposal and concept visualization\n- Technical presentations, training and educational content\n- Animation, Unreal Engine, Unity, Blender and real-time 3D workflows\n\nIMPORTANT INFORMATION:\nThis product is a 3D digital asset intended primarily for visualization, reference, layout development, presentations and related design workflows. It is not a manufacturer-certified model, engineering calculation, construction document, fabrication drawing, process design, or performance guarantee.\nDimensions, component specifications, connections, clearances, materials and other technical details may differ from actual equipment or later manufacturer revisions. Verify all critical information against current manufacturer documentation and project requirements before procurement, fabrication, installation or construction.\nThe purchaser is responsible for evaluating the asset's suitability for their intended use and for carrying out any project-specific engineering verification that may be required.\n\nAssembly created and prepared by WaterTreatment3D."
    },
    'Industrial_RO_System_2m3h_2Stage_8040_UF_IoT': {
        'title': "Industrial RO System 2m3h 2-Stage 8040 UF IoT Skid 3D CAD Model",
        'personal_price': 249.99,
        'professional_price': 499.99,
        'tags': [
            "osmosis",
            "ro",
            "membrane",
            "8040",
            "iot",
            "plc",
            "hmi",
            "pump",
            "booster",
            "skid",
            "water",
            "treatment",
            "purification",
            "industrial",
            "step",
            "fbx",
            "cad",
            "assembly",
            "mechanical",
            "engineering",
            "stainless",
            "filtration",
            "factory",
            "piping",
            "valve",
        ],
        'description': "INDUSTRIAL WATER TREATMENT 3D CAD MODEL\n\nNeed an industrial water-treatment skid without modeling every vessel, valve, fitting and pipe from scratch?\nThis detailed CAD asset provides a practical starting point for industrial water-treatment layouts, proposal and concept visualization, training content and 3D presentations.\n\nSYSTEM OVERVIEW:\n- System: Industrial RO System 2m3h\n- Reference System Capacity: ~2 m³/h (~2,000 L/h)\n- Configuration: 2-Stage RO (8040 Vessels) + Pre-UF & Cartridge Filter + Control Cabinet\n\nThe model represents a industrial reverse osmosis skid arrangement including major equipment, piping, valves, fittings, instrumentation and structural components as shown in the preview images.\n\nMAIN EQUIPMENT:\n- FRP 8040 membrane pressure vessels in a 2-stage arrangement\n- Vertical multistage high-pressure booster pump\n- Pre-filtration cartridge filter housing and hollow-fiber UF module\n- Electrical control cabinet enclosure with panel interface\n- Panel flow meters, pressure switches and instrumentation\n- SUS304 tubular skid frame with leveling pads and caster wheels\n\nINCLUDED FILE FORMATS:\n- STEP (.stp) — CAD exchange\n- FBX (.fbx) — DCC and real-time visualization\n- Blender (.blend) — Native 3D scene\n- OBJ (.obj + .mtl) — Universal mesh exchange\n- GLTF / GLB (.glb) — Web 3D and AR/VR\n- STL (.stl), SAT (.sat), IGES (.igs)\n- 2D Drawing Sheets (.dwg, .pdf, .png)\n\nSUITABLE FOR:\n- Industrial water-treatment visualization and plant layout planning\n- Conceptual GA and layout development\n- Proposal and concept visualization\n- Technical presentations, training and educational content\n- Animation, Unreal Engine, Unity, Blender and real-time 3D workflows\n\nIMPORTANT INFORMATION:\nThis product is a 3D digital asset intended primarily for visualization, reference, layout development, presentations and related design workflows. It is not a manufacturer-certified model, engineering calculation, construction document, fabrication drawing, process design, or performance guarantee.\nDimensions, component specifications, connections, clearances, materials and other technical details may differ from actual equipment or later manufacturer revisions. Verify all critical information against current manufacturer documentation and project requirements before procurement, fabrication, installation or construction.\nThe purchaser is responsible for evaluating the asset's suitability for their intended use and for carrying out any project-specific engineering verification that may be required.\n\nAssembly created and prepared by WaterTreatment3D."
    },
    'Industrial_Water_Pretreatment_Skid_4m3h_Multimedia_Carbon_Softener': {
        'title': "Industrial Water Pretreatment Skid 4m3h Sand Carbon Softener CAD",
        'personal_price': 199.99,
        'professional_price': 399.99,
        'tags': [
            "pretreatment",
            "multimedia",
            "filter",
            "carbon",
            "softener",
            "frp",
            "multiport",
            "skid",
            "water",
            "treatment",
            "purification",
            "industrial",
            "filtration",
            "step",
            "fbx",
            "cad",
            "assembly",
            "mechanical",
            "engineering",
            "piping",
            "valve",
            "vessel",
            "tank",
            "stainless",
            "solid",
        ],
        'description': "INDUSTRIAL WATER TREATMENT 3D CAD MODEL\n\nNeed an industrial water-treatment skid without modeling every vessel, valve, fitting and pipe from scratch?\nThis detailed CAD asset provides a practical starting point for industrial water-treatment layouts, proposal and concept visualization, training content and 3D presentations.\n\nSYSTEM OVERVIEW:\n- System: Industrial Water Pretreatment Skid 4m3h\n- Reference System Capacity: ~4 m³/h\n- Configuration: 3-Vessel Pretreatment Train (Multimedia + Carbon + Water Softener)\n\nThe model represents a 3-stage filtration and softening arrangement including major equipment, piping, valves, fittings, instrumentation and structural components as shown in the preview images.\n\nMAIN EQUIPMENT:\n- 3 x FRP pressure vessels (multimedia filter, carbon filter, and softener configuration)\n- Automatic multiport control valves and PE brine tank\n- Interconnecting uPVC piping manifold with pressure gauges and isolation valves\n- SUS304 stainless steel base skid frame\n\nINCLUDED FILE FORMATS:\n- STEP (.stp) — CAD exchange\n- FBX (.fbx) — DCC and real-time visualization\n- Blender (.blend) — Native 3D scene\n- OBJ (.obj + .mtl) — Universal mesh exchange\n- GLTF / GLB (.glb) — Web 3D and AR/VR\n- STL (.stl), SAT (.sat), IGES (.igs)\n- 2D Drawing Sheets (.dwg, .pdf, .png)\n\nSUITABLE FOR:\n- Industrial water-treatment visualization and plant layout planning\n- Conceptual GA and layout development\n- Proposal and concept visualization\n- Technical presentations, training and educational content\n- Animation, Unreal Engine, Unity, Blender and real-time 3D workflows\n\nIMPORTANT INFORMATION:\nThis product is a 3D digital asset intended primarily for visualization, reference, layout development, presentations and related design workflows. It is not a manufacturer-certified model, engineering calculation, construction document, fabrication drawing, process design, or performance guarantee.\nDimensions, component specifications, connections, clearances, materials and other technical details may differ from actual equipment or later manufacturer revisions. Verify all critical information against current manufacturer documentation and project requirements before procurement, fabrication, installation or construction.\nThe purchaser is responsible for evaluating the asset's suitability for their intended use and for carrying out any project-specific engineering verification that may be required.\n\nAssembly created and prepared by WaterTreatment3D."
    },
    'Industrial_Water_Softener_Skid_4m3h_Dual_FRP2162_RunxinN74A3': {
        'title': "Industrial Water Softener Skid 4m3h Dual FRP 2162 Duplex CAD Model",
        'personal_price': 189.99,
        'professional_price': 374.99,
        'tags': [
            "softener",
            "frp",
            "duplex",
            "multiport",
            "purification",
            "water",
            "treatment",
            "filtration",
            "skid",
            "industrial",
            "resin",
            "vessel",
            "tank",
            "step",
            "fbx",
            "cad",
            "assembly",
            "mechanical",
            "engineering",
            "piping",
            "valve",
            "stainless",
            "factory",
            "brine",
            "solid",
        ],
        'description': "INDUSTRIAL WATER TREATMENT 3D CAD MODEL\n\nNeed an industrial water-treatment skid without modeling every vessel, valve, fitting and pipe from scratch?\nThis detailed CAD asset provides a practical starting point for industrial water-treatment layouts, proposal and concept visualization, training content and 3D presentations.\n\nSYSTEM OVERVIEW:\n- System: Industrial Water Softener Skid 4m3h\n- Reference System Capacity: ~4 m³/h\n- Configuration: Dual FRP 2162 Vessels + Duplex Piping + Brine Tank\n\nThe model represents a duplex water softening skid arrangement including major equipment, piping, valves, fittings, instrumentation and structural components as shown in the preview images.\n\nMAIN EQUIPMENT:\n- Dual FRP 2162 water softener pressure vessels\n- Automatic multiport control valves and PE brine tank\n- Duplex uPVC piping manifold with bypass and isolation ball valves\n- SUS304 stainless steel skid base with caster wheels\n\nINCLUDED FILE FORMATS:\n- STEP (.stp) — CAD exchange\n- FBX (.fbx) — DCC and real-time visualization\n- Blender (.blend) — Native 3D scene\n- OBJ (.obj + .mtl) — Universal mesh exchange\n- GLTF / GLB (.glb) — Web 3D and AR/VR\n- STL (.stl), SAT (.sat), IGES (.igs)\n- 2D Drawing Sheets (.dwg, .pdf, .png)\n\nSUITABLE FOR:\n- Industrial water-treatment visualization and plant layout planning\n- Conceptual GA and layout development\n- Proposal and concept visualization\n- Technical presentations, training and educational content\n- Animation, Unreal Engine, Unity, Blender and real-time 3D workflows\n\nIMPORTANT INFORMATION:\nThis product is a 3D digital asset intended primarily for visualization, reference, layout development, presentations and related design workflows. It is not a manufacturer-certified model, engineering calculation, construction document, fabrication drawing, process design, or performance guarantee.\nDimensions, component specifications, connections, clearances, materials and other technical details may differ from actual equipment or later manufacturer revisions. Verify all critical information against current manufacturer documentation and project requirements before procurement, fabrication, installation or construction.\nThe purchaser is responsible for evaluating the asset's suitability for their intended use and for carrying out any project-specific engineering verification that may be required.\n\nAssembly created and prepared by WaterTreatment3D."
    },
    'Commercial_Alkaline_Water_Feeder_Cabinet_RO_Booster_1um_0.2um': {
        'title': "Commercial Alkaline Water Feeder Cabinet RO Booster Filtration CAD",
        'personal_price': 189.99,
        'professional_price': 374.99,
        'tags': [
            "alkaline",
            "cabinet",
            "booster",
            "pump",
            "filtration",
            "polishing",
            "cartridge",
            "filter",
            "water",
            "purification",
            "commercial",
            "sanitary",
            "enclosure",
            "step",
            "fbx",
            "cad",
            "assembly",
            "mechanical",
            "engineering",
            "stainless",
            "medical",
            "ionizer",
            "clean",
            "piping",
            "valve",
        ],
        'description': "INDUSTRIAL WATER TREATMENT 3D CAD MODEL\n\nNeed an industrial water-treatment skid without modeling every vessel, valve, fitting and pipe from scratch?\nThis detailed CAD asset provides a practical starting point for industrial water-treatment layouts, proposal and concept visualization, training content and 3D presentations.\n\nSYSTEM OVERVIEW:\n- System: Commercial Alkaline Water Feeder Cabinet\n- Reference System Capacity: Commercial feed-water conditioning unit (reference configuration)\n- Configuration: SUS304 Cabinet Enclosure + Booster Pump + Two-Stage Cartridge Filtration\n\nThe model represents a enclosed water booster and filtration cabinet arrangement including major equipment, piping, valves, fittings, instrumentation and structural components as shown in the preview images.\n\nMAIN EQUIPMENT:\n- SUS304 stainless steel cabinet enclosure with dual front access doors\n- Internal booster pump assembly and two-stage cartridge filter housings\n- Pressure sensor, internal piping and quick-connect fittings\n\nINCLUDED FILE FORMATS:\n- STEP (.stp) — CAD exchange\n- FBX (.fbx) — DCC and real-time visualization\n- Blender (.blend) — Native 3D scene\n- OBJ (.obj + .mtl) — Universal mesh exchange\n- GLTF / GLB (.glb) — Web 3D and AR/VR\n- STL (.stl), SAT (.sat), IGES (.igs)\n- 2D Drawing Sheets (.dwg, .pdf, .png)\n\nSUITABLE FOR:\n- Industrial water-treatment visualization and plant layout planning\n- Conceptual GA and layout development\n- Proposal and concept visualization\n- Technical presentations, training and educational content\n- Animation, Unreal Engine, Unity, Blender and real-time 3D workflows\n\nIMPORTANT INFORMATION:\nThis product is a 3D digital asset intended primarily for visualization, reference, layout development, presentations and related design workflows. It is not a manufacturer-certified model, engineering calculation, construction document, fabrication drawing, process design, or performance guarantee.\nDimensions, component specifications, connections, clearances, materials and other technical details may differ from actual equipment or later manufacturer revisions. Verify all critical information against current manufacturer documentation and project requirements before procurement, fabrication, installation or construction.\nThe purchaser is responsible for evaluating the asset's suitability for their intended use and for carrying out any project-specific engineering verification that may be required.\n\nAssembly created and prepared by WaterTreatment3D."
    },
    'Johkasou_Chemical_Dosing_System_3Tank_300L': {
        'title': "Johkasou Chemical Dosing System 3x300L Skid Frame 3D CAD Model",
        'personal_price': 224.99,
        'professional_price': 449.99,
        'tags': [
            "dosing",
            "chemical",
            "johkasou",
            "tank",
            "mixer",
            "agitator",
            "pump",
            "diaphragm",
            "pac",
            "naoh",
            "water",
            "wastewater",
            "treatment",
            "skid",
            "industrial",
            "vessel",
            "step",
            "fbx",
            "cad",
            "assembly",
            "mechanical",
            "engineering",
            "stainless",
            "japan",
            "solid",
        ],
        'description': "INDUSTRIAL WATER TREATMENT 3D CAD MODEL\n\nNeed an industrial water-treatment skid without modeling every vessel, valve, fitting and pipe from scratch?\nThis detailed CAD asset provides a practical starting point for industrial water-treatment layouts, proposal and concept visualization, training content and 3D presentations.\n\nSYSTEM OVERVIEW:\n- System: Johkasou Chemical Dosing System\n- Reference System Capacity: ~3 x 300 L chemical tanks (reference configuration)\n- Configuration: 3 PE Tanks + Mechanical Agitator + 3 Metering Pumps + Skid Frame\n\nThe model represents a chemical dosing and metering skid arrangement including major equipment, piping, valves, fittings, instrumentation and structural components as shown in the preview images.\n\nMAIN EQUIPMENT:\n- 3 x Cylindrical PE chemical storage tanks\n- Top-mounted electric gearmotor agitator mixer\n- 3 x Chemical metering pumps with calibration columns\n- SUS304 structural skid base with integrated drip containment tray\n- Dosing manifold piping, valves and accessories\n\nINCLUDED FILE FORMATS:\n- STEP (.stp) — CAD exchange\n- FBX (.fbx) — DCC and real-time visualization\n- Blender (.blend) — Native 3D scene\n- OBJ (.obj + .mtl) — Universal mesh exchange\n- GLTF / GLB (.glb) — Web 3D and AR/VR\n- STL (.stl), SAT (.sat), IGES (.igs)\n- 2D Drawing Sheets (.dwg, .pdf, .png)\n\nSUITABLE FOR:\n- Industrial water-treatment visualization and plant layout planning\n- Conceptual GA and layout development\n- Proposal and concept visualization\n- Technical presentations, training and educational content\n- Animation, Unreal Engine, Unity, Blender and real-time 3D workflows\n\nIMPORTANT INFORMATION:\nThis product is a 3D digital asset intended primarily for visualization, reference, layout development, presentations and related design workflows. It is not a manufacturer-certified model, engineering calculation, construction document, fabrication drawing, process design, or performance guarantee.\nDimensions, component specifications, connections, clearances, materials and other technical details may differ from actual equipment or later manufacturer revisions. Verify all critical information against current manufacturer documentation and project requirements before procurement, fabrication, installation or construction.\nThe purchaser is responsible for evaluating the asset's suitability for their intended use and for carrying out any project-specific engineering verification that may be required.\n\nAssembly created and prepared by WaterTreatment3D."
    },
    'Whole_House_UF_Polishing_Skid_2m3h_Dual_Cartridge_UV': {
        'title': "Whole House UF Polishing Skid 2m3h Dual Cartridge UV 3D CAD Model",
        'personal_price': 179.99,
        'professional_price': 349.99,
        'tags': [
            "filtration",
            "residential",
            "villa",
            "ultrafiltration",
            "uf",
            "uv",
            "sterilizer",
            "cartridge",
            "filter",
            "water",
            "purification",
            "treatment",
            "skid",
            "stainless",
            "step",
            "fbx",
            "cad",
            "assembly",
            "mechanical",
            "engineering",
            "piping",
            "valve",
            "purifier",
            "clean",
            "solid",
        ],
        'description': "INDUSTRIAL WATER TREATMENT 3D CAD MODEL\n\nNeed an industrial water-treatment skid without modeling every vessel, valve, fitting and pipe from scratch?\nThis detailed CAD asset provides a practical starting point for industrial water-treatment layouts, proposal and concept visualization, training content and 3D presentations.\n\nSYSTEM OVERVIEW:\n- System: Whole House UF Polishing Skid 2m3h\n- Reference System Capacity: ~2 m³/h (~2,000 L/h)\n- Configuration: Dual Cartridge Filtration + Hollow-Fiber UF Module + UV Chamber\n\nThe model represents a water polishing skid arrangement including major equipment, piping, valves, fittings, instrumentation and structural components as shown in the preview images.\n\nMAIN EQUIPMENT:\n- Dual SUS304 stainless steel cartridge filter housings\n- Hollow-fiber UF membrane module and SUS304 ultraviolet (UV) chamber\n- Compact SUS304 mobile frame with caster wheels\n- uPVC isolation valves, bypass line and sampling ports\n\nINCLUDED FILE FORMATS:\n- STEP (.stp) — CAD exchange\n- FBX (.fbx) — DCC and real-time visualization\n- Blender (.blend) — Native 3D scene\n- OBJ (.obj + .mtl) — Universal mesh exchange\n- GLTF / GLB (.glb) — Web 3D and AR/VR\n- STL (.stl), SAT (.sat), IGES (.igs)\n- 2D Drawing Sheets (.dwg, .pdf, .png)\n\nSUITABLE FOR:\n- Industrial water-treatment visualization and plant layout planning\n- Conceptual GA and layout development\n- Proposal and concept visualization\n- Technical presentations, training and educational content\n- Animation, Unreal Engine, Unity, Blender and real-time 3D workflows\n\nIMPORTANT INFORMATION:\nThis product is a 3D digital asset intended primarily for visualization, reference, layout development, presentations and related design workflows. It is not a manufacturer-certified model, engineering calculation, construction document, fabrication drawing, process design, or performance guarantee.\nDimensions, component specifications, connections, clearances, materials and other technical details may differ from actual equipment or later manufacturer revisions. Verify all critical information against current manufacturer documentation and project requirements before procurement, fabrication, installation or construction.\nThe purchaser is responsible for evaluating the asset's suitability for their intended use and for carrying out any project-specific engineering verification that may be required.\n\nAssembly created and prepared by WaterTreatment3D."
    },
    'Residential_WholeHouse_Water_Purifier_Disc_UF_UV': {
        'title': "Residential Whole House Water Purifier Disc Filter UF UV Skid CAD",
        'personal_price': 169.99,
        'professional_price': 324.99,
        'tags': [
            "residential",
            "purifier",
            "filter",
            "ultrafiltration",
            "uf",
            "uv",
            "sterilizer",
            "housing",
            "skid",
            "water",
            "treatment",
            "filtration",
            "step",
            "fbx",
            "cad",
            "assembly",
            "mechanical",
            "engineering",
            "piping",
            "valve",
            "pump",
            "stainless",
            "clean",
            "villa",
            "solid",
        ],
        'description': "INDUSTRIAL WATER TREATMENT 3D CAD MODEL\n\nNeed an industrial water-treatment skid without modeling every vessel, valve, fitting and pipe from scratch?\nThis detailed CAD asset provides a practical starting point for industrial water-treatment layouts, proposal and concept visualization, training content and 3D presentations.\n\nSYSTEM OVERVIEW:\n- System: Residential Whole House Water Purifier Skid\n- Reference System Capacity: ~3 m³/h (~3,000 L/h)\n- Configuration: Booster Pump + Disc Filter + Cartridge Housings + UF Module + UV Chamber\n\nThe model represents a multistage residential water treatment skid arrangement including major equipment, piping, valves, fittings, instrumentation and structural components as shown in the preview images.\n\nMAIN EQUIPMENT:\n- Water booster pump unit and disc pre-filter\n- Big Blue 20\" filter housing and multi-cartridge stainless housing\n- Hollow-fiber UF membrane module and stainless steel UV chamber\n- Compact stainless steel mobile skid frame with caster wheels\n\nINCLUDED FILE FORMATS:\n- STEP (.stp) — CAD exchange\n- FBX (.fbx) — DCC and real-time visualization\n- Blender (.blend) — Native 3D scene\n- OBJ (.obj + .mtl) — Universal mesh exchange\n- GLTF / GLB (.glb) — Web 3D and AR/VR\n- STL (.stl), SAT (.sat), IGES (.igs)\n- 2D Drawing Sheets (.dwg, .pdf, .png)\n\nSUITABLE FOR:\n- Industrial water-treatment visualization and plant layout planning\n- Conceptual GA and layout development\n- Proposal and concept visualization\n- Technical presentations, training and educational content\n- Animation, Unreal Engine, Unity, Blender and real-time 3D workflows\n\nIMPORTANT INFORMATION:\nThis product is a 3D digital asset intended primarily for visualization, reference, layout development, presentations and related design workflows. It is not a manufacturer-certified model, engineering calculation, construction document, fabrication drawing, process design, or performance guarantee.\nDimensions, component specifications, connections, clearances, materials and other technical details may differ from actual equipment or later manufacturer revisions. Verify all critical information against current manufacturer documentation and project requirements before procurement, fabrication, installation or construction.\nThe purchaser is responsible for evaluating the asset's suitability for their intended use and for carrying out any project-specific engineering verification that may be required.\n\nAssembly created and prepared by WaterTreatment3D."
    },
}

# ============================================================
# TÌM KIẾM FILE TỰ ĐỘNG THÔNG MINH
# ============================================================
def find_zip(folder_path, name):
    # 1. Tìm ZIP trong root
    zips = glob.glob(os.path.join(folder_path, '*.zip'))
    if zips:
        return zips[0]
    
    # 2. Tìm trong 06_Renders_and_Media\01_Marketplace_Upload_Package
    pkg_dir = os.path.join(folder_path, '06_Renders_and_Media', '01_Marketplace_Upload_Package')
    if os.path.exists(pkg_dir):
        pkg_zips = glob.glob(os.path.join(pkg_dir, '*.zip'))
        if pkg_zips:
            return pkg_zips[0]
            
    # 3. Tìm đệ quy trong thư mục
    all_zips = glob.glob(os.path.join(folder_path, '**', '*.zip'), recursive=True)
    if all_zips:
        return all_zips[0]
        
    # 4. Fallback
    return os.path.join(folder_path, f'{name}_Universal_CAD.zip')

def find_thumb(folder_path, name):
    # 1. Tìm thumbnail chuẩn ở root
    for n in ['thumbnail.png', 'thumbnail.jpg', 'thumb.png', 'thumb.jpg']:
        p = os.path.join(folder_path, n)
        if os.path.exists(p):
            return p
            
    # 2. Tìm Hero render trong 06_Renders_and_Media
    media_dir = os.path.join(folder_path, '06_Renders_and_Media')
    if os.path.exists(media_dir):
        heroes = glob.glob(os.path.join(media_dir, '**', '*Hero*TopRight*.png'), recursive=True) + \
                 glob.glob(os.path.join(media_dir, '**', '*Hero*.png'), recursive=True) + \
                 glob.glob(os.path.join(media_dir, '**', '*hero*.png'), recursive=True)
        if heroes:
            return heroes[0]
            
    # 3. Tìm ảnh bất kỳ trong root
    imgs = glob.glob(os.path.join(folder_path, '*.png')) + glob.glob(os.path.join(folder_path, '*.jpg'))
    if imgs:
        return imgs[0]
        
    # 4. Fallback
    return os.path.join(folder_path, 'thumbnail.png')

# ============================================================
# QUÉT DỰ ÁN
# ============================================================
def scan_projects(projects_dir):
    entries = []
    if not os.path.isdir(projects_dir):
        print(f'[ERROR] Not found: {projects_dir}'); return entries
    
    for folder_name in sorted(os.listdir(projects_dir)):
        fp = os.path.join(projects_dir, folder_name)
        if not os.path.isdir(fp) or folder_name.startswith('.') or folder_name.startswith('_'):
            continue
        if folder_name in EXCLUDE_DIRS:
            print(f'  [-] Excluding non-skid directory: {folder_name}')
            continue
            
        meta = PROJECTS_METADATA.get(folder_name, None)
        if meta:
            title = meta['title']
            pp = meta['personal_price']
            pro = meta['professional_price']
            tags = meta['tags']
            desc = meta['description']
        else:
            # Fallback
            clean = folder_name.replace('_', ' ')
            title = f"{clean[:55]} CAD Skid Assembly"
            pp = 109.99
            pro = 179.99
            tags = ["industrial", "water", "treatment", "skid", "step", "fbx", "cad"]
            desc = f"{clean} - Full Skid CAD 3D Assembly\\nCreated by WaterTreatment3D."
            
        entries.append({
            'name': folder_name,
            'title': title,
            'personal_price': pp,
            'professional_price': pro,
            'category': 'Tools, Objects & Decor',
            'tags': tags,
            'description': desc,
            'zip_path': find_zip(fp, folder_name),
            'thumb_path': find_thumb(fp, folder_name),
            'folder_path': fp,
        })
        print(f'  [+] {folder_name} -> "${pp} / ${pro}" | Title: {title} ({len(title)} chars)')
    return entries

def entries_to_js(entries):
    import json
    parts = []
    for e in entries:
        tags_js = ',\n        '.join(json.dumps(t) for t in e['tags'])
        desc_js = json.dumps(e['description'])
        title_js = json.dumps(e['title'])
        name_js = json.dumps(e['name'])
        cat_js = json.dumps(e['category'])
        zip_js = json.dumps(e['zip_path'])
        thumb_js = json.dumps(e['thumb_path'])
        folder_js = json.dumps(e['folder_path'])
        parts.append(
            f'    {{\n'
            f'      "name": {name_js},\n'
            f'      "title": {title_js},\n'
            f'      "personal_price": {e["personal_price"]},\n'
            f'      "professional_price": {e["professional_price"]},\n'
            f'      "category": {cat_js},\n'
            f'      "tags": [\n        {tags_js}\n      ],\n'
            f'      "description": {desc_js},\n'
            f'      "zip_path": {zip_js},\n'
            f'      "thumb_path": {thumb_js},\n'
            f'      "folder_path": {folder_js}\n'
            f'    }}'
        )
    return ',\n'.join(parts)

def build_extension_zip(ext_dir, output_zip):
    print(f"\nPackaging extension ZIP: {output_zip} ...")
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(ext_dir):
            if any(skip in root for skip in ['.git', '__pycache__', 'node_modules', '.bak']):
                continue
            for f in files:
                if f.endswith(('.zip', '.bak', '.bak_before_sync')):
                    continue
                file_path = os.path.join(root, f)
                arcname = os.path.relpath(file_path, ext_dir)
                z.write(file_path, arcname)
    print(f"Extension packaged successfully ({os.path.getsize(output_zip):,} bytes).")

# ============================================================
# MAIN
# ============================================================
def main():
    print('=' * 65)
    print(' WT3D FAB EXTENSION - Auto-Sync Projects to Extension DB (V3.6.6)')
    print('=' * 65)
    print(f'Scanning: {PROJECTS_DIR}\n')

    # 1. Scan
    entries = scan_projects(PROJECTS_DIR)
    if not entries:
        print('[ERROR] No projects found!'); return
    print(f'\nTotal CAD Skid Projects: {len(entries)}')

    # 2. Read content.js
    content = open(CONTENT_JS, encoding='utf-8').read()

    # 3. Backup
    bak = os.path.join(r'D:\WT3D_Project\Z_Tools\Archive_Extension_ZIPs', 'content.js.bak_before_sync')
    shutil.copy2(CONTENT_JS, bak)
    print(f'Backup -> {bak}')

    # 4. Build new block
    entries_js = entries_to_js(entries)
    new_block = (
        f'{BEGIN_MARKER}\n'
        f'  ,\n'
        f'  {CATEGORY_KEY}: [\n'
        f'{entries_js}\n'
        f'  ]\n'
        f'{END_MARKER}'
    )

    # 5. ATOMIC INJECTION
    if BEGIN_MARKER in content and END_MARKER in content:
        b_pos = content.find(BEGIN_MARKER)
        e_pos = content.find(END_MARKER) + len(END_MARKER)
        content_new = content[:b_pos] + new_block + content[e_pos:]
        print('[INFO] Replaced existing block between markers safely.')
    else:
        db_start = content.find('const WT3D_DATABASE = {')
        if db_start < 0:
            print('[ERROR] WT3D_DATABASE not found!'); return
        db_chunk = content[db_start:]
        close_m = re.search(r'\n\};\n', db_chunk)
        if not close_m:
            print('[ERROR] Closing }; of WT3D_DATABASE not found!'); return
        insert_at = db_start + close_m.start()
        content_new = (
            content[:insert_at]
            + '\n' + new_block
            + '\n};\n'
            + content[db_start + close_m.end():]
        )
        print('[INFO] Injected block with markers (initial setup).')

    # 6. VERIFY BRACKETS
    opens  = content_new.count('{')
    closes = content_new.count('}')
    diff   = opens - closes
    print(f'Bracket Check: {opens} open, {closes} close (diff={diff})')
    if abs(diff) > 5:
        print('[ERROR] Bracket imbalance! Aborting.')
        return

    # 7. BUMP MANIFEST VERSION
    man = open(MANIFEST_PATH, encoding='utf-8').read()
    ver_m = re.search(r'"version":\s*"([\d.]+)"', man)
    if ver_m:
        parts = ver_m.group(1).split('.')
        parts[-1] = str(int(parts[-1]) + 1)
        new_ver = '.'.join(parts)
        man_new = re.sub(r'"version":\s*"[\d.]+"', f'"version": "{new_ver}"', man)
        man_new = re.sub(r'v3\.\d+\.\d+', f'v{new_ver}', man_new)
        open(MANIFEST_PATH, 'w', encoding='utf-8').write(man_new)
        print(f'Manifest Version: {ver_m.group(1)} -> {new_ver}')
    else:
        new_ver = "3.6.6"

    # 8. WRITE & SYNC BOTH LOCATIONS
    open(CONTENT_JS, 'w', encoding='utf-8').write(content_new)
    if os.path.exists(os.path.dirname(CONTENT_JS2)):
        shutil.copy2(CONTENT_JS, CONTENT_JS2)
    if os.path.exists(os.path.dirname(MANIFEST_PATH2)):
        shutil.copy2(MANIFEST_PATH, MANIFEST_PATH2)

    nlines = len(content_new.split('\n'))
    print(f'\nWrote {CONTENT_JS}: {nlines:,} lines, {len(content_new):,} bytes')
    print(f'Synced to {CONTENT_JS2}')
    print(f'{len(entries)} skid projects active in extension database.')

    # 9. BUILD ZIP FOR EASY CHROME/EDGE INSTALLATION
    ext_dir = os.path.dirname(CONTENT_JS)
    out_zip = os.path.join(r'D:\WT3D_Project\Z_Tools\Archive_Extension_ZIPs', f'WT3D_Fab_Extension_v{new_ver}.zip')
    build_extension_zip(ext_dir, out_zip)

    # Also make a standard unversioned zip in Z_Tools
    unversioned_zip = os.path.join(r'D:\WT3D_Project\Z_Tools', 'WT3D_Fab_Extension_Latest.zip')
    shutil.copy2(out_zip, unversioned_zip)
    print(f"Latest ZIP updated: {unversioned_zip}")

    print('\n' + '=' * 65)
    print(' >>> 100% READY! Reload extension in Chrome/Edge (chrome://extensions) <<<')
    print('=' * 65)


    # [POKA-YOKE: CLEANUP __pycache__ TO PREVENT CHROME EXTENSION ERROR]
    for _ed in [os.path.dirname(CONTENT_JS), os.path.dirname(CONTENT_JS2)]:
        if os.path.exists(_ed):
            for _r, _dirs, _files in os.walk(_ed):
                for _d in list(_dirs):
                    if _d.startswith('_'):
                        shutil.rmtree(os.path.join(_r, _d), ignore_errors=True)
                for _fn in _files:
                    if _fn.startswith('_') or _fn.endswith('.pyc'):
                        try: os.remove(os.path.join(_r, _fn))
                        except Exception: pass

if __name__ == '__main__':
    main()
