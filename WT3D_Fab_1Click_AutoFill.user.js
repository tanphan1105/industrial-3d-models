// ==UserScript==
// @name         WT3D Fab.com 1-Click Draft Auto-Fill (Radix/React 18 Compatible)
// @namespace    https://watertreatment3d.com/
// @version      4.7.0
// @description  Tự động điền Title, Desc, Category, 20 Tags, Price, FAQ cho Fab.com portal - 211 industrial 3D models (Anti-Bot Sequential + Auto-Auditing + Self-Healing Remediation Loop)
// @author       WaterTreatment3D Engineering Studio
// @match        https://www.fab.com/portal/listings/*
// @match        https://fab.com/portal/listings/*
// @grant        clipboardWrite
// @grant        storage
// ==/UserScript==
(function() {
    'use strict';

    const WT3D_DATABASE = {
  "01_Pumps_and_Motors": [
    {
      "name": "BlueWhite_C630P_Chemical_Dosing_Pump",
      "title": "BlueWhite C630P Chemical Dosing Pump - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "BlueWhite C630P Chemical Dosing Pump - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\BlueWhite_C630P_Chemical_Dosing_Pump\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\BlueWhite_C630P_Chemical_Dosing_Pump_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\BlueWhite_C630P_Chemical_Dosing_Pump\\06_Renders_and_Media\\04_Watermarked_Exports\\BlueWhite_C630P_Chemical_Dosing_Pump_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\BlueWhite_C630P_Chemical_Dosing_Pump\\06_Renders_and_Media"
    },
    {
      "name": "CNP_CDH20_17_Flange_Pump",
      "title": "CNP CDH20 17 Flange Pump - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "CNP CDH20 17 Flange Pump - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\CNP_CDH20_17_Flange_Pump\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\CNP_CDH20_17_Flange_Pump_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\CNP_CDH20_17_Flange_Pump\\06_Renders_and_Media\\04_Watermarked_Exports\\CNP_CDH20_17_Flange_Pump_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\CNP_CDH20_17_Flange_Pump\\06_Renders_and_Media"
    },
    {
      "name": "CNP_CDLF15_RO_Booster_Pump",
      "title": "CNP CDLF15 RO Booster Pump - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "CNP CDLF15 RO Booster Pump - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\CNP_CDLF15_RO_Booster_Pump\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\CNP_CDLF15_RO_Booster_Pump_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\CNP_CDLF15_RO_Booster_Pump\\06_Renders_and_Media\\04_Watermarked_Exports\\CNP_CDLF15_RO_Booster_Pump_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\CNP_CDLF15_RO_Booster_Pump\\06_Renders_and_Media"
    },
    {
      "name": "CNP_CDMF15_RO_Booster_Pump",
      "title": "CNP CDMF15 RO Booster Pump - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "CNP CDMF15 RO Booster Pump - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\CNP_CDMF15_RO_Booster_Pump\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\CNP_CDMF15_RO_Booster_Pump_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\CNP_CDMF15_RO_Booster_Pump\\06_Renders_and_Media\\04_Watermarked_Exports\\CNP_CDMF15_RO_Booster_Pump_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\CNP_CDMF15_RO_Booster_Pump\\06_Renders_and_Media"
    },
    {
      "name": "CNP_ZS65_Horizontal_Centrifugal_Pump",
      "title": "CNP ZS65 Horizontal Centrifugal Pump - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "CNP ZS65 Horizontal Centrifugal Pump - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\CNP_ZS65_Horizontal_Centrifugal_Pump\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\CNP_ZS65_Horizontal_Centrifugal_Pump_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\CNP_ZS65_Horizontal_Centrifugal_Pump\\06_Renders_and_Media\\04_Watermarked_Exports\\CNP_ZS65_Horizontal_Centrifugal_Pump_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\CNP_ZS65_Horizontal_Centrifugal_Pump\\06_Renders_and_Media"
    },
    {
      "name": "Digital_Chemical_Dosing_Pump_4_20mA",
      "title": "Digital Chemical Dosing Pump 4 20mA - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Digital Chemical Dosing Pump 4 20mA - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\Digital_Chemical_Dosing_Pump_4_20mA\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Digital_Chemical_Dosing_Pump_4_20mA_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\Digital_Chemical_Dosing_Pump_4_20mA\\06_Renders_and_Media\\04_Watermarked_Exports\\Digital_Chemical_Dosing_Pump_4_20mA_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\Digital_Chemical_Dosing_Pump_4_20mA\\06_Renders_and_Media"
    },
    {
      "name": "High_Pressure_RO_Booster_Pump",
      "title": "High Pressure RO Booster Pump - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "High Pressure RO Booster Pump - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\High_Pressure_RO_Booster_Pump\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\High_Pressure_RO_Booster_Pump_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\High_Pressure_RO_Booster_Pump\\06_Renders_and_Media\\04_Watermarked_Exports\\High_Pressure_RO_Booster_Pump_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\High_Pressure_RO_Booster_Pump\\06_Renders_and_Media"
    },
    {
      "name": "Industrial_3Phase_Motor_0_37kW",
      "title": "Industrial 3Phase Motor 0 37kW - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Industrial 3Phase Motor 0 37kW - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\Industrial_3Phase_Motor_0_37kW\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Industrial_3Phase_Motor_0_37kW_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\Industrial_3Phase_Motor_0_37kW\\06_Renders_and_Media\\04_Watermarked_Exports\\Industrial_3Phase_Motor_0_37kW_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\Industrial_3Phase_Motor_0_37kW\\06_Renders_and_Media"
    },
    {
      "name": "Nikkiso_Nano_A_Chemical_Dosing_Pump",
      "title": "Nikkiso Nano A Chemical Dosing Pump - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Nikkiso Nano A Chemical Dosing Pump - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\Nikkiso_Nano_A_Chemical_Dosing_Pump\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Nikkiso_Nano_A_Chemical_Dosing_Pump_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\Nikkiso_Nano_A_Chemical_Dosing_Pump\\06_Renders_and_Media\\04_Watermarked_Exports\\Nikkiso_Nano_A_Chemical_Dosing_Pump_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\Nikkiso_Nano_A_Chemical_Dosing_Pump\\06_Renders_and_Media"
    },
    {
      "name": "SEKO_AKL803_Dosing_Pump_Station",
      "title": "SEKO AKL803 Dosing Pump Station - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "SEKO AKL803 Dosing Pump Station - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\SEKO_AKL803_Dosing_Pump_Station\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\SEKO_AKL803_Dosing_Pump_Station_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\SEKO_AKL803_Dosing_Pump_Station\\06_Renders_and_Media\\04_Watermarked_Exports\\SEKO_AKL803_Dosing_Pump_Station_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\SEKO_AKL803_Dosing_Pump_Station\\06_Renders_and_Media"
    },
    {
      "name": "Tunglee_0_4kW_Gear_Motor_3Phase",
      "title": "Tunglee 0 4kW Gear Motor 3Phase - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Tunglee 0 4kW Gear Motor 3Phase - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\Tunglee_0_4kW_Gear_Motor_3Phase\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Tunglee_0_4kW_Gear_Motor_3Phase_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\Tunglee_0_4kW_Gear_Motor_3Phase\\06_Renders_and_Media\\04_Watermarked_Exports\\Tunglee_0_4kW_Gear_Motor_3Phase_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\01_Pumps_and_Motors\\Tunglee_0_4kW_Gear_Motor_3Phase\\06_Renders_and_Media"
    }
  ],
  "02_Tanks_and_Pressure_Vessels": [
    {
      "name": "Brine_Salt_Tank_100L_PE_with_Brine_Well",
      "title": "Brine Salt Tank 100L PE with Brine Well - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Brine Salt Tank 100L PE with Brine Well - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Brine_Salt_Tank_100L_PE_with_Brine_Well\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Brine_Salt_Tank_100L_PE_with_Brine_Well_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Brine_Salt_Tank_100L_PE_with_Brine_Well\\06_Renders_and_Media\\04_Watermarked_Exports\\Brine_Salt_Tank_100L_PE_with_Brine_Well_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Brine_Salt_Tank_100L_PE_with_Brine_Well\\06_Renders_and_Media"
    },
    {
      "name": "Compact_Square_PE_Brine_Tank_80L",
      "title": "Compact Square PE Brine Tank 80L - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Compact Square PE Brine Tank 80L - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Compact_Square_PE_Brine_Tank_80L\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Compact_Square_PE_Brine_Tank_80L_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Compact_Square_PE_Brine_Tank_80L\\06_Renders_and_Media\\04_Watermarked_Exports\\Compact_Square_PE_Brine_Tank_80L_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Compact_Square_PE_Brine_Tank_80L\\06_Renders_and_Media"
    },
    {
      "name": "Industrial_Sand_Filter_Tank_D2100_SS304",
      "title": "Industrial Sand Filter Tank D2100 SS304 - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Industrial Sand Filter Tank D2100 SS304 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Industrial_Sand_Filter_Tank_D2100_SS304\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Industrial_Sand_Filter_Tank_D2100_SS304_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Industrial_Sand_Filter_Tank_D2100_SS304\\06_Renders_and_Media\\04_Watermarked_Exports\\Industrial_Sand_Filter_Tank_D2100_SS304_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Industrial_Sand_Filter_Tank_D2100_SS304\\06_Renders_and_Media"
    },
    {
      "name": "Low_Profile_Square_Brine_Tank_100L",
      "title": "Low Profile Square Brine Tank 100L - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Low Profile Square Brine Tank 100L - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Low_Profile_Square_Brine_Tank_100L\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Low_Profile_Square_Brine_Tank_100L_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Low_Profile_Square_Brine_Tank_100L\\06_Renders_and_Media\\04_Watermarked_Exports\\Low_Profile_Square_Brine_Tank_100L_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Low_Profile_Square_Brine_Tank_100L\\06_Renders_and_Media"
    },
    {
      "name": "Round_PE_Brine_Tank_200L_Softener",
      "title": "Round PE Brine Tank 200L Softener - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Round PE Brine Tank 200L Softener - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Round_PE_Brine_Tank_200L_Softener\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Round_PE_Brine_Tank_200L_Softener_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Round_PE_Brine_Tank_200L_Softener\\06_Renders_and_Media\\04_Watermarked_Exports\\Round_PE_Brine_Tank_200L_Softener_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Round_PE_Brine_Tank_200L_Softener\\06_Renders_and_Media"
    },
    {
      "name": "Round_PE_Brine_Tank_300L_Softener",
      "title": "Round PE Brine Tank 300L Softener - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Round PE Brine Tank 300L Softener - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Round_PE_Brine_Tank_300L_Softener\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Round_PE_Brine_Tank_300L_Softener_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Round_PE_Brine_Tank_300L_Softener\\06_Renders_and_Media\\04_Watermarked_Exports\\Round_PE_Brine_Tank_300L_Softener_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Round_PE_Brine_Tank_300L_Softener\\06_Renders_and_Media"
    },
    {
      "name": "Stainless_RO_Water_Tank_3000L_SUS304",
      "title": "Stainless RO Water Tank 3000L SUS304 - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Stainless RO Water Tank 3000L SUS304 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Stainless_RO_Water_Tank_3000L_SUS304\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Stainless_RO_Water_Tank_3000L_SUS304_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Stainless_RO_Water_Tank_3000L_SUS304\\06_Renders_and_Media\\04_Watermarked_Exports\\Stainless_RO_Water_Tank_3000L_SUS304_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Stainless_RO_Water_Tank_3000L_SUS304\\06_Renders_and_Media"
    },
    {
      "name": "Stainless_Steel_Storage_Tank_10m3_SUS304",
      "title": "Stainless Steel Storage Tank 10m3 SUS304 - Industrial CAD 3D Model",
      "personal_price": 189.99,
      "professional_price": 284.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Stainless Steel Storage Tank 10m3 SUS304 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Stainless_Steel_Storage_Tank_10m3_SUS304\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Stainless_Steel_Storage_Tank_10m3_SUS304_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Stainless_Steel_Storage_Tank_10m3_SUS304\\06_Renders_and_Media\\04_Watermarked_Exports\\Stainless_Steel_Storage_Tank_10m3_SUS304_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Stainless_Steel_Storage_Tank_10m3_SUS304\\06_Renders_and_Media"
    },
    {
      "name": "Stainless_Steel_Storage_Tank_2000L_Vertical_SUS304",
      "title": "Stainless Steel Storage Tank 2000L Vertical SUS304 - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Stainless Steel Storage Tank 2000L Vertical SUS304 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Stainless_Steel_Storage_Tank_2000L_Vertical_SUS304\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Stainless_Steel_Storage_Tank_2000L_Vertical_SUS304_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Stainless_Steel_Storage_Tank_2000L_Vertical_SUS304\\06_Renders_and_Media\\04_Watermarked_Exports\\Stainless_Steel_Storage_Tank_2000L_Vertical_SUS304_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\02_Tanks_and_Pressure_Vessels\\Stainless_Steel_Storage_Tank_2000L_Vertical_SUS304\\06_Renders_and_Media"
    }
  ],
  "03_Piping_and_Fittings": [
    {
      "name": "Clear_UPVC_Static_Mixer_DN25_Union",
      "title": "Clear UPVC Static Mixer DN25 Union - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Clear UPVC Static Mixer DN25 Union - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Clear_UPVC_Static_Mixer_DN25_Union\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Clear_UPVC_Static_Mixer_DN25_Union_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Clear_UPVC_Static_Mixer_DN25_Union\\06_Renders_and_Media\\04_Watermarked_Exports\\Clear_UPVC_Static_Mixer_DN25_Union_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Clear_UPVC_Static_Mixer_DN25_Union\\06_Renders_and_Media"
    },
    {
      "name": "Clear_UPVC_Static_Mixer_DN50_Union",
      "title": "Clear UPVC Static Mixer DN50 Union - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Clear UPVC Static Mixer DN50 Union - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Clear_UPVC_Static_Mixer_DN50_Union\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Clear_UPVC_Static_Mixer_DN50_Union_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Clear_UPVC_Static_Mixer_DN50_Union\\06_Renders_and_Media\\04_Watermarked_Exports\\Clear_UPVC_Static_Mixer_DN50_Union_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Clear_UPVC_Static_Mixer_DN50_Union\\06_Renders_and_Media"
    },
    {
      "name": "Dual_UPVC_Flange_Connection_DN65",
      "title": "Dual UPVC Flange Connection DN65 - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Dual UPVC Flange Connection DN65 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Dual_UPVC_Flange_Connection_DN65\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Dual_UPVC_Flange_Connection_DN65_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Dual_UPVC_Flange_Connection_DN65\\06_Renders_and_Media\\04_Watermarked_Exports\\Dual_UPVC_Flange_Connection_DN65_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Dual_UPVC_Flange_Connection_DN65\\06_Renders_and_Media"
    },
    {
      "name": "Dual_UPVC_Flange_Connection_DN80",
      "title": "Dual UPVC Flange Connection DN80 - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Dual UPVC Flange Connection DN80 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Dual_UPVC_Flange_Connection_DN80\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Dual_UPVC_Flange_Connection_DN80_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Dual_UPVC_Flange_Connection_DN80\\06_Renders_and_Media\\04_Watermarked_Exports\\Dual_UPVC_Flange_Connection_DN80_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Dual_UPVC_Flange_Connection_DN80\\06_Renders_and_Media"
    },
    {
      "name": "HDPE_Clamp_Saddle_DN80_to_DN15",
      "title": "HDPE Clamp Saddle DN80 to DN15 - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "HDPE Clamp Saddle DN80 to DN15 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\HDPE_Clamp_Saddle_DN80_to_DN15\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\HDPE_Clamp_Saddle_DN80_to_DN15_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\HDPE_Clamp_Saddle_DN80_to_DN15\\06_Renders_and_Media\\04_Watermarked_Exports\\HDPE_Clamp_Saddle_DN80_to_DN15_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\HDPE_Clamp_Saddle_DN80_to_DN15\\06_Renders_and_Media"
    },
    {
      "name": "Tied_Flexible_Pump_Connector_SUS304",
      "title": "Tied Flexible Pump Connector SUS304 - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Tied Flexible Pump Connector SUS304 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Tied_Flexible_Pump_Connector_SUS304\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Tied_Flexible_Pump_Connector_SUS304_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Tied_Flexible_Pump_Connector_SUS304\\06_Renders_and_Media\\04_Watermarked_Exports\\Tied_Flexible_Pump_Connector_SUS304_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Tied_Flexible_Pump_Connector_SUS304\\06_Renders_and_Media"
    },
    {
      "name": "Victaulic_Grooved_Joint_DN40_SS",
      "title": "Victaulic Grooved Joint DN40 SS - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Victaulic Grooved Joint DN40 SS - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Victaulic_Grooved_Joint_DN40_SS\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Victaulic_Grooved_Joint_DN40_SS_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Victaulic_Grooved_Joint_DN40_SS\\06_Renders_and_Media\\04_Watermarked_Exports\\Victaulic_Grooved_Joint_DN40_SS_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Victaulic_Grooved_Joint_DN40_SS\\06_Renders_and_Media"
    },
    {
      "name": "Victaulic_Grooved_Joint_DN50_SS",
      "title": "Victaulic Grooved Joint DN50 SS - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Victaulic Grooved Joint DN50 SS - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Victaulic_Grooved_Joint_DN50_SS\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Victaulic_Grooved_Joint_DN50_SS_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Victaulic_Grooved_Joint_DN50_SS\\06_Renders_and_Media\\04_Watermarked_Exports\\Victaulic_Grooved_Joint_DN50_SS_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\03_Piping_and_Fittings\\Victaulic_Grooved_Joint_DN50_SS\\06_Renders_and_Media"
    }
  ],
  "04_Valves_and_Actuators": [
    {
      "name": "Anti_Siphon_Chemical_Injection_Valve",
      "title": "Anti Siphon Chemical Injection Valve - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Anti Siphon Chemical Injection Valve - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Anti_Siphon_Chemical_Injection_Valve\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Anti_Siphon_Chemical_Injection_Valve_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Anti_Siphon_Chemical_Injection_Valve\\06_Renders_and_Media\\04_Watermarked_Exports\\Anti_Siphon_Chemical_Injection_Valve_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Anti_Siphon_Chemical_Injection_Valve\\06_Renders_and_Media"
    },
    {
      "name": "Auto_3Way_Backwash_Valve_DN50_Victaulic",
      "title": "Auto 3Way Backwash Valve DN50 Victaulic - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Auto 3Way Backwash Valve DN50 Victaulic - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Auto_3Way_Backwash_Valve_DN50_Victaulic\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Auto_3Way_Backwash_Valve_DN50_Victaulic_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Auto_3Way_Backwash_Valve_DN50_Victaulic\\06_Renders_and_Media\\04_Watermarked_Exports\\Auto_3Way_Backwash_Valve_DN50_Victaulic_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Auto_3Way_Backwash_Valve_DN50_Victaulic\\06_Renders_and_Media"
    },
    {
      "name": "Ball_Valve_Compact_DN25_PPR",
      "title": "Ball Valve Compact DN25 PPR - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Ball Valve Compact DN25 PPR - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Ball_Valve_Compact_DN25_PPR\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Ball_Valve_Compact_DN25_PPR_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Ball_Valve_Compact_DN25_PPR\\06_Renders_and_Media\\04_Watermarked_Exports\\Ball_Valve_Compact_DN25_PPR_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Ball_Valve_Compact_DN25_PPR\\06_Renders_and_Media"
    },
    {
      "name": "Ball_Valve_True_Union_DN32_PPR",
      "title": "Ball Valve True Union DN32 PPR - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Ball Valve True Union DN32 PPR - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Ball_Valve_True_Union_DN32_PPR\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Ball_Valve_True_Union_DN32_PPR_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Ball_Valve_True_Union_DN32_PPR\\06_Renders_and_Media\\04_Watermarked_Exports\\Ball_Valve_True_Union_DN32_PPR_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Ball_Valve_True_Union_DN32_PPR\\06_Renders_and_Media"
    },
    {
      "name": "Check_Valve_Swing_Type_DN25_PPR_uPVC",
      "title": "Check Valve Swing Type DN25 PPR uPVC - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Check Valve Swing Type DN25 PPR uPVC - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Check_Valve_Swing_Type_DN25_PPR_uPVC\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Check_Valve_Swing_Type_DN25_PPR_uPVC_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Check_Valve_Swing_Type_DN25_PPR_uPVC\\06_Renders_and_Media\\04_Watermarked_Exports\\Check_Valve_Swing_Type_DN25_PPR_uPVC_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Check_Valve_Swing_Type_DN25_PPR_uPVC\\06_Renders_and_Media"
    },
    {
      "name": "Electric_Ball_Valve_DN40_KE006_SUS304",
      "title": "Electric Ball Valve DN40 KE006 SUS304 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Electric Ball Valve DN40 KE006 SUS304 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Electric_Ball_Valve_DN40_KE006_SUS304\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Electric_Ball_Valve_DN40_KE006_SUS304_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Electric_Ball_Valve_DN40_KE006_SUS304\\06_Renders_and_Media\\04_Watermarked_Exports\\Electric_Ball_Valve_DN40_KE006_SUS304_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Electric_Ball_Valve_DN40_KE006_SUS304\\06_Renders_and_Media"
    },
    {
      "name": "Electromagnetic_Solenoid_Valve_DN20_220VAC",
      "title": "Electromagnetic Solenoid Valve DN20 220VAC - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Electromagnetic Solenoid Valve DN20 220VAC - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Electromagnetic_Solenoid_Valve_DN20_220VAC\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Electromagnetic_Solenoid_Valve_DN20_220VAC_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Electromagnetic_Solenoid_Valve_DN20_220VAC\\06_Renders_and_Media\\04_Watermarked_Exports\\Electromagnetic_Solenoid_Valve_DN20_220VAC_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Electromagnetic_Solenoid_Valve_DN20_220VAC\\06_Renders_and_Media"
    },
    {
      "name": "Electromagnetic_Solenoid_Valve_DN32_PPR_220VAC",
      "title": "Electromagnetic Solenoid Valve DN32 PPR 220VAC - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Electromagnetic Solenoid Valve DN32 PPR 220VAC - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Electromagnetic_Solenoid_Valve_DN32_PPR_220VAC\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Electromagnetic_Solenoid_Valve_DN32_PPR_220VAC_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Electromagnetic_Solenoid_Valve_DN32_PPR_220VAC\\06_Renders_and_Media\\04_Watermarked_Exports\\Electromagnetic_Solenoid_Valve_DN32_PPR_220VAC_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Electromagnetic_Solenoid_Valve_DN32_PPR_220VAC\\06_Renders_and_Media"
    },
    {
      "name": "Electromagnetic_Solenoid_Valve_DN32_uPVC_220VAC",
      "title": "Electromagnetic Solenoid Valve DN32 uPVC 220VAC - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Electromagnetic Solenoid Valve DN32 uPVC 220VAC - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Electromagnetic_Solenoid_Valve_DN32_uPVC_220VAC\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Electromagnetic_Solenoid_Valve_DN32_uPVC_220VAC_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Electromagnetic_Solenoid_Valve_DN32_uPVC_220VAC\\06_Renders_and_Media\\04_Watermarked_Exports\\Electromagnetic_Solenoid_Valve_DN32_uPVC_220VAC_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Electromagnetic_Solenoid_Valve_DN32_uPVC_220VAC\\06_Renders_and_Media"
    },
    {
      "name": "Lever_Butterfly_Valve_DN50_Flanged",
      "title": "Lever Butterfly Valve DN50 Flanged - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Lever Butterfly Valve DN50 Flanged - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Lever_Butterfly_Valve_DN50_Flanged\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Lever_Butterfly_Valve_DN50_Flanged_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Lever_Butterfly_Valve_DN50_Flanged\\06_Renders_and_Media\\04_Watermarked_Exports\\Lever_Butterfly_Valve_DN50_Flanged_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Lever_Butterfly_Valve_DN50_Flanged\\06_Renders_and_Media"
    },
    {
      "name": "Lever_Butterfly_Valve_DN65_Flanged",
      "title": "Lever Butterfly Valve DN65 Flanged - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Lever Butterfly Valve DN65 Flanged - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Lever_Butterfly_Valve_DN65_Flanged\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Lever_Butterfly_Valve_DN65_Flanged_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Lever_Butterfly_Valve_DN65_Flanged\\06_Renders_and_Media\\04_Watermarked_Exports\\Lever_Butterfly_Valve_DN65_Flanged_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Lever_Butterfly_Valve_DN65_Flanged\\06_Renders_and_Media"
    },
    {
      "name": "Lever_Butterfly_Valve_DN65_Wafer",
      "title": "Lever Butterfly Valve DN65 Wafer - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Lever Butterfly Valve DN65 Wafer - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Lever_Butterfly_Valve_DN65_Wafer\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Lever_Butterfly_Valve_DN65_Wafer_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Lever_Butterfly_Valve_DN65_Wafer\\06_Renders_and_Media\\04_Watermarked_Exports\\Lever_Butterfly_Valve_DN65_Wafer_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Lever_Butterfly_Valve_DN65_Wafer\\06_Renders_and_Media"
    },
    {
      "name": "Lever_Butterfly_Valve_DN80_Flanged",
      "title": "Lever Butterfly Valve DN80 Flanged - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Lever Butterfly Valve DN80 Flanged - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Lever_Butterfly_Valve_DN80_Flanged\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Lever_Butterfly_Valve_DN80_Flanged_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Lever_Butterfly_Valve_DN80_Flanged\\06_Renders_and_Media\\04_Watermarked_Exports\\Lever_Butterfly_Valve_DN80_Flanged_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Lever_Butterfly_Valve_DN80_Flanged\\06_Renders_and_Media"
    },
    {
      "name": "Lever_Butterfly_Valve_DN80_Wafer",
      "title": "Lever Butterfly Valve DN80 Wafer - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Lever Butterfly Valve DN80 Wafer - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Lever_Butterfly_Valve_DN80_Wafer\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Lever_Butterfly_Valve_DN80_Wafer_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Lever_Butterfly_Valve_DN80_Wafer\\06_Renders_and_Media\\04_Watermarked_Exports\\Lever_Butterfly_Valve_DN80_Wafer_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Lever_Butterfly_Valve_DN80_Wafer\\06_Renders_and_Media"
    },
    {
      "name": "Motorized_Butterfly_Valve_DN65",
      "title": "Motorized Butterfly Valve DN65 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Motorized Butterfly Valve DN65 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Motorized_Butterfly_Valve_DN65\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Motorized_Butterfly_Valve_DN65_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Motorized_Butterfly_Valve_DN65\\06_Renders_and_Media\\04_Watermarked_Exports\\Motorized_Butterfly_Valve_DN65_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Motorized_Butterfly_Valve_DN65\\06_Renders_and_Media"
    },
    {
      "name": "Motorized_Butterfly_Valve_DN65_Flanged",
      "title": "Motorized Butterfly Valve DN65 Flanged - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Motorized Butterfly Valve DN65 Flanged - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Motorized_Butterfly_Valve_DN65_Flanged\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Motorized_Butterfly_Valve_DN65_Flanged_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Motorized_Butterfly_Valve_DN65_Flanged\\06_Renders_and_Media\\04_Watermarked_Exports\\Motorized_Butterfly_Valve_DN65_Flanged_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Motorized_Butterfly_Valve_DN65_Flanged\\06_Renders_and_Media"
    },
    {
      "name": "Motorized_Butterfly_Valve_DN80",
      "title": "Motorized Butterfly Valve DN80 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Motorized Butterfly Valve DN80 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Motorized_Butterfly_Valve_DN80\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Motorized_Butterfly_Valve_DN80_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Motorized_Butterfly_Valve_DN80\\06_Renders_and_Media\\04_Watermarked_Exports\\Motorized_Butterfly_Valve_DN80_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Motorized_Butterfly_Valve_DN80\\06_Renders_and_Media"
    },
    {
      "name": "Motorized_Butterfly_Valve_DN80_Flanged",
      "title": "Motorized Butterfly Valve DN80 Flanged - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Motorized Butterfly Valve DN80 Flanged - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Motorized_Butterfly_Valve_DN80_Flanged\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Motorized_Butterfly_Valve_DN80_Flanged_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Motorized_Butterfly_Valve_DN80_Flanged\\06_Renders_and_Media\\04_Watermarked_Exports\\Motorized_Butterfly_Valve_DN80_Flanged_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Motorized_Butterfly_Valve_DN80_Flanged\\06_Renders_and_Media"
    },
    {
      "name": "Motorized_PVC_Ball_Valve_DN20_Union",
      "title": "Motorized PVC Ball Valve DN20 Union - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Motorized PVC Ball Valve DN20 Union - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Motorized_PVC_Ball_Valve_DN20_Union\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Motorized_PVC_Ball_Valve_DN20_Union_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Motorized_PVC_Ball_Valve_DN20_Union\\06_Renders_and_Media\\04_Watermarked_Exports\\Motorized_PVC_Ball_Valve_DN20_Union_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Motorized_PVC_Ball_Valve_DN20_Union\\06_Renders_and_Media"
    },
    {
      "name": "Plastic_Solenoid_Valve_24V_DN15",
      "title": "Plastic Solenoid Valve 24V DN15 - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Plastic Solenoid Valve 24V DN15 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Plastic_Solenoid_Valve_24V_DN15\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Plastic_Solenoid_Valve_24V_DN15_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Plastic_Solenoid_Valve_24V_DN15\\06_Renders_and_Media\\04_Watermarked_Exports\\Plastic_Solenoid_Valve_24V_DN15_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Plastic_Solenoid_Valve_24V_DN15\\06_Renders_and_Media"
    },
    {
      "name": "Pneumatic_Ball_Valve_DN25_SUS304",
      "title": "Pneumatic Ball Valve DN25 SUS304 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Pneumatic Ball Valve DN25 SUS304 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Pneumatic_Ball_Valve_DN25_SUS304\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Pneumatic_Ball_Valve_DN25_SUS304_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Pneumatic_Ball_Valve_DN25_SUS304\\06_Renders_and_Media\\04_Watermarked_Exports\\Pneumatic_Ball_Valve_DN25_SUS304_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Pneumatic_Ball_Valve_DN25_SUS304\\06_Renders_and_Media"
    },
    {
      "name": "Pneumatic_Ball_Valve_DN50_SUS304",
      "title": "Pneumatic Ball Valve DN50 SUS304 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Pneumatic Ball Valve DN50 SUS304 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Pneumatic_Ball_Valve_DN50_SUS304\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Pneumatic_Ball_Valve_DN50_SUS304_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Pneumatic_Ball_Valve_DN50_SUS304\\06_Renders_and_Media\\04_Watermarked_Exports\\Pneumatic_Ball_Valve_DN50_SUS304_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Pneumatic_Ball_Valve_DN50_SUS304\\06_Renders_and_Media"
    },
    {
      "name": "Pneumatic_Gas_Solenoid_Valve_12mm",
      "title": "Pneumatic Gas Solenoid Valve 12mm - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Pneumatic Gas Solenoid Valve 12mm - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Pneumatic_Gas_Solenoid_Valve_12mm\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Pneumatic_Gas_Solenoid_Valve_12mm_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Pneumatic_Gas_Solenoid_Valve_12mm\\06_Renders_and_Media\\04_Watermarked_Exports\\Pneumatic_Gas_Solenoid_Valve_12mm_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Pneumatic_Gas_Solenoid_Valve_12mm\\06_Renders_and_Media"
    },
    {
      "name": "Pneumatic_Valve_Limit_Switch_Box",
      "title": "Pneumatic Valve Limit Switch Box - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Pneumatic Valve Limit Switch Box - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Pneumatic_Valve_Limit_Switch_Box\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Pneumatic_Valve_Limit_Switch_Box_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Pneumatic_Valve_Limit_Switch_Box\\06_Renders_and_Media\\04_Watermarked_Exports\\Pneumatic_Valve_Limit_Switch_Box_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Pneumatic_Valve_Limit_Switch_Box\\06_Renders_and_Media"
    },
    {
      "name": "Runxin_N74A3_Metered_Softener_Valve",
      "title": "Runxin N74A3 Metered Softener Valve - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Runxin N74A3 Metered Softener Valve - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Runxin_N74A3_Metered_Softener_Valve\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Runxin_N74A3_Metered_Softener_Valve_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Runxin_N74A3_Metered_Softener_Valve\\06_Renders_and_Media\\04_Watermarked_Exports\\Runxin_N74A3_Metered_Softener_Valve_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Runxin_N74A3_Metered_Softener_Valve\\06_Renders_and_Media"
    },
    {
      "name": "Sanitary_Clamp_Ball_Valve_DN50_SS",
      "title": "Sanitary Clamp Ball Valve DN50 SS - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Sanitary Clamp Ball Valve DN50 SS - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Sanitary_Clamp_Ball_Valve_DN50_SS\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Sanitary_Clamp_Ball_Valve_DN50_SS_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Sanitary_Clamp_Ball_Valve_DN50_SS\\06_Renders_and_Media\\04_Watermarked_Exports\\Sanitary_Clamp_Ball_Valve_DN50_SS_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Sanitary_Clamp_Ball_Valve_DN50_SS\\06_Renders_and_Media"
    },
    {
      "name": "Sanitary_Clamp_Butterfly_Valve_DN50_SS",
      "title": "Sanitary Clamp Butterfly Valve DN50 SS - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Sanitary Clamp Butterfly Valve DN50 SS - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Sanitary_Clamp_Butterfly_Valve_DN50_SS\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Sanitary_Clamp_Butterfly_Valve_DN50_SS_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Sanitary_Clamp_Butterfly_Valve_DN50_SS\\06_Renders_and_Media\\04_Watermarked_Exports\\Sanitary_Clamp_Butterfly_Valve_DN50_SS_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Sanitary_Clamp_Butterfly_Valve_DN50_SS\\06_Renders_and_Media"
    },
    {
      "name": "Sanitary_Clamp_Check_Valve_DN32_SS",
      "title": "Sanitary Clamp Check Valve DN32 SS - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Sanitary Clamp Check Valve DN32 SS - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Sanitary_Clamp_Check_Valve_DN32_SS\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Sanitary_Clamp_Check_Valve_DN32_SS_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Sanitary_Clamp_Check_Valve_DN32_SS\\06_Renders_and_Media\\04_Watermarked_Exports\\Sanitary_Clamp_Check_Valve_DN32_SS_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Sanitary_Clamp_Check_Valve_DN32_SS\\06_Renders_and_Media"
    },
    {
      "name": "Sanitary_Clamp_Check_Valve_DN40_SS",
      "title": "Sanitary Clamp Check Valve DN40 SS - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Sanitary Clamp Check Valve DN40 SS - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Sanitary_Clamp_Check_Valve_DN40_SS\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Sanitary_Clamp_Check_Valve_DN40_SS_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Sanitary_Clamp_Check_Valve_DN40_SS\\06_Renders_and_Media\\04_Watermarked_Exports\\Sanitary_Clamp_Check_Valve_DN40_SS_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Sanitary_Clamp_Check_Valve_DN40_SS\\06_Renders_and_Media"
    },
    {
      "name": "Sanitary_Clamp_Globe_Valve_DN50_SS",
      "title": "Sanitary Clamp Globe Valve DN50 SS - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Sanitary Clamp Globe Valve DN50 SS - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Sanitary_Clamp_Globe_Valve_DN50_SS\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Sanitary_Clamp_Globe_Valve_DN50_SS_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Sanitary_Clamp_Globe_Valve_DN50_SS\\06_Renders_and_Media\\04_Watermarked_Exports\\Sanitary_Clamp_Globe_Valve_DN50_SS_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\Sanitary_Clamp_Globe_Valve_DN50_SS\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_Spring_Check_Valve_SCH80_DN15",
      "title": "UPVC Spring Check Valve SCH80 DN15 - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC Spring Check Valve SCH80 DN15 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_Spring_Check_Valve_SCH80_DN15\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_Spring_Check_Valve_SCH80_DN15_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_Spring_Check_Valve_SCH80_DN15\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_Spring_Check_Valve_SCH80_DN15_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_Spring_Check_Valve_SCH80_DN15\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_Spring_Check_Valve_SCH80_DN20",
      "title": "UPVC Spring Check Valve SCH80 DN20 - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC Spring Check Valve SCH80 DN20 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_Spring_Check_Valve_SCH80_DN20\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_Spring_Check_Valve_SCH80_DN20_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_Spring_Check_Valve_SCH80_DN20\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_Spring_Check_Valve_SCH80_DN20_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_Spring_Check_Valve_SCH80_DN20\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_Spring_Check_Valve_SCH80_DN25",
      "title": "UPVC Spring Check Valve SCH80 DN25 - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC Spring Check Valve SCH80 DN25 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_Spring_Check_Valve_SCH80_DN25\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_Spring_Check_Valve_SCH80_DN25_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_Spring_Check_Valve_SCH80_DN25\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_Spring_Check_Valve_SCH80_DN25_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_Spring_Check_Valve_SCH80_DN25\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_Spring_Check_Valve_SCH80_DN32",
      "title": "UPVC Spring Check Valve SCH80 DN32 - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC Spring Check Valve SCH80 DN32 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_Spring_Check_Valve_SCH80_DN32\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_Spring_Check_Valve_SCH80_DN32_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_Spring_Check_Valve_SCH80_DN32\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_Spring_Check_Valve_SCH80_DN32_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_Spring_Check_Valve_SCH80_DN32\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_Spring_Check_Valve_SCH80_DN40",
      "title": "UPVC Spring Check Valve SCH80 DN40 - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC Spring Check Valve SCH80 DN40 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_Spring_Check_Valve_SCH80_DN40\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_Spring_Check_Valve_SCH80_DN40_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_Spring_Check_Valve_SCH80_DN40\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_Spring_Check_Valve_SCH80_DN40_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_Spring_Check_Valve_SCH80_DN40\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_Spring_Check_Valve_SCH80_DN50",
      "title": "UPVC Spring Check Valve SCH80 DN50 - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC Spring Check Valve SCH80 DN50 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_Spring_Check_Valve_SCH80_DN50\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_Spring_Check_Valve_SCH80_DN50_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_Spring_Check_Valve_SCH80_DN50\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_Spring_Check_Valve_SCH80_DN50_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_Spring_Check_Valve_SCH80_DN50\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_True_Union_Ball_Valve_SCH80_DN15",
      "title": "UPVC True Union Ball Valve SCH80 DN15 - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC True Union Ball Valve SCH80 DN15 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_True_Union_Ball_Valve_SCH80_DN15\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_True_Union_Ball_Valve_SCH80_DN15_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_True_Union_Ball_Valve_SCH80_DN15\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_True_Union_Ball_Valve_SCH80_DN15_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_True_Union_Ball_Valve_SCH80_DN15\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_True_Union_Ball_Valve_SCH80_DN20",
      "title": "UPVC True Union Ball Valve SCH80 DN20 - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC True Union Ball Valve SCH80 DN20 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_True_Union_Ball_Valve_SCH80_DN20\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_True_Union_Ball_Valve_SCH80_DN20_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_True_Union_Ball_Valve_SCH80_DN20\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_True_Union_Ball_Valve_SCH80_DN20_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_True_Union_Ball_Valve_SCH80_DN20\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_True_Union_Ball_Valve_SCH80_DN25",
      "title": "UPVC True Union Ball Valve SCH80 DN25 - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC True Union Ball Valve SCH80 DN25 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_True_Union_Ball_Valve_SCH80_DN25\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_True_Union_Ball_Valve_SCH80_DN25_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_True_Union_Ball_Valve_SCH80_DN25\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_True_Union_Ball_Valve_SCH80_DN25_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_True_Union_Ball_Valve_SCH80_DN25\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_True_Union_Ball_Valve_SCH80_DN32",
      "title": "UPVC True Union Ball Valve SCH80 DN32 - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC True Union Ball Valve SCH80 DN32 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_True_Union_Ball_Valve_SCH80_DN32\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_True_Union_Ball_Valve_SCH80_DN32_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_True_Union_Ball_Valve_SCH80_DN32\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_True_Union_Ball_Valve_SCH80_DN32_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_True_Union_Ball_Valve_SCH80_DN32\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_True_Union_Ball_Valve_SCH80_DN40",
      "title": "UPVC True Union Ball Valve SCH80 DN40 - Industrial CAD 3D Model",
      "personal_price": 19.99,
      "professional_price": 29.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC True Union Ball Valve SCH80 DN40 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_True_Union_Ball_Valve_SCH80_DN40\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_True_Union_Ball_Valve_SCH80_DN40_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_True_Union_Ball_Valve_SCH80_DN40\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_True_Union_Ball_Valve_SCH80_DN40_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_True_Union_Ball_Valve_SCH80_DN40\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_True_Union_Ball_Valve_SCH80_DN50",
      "title": "UPVC True Union Ball Valve SCH80 DN50 - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC True Union Ball Valve SCH80 DN50 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_True_Union_Ball_Valve_SCH80_DN50\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_True_Union_Ball_Valve_SCH80_DN50_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_True_Union_Ball_Valve_SCH80_DN50\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_True_Union_Ball_Valve_SCH80_DN50_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\04_Valves_and_Actuators\\UPVC_True_Union_Ball_Valve_SCH80_DN50\\06_Renders_and_Media"
    }
  ],
  "05_Filters_and_Clarifiers": [
    {
      "name": "Big_Blue_Filter_Housing_20Inch",
      "title": "Big Blue Filter Housing 20Inch - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Big Blue Filter Housing 20Inch - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Big_Blue_Filter_Housing_20Inch\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Big_Blue_Filter_Housing_20Inch_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Big_Blue_Filter_Housing_20Inch\\06_Renders_and_Media\\04_Watermarked_Exports\\Big_Blue_Filter_Housing_20Inch_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Big_Blue_Filter_Housing_20Inch\\06_Renders_and_Media"
    },
    {
      "name": "Cartridge_Filter_Housing_20Inch_Blue",
      "title": "Cartridge Filter Housing 20Inch Blue - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Cartridge Filter Housing 20Inch Blue - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Cartridge_Filter_Housing_20Inch_Blue\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Cartridge_Filter_Housing_20Inch_Blue_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Cartridge_Filter_Housing_20Inch_Blue\\06_Renders_and_Media\\04_Watermarked_Exports\\Cartridge_Filter_Housing_20Inch_Blue_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Cartridge_Filter_Housing_20Inch_Blue\\06_Renders_and_Media"
    },
    {
      "name": "Cartridge_Filter_Housing_5x20In_SS",
      "title": "Cartridge Filter Housing 5x20In SS - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Cartridge Filter Housing 5x20In SS - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Cartridge_Filter_Housing_5x20In_SS\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Cartridge_Filter_Housing_5x20In_SS_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Cartridge_Filter_Housing_5x20In_SS\\06_Renders_and_Media\\04_Watermarked_Exports\\Cartridge_Filter_Housing_5x20In_SS_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Cartridge_Filter_Housing_5x20In_SS\\06_Renders_and_Media"
    },
    {
      "name": "Cartridge_Filter_Housing_7x20_SUS304",
      "title": "Cartridge Filter Housing 7x20 SUS304 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Cartridge Filter Housing 7x20 SUS304 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Cartridge_Filter_Housing_7x20_SUS304\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Cartridge_Filter_Housing_7x20_SUS304_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Cartridge_Filter_Housing_7x20_SUS304\\06_Renders_and_Media\\04_Watermarked_Exports\\Cartridge_Filter_Housing_7x20_SUS304_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Cartridge_Filter_Housing_7x20_SUS304\\06_Renders_and_Media"
    },
    {
      "name": "Cartridge_Filter_Housing_7x40In_SS",
      "title": "Cartridge Filter Housing 7x40In SS - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Cartridge Filter Housing 7x40In SS - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Cartridge_Filter_Housing_7x40In_SS\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Cartridge_Filter_Housing_7x40In_SS_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Cartridge_Filter_Housing_7x40In_SS\\06_Renders_and_Media\\04_Watermarked_Exports\\Cartridge_Filter_Housing_7x40In_SS_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Cartridge_Filter_Housing_7x40In_SS\\06_Renders_and_Media"
    },
    {
      "name": "Dual_20In_Filter_Housing_Bracket",
      "title": "Dual 20In Filter Housing Bracket - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Dual 20In Filter Housing Bracket - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Dual_20In_Filter_Housing_Bracket\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Dual_20In_Filter_Housing_Bracket_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Dual_20In_Filter_Housing_Bracket\\06_Renders_and_Media\\04_Watermarked_Exports\\Dual_20In_Filter_Housing_Bracket_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Dual_20In_Filter_Housing_Bracket\\06_Renders_and_Media"
    },
    {
      "name": "Plastic_Bag_Filter_Housing_DN50",
      "title": "Plastic Bag Filter Housing DN50 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Plastic Bag Filter Housing DN50 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Plastic_Bag_Filter_Housing_DN50\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Plastic_Bag_Filter_Housing_DN50_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Plastic_Bag_Filter_Housing_DN50\\06_Renders_and_Media\\04_Watermarked_Exports\\Plastic_Bag_Filter_Housing_DN50_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Plastic_Bag_Filter_Housing_DN50\\06_Renders_and_Media"
    },
    {
      "name": "Pool_Pleated_Cartridge_Filter_DN50",
      "title": "Pool Pleated Cartridge Filter DN50 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Pool Pleated Cartridge Filter DN50 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Pool_Pleated_Cartridge_Filter_DN50\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Pool_Pleated_Cartridge_Filter_DN50_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Pool_Pleated_Cartridge_Filter_DN50\\06_Renders_and_Media\\04_Watermarked_Exports\\Pool_Pleated_Cartridge_Filter_DN50_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Pool_Pleated_Cartridge_Filter_DN50\\06_Renders_and_Media"
    },
    {
      "name": "SS304_Mesh_Water_PreFilter_DN25",
      "title": "SS304 Mesh Water PreFilter DN25 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "SS304 Mesh Water PreFilter DN25 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\SS304_Mesh_Water_PreFilter_DN25\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\SS304_Mesh_Water_PreFilter_DN25_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\SS304_Mesh_Water_PreFilter_DN25\\06_Renders_and_Media\\04_Watermarked_Exports\\SS304_Mesh_Water_PreFilter_DN25_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\SS304_Mesh_Water_PreFilter_DN25\\06_Renders_and_Media"
    },
    {
      "name": "Stainless_Bag_Filter_Housing_SS304",
      "title": "Stainless Bag Filter Housing SS304 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Stainless Bag Filter Housing SS304 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Stainless_Bag_Filter_Housing_SS304\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Stainless_Bag_Filter_Housing_SS304_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Stainless_Bag_Filter_Housing_SS304\\06_Renders_and_Media\\04_Watermarked_Exports\\Stainless_Bag_Filter_Housing_SS304_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Stainless_Bag_Filter_Housing_SS304\\06_Renders_and_Media"
    },
    {
      "name": "Stainless_Screen_Filter_DN40_Bracket",
      "title": "Stainless Screen Filter DN40 Bracket - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Stainless Screen Filter DN40 Bracket - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Stainless_Screen_Filter_DN40_Bracket\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Stainless_Screen_Filter_DN40_Bracket_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Stainless_Screen_Filter_DN40_Bracket\\06_Renders_and_Media\\04_Watermarked_Exports\\Stainless_Screen_Filter_DN40_Bracket_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Stainless_Screen_Filter_DN40_Bracket\\06_Renders_and_Media"
    },
    {
      "name": "Triple_20In_Filter_Housing_Bracket",
      "title": "Triple 20In Filter Housing Bracket - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Triple 20In Filter Housing Bracket - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Triple_20In_Filter_Housing_Bracket\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Triple_20In_Filter_Housing_Bracket_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Triple_20In_Filter_Housing_Bracket\\06_Renders_and_Media\\04_Watermarked_Exports\\Triple_20In_Filter_Housing_Bracket_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Triple_20In_Filter_Housing_Bracket\\06_Renders_and_Media"
    },
    {
      "name": "Victaulic_T_Disc_Filter_DN50_D60",
      "title": "Victaulic T Disc Filter DN50 D60 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Victaulic T Disc Filter DN50 D60 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Victaulic_T_Disc_Filter_DN50_D60\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Victaulic_T_Disc_Filter_DN50_D60_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Victaulic_T_Disc_Filter_DN50_D60\\06_Renders_and_Media\\04_Watermarked_Exports\\Victaulic_T_Disc_Filter_DN50_D60_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Victaulic_T_Disc_Filter_DN50_D60\\06_Renders_and_Media"
    },
    {
      "name": "Y_Strainer_Filter_uPVC_DN40_D49",
      "title": "Y Strainer Filter uPVC DN40 D49 - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Y Strainer Filter uPVC DN40 D49 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Y_Strainer_Filter_uPVC_DN40_D49\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Y_Strainer_Filter_uPVC_DN40_D49_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Y_Strainer_Filter_uPVC_DN40_D49\\06_Renders_and_Media\\04_Watermarked_Exports\\Y_Strainer_Filter_uPVC_DN40_D49_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Y_Strainer_Filter_uPVC_DN40_D49\\06_Renders_and_Media"
    },
    {
      "name": "Y_Type_Disc_Filter_DN20_D27",
      "title": "Y Type Disc Filter DN20 D27 - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Y Type Disc Filter DN20 D27 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Y_Type_Disc_Filter_DN20_D27\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Y_Type_Disc_Filter_DN20_D27_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Y_Type_Disc_Filter_DN20_D27\\06_Renders_and_Media\\04_Watermarked_Exports\\Y_Type_Disc_Filter_DN20_D27_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Y_Type_Disc_Filter_DN20_D27\\06_Renders_and_Media"
    },
    {
      "name": "Y_Type_Disc_Filter_DN25_D34",
      "title": "Y Type Disc Filter DN25 D34 - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Y Type Disc Filter DN25 D34 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Y_Type_Disc_Filter_DN25_D34\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Y_Type_Disc_Filter_DN25_D34_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Y_Type_Disc_Filter_DN25_D34\\06_Renders_and_Media\\04_Watermarked_Exports\\Y_Type_Disc_Filter_DN25_D34_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Y_Type_Disc_Filter_DN25_D34\\06_Renders_and_Media"
    },
    {
      "name": "Y_Type_Disc_Filter_DN40_D49",
      "title": "Y Type Disc Filter DN40 D49 - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Y Type Disc Filter DN40 D49 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Y_Type_Disc_Filter_DN40_D49\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Y_Type_Disc_Filter_DN40_D49_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Y_Type_Disc_Filter_DN40_D49\\06_Renders_and_Media\\04_Watermarked_Exports\\Y_Type_Disc_Filter_DN40_D49_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\05_Filters_and_Clarifiers\\Y_Type_Disc_Filter_DN40_D49\\06_Renders_and_Media"
    }
  ],
  "06_Membranes_and_Advanced_Separation": [
    {
      "name": "Electrodeionization_Module_EDI_50L",
      "title": "Electrodeionization Module EDI 50L - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Electrodeionization Module EDI 50L - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Electrodeionization_Module_EDI_50L\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Electrodeionization_Module_EDI_50L_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Electrodeionization_Module_EDI_50L\\06_Renders_and_Media\\04_Watermarked_Exports\\Electrodeionization_Module_EDI_50L_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Electrodeionization_Module_EDI_50L\\06_Renders_and_Media"
    },
    {
      "name": "FRP_RO_Membrane_Housing_4040_1Element",
      "title": "FRP RO Membrane Housing 4040 1Element - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "FRP RO Membrane Housing 4040 1Element - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\FRP_RO_Membrane_Housing_4040_1Element\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\FRP_RO_Membrane_Housing_4040_1Element_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\FRP_RO_Membrane_Housing_4040_1Element\\06_Renders_and_Media\\04_Watermarked_Exports\\FRP_RO_Membrane_Housing_4040_1Element_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\FRP_RO_Membrane_Housing_4040_1Element\\06_Renders_and_Media"
    },
    {
      "name": "FRP_RO_Membrane_Housing_8040_1Element",
      "title": "FRP RO Membrane Housing 8040 1Element - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "FRP RO Membrane Housing 8040 1Element - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\FRP_RO_Membrane_Housing_8040_1Element\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\FRP_RO_Membrane_Housing_8040_1Element_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\FRP_RO_Membrane_Housing_8040_1Element\\06_Renders_and_Media\\04_Watermarked_Exports\\FRP_RO_Membrane_Housing_8040_1Element_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\FRP_RO_Membrane_Housing_8040_1Element\\06_Renders_and_Media"
    },
    {
      "name": "FRP_RO_Membrane_Housing_8040_2Element",
      "title": "FRP RO Membrane Housing 8040 2Element - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "FRP RO Membrane Housing 8040 2Element - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\FRP_RO_Membrane_Housing_8040_2Element\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\FRP_RO_Membrane_Housing_8040_2Element_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\FRP_RO_Membrane_Housing_8040_2Element\\06_Renders_and_Media\\04_Watermarked_Exports\\FRP_RO_Membrane_Housing_8040_2Element_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\FRP_RO_Membrane_Housing_8040_2Element\\06_Renders_and_Media"
    },
    {
      "name": "FRP_RO_Membrane_Housing_8040_3Element",
      "title": "FRP RO Membrane Housing 8040 3Element - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "FRP RO Membrane Housing 8040 3Element - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\FRP_RO_Membrane_Housing_8040_3Element\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\FRP_RO_Membrane_Housing_8040_3Element_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\FRP_RO_Membrane_Housing_8040_3Element\\06_Renders_and_Media\\04_Watermarked_Exports\\FRP_RO_Membrane_Housing_8040_3Element_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\FRP_RO_Membrane_Housing_8040_3Element\\06_Renders_and_Media"
    },
    {
      "name": "FRP_RO_Membrane_Housing_8040_4Element",
      "title": "FRP RO Membrane Housing 8040 4Element - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "FRP RO Membrane Housing 8040 4Element - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\FRP_RO_Membrane_Housing_8040_4Element\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\FRP_RO_Membrane_Housing_8040_4Element_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\FRP_RO_Membrane_Housing_8040_4Element\\06_Renders_and_Media\\04_Watermarked_Exports\\FRP_RO_Membrane_Housing_8040_4Element_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\FRP_RO_Membrane_Housing_8040_4Element\\06_Renders_and_Media"
    },
    {
      "name": "Inline_UF_Ultrafiltration_Cartridge",
      "title": "Inline UF Ultrafiltration Cartridge - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Inline UF Ultrafiltration Cartridge - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Inline_UF_Ultrafiltration_Cartridge\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Inline_UF_Ultrafiltration_Cartridge_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Inline_UF_Ultrafiltration_Cartridge\\06_Renders_and_Media\\04_Watermarked_Exports\\Inline_UF_Ultrafiltration_Cartridge_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Inline_UF_Ultrafiltration_Cartridge\\06_Renders_and_Media"
    },
    {
      "name": "RO_Membrane_Housing_300G_3012",
      "title": "RO Membrane Housing 300G 3012 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "RO Membrane Housing 300G 3012 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\RO_Membrane_Housing_300G_3012\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\RO_Membrane_Housing_300G_3012_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\RO_Membrane_Housing_300G_3012\\06_Renders_and_Media\\04_Watermarked_Exports\\RO_Membrane_Housing_300G_3012_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\RO_Membrane_Housing_300G_3012\\06_Renders_and_Media"
    },
    {
      "name": "RO_Membrane_Housing_8040_1Element_SUS304",
      "title": "RO Membrane Housing 8040 1Element SUS304 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "RO Membrane Housing 8040 1Element SUS304 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\RO_Membrane_Housing_8040_1Element_SUS304\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\RO_Membrane_Housing_8040_1Element_SUS304_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\RO_Membrane_Housing_8040_1Element_SUS304\\06_Renders_and_Media\\04_Watermarked_Exports\\RO_Membrane_Housing_8040_1Element_SUS304_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\RO_Membrane_Housing_8040_1Element_SUS304\\06_Renders_and_Media"
    },
    {
      "name": "Reverse_Osmosis_Membrane_4040",
      "title": "Reverse Osmosis Membrane 4040 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Reverse Osmosis Membrane 4040 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Reverse_Osmosis_Membrane_4040\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Reverse_Osmosis_Membrane_4040_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Reverse_Osmosis_Membrane_4040\\06_Renders_and_Media\\04_Watermarked_Exports\\Reverse_Osmosis_Membrane_4040_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Reverse_Osmosis_Membrane_4040\\06_Renders_and_Media"
    },
    {
      "name": "Stainless_RO_Membrane_Housing_4040",
      "title": "Stainless RO Membrane Housing 4040 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Stainless RO Membrane Housing 4040 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Stainless_RO_Membrane_Housing_4040\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Stainless_RO_Membrane_Housing_4040_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Stainless_RO_Membrane_Housing_4040\\06_Renders_and_Media\\04_Watermarked_Exports\\Stainless_RO_Membrane_Housing_4040_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Stainless_RO_Membrane_Housing_4040\\06_Renders_and_Media"
    },
    {
      "name": "Stainless_UF_Filter_Housing_Vessel",
      "title": "Stainless UF Filter Housing Vessel - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Stainless UF Filter Housing Vessel - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Stainless_UF_Filter_Housing_Vessel\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Stainless_UF_Filter_Housing_Vessel_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Stainless_UF_Filter_Housing_Vessel\\06_Renders_and_Media\\04_Watermarked_Exports\\Stainless_UF_Filter_Housing_Vessel_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Stainless_UF_Filter_Housing_Vessel\\06_Renders_and_Media"
    },
    {
      "name": "Stainless_UF_Membrane_Module_1000L",
      "title": "Stainless UF Membrane Module 1000L - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Stainless UF Membrane Module 1000L - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Stainless_UF_Membrane_Module_1000L\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Stainless_UF_Membrane_Module_1000L_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Stainless_UF_Membrane_Module_1000L\\06_Renders_and_Media\\04_Watermarked_Exports\\Stainless_UF_Membrane_Module_1000L_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Stainless_UF_Membrane_Module_1000L\\06_Renders_and_Media"
    },
    {
      "name": "Stainless_UF_Membrane_Module_3000L",
      "title": "Stainless UF Membrane Module 3000L - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Stainless UF Membrane Module 3000L - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Stainless_UF_Membrane_Module_3000L\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Stainless_UF_Membrane_Module_3000L_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Stainless_UF_Membrane_Module_3000L\\06_Renders_and_Media\\04_Watermarked_Exports\\Stainless_UF_Membrane_Module_3000L_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Stainless_UF_Membrane_Module_3000L\\06_Renders_and_Media"
    },
    {
      "name": "Stainless_UF_Membrane_Module_5000L",
      "title": "Stainless UF Membrane Module 5000L - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Stainless UF Membrane Module 5000L - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Stainless_UF_Membrane_Module_5000L\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Stainless_UF_Membrane_Module_5000L_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Stainless_UF_Membrane_Module_5000L\\06_Renders_and_Media\\04_Watermarked_Exports\\Stainless_UF_Membrane_Module_5000L_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\Stainless_UF_Membrane_Module_5000L\\06_Renders_and_Media"
    },
    {
      "name": "T33_Post_Carbon_Filter_Cartridge",
      "title": "T33 Post Carbon Filter Cartridge - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "T33 Post Carbon Filter Cartridge - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\T33_Post_Carbon_Filter_Cartridge\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\T33_Post_Carbon_Filter_Cartridge_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\T33_Post_Carbon_Filter_Cartridge\\06_Renders_and_Media\\04_Watermarked_Exports\\T33_Post_Carbon_Filter_Cartridge_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\T33_Post_Carbon_Filter_Cartridge\\06_Renders_and_Media"
    },
    {
      "name": "UF_Ultrafiltration_Module_5000Lph_DN25",
      "title": "UF Ultrafiltration Module 5000Lph DN25 - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UF Ultrafiltration Module 5000Lph DN25 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\UF_Ultrafiltration_Module_5000Lph_DN25\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UF_Ultrafiltration_Module_5000Lph_DN25_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\UF_Ultrafiltration_Module_5000Lph_DN25\\06_Renders_and_Media\\04_Watermarked_Exports\\UF_Ultrafiltration_Module_5000Lph_DN25_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\06_Membranes_and_Advanced_Separation\\UF_Ultrafiltration_Module_5000Lph_DN25\\06_Renders_and_Media"
    }
  ],
  "07_Disinfection_and_Water_Conditioning": [
    {
      "name": "Aquapro_55W_UV_Water_Sterilizer_SS",
      "title": "Aquapro 55W UV Water Sterilizer SS - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Aquapro 55W UV Water Sterilizer SS - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Aquapro_55W_UV_Water_Sterilizer_SS\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Aquapro_55W_UV_Water_Sterilizer_SS_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Aquapro_55W_UV_Water_Sterilizer_SS\\06_Renders_and_Media\\04_Watermarked_Exports\\Aquapro_55W_UV_Water_Sterilizer_SS_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Aquapro_55W_UV_Water_Sterilizer_SS\\06_Renders_and_Media"
    },
    {
      "name": "Automatic_Garden_Water_Timer_Valve",
      "title": "Automatic Garden Water Timer Valve - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Automatic Garden Water Timer Valve - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Automatic_Garden_Water_Timer_Valve\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Automatic_Garden_Water_Timer_Valve_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Automatic_Garden_Water_Timer_Valve\\06_Renders_and_Media\\04_Watermarked_Exports\\Automatic_Garden_Water_Timer_Valve_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Automatic_Garden_Water_Timer_Valve\\06_Renders_and_Media"
    },
    {
      "name": "Cleanroom_Air_Handling_Unit_AHU_3m",
      "title": "Cleanroom Air Handling Unit AHU 3m - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Cleanroom Air Handling Unit AHU 3m - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Cleanroom_Air_Handling_Unit_AHU_3m\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Cleanroom_Air_Handling_Unit_AHU_3m_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Cleanroom_Air_Handling_Unit_AHU_3m\\06_Renders_and_Media\\04_Watermarked_Exports\\Cleanroom_Air_Handling_Unit_AHU_3m_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Cleanroom_Air_Handling_Unit_AHU_3m\\06_Renders_and_Media"
    },
    {
      "name": "Industrial_UV_Sterilizer_440W_DN80",
      "title": "Industrial UV Sterilizer 440W DN80 - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Industrial UV Sterilizer 440W DN80 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Industrial_UV_Sterilizer_440W_DN80\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Industrial_UV_Sterilizer_440W_DN80_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Industrial_UV_Sterilizer_440W_DN80\\06_Renders_and_Media\\04_Watermarked_Exports\\Industrial_UV_Sterilizer_440W_DN80_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Industrial_UV_Sterilizer_440W_DN80\\06_Renders_and_Media"
    },
    {
      "name": "Magnetic_Water_Descaler_Conditioner",
      "title": "Magnetic Water Descaler Conditioner - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Magnetic Water Descaler Conditioner - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Magnetic_Water_Descaler_Conditioner\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Magnetic_Water_Descaler_Conditioner_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Magnetic_Water_Descaler_Conditioner\\06_Renders_and_Media\\04_Watermarked_Exports\\Magnetic_Water_Descaler_Conditioner_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Magnetic_Water_Descaler_Conditioner\\06_Renders_and_Media"
    },
    {
      "name": "Mini_Inline_UV_Water_Sterilizer",
      "title": "Mini Inline UV Water Sterilizer - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Mini Inline UV Water Sterilizer - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Mini_Inline_UV_Water_Sterilizer\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Mini_Inline_UV_Water_Sterilizer_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Mini_Inline_UV_Water_Sterilizer\\06_Renders_and_Media\\04_Watermarked_Exports\\Mini_Inline_UV_Water_Sterilizer_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Mini_Inline_UV_Water_Sterilizer\\06_Renders_and_Media"
    },
    {
      "name": "Plastic_Venturi_Chemical_Ejector_DN25",
      "title": "Plastic Venturi Chemical Ejector DN25 - Industrial CAD 3D Model",
      "personal_price": 29.99,
      "professional_price": 44.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Plastic Venturi Chemical Ejector DN25 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Plastic_Venturi_Chemical_Ejector_DN25\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Plastic_Venturi_Chemical_Ejector_DN25_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Plastic_Venturi_Chemical_Ejector_DN25\\06_Renders_and_Media\\04_Watermarked_Exports\\Plastic_Venturi_Chemical_Ejector_DN25_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Plastic_Venturi_Chemical_Ejector_DN25\\06_Renders_and_Media"
    },
    {
      "name": "Submersible_UV_Pond_Clarifier_100W",
      "title": "Submersible UV Pond Clarifier 100W - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Submersible UV Pond Clarifier 100W - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Submersible_UV_Pond_Clarifier_100W\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Submersible_UV_Pond_Clarifier_100W_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Submersible_UV_Pond_Clarifier_100W\\06_Renders_and_Media\\04_Watermarked_Exports\\Submersible_UV_Pond_Clarifier_100W_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Submersible_UV_Pond_Clarifier_100W\\06_Renders_and_Media"
    },
    {
      "name": "Submersible_UV_Pond_Clarifier_55W",
      "title": "Submersible UV Pond Clarifier 55W - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Submersible UV Pond Clarifier 55W - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Submersible_UV_Pond_Clarifier_55W\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Submersible_UV_Pond_Clarifier_55W_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Submersible_UV_Pond_Clarifier_55W\\06_Renders_and_Media\\04_Watermarked_Exports\\Submersible_UV_Pond_Clarifier_55W_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Submersible_UV_Pond_Clarifier_55W\\06_Renders_and_Media"
    },
    {
      "name": "UV_Sterilizer_System_55W_SUS304_DN25",
      "title": "UV Sterilizer System 55W SUS304 DN25 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UV Sterilizer System 55W SUS304 DN25 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\UV_Sterilizer_System_55W_SUS304_DN25\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UV_Sterilizer_System_55W_SUS304_DN25_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\UV_Sterilizer_System_55W_SUS304_DN25\\06_Renders_and_Media\\04_Watermarked_Exports\\UV_Sterilizer_System_55W_SUS304_DN25_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\UV_Sterilizer_System_55W_SUS304_DN25\\06_Renders_and_Media"
    },
    {
      "name": "Ultrasonic_Humidifier_Box_20Head",
      "title": "Ultrasonic Humidifier Box 20Head - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Ultrasonic Humidifier Box 20Head - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Ultrasonic_Humidifier_Box_20Head\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Ultrasonic_Humidifier_Box_20Head_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Ultrasonic_Humidifier_Box_20Head\\06_Renders_and_Media\\04_Watermarked_Exports\\Ultrasonic_Humidifier_Box_20Head_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Ultrasonic_Humidifier_Box_20Head\\06_Renders_and_Media"
    },
    {
      "name": "Ultrasonic_Mist_Maker_10Head_48V",
      "title": "Ultrasonic Mist Maker 10Head 48V - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Ultrasonic Mist Maker 10Head 48V - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Ultrasonic_Mist_Maker_10Head_48V\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Ultrasonic_Mist_Maker_10Head_48V_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Ultrasonic_Mist_Maker_10Head_48V\\06_Renders_and_Media\\04_Watermarked_Exports\\Ultrasonic_Mist_Maker_10Head_48V_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Ultrasonic_Mist_Maker_10Head_48V\\06_Renders_and_Media"
    },
    {
      "name": "Venturi_Aeration_Ejector_DN80_SS304",
      "title": "Venturi Aeration Ejector DN80 SS304 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Venturi Aeration Ejector DN80 SS304 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Venturi_Aeration_Ejector_DN80_SS304\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Venturi_Aeration_Ejector_DN80_SS304_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Venturi_Aeration_Ejector_DN80_SS304\\06_Renders_and_Media\\04_Watermarked_Exports\\Venturi_Aeration_Ejector_DN80_SS304_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\07_Disinfection_and_Water_Conditioning\\Venturi_Aeration_Ejector_DN80_SS304\\06_Renders_and_Media"
    }
  ],
  "08_Instrumentation_and_Analyzers": [
    {
      "name": "Air_Gas_Panel_Flowmeter_With_Valve",
      "title": "Air Gas Panel Flowmeter With Valve - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Air Gas Panel Flowmeter With Valve - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Air_Gas_Panel_Flowmeter_With_Valve\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Air_Gas_Panel_Flowmeter_With_Valve_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Air_Gas_Panel_Flowmeter_With_Valve\\06_Renders_and_Media\\04_Watermarked_Exports\\Air_Gas_Panel_Flowmeter_With_Valve_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Air_Gas_Panel_Flowmeter_With_Valve\\06_Renders_and_Media"
    },
    {
      "name": "Brass_Magnetic_Flow_Switch_DN20_34",
      "title": "Brass Magnetic Flow Switch DN20 34 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Brass Magnetic Flow Switch DN20 34 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Brass_Magnetic_Flow_Switch_DN20_34\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Brass_Magnetic_Flow_Switch_DN20_34_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Brass_Magnetic_Flow_Switch_DN20_34\\06_Renders_and_Media\\04_Watermarked_Exports\\Brass_Magnetic_Flow_Switch_DN20_34_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Brass_Magnetic_Flow_Switch_DN20_34\\06_Renders_and_Media"
    },
    {
      "name": "Differential_Pressure_Transmitter_4_20mA",
      "title": "Differential Pressure Transmitter 4 20mA - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Differential Pressure Transmitter 4 20mA - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Differential_Pressure_Transmitter_4_20mA\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Differential_Pressure_Transmitter_4_20mA_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Differential_Pressure_Transmitter_4_20mA\\06_Renders_and_Media\\04_Watermarked_Exports\\Differential_Pressure_Transmitter_4_20mA_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Differential_Pressure_Transmitter_4_20mA\\06_Renders_and_Media"
    },
    {
      "name": "EDI_Megaohm_Resistivity_Sensor_SUS316",
      "title": "EDI Megaohm Resistivity Sensor SUS316 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "EDI Megaohm Resistivity Sensor SUS316 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\EDI_Megaohm_Resistivity_Sensor_SUS316\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\EDI_Megaohm_Resistivity_Sensor_SUS316_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\EDI_Megaohm_Resistivity_Sensor_SUS316\\06_Renders_and_Media\\04_Watermarked_Exports\\EDI_Megaohm_Resistivity_Sensor_SUS316_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\EDI_Megaohm_Resistivity_Sensor_SUS316\\06_Renders_and_Media"
    },
    {
      "name": "Electromagnetic_Flowmeter_DN50",
      "title": "Electromagnetic Flowmeter DN50 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Electromagnetic Flowmeter DN50 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Electromagnetic_Flowmeter_DN50\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Electromagnetic_Flowmeter_DN50_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Electromagnetic_Flowmeter_DN50\\06_Renders_and_Media\\04_Watermarked_Exports\\Electromagnetic_Flowmeter_DN50_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Electromagnetic_Flowmeter_DN50\\06_Renders_and_Media"
    },
    {
      "name": "Electromagnetic_Flowmeter_DN65",
      "title": "Electromagnetic Flowmeter DN65 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Electromagnetic Flowmeter DN65 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Electromagnetic_Flowmeter_DN65\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Electromagnetic_Flowmeter_DN65_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Electromagnetic_Flowmeter_DN65\\06_Renders_and_Media\\04_Watermarked_Exports\\Electromagnetic_Flowmeter_DN65_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Electromagnetic_Flowmeter_DN65\\06_Renders_and_Media"
    },
    {
      "name": "Electromagnetic_Flowmeter_DN65_Flanged",
      "title": "Electromagnetic Flowmeter DN65 Flanged - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Electromagnetic Flowmeter DN65 Flanged - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Electromagnetic_Flowmeter_DN65_Flanged\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Electromagnetic_Flowmeter_DN65_Flanged_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Electromagnetic_Flowmeter_DN65_Flanged\\06_Renders_and_Media\\04_Watermarked_Exports\\Electromagnetic_Flowmeter_DN65_Flanged_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Electromagnetic_Flowmeter_DN65_Flanged\\06_Renders_and_Media"
    },
    {
      "name": "Hydrostatic_Submersible_Level_Sensor",
      "title": "Hydrostatic Submersible Level Sensor - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Hydrostatic Submersible Level Sensor - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Hydrostatic_Submersible_Level_Sensor\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Hydrostatic_Submersible_Level_Sensor_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Hydrostatic_Submersible_Level_Sensor\\06_Renders_and_Media\\04_Watermarked_Exports\\Hydrostatic_Submersible_Level_Sensor_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Hydrostatic_Submersible_Level_Sensor\\06_Renders_and_Media"
    },
    {
      "name": "Industrial_Pressure_Transmitter_4_20mA",
      "title": "Industrial Pressure Transmitter 4 20mA - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Industrial Pressure Transmitter 4 20mA - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Industrial_Pressure_Transmitter_4_20mA\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Industrial_Pressure_Transmitter_4_20mA_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Industrial_Pressure_Transmitter_4_20mA\\06_Renders_and_Media\\04_Watermarked_Exports\\Industrial_Pressure_Transmitter_4_20mA_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Industrial_Pressure_Transmitter_4_20mA\\06_Renders_and_Media"
    },
    {
      "name": "Industrial_Submersible_pH_Sensor_Probe",
      "title": "Industrial Submersible pH Sensor Probe - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Industrial Submersible pH Sensor Probe - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Industrial_Submersible_pH_Sensor_Probe\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Industrial_Submersible_pH_Sensor_Probe_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Industrial_Submersible_pH_Sensor_Probe\\06_Renders_and_Media\\04_Watermarked_Exports\\Industrial_Submersible_pH_Sensor_Probe_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Industrial_Submersible_pH_Sensor_Probe\\06_Renders_and_Media"
    },
    {
      "name": "Industrial_pH_ORP_Electrode_Sensor",
      "title": "Industrial pH ORP Electrode Sensor - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Industrial pH ORP Electrode Sensor - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Industrial_pH_ORP_Electrode_Sensor\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Industrial_pH_ORP_Electrode_Sensor_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Industrial_pH_ORP_Electrode_Sensor\\06_Renders_and_Media\\04_Watermarked_Exports\\Industrial_pH_ORP_Electrode_Sensor_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Industrial_pH_ORP_Electrode_Sensor\\06_Renders_and_Media"
    },
    {
      "name": "Inline_Conductivity_EC_Sensor_SUS316",
      "title": "Inline Conductivity EC Sensor SUS316 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Inline Conductivity EC Sensor SUS316 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Inline_Conductivity_EC_Sensor_SUS316\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Inline_Conductivity_EC_Sensor_SUS316_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Inline_Conductivity_EC_Sensor_SUS316\\06_Renders_and_Media\\04_Watermarked_Exports\\Inline_Conductivity_EC_Sensor_SUS316_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Inline_Conductivity_EC_Sensor_SUS316\\06_Renders_and_Media"
    },
    {
      "name": "Inline_Water_TDS_Probe_Sensor",
      "title": "Inline Water TDS Probe Sensor - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Inline Water TDS Probe Sensor - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Inline_Water_TDS_Probe_Sensor\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Inline_Water_TDS_Probe_Sensor_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Inline_Water_TDS_Probe_Sensor\\06_Renders_and_Media\\04_Watermarked_Exports\\Inline_Water_TDS_Probe_Sensor_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Inline_Water_TDS_Probe_Sensor\\06_Renders_and_Media"
    },
    {
      "name": "Lohand_LHD6901_Water_Quality_Controller",
      "title": "Lohand LHD6901 Water Quality Controller - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Lohand LHD6901 Water Quality Controller - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Lohand_LHD6901_Water_Quality_Controller\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Lohand_LHD6901_Water_Quality_Controller_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Lohand_LHD6901_Water_Quality_Controller\\06_Renders_and_Media\\04_Watermarked_Exports\\Lohand_LHD6901_Water_Quality_Controller_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Lohand_LHD6901_Water_Quality_Controller\\06_Renders_and_Media"
    },
    {
      "name": "Lohand_Residual_Chlorine_Flow_Cell",
      "title": "Lohand Residual Chlorine Flow Cell - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Lohand Residual Chlorine Flow Cell - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Lohand_Residual_Chlorine_Flow_Cell\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Lohand_Residual_Chlorine_Flow_Cell_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Lohand_Residual_Chlorine_Flow_Cell\\06_Renders_and_Media\\04_Watermarked_Exports\\Lohand_Residual_Chlorine_Flow_Cell_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Lohand_Residual_Chlorine_Flow_Cell\\06_Renders_and_Media"
    },
    {
      "name": "Lohand_Turbidity_Sensor_Flow_Cell",
      "title": "Lohand Turbidity Sensor Flow Cell - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Lohand Turbidity Sensor Flow Cell - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Lohand_Turbidity_Sensor_Flow_Cell\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Lohand_Turbidity_Sensor_Flow_Cell_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Lohand_Turbidity_Sensor_Flow_Cell\\06_Renders_and_Media\\04_Watermarked_Exports\\Lohand_Turbidity_Sensor_Flow_Cell_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Lohand_Turbidity_Sensor_Flow_Cell\\06_Renders_and_Media"
    },
    {
      "name": "Mini_Panel_Flowmeter_2LPM_Valve",
      "title": "Mini Panel Flowmeter 2LPM Valve - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Mini Panel Flowmeter 2LPM Valve - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Mini_Panel_Flowmeter_2LPM_Valve\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Mini_Panel_Flowmeter_2LPM_Valve_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Mini_Panel_Flowmeter_2LPM_Valve\\06_Renders_and_Media\\04_Watermarked_Exports\\Mini_Panel_Flowmeter_2LPM_Valve_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Mini_Panel_Flowmeter_2LPM_Valve\\06_Renders_and_Media"
    },
    {
      "name": "Mini_Panel_Flowmeter_600ml_Valve",
      "title": "Mini Panel Flowmeter 600ml Valve - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Mini Panel Flowmeter 600ml Valve - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Mini_Panel_Flowmeter_600ml_Valve\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Mini_Panel_Flowmeter_600ml_Valve_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Mini_Panel_Flowmeter_600ml_Valve\\06_Renders_and_Media\\04_Watermarked_Exports\\Mini_Panel_Flowmeter_600ml_Valve_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Mini_Panel_Flowmeter_600ml_Valve\\06_Renders_and_Media"
    },
    {
      "name": "Mini_Pulse_Flow_Sensor_10mm",
      "title": "Mini Pulse Flow Sensor 10mm - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Mini Pulse Flow Sensor 10mm - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Mini_Pulse_Flow_Sensor_10mm\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Mini_Pulse_Flow_Sensor_10mm_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Mini_Pulse_Flow_Sensor_10mm\\06_Renders_and_Media\\04_Watermarked_Exports\\Mini_Pulse_Flow_Sensor_10mm_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Mini_Pulse_Flow_Sensor_10mm\\06_Renders_and_Media"
    },
    {
      "name": "Panel_Mount_Flowmeter_4_8m3h_DN20",
      "title": "Panel Mount Flowmeter 4 8m3h DN20 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Panel Mount Flowmeter 4 8m3h DN20 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Panel_Mount_Flowmeter_4_8m3h_DN20\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Panel_Mount_Flowmeter_4_8m3h_DN20_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Panel_Mount_Flowmeter_4_8m3h_DN20\\06_Renders_and_Media\\04_Watermarked_Exports\\Panel_Mount_Flowmeter_4_8m3h_DN20_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Panel_Mount_Flowmeter_4_8m3h_DN20\\06_Renders_and_Media"
    },
    {
      "name": "Panel_Mount_Flowmeter_DN15_D21",
      "title": "Panel Mount Flowmeter DN15 D21 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Panel Mount Flowmeter DN15 D21 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Panel_Mount_Flowmeter_DN15_D21\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Panel_Mount_Flowmeter_DN15_D21_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Panel_Mount_Flowmeter_DN15_D21\\06_Renders_and_Media\\04_Watermarked_Exports\\Panel_Mount_Flowmeter_DN15_D21_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Panel_Mount_Flowmeter_DN15_D21\\06_Renders_and_Media"
    },
    {
      "name": "Panel_Mount_Flowmeter_DN20_D27",
      "title": "Panel Mount Flowmeter DN20 D27 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Panel Mount Flowmeter DN20 D27 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Panel_Mount_Flowmeter_DN20_D27\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Panel_Mount_Flowmeter_DN20_D27_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Panel_Mount_Flowmeter_DN20_D27\\06_Renders_and_Media\\04_Watermarked_Exports\\Panel_Mount_Flowmeter_DN20_D27_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Panel_Mount_Flowmeter_DN20_D27\\06_Renders_and_Media"
    },
    {
      "name": "Panel_Mount_Pressure_Gauge",
      "title": "Panel Mount Pressure Gauge - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Panel Mount Pressure Gauge - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Panel_Mount_Pressure_Gauge\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Panel_Mount_Pressure_Gauge_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Panel_Mount_Pressure_Gauge\\06_Renders_and_Media\\04_Watermarked_Exports\\Panel_Mount_Pressure_Gauge_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Panel_Mount_Pressure_Gauge\\06_Renders_and_Media"
    },
    {
      "name": "Panel_Mount_Pressure_Gauge_D100_Back",
      "title": "Panel Mount Pressure Gauge D100 Back - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Panel Mount Pressure Gauge D100 Back - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Panel_Mount_Pressure_Gauge_D100_Back\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Panel_Mount_Pressure_Gauge_D100_Back_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Panel_Mount_Pressure_Gauge_D100_Back\\06_Renders_and_Media\\04_Watermarked_Exports\\Panel_Mount_Pressure_Gauge_D100_Back_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Panel_Mount_Pressure_Gauge_D100_Back\\06_Renders_and_Media"
    },
    {
      "name": "Panel_Mount_Pressure_Gauge_D60_Back",
      "title": "Panel Mount Pressure Gauge D60 Back - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Panel Mount Pressure Gauge D60 Back - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Panel_Mount_Pressure_Gauge_D60_Back\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Panel_Mount_Pressure_Gauge_D60_Back_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Panel_Mount_Pressure_Gauge_D60_Back\\06_Renders_and_Media\\04_Watermarked_Exports\\Panel_Mount_Pressure_Gauge_D60_Back_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Panel_Mount_Pressure_Gauge_D60_Back\\06_Renders_and_Media"
    },
    {
      "name": "Plastic_EC_Conductivity_Sensor_CON1134",
      "title": "Plastic EC Conductivity Sensor CON1134 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Plastic EC Conductivity Sensor CON1134 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Plastic_EC_Conductivity_Sensor_CON1134\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Plastic_EC_Conductivity_Sensor_CON1134_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Plastic_EC_Conductivity_Sensor_CON1134\\06_Renders_and_Media\\04_Watermarked_Exports\\Plastic_EC_Conductivity_Sensor_CON1134_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Plastic_EC_Conductivity_Sensor_CON1134\\06_Renders_and_Media"
    },
    {
      "name": "Pressure_Gauge_Siphon_Tube_DN15_SS",
      "title": "Pressure Gauge Siphon Tube DN15 SS - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Pressure Gauge Siphon Tube DN15 SS - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Pressure_Gauge_Siphon_Tube_DN15_SS\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Pressure_Gauge_Siphon_Tube_DN15_SS_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Pressure_Gauge_Siphon_Tube_DN15_SS\\06_Renders_and_Media\\04_Watermarked_Exports\\Pressure_Gauge_Siphon_Tube_DN15_SS_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Pressure_Gauge_Siphon_Tube_DN15_SS\\06_Renders_and_Media"
    },
    {
      "name": "ProMinent_pH_Sensor_DULCOTEST",
      "title": "ProMinent pH Sensor DULCOTEST - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "ProMinent pH Sensor DULCOTEST - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\ProMinent_pH_Sensor_DULCOTEST\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\ProMinent_pH_Sensor_DULCOTEST_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\ProMinent_pH_Sensor_DULCOTEST\\06_Renders_and_Media\\04_Watermarked_Exports\\ProMinent_pH_Sensor_DULCOTEST_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\ProMinent_pH_Sensor_DULCOTEST\\06_Renders_and_Media"
    },
    {
      "name": "Pulse_Output_Flow_Sensor_DN25",
      "title": "Pulse Output Flow Sensor DN25 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Pulse Output Flow Sensor DN25 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Pulse_Output_Flow_Sensor_DN25\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Pulse_Output_Flow_Sensor_DN25_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Pulse_Output_Flow_Sensor_DN25\\06_Renders_and_Media\\04_Watermarked_Exports\\Pulse_Output_Flow_Sensor_DN25_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Pulse_Output_Flow_Sensor_DN25\\06_Renders_and_Media"
    },
    {
      "name": "Pulse_Output_Flow_Sensor_DN40",
      "title": "Pulse Output Flow Sensor DN40 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Pulse Output Flow Sensor DN40 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Pulse_Output_Flow_Sensor_DN40\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Pulse_Output_Flow_Sensor_DN40_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Pulse_Output_Flow_Sensor_DN40\\06_Renders_and_Media\\04_Watermarked_Exports\\Pulse_Output_Flow_Sensor_DN40_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Pulse_Output_Flow_Sensor_DN40\\06_Renders_and_Media"
    },
    {
      "name": "ROC_CCT3300_Conductivity_Monitor",
      "title": "ROC CCT3300 Conductivity Monitor - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "ROC CCT3300 Conductivity Monitor - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\ROC_CCT3300_Conductivity_Monitor\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\ROC_CCT3300_Conductivity_Monitor_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\ROC_CCT3300_Conductivity_Monitor\\06_Renders_and_Media\\04_Watermarked_Exports\\ROC_CCT3300_Conductivity_Monitor_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\ROC_CCT3300_Conductivity_Monitor\\06_Renders_and_Media"
    },
    {
      "name": "RO_Pump_Discharge_Pressure_Station",
      "title": "RO Pump Discharge Pressure Station - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "RO Pump Discharge Pressure Station - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\RO_Pump_Discharge_Pressure_Station\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\RO_Pump_Discharge_Pressure_Station_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\RO_Pump_Discharge_Pressure_Station\\06_Renders_and_Media\\04_Watermarked_Exports\\RO_Pump_Discharge_Pressure_Station_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\RO_Pump_Discharge_Pressure_Station\\06_Renders_and_Media"
    },
    {
      "name": "Remond_Digital_EC_Sensor_RS485",
      "title": "Remond Digital EC Sensor RS485 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Remond Digital EC Sensor RS485 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Remond_Digital_EC_Sensor_RS485\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Remond_Digital_EC_Sensor_RS485_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Remond_Digital_EC_Sensor_RS485\\06_Renders_and_Media\\04_Watermarked_Exports\\Remond_Digital_EC_Sensor_RS485_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Remond_Digital_EC_Sensor_RS485\\06_Renders_and_Media"
    },
    {
      "name": "Remond_Digital_pH_Sensor_RS485",
      "title": "Remond Digital pH Sensor RS485 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Remond Digital pH Sensor RS485 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Remond_Digital_pH_Sensor_RS485\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Remond_Digital_pH_Sensor_RS485_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Remond_Digital_pH_Sensor_RS485\\06_Renders_and_Media\\04_Watermarked_Exports\\Remond_Digital_pH_Sensor_RS485_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Remond_Digital_pH_Sensor_RS485\\06_Renders_and_Media"
    },
    {
      "name": "Rotameter_Flowmeter_PPR_Union_DN25",
      "title": "Rotameter Flowmeter PPR Union DN25 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Rotameter Flowmeter PPR Union DN25 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Rotameter_Flowmeter_PPR_Union_DN25\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Rotameter_Flowmeter_PPR_Union_DN25_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Rotameter_Flowmeter_PPR_Union_DN25\\06_Renders_and_Media\\04_Watermarked_Exports\\Rotameter_Flowmeter_PPR_Union_DN25_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Rotameter_Flowmeter_PPR_Union_DN25\\06_Renders_and_Media"
    },
    {
      "name": "Rotameter_Flowmeter_PanelMount_2_18LPM_DN25",
      "title": "Rotameter Flowmeter PanelMount 2 18LPM DN25 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Rotameter Flowmeter PanelMount 2 18LPM DN25 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Rotameter_Flowmeter_PanelMount_2_18LPM_DN25\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Rotameter_Flowmeter_PanelMount_2_18LPM_DN25_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Rotameter_Flowmeter_PanelMount_2_18LPM_DN25\\06_Renders_and_Media\\04_Watermarked_Exports\\Rotameter_Flowmeter_PanelMount_2_18LPM_DN25_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Rotameter_Flowmeter_PanelMount_2_18LPM_DN25\\06_Renders_and_Media"
    },
    {
      "name": "Round_Tube_Rotameter_DN25_D34",
      "title": "Round Tube Rotameter DN25 D34 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Round Tube Rotameter DN25 D34 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Round_Tube_Rotameter_DN25_D34\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Round_Tube_Rotameter_DN25_D34_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Round_Tube_Rotameter_DN25_D34\\06_Renders_and_Media\\04_Watermarked_Exports\\Round_Tube_Rotameter_DN25_D34_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Round_Tube_Rotameter_DN25_D34\\06_Renders_and_Media"
    },
    {
      "name": "Short_Rotameter_16m3h_DN40_Threaded",
      "title": "Short Rotameter 16m3h DN40 Threaded - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Short Rotameter 16m3h DN40 Threaded - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Short_Rotameter_16m3h_DN40_Threaded\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Short_Rotameter_16m3h_DN40_Threaded_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Short_Rotameter_16m3h_DN40_Threaded\\06_Renders_and_Media\\04_Watermarked_Exports\\Short_Rotameter_16m3h_DN40_Threaded_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Short_Rotameter_16m3h_DN40_Threaded\\06_Renders_and_Media"
    },
    {
      "name": "Short_Tube_Rotameter_2500LPH_DN20",
      "title": "Short Tube Rotameter 2500LPH DN20 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Short Tube Rotameter 2500LPH DN20 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Short_Tube_Rotameter_2500LPH_DN20\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Short_Tube_Rotameter_2500LPH_DN20_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Short_Tube_Rotameter_2500LPH_DN20\\06_Renders_and_Media\\04_Watermarked_Exports\\Short_Tube_Rotameter_2500LPH_DN20_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Short_Tube_Rotameter_2500LPH_DN20\\06_Renders_and_Media"
    },
    {
      "name": "Short_Tube_Rotameter_6000LPH_DN25",
      "title": "Short Tube Rotameter 6000LPH DN25 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Short Tube Rotameter 6000LPH DN25 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Short_Tube_Rotameter_6000LPH_DN25\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Short_Tube_Rotameter_6000LPH_DN25_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Short_Tube_Rotameter_6000LPH_DN25\\06_Renders_and_Media\\04_Watermarked_Exports\\Short_Tube_Rotameter_6000LPH_DN25_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Short_Tube_Rotameter_6000LPH_DN25\\06_Renders_and_Media"
    },
    {
      "name": "Short_Tube_Rotameter_DN20_Female",
      "title": "Short Tube Rotameter DN20 Female - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Short Tube Rotameter DN20 Female - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Short_Tube_Rotameter_DN20_Female\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Short_Tube_Rotameter_DN20_Female_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Short_Tube_Rotameter_DN20_Female\\06_Renders_and_Media\\04_Watermarked_Exports\\Short_Tube_Rotameter_DN20_Female_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Short_Tube_Rotameter_DN20_Female\\06_Renders_and_Media"
    },
    {
      "name": "Soil_EC_Moisture_Sensor_RS485",
      "title": "Soil EC Moisture Sensor RS485 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Soil EC Moisture Sensor RS485 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Soil_EC_Moisture_Sensor_RS485\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Soil_EC_Moisture_Sensor_RS485_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Soil_EC_Moisture_Sensor_RS485\\06_Renders_and_Media\\04_Watermarked_Exports\\Soil_EC_Moisture_Sensor_RS485_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Soil_EC_Moisture_Sensor_RS485\\06_Renders_and_Media"
    },
    {
      "name": "Supmea_Online_Chlorine_Controller",
      "title": "Supmea Online Chlorine Controller - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Supmea Online Chlorine Controller - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Supmea_Online_Chlorine_Controller\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Supmea_Online_Chlorine_Controller_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Supmea_Online_Chlorine_Controller\\06_Renders_and_Media\\04_Watermarked_Exports\\Supmea_Online_Chlorine_Controller_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Supmea_Online_Chlorine_Controller\\06_Renders_and_Media"
    },
    {
      "name": "Supmea_Residual_Chlorine_Flow_Cell",
      "title": "Supmea Residual Chlorine Flow Cell - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Supmea Residual Chlorine Flow Cell - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Supmea_Residual_Chlorine_Flow_Cell\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Supmea_Residual_Chlorine_Flow_Cell_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Supmea_Residual_Chlorine_Flow_Cell\\06_Renders_and_Media\\04_Watermarked_Exports\\Supmea_Residual_Chlorine_Flow_Cell_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Supmea_Residual_Chlorine_Flow_Cell\\06_Renders_and_Media"
    },
    {
      "name": "Supmea_SUP1100_Digital_Process_Meter",
      "title": "Supmea SUP1100 Digital Process Meter - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Supmea SUP1100 Digital Process Meter - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Supmea_SUP1100_Digital_Process_Meter\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Supmea_SUP1100_Digital_Process_Meter_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Supmea_SUP1100_Digital_Process_Meter\\06_Renders_and_Media\\04_Watermarked_Exports\\Supmea_SUP1100_Digital_Process_Meter_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Supmea_SUP1100_Digital_Process_Meter\\06_Renders_and_Media"
    },
    {
      "name": "Tank_Pressure_Monitoring_Station_Unit",
      "title": "Tank Pressure Monitoring Station Unit - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Tank Pressure Monitoring Station Unit - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Tank_Pressure_Monitoring_Station_Unit\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Tank_Pressure_Monitoring_Station_Unit_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Tank_Pressure_Monitoring_Station_Unit\\06_Renders_and_Media\\04_Watermarked_Exports\\Tank_Pressure_Monitoring_Station_Unit_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Tank_Pressure_Monitoring_Station_Unit\\06_Renders_and_Media"
    },
    {
      "name": "Threaded_Pressure_Gauge_D100_Bottom",
      "title": "Threaded Pressure Gauge D100 Bottom - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Threaded Pressure Gauge D100 Bottom - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Threaded_Pressure_Gauge_D100_Bottom\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Threaded_Pressure_Gauge_D100_Bottom_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Threaded_Pressure_Gauge_D100_Bottom\\06_Renders_and_Media\\04_Watermarked_Exports\\Threaded_Pressure_Gauge_D100_Bottom_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Threaded_Pressure_Gauge_D100_Bottom\\06_Renders_and_Media"
    },
    {
      "name": "Threaded_Pressure_Gauge_D60_Bottom",
      "title": "Threaded Pressure Gauge D60 Bottom - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Threaded Pressure Gauge D60 Bottom - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Threaded_Pressure_Gauge_D60_Bottom\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Threaded_Pressure_Gauge_D60_Bottom_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Threaded_Pressure_Gauge_D60_Bottom\\06_Renders_and_Media\\04_Watermarked_Exports\\Threaded_Pressure_Gauge_D60_Bottom_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Threaded_Pressure_Gauge_D60_Bottom\\06_Renders_and_Media"
    },
    {
      "name": "Threaded_Pressure_Gauge_SUS304",
      "title": "Threaded Pressure Gauge SUS304 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Threaded Pressure Gauge SUS304 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Threaded_Pressure_Gauge_SUS304\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Threaded_Pressure_Gauge_SUS304_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Threaded_Pressure_Gauge_SUS304\\06_Renders_and_Media\\04_Watermarked_Exports\\Threaded_Pressure_Gauge_SUS304_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Threaded_Pressure_Gauge_SUS304\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_Inlet_Pressure_Sensor_Assembly",
      "title": "UPVC Inlet Pressure Sensor Assembly - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC Inlet Pressure Sensor Assembly - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Inlet_Pressure_Sensor_Assembly\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_Inlet_Pressure_Sensor_Assembly_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Inlet_Pressure_Sensor_Assembly\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_Inlet_Pressure_Sensor_Assembly_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Inlet_Pressure_Sensor_Assembly\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_Long_Tube_Rotameter_DN15_D21",
      "title": "UPVC Long Tube Rotameter DN15 D21 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC Long Tube Rotameter DN15 D21 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Long_Tube_Rotameter_DN15_D21\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_Long_Tube_Rotameter_DN15_D21_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Long_Tube_Rotameter_DN15_D21\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_Long_Tube_Rotameter_DN15_D21_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Long_Tube_Rotameter_DN15_D21\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_Long_Tube_Rotameter_DN20_D27",
      "title": "UPVC Long Tube Rotameter DN20 D27 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC Long Tube Rotameter DN20 D27 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Long_Tube_Rotameter_DN20_D27\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_Long_Tube_Rotameter_DN20_D27_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Long_Tube_Rotameter_DN20_D27\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_Long_Tube_Rotameter_DN20_D27_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Long_Tube_Rotameter_DN20_D27\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_Short_Tube_Rotameter_DN32_D42",
      "title": "UPVC Short Tube Rotameter DN32 D42 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC Short Tube Rotameter DN32 D42 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Short_Tube_Rotameter_DN32_D42\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_Short_Tube_Rotameter_DN32_D42_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Short_Tube_Rotameter_DN32_D42\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_Short_Tube_Rotameter_DN32_D42_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Short_Tube_Rotameter_DN32_D42\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_Short_Tube_Rotameter_DN50_D63",
      "title": "UPVC Short Tube Rotameter DN50 D63 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC Short Tube Rotameter DN50 D63 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Short_Tube_Rotameter_DN50_D63\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_Short_Tube_Rotameter_DN50_D63_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Short_Tube_Rotameter_DN50_D63\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_Short_Tube_Rotameter_DN50_D63_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Short_Tube_Rotameter_DN50_D63\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_Short_Tube_Rotameter_DN80_D90",
      "title": "UPVC Short Tube Rotameter DN80 D90 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC Short Tube Rotameter DN80 D90 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Short_Tube_Rotameter_DN80_D90\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_Short_Tube_Rotameter_DN80_D90_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Short_Tube_Rotameter_DN80_D90\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_Short_Tube_Rotameter_DN80_D90_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Short_Tube_Rotameter_DN80_D90\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_Tube_Rotameter_Union_DN20_D27",
      "title": "UPVC Tube Rotameter Union DN20 D27 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC Tube Rotameter Union DN20 D27 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Tube_Rotameter_Union_DN20_D27\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_Tube_Rotameter_Union_DN20_D27_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Tube_Rotameter_Union_DN20_D27\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_Tube_Rotameter_Union_DN20_D27_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Tube_Rotameter_Union_DN20_D27\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_Tube_Rotameter_Union_DN50_D63",
      "title": "UPVC Tube Rotameter Union DN50 D63 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC Tube Rotameter Union DN50 D63 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Tube_Rotameter_Union_DN50_D63\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_Tube_Rotameter_Union_DN50_D63_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Tube_Rotameter_Union_DN50_D63\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_Tube_Rotameter_Union_DN50_D63_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Tube_Rotameter_Union_DN50_D63\\06_Renders_and_Media"
    },
    {
      "name": "UPVC_Tube_Rotameter_Union_DN65_D75",
      "title": "UPVC Tube Rotameter Union DN65 D75 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "UPVC Tube Rotameter Union DN65 D75 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Tube_Rotameter_Union_DN65_D75\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\UPVC_Tube_Rotameter_Union_DN65_D75_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Tube_Rotameter_Union_DN65_D75\\06_Renders_and_Media\\04_Watermarked_Exports\\UPVC_Tube_Rotameter_Union_DN65_D75_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\UPVC_Tube_Rotameter_Union_DN65_D75\\06_Renders_and_Media"
    },
    {
      "name": "Ultrapure_Resistivity_Sensor_6mm",
      "title": "Ultrapure Resistivity Sensor 6mm - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Ultrapure Resistivity Sensor 6mm - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Ultrapure_Resistivity_Sensor_6mm\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Ultrapure_Resistivity_Sensor_6mm_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Ultrapure_Resistivity_Sensor_6mm\\06_Renders_and_Media\\04_Watermarked_Exports\\Ultrapure_Resistivity_Sensor_6mm_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\08_Instrumentation_and_Analyzers\\Ultrapure_Resistivity_Sensor_6mm\\06_Renders_and_Media"
    }
  ],
  "09_Electrical_Control_and_IoT": [
    {
      "name": "3in1_AC_Power_Entry_EMI_Filter_Module",
      "title": "3in1 AC Power Entry EMI Filter Module - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "3in1 AC Power Entry EMI Filter Module - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\3in1_AC_Power_Entry_EMI_Filter_Module\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\3in1_AC_Power_Entry_EMI_Filter_Module_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\3in1_AC_Power_Entry_EMI_Filter_Module\\06_Renders_and_Media\\04_Watermarked_Exports\\3in1_AC_Power_Entry_EMI_Filter_Module_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\3in1_AC_Power_Entry_EMI_Filter_Module\\06_Renders_and_Media"
    },
    {
      "name": "Air_Quality_LED_Display_Board_600x400",
      "title": "Air Quality LED Display Board 600x400 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Air Quality LED Display Board 600x400 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Air_Quality_LED_Display_Board_600x400\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Air_Quality_LED_Display_Board_600x400_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Air_Quality_LED_Display_Board_600x400\\06_Renders_and_Media\\04_Watermarked_Exports\\Air_Quality_LED_Display_Board_600x400_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Air_Quality_LED_Display_Board_600x400\\06_Renders_and_Media"
    },
    {
      "name": "Air_Temp_Humidity_Sensor_RS485",
      "title": "Air Temp Humidity Sensor RS485 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Air Temp Humidity Sensor RS485 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Air_Temp_Humidity_Sensor_RS485\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Air_Temp_Humidity_Sensor_RS485_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Air_Temp_Humidity_Sensor_RS485\\06_Renders_and_Media\\04_Watermarked_Exports\\Air_Temp_Humidity_Sensor_RS485_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Air_Temp_Humidity_Sensor_RS485\\06_Renders_and_Media"
    },
    {
      "name": "Alarm_Warning_Beacon_Light_24VDC_Red",
      "title": "Alarm Warning Beacon Light 24VDC Red - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Alarm Warning Beacon Light 24VDC Red - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Alarm_Warning_Beacon_Light_24VDC_Red\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Alarm_Warning_Beacon_Light_24VDC_Red_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Alarm_Warning_Beacon_Light_24VDC_Red\\06_Renders_and_Media\\04_Watermarked_Exports\\Alarm_Warning_Beacon_Light_24VDC_Red_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Alarm_Warning_Beacon_Light_24VDC_Red\\06_Renders_and_Media"
    },
    {
      "name": "Ambient_Light_Sensor_RS485_Modbus",
      "title": "Ambient Light Sensor RS485 Modbus - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Ambient Light Sensor RS485 Modbus - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Ambient_Light_Sensor_RS485_Modbus\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Ambient_Light_Sensor_RS485_Modbus_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Ambient_Light_Sensor_RS485_Modbus\\06_Renders_and_Media\\04_Watermarked_Exports\\Ambient_Light_Sensor_RS485_Modbus_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Ambient_Light_Sensor_RS485_Modbus\\06_Renders_and_Media"
    },
    {
      "name": "Boxco_Plastic_Enclosure_300x200x130",
      "title": "Boxco Plastic Enclosure 300x200x130 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Boxco Plastic Enclosure 300x200x130 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Boxco_Plastic_Enclosure_300x200x130\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Boxco_Plastic_Enclosure_300x200x130_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Boxco_Plastic_Enclosure_300x200x130\\06_Renders_and_Media\\04_Watermarked_Exports\\Boxco_Plastic_Enclosure_300x200x130_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Boxco_Plastic_Enclosure_300x200x130\\06_Renders_and_Media"
    },
    {
      "name": "Boxco_Plastic_Enclosure_300x200x180",
      "title": "Boxco Plastic Enclosure 300x200x180 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Boxco Plastic Enclosure 300x200x180 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Boxco_Plastic_Enclosure_300x200x180\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Boxco_Plastic_Enclosure_300x200x180_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Boxco_Plastic_Enclosure_300x200x180\\06_Renders_and_Media\\04_Watermarked_Exports\\Boxco_Plastic_Enclosure_300x200x180_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Boxco_Plastic_Enclosure_300x200x180\\06_Renders_and_Media"
    },
    {
      "name": "Boxco_Plastic_Enclosure_400x500x200",
      "title": "Boxco Plastic Enclosure 400x500x200 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Boxco Plastic Enclosure 400x500x200 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Boxco_Plastic_Enclosure_400x500x200\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Boxco_Plastic_Enclosure_400x500x200_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Boxco_Plastic_Enclosure_400x500x200\\06_Renders_and_Media\\04_Watermarked_Exports\\Boxco_Plastic_Enclosure_400x500x200_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Boxco_Plastic_Enclosure_400x500x200\\06_Renders_and_Media"
    },
    {
      "name": "CHINT_1P_Miniature_Circuit_Breaker",
      "title": "CHINT 1P Miniature Circuit Breaker - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "CHINT 1P Miniature Circuit Breaker - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\CHINT_1P_Miniature_Circuit_Breaker\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\CHINT_1P_Miniature_Circuit_Breaker_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\CHINT_1P_Miniature_Circuit_Breaker\\06_Renders_and_Media\\04_Watermarked_Exports\\CHINT_1P_Miniature_Circuit_Breaker_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\CHINT_1P_Miniature_Circuit_Breaker\\06_Renders_and_Media"
    },
    {
      "name": "CO2_Air_Quality_Sensor_RS485",
      "title": "CO2 Air Quality Sensor RS485 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "CO2 Air Quality Sensor RS485 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\CO2_Air_Quality_Sensor_RS485\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\CO2_Air_Quality_Sensor_RS485_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\CO2_Air_Quality_Sensor_RS485\\06_Renders_and_Media\\04_Watermarked_Exports\\CO2_Air_Quality_Sensor_RS485_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\CO2_Air_Quality_Sensor_RS485\\06_Renders_and_Media"
    },
    {
      "name": "DIN_Rail_Cartridge_Fuse_Holder_10x38",
      "title": "DIN Rail Cartridge Fuse Holder 10x38 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "DIN Rail Cartridge Fuse Holder 10x38 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\DIN_Rail_Cartridge_Fuse_Holder_10x38\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\DIN_Rail_Cartridge_Fuse_Holder_10x38_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\DIN_Rail_Cartridge_Fuse_Holder_10x38\\06_Renders_and_Media\\04_Watermarked_Exports\\DIN_Rail_Cartridge_Fuse_Holder_10x38_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\DIN_Rail_Cartridge_Fuse_Holder_10x38\\06_Renders_and_Media"
    },
    {
      "name": "GreatControl_2CH_Analog_to_RS485_Module",
      "title": "GreatControl 2CH Analog to RS485 Module - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "GreatControl 2CH Analog to RS485 Module - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\GreatControl_2CH_Analog_to_RS485_Module\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\GreatControl_2CH_Analog_to_RS485_Module_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\GreatControl_2CH_Analog_to_RS485_Module\\06_Renders_and_Media\\04_Watermarked_Exports\\GreatControl_2CH_Analog_to_RS485_Module_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\GreatControl_2CH_Analog_to_RS485_Module\\06_Renders_and_Media"
    },
    {
      "name": "GreatControl_8CH_Analog_to_RS485_Module",
      "title": "GreatControl 8CH Analog to RS485 Module - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "GreatControl 8CH Analog to RS485 Module - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\GreatControl_8CH_Analog_to_RS485_Module\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\GreatControl_8CH_Analog_to_RS485_Module_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\GreatControl_8CH_Analog_to_RS485_Module\\06_Renders_and_Media\\04_Watermarked_Exports\\GreatControl_8CH_Analog_to_RS485_Module_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\GreatControl_8CH_Analog_to_RS485_Module\\06_Renders_and_Media"
    },
    {
      "name": "Industrial_3_Tier_LED_Tower_Light",
      "title": "Industrial 3 Tier LED Tower Light - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Industrial 3 Tier LED Tower Light - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Industrial_3_Tier_LED_Tower_Light\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Industrial_3_Tier_LED_Tower_Light_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Industrial_3_Tier_LED_Tower_Light\\06_Renders_and_Media\\04_Watermarked_Exports\\Industrial_3_Tier_LED_Tower_Light_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Industrial_3_Tier_LED_Tower_Light\\06_Renders_and_Media"
    },
    {
      "name": "Industrial_DIN_Rail_Power_Supply_24V",
      "title": "Industrial DIN Rail Power Supply 24V - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Industrial DIN Rail Power Supply 24V - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Industrial_DIN_Rail_Power_Supply_24V\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Industrial_DIN_Rail_Power_Supply_24V_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Industrial_DIN_Rail_Power_Supply_24V\\06_Renders_and_Media\\04_Watermarked_Exports\\Industrial_DIN_Rail_Power_Supply_24V_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Industrial_DIN_Rail_Power_Supply_24V\\06_Renders_and_Media"
    },
    {
      "name": "Industrial_Electromagnetic_Relay_Base",
      "title": "Industrial Electromagnetic Relay Base - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Industrial Electromagnetic Relay Base - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Industrial_Electromagnetic_Relay_Base\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Industrial_Electromagnetic_Relay_Base_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Industrial_Electromagnetic_Relay_Base\\06_Renders_and_Media\\04_Watermarked_Exports\\Industrial_Electromagnetic_Relay_Base_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Industrial_Electromagnetic_Relay_Base\\06_Renders_and_Media"
    },
    {
      "name": "Industrial_Exhaust_Blower_Fan",
      "title": "Industrial Exhaust Blower Fan - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Industrial Exhaust Blower Fan - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Industrial_Exhaust_Blower_Fan\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Industrial_Exhaust_Blower_Fan_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Industrial_Exhaust_Blower_Fan\\06_Renders_and_Media\\04_Watermarked_Exports\\Industrial_Exhaust_Blower_Fan_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Industrial_Exhaust_Blower_Fan\\06_Renders_and_Media"
    },
    {
      "name": "Industrial_PLC_Controller_8DI_8DO_RS485",
      "title": "Industrial PLC Controller 8DI 8DO RS485 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Industrial PLC Controller 8DI 8DO RS485 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Industrial_PLC_Controller_8DI_8DO_RS485\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Industrial_PLC_Controller_8DI_8DO_RS485_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Industrial_PLC_Controller_8DI_8DO_RS485\\06_Renders_and_Media\\04_Watermarked_Exports\\Industrial_PLC_Controller_8DI_8DO_RS485_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Industrial_PLC_Controller_8DI_8DO_RS485\\06_Renders_and_Media"
    },
    {
      "name": "Industrial_PLC_HMI_Control_Panel_IoT",
      "title": "Industrial PLC HMI Control Panel IoT - Industrial CAD 3D Model",
      "personal_price": 69.99,
      "professional_price": 99.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Industrial PLC HMI Control Panel IoT - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Industrial_PLC_HMI_Control_Panel_IoT\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Industrial_PLC_HMI_Control_Panel_IoT_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Industrial_PLC_HMI_Control_Panel_IoT\\06_Renders_and_Media\\04_Watermarked_Exports\\Industrial_PLC_HMI_Control_Panel_IoT_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Industrial_PLC_HMI_Control_Panel_IoT\\06_Renders_and_Media"
    },
    {
      "name": "Kinseal_7_Inch_Industrial_HMI_Panel",
      "title": "Kinseal 7 Inch Industrial HMI Panel - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Kinseal 7 Inch Industrial HMI Panel - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Kinseal_7_Inch_Industrial_HMI_Panel\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Kinseal_7_Inch_Industrial_HMI_Panel_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Kinseal_7_Inch_Industrial_HMI_Panel\\06_Renders_and_Media\\04_Watermarked_Exports\\Kinseal_7_Inch_Industrial_HMI_Panel_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Kinseal_7_Inch_Industrial_HMI_Panel\\06_Renders_and_Media"
    },
    {
      "name": "PM2_5_Dust_Particle_Sensor_RS485",
      "title": "PM2 5 Dust Particle Sensor RS485 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "PM2 5 Dust Particle Sensor RS485 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\PM2_5_Dust_Particle_Sensor_RS485\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\PM2_5_Dust_Particle_Sensor_RS485_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\PM2_5_Dust_Particle_Sensor_RS485\\06_Renders_and_Media\\04_Watermarked_Exports\\PM2_5_Dust_Particle_Sensor_RS485_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\PM2_5_Dust_Particle_Sensor_RS485\\06_Renders_and_Media"
    },
    {
      "name": "Panel_Exhaust_Cooling_Fan",
      "title": "Panel Exhaust Cooling Fan - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Panel Exhaust Cooling Fan - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Panel_Exhaust_Cooling_Fan\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Panel_Exhaust_Cooling_Fan_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Panel_Exhaust_Cooling_Fan\\06_Renders_and_Media\\04_Watermarked_Exports\\Panel_Exhaust_Cooling_Fan_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Panel_Exhaust_Cooling_Fan\\06_Renders_and_Media"
    },
    {
      "name": "Panel_Pilot_Indicator_Light_Green",
      "title": "Panel Pilot Indicator Light Green - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Panel Pilot Indicator Light Green - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Panel_Pilot_Indicator_Light_Green\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Panel_Pilot_Indicator_Light_Green_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Panel_Pilot_Indicator_Light_Green\\06_Renders_and_Media\\04_Watermarked_Exports\\Panel_Pilot_Indicator_Light_Green_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Panel_Pilot_Indicator_Light_Green\\06_Renders_and_Media"
    },
    {
      "name": "Panel_Pilot_Indicator_Light_Red",
      "title": "Panel Pilot Indicator Light Red - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Panel Pilot Indicator Light Red - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Panel_Pilot_Indicator_Light_Red\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Panel_Pilot_Indicator_Light_Red_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Panel_Pilot_Indicator_Light_Red\\06_Renders_and_Media\\04_Watermarked_Exports\\Panel_Pilot_Indicator_Light_Red_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Panel_Pilot_Indicator_Light_Red\\06_Renders_and_Media"
    },
    {
      "name": "Panel_Pilot_Indicator_Light_Yellow",
      "title": "Panel Pilot Indicator Light Yellow - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Panel Pilot Indicator Light Yellow - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Panel_Pilot_Indicator_Light_Yellow\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Panel_Pilot_Indicator_Light_Yellow_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Panel_Pilot_Indicator_Light_Yellow\\06_Renders_and_Media\\04_Watermarked_Exports\\Panel_Pilot_Indicator_Light_Yellow_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Panel_Pilot_Indicator_Light_Yellow\\06_Renders_and_Media"
    },
    {
      "name": "Rotary_Selector_Switch_3_Position",
      "title": "Rotary Selector Switch 3 Position - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Rotary Selector Switch 3 Position - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Rotary_Selector_Switch_3_Position\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Rotary_Selector_Switch_3_Position_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Rotary_Selector_Switch_3_Position\\06_Renders_and_Media\\04_Watermarked_Exports\\Rotary_Selector_Switch_3_Position_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Rotary_Selector_Switch_3_Position\\06_Renders_and_Media"
    },
    {
      "name": "Single_Phase_RCBO_Circuit_Breaker",
      "title": "Single Phase RCBO Circuit Breaker - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Single Phase RCBO Circuit Breaker - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Single_Phase_RCBO_Circuit_Breaker\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Single_Phase_RCBO_Circuit_Breaker_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Single_Phase_RCBO_Circuit_Breaker\\06_Renders_and_Media\\04_Watermarked_Exports\\Single_Phase_RCBO_Circuit_Breaker_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Single_Phase_RCBO_Circuit_Breaker\\06_Renders_and_Media"
    },
    {
      "name": "Slotted_Aluminum_DIN_Rail_35mm_160L",
      "title": "Slotted Aluminum DIN Rail 35mm 160L - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Slotted Aluminum DIN Rail 35mm 160L - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Slotted_Aluminum_DIN_Rail_35mm_160L\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Slotted_Aluminum_DIN_Rail_35mm_160L_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Slotted_Aluminum_DIN_Rail_35mm_160L\\06_Renders_and_Media\\04_Watermarked_Exports\\Slotted_Aluminum_DIN_Rail_35mm_160L_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Slotted_Aluminum_DIN_Rail_35mm_160L\\06_Renders_and_Media"
    },
    {
      "name": "Tokin_Industrial_EMI_Noise_Filter",
      "title": "Tokin Industrial EMI Noise Filter - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Tokin Industrial EMI Noise Filter - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Tokin_Industrial_EMI_Noise_Filter\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Tokin_Industrial_EMI_Noise_Filter_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Tokin_Industrial_EMI_Noise_Filter\\06_Renders_and_Media\\04_Watermarked_Exports\\Tokin_Industrial_EMI_Noise_Filter_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Tokin_Industrial_EMI_Noise_Filter\\06_Renders_and_Media"
    },
    {
      "name": "Waterproof_Plastic_Enclosure_300x200x160",
      "title": "Waterproof Plastic Enclosure 300x200x160 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Waterproof Plastic Enclosure 300x200x160 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Waterproof_Plastic_Enclosure_300x200x160\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Waterproof_Plastic_Enclosure_300x200x160_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Waterproof_Plastic_Enclosure_300x200x160\\06_Renders_and_Media\\04_Watermarked_Exports\\Waterproof_Plastic_Enclosure_300x200x160_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Waterproof_Plastic_Enclosure_300x200x160\\06_Renders_and_Media"
    },
    {
      "name": "Wire_Mesh_Cable_Tray_133x50_SUS304",
      "title": "Wire Mesh Cable Tray 133x50 SUS304 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Wire Mesh Cable Tray 133x50 SUS304 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Wire_Mesh_Cable_Tray_133x50_SUS304\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Wire_Mesh_Cable_Tray_133x50_SUS304_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Wire_Mesh_Cable_Tray_133x50_SUS304\\06_Renders_and_Media\\04_Watermarked_Exports\\Wire_Mesh_Cable_Tray_133x50_SUS304_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Wire_Mesh_Cable_Tray_133x50_SUS304\\06_Renders_and_Media"
    },
    {
      "name": "Wire_Mesh_Cable_Tray_233x50_SUS304",
      "title": "Wire Mesh Cable Tray 233x50 SUS304 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Wire Mesh Cable Tray 233x50 SUS304 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Wire_Mesh_Cable_Tray_233x50_SUS304\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Wire_Mesh_Cable_Tray_233x50_SUS304_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Wire_Mesh_Cable_Tray_233x50_SUS304\\06_Renders_and_Media\\04_Watermarked_Exports\\Wire_Mesh_Cable_Tray_233x50_SUS304_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Wire_Mesh_Cable_Tray_233x50_SUS304\\06_Renders_and_Media"
    },
    {
      "name": "Wire_Mesh_Cable_Tray_50x50_SUS304",
      "title": "Wire Mesh Cable Tray 50x50 SUS304 - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Wire Mesh Cable Tray 50x50 SUS304 - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Wire_Mesh_Cable_Tray_50x50_SUS304\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Wire_Mesh_Cable_Tray_50x50_SUS304_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Wire_Mesh_Cable_Tray_50x50_SUS304\\06_Renders_and_Media\\04_Watermarked_Exports\\Wire_Mesh_Cable_Tray_50x50_SUS304_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\09_Electrical_Control_and_IoT\\Wire_Mesh_Cable_Tray_50x50_SUS304\\06_Renders_and_Media"
    }
  ],
  "10_Skid_Structure_and_Mechanical": [
    {
      "name": "Industrial_Caged_Safety_Ladder_3580H",
      "title": "Industrial Caged Safety Ladder 3580H - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Industrial Caged Safety Ladder 3580H - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\10_Skid_Structure_and_Mechanical\\Industrial_Caged_Safety_Ladder_3580H\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Industrial_Caged_Safety_Ladder_3580H_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\10_Skid_Structure_and_Mechanical\\Industrial_Caged_Safety_Ladder_3580H\\06_Renders_and_Media\\04_Watermarked_Exports\\Industrial_Caged_Safety_Ladder_3580H_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\10_Skid_Structure_and_Mechanical\\Industrial_Caged_Safety_Ladder_3580H\\06_Renders_and_Media"
    },
    {
      "name": "Swivel_Caster_Wheel_With_Brake",
      "title": "Swivel Caster Wheel With Brake - Industrial CAD 3D Model",
      "personal_price": 49.99,
      "professional_price": 74.99,
      "category": "Architecture > Industrial Equipment",
      "tags": [
        "filter",
        "vessel",
        "filtration",
        "treatment",
        "purification",
        "system",
        "water",
        "tank",
        "skid",
        "industrial",
        "pump",
        "valve",
        "machinery",
        "equipment",
        "piping",
        "mechanical",
        "stainless",
        "desalination",
        "clarifier",
        "realistic"
      ],
      "description": "Swivel Caster Wheel With Brake - Professional Industrial 3D CAD Model\nHigh-precision, production-grade 3D model designed specifically for Unreal Engine, Blender, Unity, CAD Engineering, EPC Simulation, Digital Twins, and Architecture Visualization.\n\nKey Features & Technical Specifications:\n- True Real-World Scale (1:1 Meters): Perfectly aligned with origin coordinate (0,0,0) and Y-Up / Z-Up compatibility.\n- Universal Multi-CAD & DCC Support: Native compatibility with all leading 3D software and game engines.\n- Clean Topology & Clean Meshing: Optimized geometry with clear normals, zero flipped faces, and separated functional components.\n- Engineering Accuracy: Modeled according to industrial DIN / ISO / ANSI standards for industrial water treatment and mechanical engineering plants.\n\nIncluded Formats in Package:\n1. FBX (Unreal Engine 5.x, Unity, 3ds Max, Maya ready)\n2. OBJ + MTL (Universal 3D exchange)\n3. STEP (.stp / .step) (Universal Solid CAD geometry for SolidWorks, Inventor, Fusion 360, Rhino)\n4. GLTF / GLB (Web 3D, AR/VR, Blender)\n5. SAT (.sat) (ACIS standard geometry)\n6. 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG)\n\nIdeal Use Cases:\n- Industrial Plant Design & Simulation (EPC, BIM, Architecture)\n- Game Development & Real-time Visualization (Unreal Engine / Unity)\n- VR/AR Training & Digital Twin Systems\n- High-End Cinematic Rendering and Marketing Media\n\nCreated by WaterTreatment3D Engineering Studio.",
      "zip_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\10_Skid_Structure_and_Mechanical\\Swivel_Caster_Wheel_With_Brake\\06_Renders_and_Media\\01_Marketplace_Upload_Package\\Swivel_Caster_Wheel_With_Brake_Universal_CAD.zip",
      "thumb_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\10_Skid_Structure_and_Mechanical\\Swivel_Caster_Wheel_With_Brake\\06_Renders_and_Media\\04_Watermarked_Exports\\Swivel_Caster_Wheel_With_Brake_01_Hero3D_Iso_TopRight.png",
      "folder_path": "D:\\INVENTOR_DATA\\05_STANDARD_COMPONENTS\\10_Skid_Structure_and_Mechanical\\Swivel_Caster_Wheel_With_Brake\\06_Renders_and_Media"
    }
  ]
};

    // =====================================================================
    // WT3D CORE UTILS — dùng chung cho toàn bộ script, thay cho các đoạn
    // querySelectorAll lặp đi lặp lại + sleep() cố định ở bản cũ.
    // =====================================================================

    const WT = (() => {
        const OWN_ID = 'wt3d';

        // Độ trễ ngẫu nhiên mô phỏng phản xạ con người (Human Jitter)
        function randomDelay(min = 120, max = 350) {
            const ms = Math.floor(Math.random() * (max - min + 1)) + min;
            return new Promise((r) => setTimeout(r, ms));
        }

        const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

        function isOwn(el) {
            return !el ? false : !!(el.id?.includes(OWN_ID) || el.closest?.(`#wt3d-fab-floating-panel`));
        }

        function isVisible(el) {
            if (!el) return false;
            const style = window.getComputedStyle(el);
            return style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0' && (el.offsetWidth > 0 || el.offsetHeight > 0);
        }

        async function waitFor(fn, { timeout = 3500, interval = 70 } = {}) {
            const start = Date.now();
            while (Date.now() - start < timeout) {
                let result;
                try { result = fn(); } catch (_) { result = null; }
                if (result) return result;
                await sleep(interval);
            }
            return null;
        }

        // Mô phỏng Click chuột người thật 100% với tọa độ ngẫu nhiên & chuỗi sự kiện tự nhiên
        async function humanClick(el) {
            if (!el) return false;
            try {
                // 1. Cuộn mượt đến phần tử như người dùng nhìn thấy
                el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                await randomDelay(80, 180);

                const rect = el.getBoundingClientRect();
                // Random vị trí bấm quanh tâm phần tử (sai số ±4px)
                const offsetX = (rect.width / 2) + (Math.random() * 8 - 4);
                const offsetY = (rect.height / 2) + (Math.random() * 8 - 4);
                const clientX = Math.round(rect.left + offsetX);
                const clientY = Math.round(rect.top + offsetY);

                const eventInit = {
                    bubbles: true,
                    cancelable: true,
                    composed: true,
                    view: window,
                    clientX: clientX,
                    clientY: clientY,
                    screenX: clientX + window.screenX,
                    screenY: clientY + window.screenY,
                    button: 0,
                    buttons: 1
                };

                // 2. Di chuột vào phần tử
                el.dispatchEvent(new MouseEvent('mouseover', eventInit));
                el.dispatchEvent(new MouseEvent('mouseenter', eventInit));
                el.dispatchEvent(new MouseEvent('mousemove', eventInit));
                await randomDelay(30, 70);

                // 3. Nhấn chuột xuống (pointerdown -> mousedown)
                if (typeof PointerEvent !== 'undefined') {
                    el.dispatchEvent(new PointerEvent('pointerdown', { ...eventInit, pointerType: 'mouse', isPrimary: true }));
                }
                el.dispatchEvent(new MouseEvent('mousedown', eventInit));
                el.focus?.();

                // 4. Thời gian giữ phím chuột (Human click duration: 60ms - 130ms)
                await randomDelay(60, 130);

                // 5. Thả chuột ra và kích hoạt click
                if (typeof PointerEvent !== 'undefined') {
                    el.dispatchEvent(new PointerEvent('pointerup', { ...eventInit, pointerType: 'mouse', isPrimary: true }));
                }
                el.dispatchEvent(new MouseEvent('mouseup', { ...eventInit, buttons: 0 }));
                el.dispatchEvent(new MouseEvent('click', { ...eventInit, buttons: 0 }));

                return true;
            } catch (err) {
                console.warn('[WT3D] Human click fallback:', err);
                el.click();
                return true;
            }
        }

        // Set giá trị input an toàn & tự nhiên
        function setNativeValue(el, value) {
            if (!el) return false;
            const proto =
                el.tagName === 'TEXTAREA' ? window.HTMLTextAreaElement.prototype :
                el.tagName === 'SELECT' ? window.HTMLSelectElement.prototype :
                window.HTMLInputElement.prototype;
            try {
                const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;
                if (setter) setter.call(el, value); else el.value = value;
                el.dispatchEvent(new Event('input', { bubbles: true, cancelable: true }));
                el.dispatchEvent(new Event('change', { bubbles: true, cancelable: true }));
                return true;
            } catch (e) {
                console.error('[WT3D] setNativeValue error:', e);
                return false;
            }
        }

        async function setReactInputValue(el, value) {
            if (!el) return false;
            el.focus();
            await randomDelay(40, 90);
            const ok = setNativeValue(el, value);
            await randomDelay(40, 90);
            el.dispatchEvent(new Event('blur', { bubbles: true, cancelable: true }));
            return ok;
        }

        async function setContentEditable(el, value) {
            if (!el) return false;
            el.focus();
            await randomDelay(50, 120);
            document.execCommand('selectAll', false, null);
            document.execCommand('insertText', false, value);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            await randomDelay(50, 100);
            el.dispatchEvent(new FocusEvent('blur', { bubbles: true }));
            return true;
        }

        function findAllByText(substring, selector = '*') {
            const nodes = Array.from(document.querySelectorAll(selector));
            return nodes.filter((el) => !isOwn(el) && (el.textContent || '').includes(substring));
        }

        async function clickByText(substring) {
            const xpath = `//*[contains(text(), '${substring.replace(/'/g, "\\'")}')]`;
            const result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
            for (let i = 0; i < result.snapshotLength; i++) {
                const node = result.snapshotItem(i);
                if (!isVisible(node) || isOwn(node)) continue;
                const target =
                    node.closest('label') ||
                    node.closest('button') ||
                    node.closest('div[role="radio"]') ||
                    node.closest('div[role="checkbox"]') ||
                    node;
                await humanClick(target);
                return true;
            }
            return false;
        }

        function findNearLabel(labelEl, innerSelector, depth = 6) {
            let container = labelEl?.parentElement;
            for (let i = 0; i < depth && container; i++) {
                const found = container.querySelector(innerSelector);
                if (found && !isOwn(found)) return found;
                container = container.parentElement;
            }
            return null;
        }

        function findShortLabel(texts, maxLen = 100) {
            const candidates = document.querySelectorAll('label, div, span, p, h3, h4, h5');
            const wanted = Array.isArray(texts) ? texts : [texts];
            for (const el of candidates) {
                const t = (el.textContent || '').trim();
                if (t.length > maxLen) continue;
                if (wanted.some((w) => t === w || t.includes(w))) return el;
            }
            return null;
        }

        async function ensureGenerativeAICheckboxTicked() {
            const label = 'Do not allow this product to be used by Generative AI Programs';
            const checkboxes = Array.from(
                document.querySelectorAll('input[type="checkbox"], button[role="checkbox"], [role="checkbox"]')
            );
            for (const cb of checkboxes) {
                const parentText = (cb.closest('label') || cb.closest('div') || cb.parentElement)?.textContent || '';
                if (!parentText.includes(label)) continue;
                const isChecked = cb.checked === true || cb.getAttribute('aria-checked') === 'true' || cb.classList.contains('checked');
                if (!isChecked) await humanClick(cb);
                return true;
            }
            const node = findAllByText(label)[0];
            if (node) {
                const container = node.closest('label') || node.closest('div') || node;
                const cb = container.querySelector('input[type="checkbox"], button[role="checkbox"], [role="checkbox"]');
                if (cb) {
                    if (!cb.checked && cb.getAttribute('aria-checked') !== 'true') await humanClick(cb);
                } else {
                    await humanClick(container);
                }
                return true;
            }
            return false;
        }

        return {
            sleep, randomDelay, humanClick, waitFor, setNativeValue, setReactInputValue, setContentEditable,
            findAllByText, clickByText, findNearLabel, findShortLabel,
            ensureGenerativeAICheckboxTicked, isOwn, isVisible,
        };
    })();

    const setReactInputValue = WT.setReactInputValue;
    const clickElementByText = WT.clickByText;
    const ensureGenerativeAICheckboxTicked = WT.ensureGenerativeAICheckboxTicked;
    const sleep = WT.sleep;
    const randomDelay = WT.randomDelay;
    const humanClick = WT.humanClick;

    // =====================================================================
    // =====================================================================
    // 1. CHỌN GIÁ (Personal / Professional) — Tương thích 100% Radix UI & React 18
    // =====================================================================
    async function selectFabDropdownPrice(typeLabel, priceValue) {
        const formatted = priceValue.toFixed(2);
        console.log(`[WT3D] >>> Chọn ${typeLabel}: $${formatted}`);

        try {
            let trigger = null;

            // 1. Tìm label chứa "Personal price" hoặc "Professional price"
            const labels = Array.from(document.querySelectorAll('label, div, span, h4, h5, p'))
                .filter(el => !WT.isOwn(el) && (el.textContent || '').toLowerCase().includes(typeLabel.toLowerCase()) && (el.textContent || '').trim().length < 60);

            labels.sort((a, b) => (a.textContent || '').trim().length - (b.textContent || '').trim().length);

            for (const lb of labels) {
                // Đi lên các cấp cha để tìm button dropdown trong cùng form-group
                let p = lb.parentElement;
                for (let i = 0; i < 5 && p; i++) {
                    const btn = p.querySelector('button, [role="combobox"], [role="button"], select, div[tabindex="0"]');
                    if (btn && !WT.isOwn(btn) && btn !== lb && !lb.contains(btn)) {
                        trigger = btn;
                        break;
                    }
                    p = p.parentElement;
                }
                if (trigger) break;
            }

            if (!trigger) {
                trigger = document.querySelector(`[aria-label*="${typeLabel}" i]`) ||
                          Array.from(document.querySelectorAll('button, [role="combobox"]')).find(b =>
                              !WT.isOwn(b) && (b.textContent || '').toLowerCase().includes(typeLabel.toLowerCase())
                          );
            }

            if (!trigger) {
                console.warn(`[WT3D] Không tìm thấy trigger cho ${typeLabel}`);
                return false;
            }

            if (trigger.tagName === 'SELECT') {
                WT.setNativeValue(trigger, formatted);
                return true;
            }

            // Click trực tiếp trigger để mở dropdown (không dùng synthetic pointerdown làm crash Radix)
            trigger.scrollIntoView({ behavior: 'smooth', block: 'center' });
            await WT.sleep(150);
            trigger.focus?.();
            trigger.click();

            await WT.sleep(400);

            // 2. Tìm option giá $XX.99 trên toàn bộ DOM (bao gồm cả Portal của React)
            let matchedOption = null;
            const startTime = Date.now();

            while (Date.now() - startTime < 3500) {
                const candidates = Array.from(document.querySelectorAll(
                    '[role="option"], [role="menuitem"], [data-radix-collection-item], li, button, div[class*="option"], div[class*="item"], div[tabindex="0"], div[tabindex="-1"], span'
                )).filter(el => !WT.isOwn(el) && WT.isVisible(el) && el !== trigger && !trigger.contains(el));

                // So khớp chính xác số tiền (vd: "49.99" hoặc "$49.99")
                matchedOption = candidates.find(el => {
                    const t = (el.textContent || '').trim();
                    return (t.includes(formatted) || t.includes(`$${formatted}`)) &&
                           !t.toLowerCase().includes('select') &&
                           !t.toLowerCase().includes('price');
                });

                if (matchedOption) break;
                await WT.sleep(100);
            }

            if (!matchedOption) {
                console.warn(`[WT3D] Không tìm thấy option giá $${formatted}`);
                return false;
            }

            matchedOption.scrollIntoView({ behavior: 'smooth', block: 'center' });
            await WT.sleep(100);
            matchedOption.click();
            console.log(`[WT3D] ✅ Đã chọn thành công ${typeLabel}: $${formatted}`);
            return true;
        } catch (e) {
            console.error(`[WT3D] Lỗi chọn ${typeLabel}:`, e);
            return false;
        }
    }

    // =====================================================================
    // 2. CHỌN CATEGORY — Tương thích 100% Radix UI & React 18
    // =====================================================================
    async function selectFabCategory(category) {
        if (!category) return false;
        console.log(`[WT3D] >>> Chọn Category: ${category}`);

        try {
            let catTrigger = null;
            const catLabels = Array.from(document.querySelectorAll('label, div, span, h4, h5, p'))
                .filter(el => !WT.isOwn(el) && ['category *', 'category'].includes((el.textContent || '').trim().toLowerCase()));

            for (const lb of catLabels) {
                let p = lb.parentElement;
                for (let i = 0; i < 5 && p; i++) {
                    const btn = p.querySelector('button, [role="combobox"], [role="button"], div[tabindex="0"]');
                    if (btn && !WT.isOwn(btn) && btn !== lb && !lb.contains(btn)) {
                        catTrigger = btn;
                        break;
                    }
                    p = p.parentElement;
                }
                if (catTrigger) break;
            }

            if (!catTrigger) {
                catTrigger = Array.from(document.querySelectorAll('button, div[tabindex="0"]')).find(el =>
                    !WT.isOwn(el) && el.querySelector('svg, [class*="arrow"], [class*="chevron"], [class*="caret"]') && (el.textContent || '').length < 80
                );
            }

            if (!catTrigger) {
                console.warn('[WT3D] Không tìm thấy Category trigger');
                return false;
            }

            catTrigger.scrollIntoView({ behavior: 'smooth', block: 'center' });
            await WT.sleep(150);
            catTrigger.focus?.();
            catTrigger.click();

            await WT.sleep(400);

            // Gõ tìm kiếm nếu có ô Search Input trong dropdown
            const searchInput = await WT.waitFor(() => {
                const inps = Array.from(document.querySelectorAll('input[type="text"], input:not([type])')).filter(inp =>
                    !WT.isOwn(inp) && WT.isVisible(inp) && (
                        (inp.placeholder || '').toLowerCase().includes('search') ||
                        (inp.placeholder || '').toLowerCase().includes('category') ||
                        inp.closest('[role="dialog"], [role="listbox"], [data-radix-popper-content-wrapper], div[class*="popup"], div[class*="menu"]')
                    )
                );
                return inps.length ? inps[0] : null;
            }, { timeout: 1500 });

            const targetTerm = category.split('>').pop().trim(); // "Industrial Equipment"
            if (searchInput) {
                searchInput.focus();
                WT.setNativeValue(searchInput, targetTerm);
                searchInput.dispatchEvent(new Event('input', { bubbles: true }));
                searchInput.dispatchEvent(new Event('change', { bubbles: true }));
                await WT.sleep(400);
            }

            // Quét các option danh mục
            const searchTerms = [
                targetTerm.toLowerCase(),
                ...category.split('>').map(s => s.trim().toLowerCase()).reverse(),
                'industrial'
            ];

            let matchedCat = null;
            const startTime = Date.now();

            while (Date.now() - startTime < 3500) {
                const options = Array.from(document.querySelectorAll(
                    '[role="option"], [role="menuitem"], [data-radix-collection-item], li, button, div[class*="option"], div[class*="item"], span'
                )).filter(el => !WT.isOwn(el) && WT.isVisible(el) && el !== catTrigger && !catTrigger.contains(el));

                for (const term of searchTerms) {
                    matchedCat = options.find(o => {
                        const t = (o.textContent || '').trim().toLowerCase();
                        return t.includes(term) && !t.includes('select category');
                    });
                    if (matchedCat) break;
                }

                if (matchedCat) break;
                await WT.sleep(100);
            }

            if (!matchedCat) {
                console.warn(`[WT3D] Không tìm thấy option khớp Category: ${category}`);
                return false;
            }

            matchedCat.scrollIntoView({ behavior: 'smooth', block: 'center' });
            await WT.sleep(100);
            matchedCat.click();
            console.log(`[WT3D] ✅ Đã chọn Category: ${matchedCat.textContent.trim()}`);
            return true;
        } catch (e) {
            console.error('[WT3D] Lỗi chọn Category:', e);
            return false;
        }
    }

    // =====================================================================
    // 3. ĐIỀN TITLE & DESCRIPTION
    // =====================================================================
    async function fillTitle(title) {
        const allInputs = Array.from(document.querySelectorAll('input[type="text"], input:not([type])'));
        const input = allInputs.find((inp) => {
            if (WT.isOwn(inp)) return false;
            const ph = (inp.placeholder || '').toLowerCase();
            const aria = (inp.getAttribute('aria-label') || '').toLowerCase();
            return ph.includes('title') || aria.includes('title') || inp.maxLength === 80 ||
                (inp.parentElement && inp.parentElement.textContent.includes('Title'));
        });
        if (!input) return false;
        return await WT.setReactInputValue(input, title);
    }

    async function fillDescription(description) {
        const descEl = document.querySelector('div[contenteditable="true"], div[role="textbox"], textarea');
        if (!descEl) return false;
        if (descEl.tagName === 'TEXTAREA') {
            return WT.setNativeValue(descEl, description);
        } else {
            return await WT.setContentEditable(descEl, description);
        }
    }

    // =====================================================================
    // 4. ĐIỀN TAGS — Tốc độ gõ phím & Enter tự nhiên
    // =====================================================================
    function findTagInput() {
        let tagInput = document.querySelector('input[placeholder*="Search a tag" i]') ||
                        document.querySelector('input[placeholder*="tag" i]');
        if (tagInput) return tagInput;

        const label = Array.from(document.querySelectorAll('label, div, span, h3, h4'))
            .find((lb) => ['Tags *', 'Tags'].includes((lb.textContent || '').trim()));
        return label ? WT.findNearLabel(label, 'input', 5) : null;
    }

    function countExistingTagChips() {
        return document.querySelectorAll(
            '[class*="tag"] button, [class*="chip"] button, [class*="badge"] button, button[aria-label*="Remove"], button[aria-label*="remove"]'
        ).length;
    }

    async function fillTags(tags) {
        if (!Array.isArray(tags) || !tags.length) return { done: false, added: 0 };
        const tagInput = findTagInput();
        if (!tagInput) {
            console.warn('[WT3D] Tag input not found!');
            return { done: false, added: 0 };
        }

        if (countExistingTagChips() >= tags.length) {
            console.log('[WT3D] Tags already filled — skipping.');
            return { done: true, added: tags.length, skipped: true };
        }

        navigator.clipboard.writeText(tags.join(', ')).catch(() => {});
        let added = 0;
        for (const t of tags) {
            try {
                tagInput.focus();
                WT.setNativeValue(tagInput, t);
                await randomDelay(80, 160);

                const eOpts = { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, charCode: 13, bubbles: true, cancelable: true };
                tagInput.dispatchEvent(new KeyboardEvent('keydown', eOpts));
                await randomDelay(20, 50);
                tagInput.dispatchEvent(new KeyboardEvent('keypress', eOpts));
                tagInput.dispatchEvent(new KeyboardEvent('keyup', eOpts));
                added++;
                console.log('[WT3D] Tag added:', t, `(${added}/${tags.length})`);
                await randomDelay(120, 220);
            } catch (err) {
                console.error('[WT3D] Error adding tag:', t, err);
            }
        }
        return { done: added === tags.length, added };
    }

    // =====================================================================
    // 5. FAQ — Điền & Click xác nhận từng câu
    // =====================================================================
    const WT3D_FAQS = [
        {
            q: 'What file formats are included in this package?',
            a: 'This package includes: FBX (Unreal Engine 5, Unity, 3ds Max, Maya), OBJ + MTL (Universal 3D exchange), STEP / STP (SolidWorks, Inventor, Fusion 360, Rhino), GLTF / GLB (Web 3D, AR/VR, Blender), SAT (ACIS standard geometry), and 2D Engineering Blueprint Sheets (DWG, Vector PDF, High-Res PNG). All formats are production-ready and tested.',
        },
        {
            q: 'Is this model built to real-world scale?',
            a: 'Yes. All models are built at true 1:1 real-world scale in meters, with the origin precisely at coordinate (0,0,0). They are compatible with both Y-Up and Z-Up coordinate systems for seamless import into any 3D software or game engine.',
        },
        {
            q: 'Can I use this model in Unreal Engine, Unity, or Blender?',
            a: 'Absolutely. The FBX format is fully optimized for Unreal Engine 5.x, Unity, 3ds Max, and Maya. The GLTF/GLB format works natively with Blender, Web 3D viewers, and AR/VR applications. Clean topology, correct normals, and separated components are guaranteed.',
        },
        {
            q: 'Can I modify or edit this 3D model after purchase?',
            a: 'Yes. The included STEP (.stp) format allows full solid-body editing in parametric CAD software such as SolidWorks, Autodesk Inventor, Fusion 360, and Rhino. The FBX and OBJ formats can also be freely edited in any 3D DCC software for visualization and game development purposes.',
        },
    ];

    async function fillFAQs() {
        const existingCount = Array.from(document.querySelectorAll('button')).filter((el) => (el.textContent || '').trim() === 'Edit').length;
        console.log('[WT3D] Existing FAQs:', existingCount, '/ needed:', WT3D_FAQS.length);

        if (existingCount >= WT3D_FAQS.length) {
            console.log('[WT3D] All FAQs already exist — skipping.');
            return { skipped: true, added: 0, total: 0 };
        }

        const faqsToAdd = WT3D_FAQS.slice(existingCount);
        let added = 0;
        for (const faq of faqsToAdd) {
            try {
                const openModal = document.querySelector('[role="dialog"], div[class*="modal"]');
                const addFaqBtn = Array.from(document.querySelectorAll('button')).find((el) => {
                    const t = (el.textContent || '').trim();
                    return (t === '+ Add FAQ' || t === 'Add FAQ' || t.includes('Add FAQ')) &&
                           !t.includes('Cancel') &&
                           !(openModal && openModal.contains(el));
                });

                if (!addFaqBtn) { console.warn('[WT3D] "+ Add FAQ" not found'); break; }
                await humanClick(addFaqBtn);
                await randomDelay(350, 600);

                // 1. Điền Question
                const qInput = await WT.waitFor(() =>
                    document.querySelector('input[placeholder*="question" i], input[placeholder*="Enter a question" i]')
                , { timeout: 2500 });

                if (qInput) {
                    qInput.focus();
                    await randomDelay(60, 120);
                    WT.setNativeValue(qInput, faq.q);
                    qInput.dispatchEvent(new Event('input', { bubbles: true }));
                    qInput.dispatchEvent(new Event('change', { bubbles: true }));
                    await randomDelay(50, 90);
                    qInput.dispatchEvent(new Event('blur', { bubbles: true }));
                }
                await randomDelay(200, 350);

                // 2. Điền Answer
                const modal = document.querySelector('[role="dialog"], [class*="modal"], [class*="dialog"]');
                const scope = modal || document;
                const aBox = scope.querySelector('[contenteditable="true"]') || scope.querySelector('div[role="textbox"]');
                if (aBox) {
                    aBox.focus();
                    await randomDelay(60, 120);
                    document.execCommand('selectAll', false, null);
                    document.execCommand('insertText', false, faq.a);
                    aBox.dispatchEvent(new Event('input', { bubbles: true }));
                    aBox.dispatchEvent(new Event('change', { bubbles: true }));
                    await randomDelay(50, 90);
                    aBox.dispatchEvent(new FocusEvent('blur', { bubbles: true }));
                } else {
                    const aTA = scope.querySelector('textarea');
                    if (aTA) {
                        aTA.focus();
                        await randomDelay(60, 120);
                        WT.setNativeValue(aTA, faq.a);
                        aTA.dispatchEvent(new Event('blur', { bubbles: true }));
                    }
                }
                await randomDelay(400, 700);

                // 3. Click nút "Add FAQ" bên trong modal
                const confirmBtn = await WT.waitFor(() => {
                    const allBtns = Array.from((modal || document).querySelectorAll('button')).filter((el) =>
                        (el.textContent || '').trim() === 'Add FAQ' && !el.disabled
                    );
                    return allBtns.length ? allBtns[allBtns.length - 1] : null;
                }, { timeout: 3000, interval: 100 });

                if (confirmBtn) {
                    await randomDelay(100, 220);
                    await humanClick(confirmBtn);
                    added++;
                    console.log('[WT3D] FAQ added:', faq.q.substring(0, 40) + '...');
                } else {
                    console.warn('[WT3D] Confirm "Add FAQ" button not enabled/found!');
                }
                await randomDelay(400, 700);
            } catch (err) {
                console.error('[WT3D] Error adding FAQ:', err);
            }
        }
        return { skipped: false, added, total: faqsToAdd.length };
    }

    // =====================================================================
    // 6. GIAO DIỆN PANEL (UI & DRAG & DROP)
    // =====================================================================
    // =====================================================================
    // 7. HÀM TỰ ĐỘNG KIỂM ĐỊNH THỰC TẾ TRÊN DOM SAU KHI ĐIỀN (POST-RUN AUDIT)
    // =====================================================================
    async function auditActualFormResult(model) {
        console.log('[WT3D] >>> 🔍 BẮT ĐẦU VÒNG TỰ ĐỘNG KIỂM ĐỊNH THỰC TẾ TRÊN FORM...');
        const auditResults = {
            title: false,
            desc: false,
            category: false,
            licenses: false,
            pricePersonal: false,
            priceProfessional: false,
            tags: false,
            faqs: false
        };

        await WT.sleep(400);

        // 1. Check Title
        const titleInp = Array.from(document.querySelectorAll('input[type="text"], input:not([type])')).find(inp =>
            !WT.isOwn(inp) && ((inp.placeholder || '').toLowerCase().includes('title') || inp.maxLength === 80 || (inp.value && inp.value.length > 5))
        );
        if (titleInp && titleInp.value && titleInp.value.trim().length > 5) {
            auditResults.title = true;
        }

        // 2. Check Description
        const descEl = document.querySelector('div[contenteditable="true"], div[role="textbox"], textarea');
        if (descEl) {
            const content = descEl.tagName === 'TEXTAREA' ? descEl.value : descEl.innerText || descEl.textContent;
            if (content && content.trim().length > 50) {
                auditResults.desc = true;
            }
        }

        // 3. Check Category
        const catBtn = Array.from(document.querySelectorAll('button, div[role="combobox"], div[tabindex="0"]')).find(el =>
            !WT.isOwn(el) && (el.textContent || '').toLowerCase().includes('industrial')
        );
        if (catBtn) auditResults.category = true;

        // 4. Check Licenses & AI checkboxes
        const aiLabel = 'Do not allow this product to be used by Generative AI Programs';
        const aiCb = Array.from(document.querySelectorAll('input[type="checkbox"], button[role="checkbox"], [role="checkbox"]')).find(cb => {
            const pText = (cb.closest('label') || cb.closest('div') || cb.parentElement)?.textContent || '';
            return pText.includes(aiLabel) && (cb.checked === true || cb.getAttribute('aria-checked') === 'true' || cb.classList.contains('checked'));
        });
        if (aiCb) auditResults.licenses = true;

        // 5. Check Prices
        const pFormatted = model.personal_price.toFixed(2);
        const proFormatted = model.professional_price.toFixed(2);
        const priceEls = Array.from(document.querySelectorAll('button, [role="combobox"], span, div')).filter(el => !WT.isOwn(el) && WT.isVisible(el));

        if (priceEls.some(el => (el.textContent || '').includes(pFormatted) || (el.textContent || '').includes(`$${pFormatted}`))) {
            auditResults.pricePersonal = true;
        }
        if (priceEls.some(el => (el.textContent || '').includes(proFormatted) || (el.textContent || '').includes(`$${proFormatted}`))) {
            auditResults.priceProfessional = true;
        }

        // 6. Check Tags (đếm chip)
        const tagCount = countExistingTagChips();
        if (tagCount >= 10) {
            auditResults.tags = true;
        }

        // 7. Check FAQs (đếm nút Edit của mỗi câu FAQ)
        const faqCount = Array.from(document.querySelectorAll('button')).filter(el => (el.textContent || '').trim() === 'Edit').length;
        if (faqCount >= 4) {
            auditResults.faqs = true;
        }

        const totalPassed = Object.values(auditResults).filter(Boolean).length;
        const totalItems = Object.keys(auditResults).length;

        console.log(`[WT3D] Kết quả kiểm định thực tế: ${totalPassed}/${totalItems} mục đạt chuẩn!`, auditResults);

        return {
            passed: totalPassed,
            total: totalItems,
            details: auditResults,
            tagCount,
            faqCount
        };
    }

    function createFloatingPanel() {
        if (document.getElementById('wt3d-fab-floating-panel')) return;

        const panel = document.createElement('div');
        panel.id = 'wt3d-fab-floating-panel';
        panel.style.cssText = `
            position: fixed;
            top: 15px;
            right: 20px;
            z-index: 999999;
            background: rgba(15, 23, 42, 0.98);
            backdrop-filter: blur(16px);
            border: 2px solid #0078f2;
            box-shadow: 0 12px 35px rgba(0, 120, 242, 0.45);
            border-radius: 14px;
            padding: 16px 20px;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            width: 450px;
            box-sizing: border-box;
        `;

        panel.innerHTML = `
            <div id="wt3d-drag-handle" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid #334155; padding-bottom: 8px; cursor: move; user-select: none;">
                <div style="font-weight: 800; color: #38bdf8; font-size: 14px; display: flex; align-items: center; gap: 6px;">
                    <span>⚡ WT3D FAB 1-CLICK COMPLETE HELPER</span>
                </div>
                <span id="wt3d-close-btn" style="cursor: pointer; color: #94a3b8; font-weight: bold; font-size: 18px;">✕</span>
            </div>

            <div style="margin-bottom: 10px;">
                <label style="font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; display: block; margin-bottom: 4px;">
                    📂 1. Chọn Thư Mục / Nhóm:
                </label>
                <select id="wt3d-folder-select" style="width: 100%; background: #1e293b; color: #34d399; border: 1px solid #475569; border-radius: 6px; padding: 8px 10px; font-size: 12px; font-weight: 700; outline: none; cursor: pointer;">
                </select>
            </div>

            <div style="margin-bottom: 12px;">
                <label style="font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; display: block; margin-bottom: 4px;">
                    🎯 2. Chọn Model Muốn Upload:
                </label>
                <select id="wt3d-model-select" style="width: 100%; background: #0f172a; color: #fff; border: 1px solid #0078f2; border-radius: 6px; padding: 8px 10px; font-size: 13px; font-weight: 600; outline: none; cursor: pointer;">
                </select>
            </div>

            <button id="wt3d-fill-btn" style="width: 100%; background: linear-gradient(135deg, #0078f2, #004d9b); color: #fff; border: none; border-radius: 8px; padding: 13px; font-size: 14px; font-weight: 800; cursor: pointer; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 4px 15px rgba(0, 120, 242, 0.5); transition: all 0.2s;">
                ⚡ 1-CLICK ĐIỀN & TICK HẾT 100% FORM
            </button>

            <div style="margin-top: 8px; display: flex; gap: 8px;">
                <button id="wt3d-copy-tags-btn" style="flex: 1; background: #334155; color: #38bdf8; border: 1px solid #475569; border-radius: 6px; padding: 6px; font-size: 11px; font-weight: 700; cursor: pointer;">
                    📋 Copy 15 Tags
                </button>
                <button id="wt3d-copy-price-btn" style="flex: 1; background: #334155; color: #34d399; border: 1px solid #475569; border-radius: 6px; padding: 6px; font-size: 11px; font-weight: 700; cursor: pointer;">
                    💵 Copy Giá Personal / Pro
                </button>
            </div>

            <div id="wt3d-info-box" style="margin-top: 12px; background: #0b1120; border: 1px solid #334155; border-radius: 8px; padding: 10px; font-size: 11px; color: #cbd5e1; line-height: 1.4;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="color: #94a3b8;">Personal / Pro Price:</span>
                    <b id="wt3d-price-tag" style="color: #10b981; font-size: 12px;">$49.99 / $74.99 USD</b>
                </div>
                <div style="margin-bottom: 4px;">
                    <span style="color: #94a3b8;">Đường dẫn thư mục Media (Click để copy):</span>
                    <input type="text" id="wt3d-folder-path" readonly style="width: 100%; background: #1e293b; color: #38bdf8; border: 1px solid #475569; padding: 5px 8px; border-radius: 4px; font-size: 10px; margin-top: 3px; font-family: monospace; cursor: pointer;" onclick="this.select(); document.execCommand('copy'); alert('Đã copy đường dẫn thư mục!');" title="Click để copy">
                </div>
            </div>

            <div id="wt3d-status-text" style="margin-top: 8px; font-size: 11px; color: #10b981; text-align: center; font-weight: 700; min-height: 15px;"></div>
        `;

        document.body.appendChild(panel);

        // Kéo thả di chuyển panel
        (function makeDraggable(el) {
            const header = el.querySelector('#wt3d-drag-handle') || el.firstElementChild;
            let startX, startY, startL, startT;
            header.addEventListener('mousedown', (e) => {
                if (e.target.id === 'wt3d-close-btn') return;
                startX = e.clientX; startY = e.clientY;
                const rect = el.getBoundingClientRect();
                startL = rect.left; startT = rect.top;
                el.style.right = 'auto';
                el.style.left  = startL + 'px';
                el.style.top   = startT + 'px';
                const onMove = (ev) => {
                    const nx = startL + ev.clientX - startX;
                    const ny = startT + ev.clientY - startY;
                    el.style.left = Math.max(0, Math.min(nx, window.innerWidth - el.offsetWidth)) + 'px';
                    el.style.top  = Math.max(0, Math.min(ny, window.innerHeight - el.offsetHeight)) + 'px';
                };
                const onUp = () => {
                    document.removeEventListener('mousemove', onMove);
                    document.removeEventListener('mouseup',   onUp);
                };
                document.addEventListener('mousemove', onMove);
                document.addEventListener('mouseup',   onUp);
                e.preventDefault();
            });
        })(panel);

        const folderSelect = document.getElementById('wt3d-folder-select');
        const modelSelect = document.getElementById('wt3d-model-select');
        const priceTag = document.getElementById('wt3d-price-tag');
        const folderPathInput = document.getElementById('wt3d-folder-path');
        const statusText = document.getElementById('wt3d-status-text');

        Object.keys(WT3D_DATABASE).forEach((cat) => {
            const opt = document.createElement('option');
            opt.value = cat;
            opt.textContent = `${cat} (${WT3D_DATABASE[cat].length} models)`;
            folderSelect.appendChild(opt);
        });

        function currentModel() {
            const catKey = folderSelect.value;
            const idx = parseInt(modelSelect.value, 10) || 0;
            return WT3D_DATABASE[catKey] ? WT3D_DATABASE[catKey][idx] : null;
        }

        function updateModelInfo() {
            const m = currentModel();
            if (m) {
                priceTag.textContent = `$${m.personal_price} (Personal) / $${m.professional_price} (Pro)`;
                folderPathInput.value = m.folder_path;
            }
        }

        function populateModels(catKey) {
            modelSelect.innerHTML = '';
            const list = WT3D_DATABASE[catKey] || [];
            list.forEach((m, idx) => {
                const opt = document.createElement('option');
                opt.value = idx;
                opt.textContent = `${idx + 1}. ${m.name} ($${m.personal_price} / $${m.professional_price})`;
                modelSelect.appendChild(opt);
            });
            updateModelInfo();
        }

        folderSelect.addEventListener('change', () => populateModels(folderSelect.value));
        modelSelect.addEventListener('change', updateModelInfo);
        populateModels(folderSelect.value);

        document.getElementById('wt3d-copy-tags-btn').addEventListener('click', () => {
            const m = currentModel();
            if (!m) return;
            const tagsStr = Array.isArray(m.tags) ? m.tags.join(', ') : m.tags;
            navigator.clipboard.writeText(tagsStr);
            alert('Đã copy 15 Tags vào Clipboard!');
        });

        document.getElementById('wt3d-copy-price-btn').addEventListener('click', () => {
            const m = currentModel();
            if (!m) return;
            navigator.clipboard.writeText(`Personal: $${m.personal_price} | Pro: $${m.professional_price}`);
            alert(`Đã copy: Personal $${m.personal_price} | Professional $${m.professional_price}`);
        });

        document.getElementById('wt3d-fill-btn').addEventListener('click', async () => {
            const m = currentModel();
            if (!m) return;

            const fillBtn = document.getElementById('wt3d-fill-btn');
            fillBtn.disabled = true;
            fillBtn.style.opacity = '0.7';
            fillBtn.style.cursor = 'not-allowed';

            const report = [];

            // =========================================================
            // BƯỚC 1/6: CHỌN CATEGORY (DANH MỤC)
            // =========================================================
            if (m.category) {
                statusText.textContent = `⏳ [1/6] Đang chọn Category: ${m.category.split('>').pop().trim()}...`;
                statusText.style.color = '#38bdf8';
                const ok = await selectFabCategory(m.category);
                if (ok) report.push('Category');
                await randomDelay(500, 800); // Nghỉ tự nhiên trước khi sang bước tiếp theo
            }

            // =========================================================
            // BƯỚC 2/6: ĐIỀN TITLE & DESCRIPTION (TIÊU ĐỀ & MÔ TẢ)
            // =========================================================
            statusText.textContent = '⏳ [2/6] Đang điền Title & Mô tả sản phẩm...';
            statusText.style.color = '#38bdf8';

            const titleOk = await fillTitle(m.title);
            if (titleOk) report.push('Title');
            await randomDelay(400, 700);

            const descOk = await fillDescription(m.description);
            if (descOk) report.push('Desc');
            await randomDelay(600, 900); // Nghỉ sau khi điền xong phần mô tả dài

            // =========================================================
            // BƯỚC 3/6: CÀI ĐẶT BẢN QUYỀN & CHỐNG AI (LICENSES & SETTINGS)
            // =========================================================
            statusText.textContent = '⏳ [3/6] Đang thiết lập Bản quyền Standard & Chống AI...';
            statusText.style.color = '#38bdf8';

            await clickElementByText('Standard License');
            await randomDelay(200, 350);

            await clickElementByText('No, this listing does not contain mature content');
            await randomDelay(200, 350);

            await ensureGenerativeAICheckboxTicked();
            await randomDelay(200, 350);

            await clickElementByText('No, it was not partly or fully created with generative AI');
            await randomDelay(200, 350);

            await clickElementByText('No, do not create a forum post');
            report.push('License & AI');
            await randomDelay(600, 900); // Nghỉ trước khi sang bước chọn giá

            // =========================================================
            // BƯỚC 4/6: THIẾT LẬP GIÁ BÁN (PERSONAL & PRO PRICE)
            // =========================================================
            statusText.textContent = `⏳ [4/6] Đang chọn Giá: Personal $${m.personal_price} & Pro $${m.professional_price}...`;
            statusText.style.color = '#38bdf8';

            const pOk = await selectFabDropdownPrice('Personal price', m.personal_price);
            if (pOk) report.push(`Personal: $${m.personal_price}`);
            await randomDelay(500, 800); // Nghỉ giữa 2 lần chọn giá

            const proOk = await selectFabDropdownPrice('Professional price', m.professional_price);
            if (proOk) report.push(`Pro: $${m.professional_price}`);
            await randomDelay(600, 900); // Nghỉ trước khi sang phần Tags

            // =========================================================
            // BƯỚC 5/6: ĐIỀN BỘ 15/20 TAGS TỪ KHÓA
            // =========================================================
            statusText.textContent = '⏳ [5/6] Đang gõ và gắn bộ Tags từ khóa...';
            statusText.style.color = '#38bdf8';

            const tagResult = await fillTags(m.tags);
            report.push(tagResult.skipped ? 'Tags: already done' : `Tags: ${tagResult.added}/${m.tags.length}`);
            await randomDelay(600, 900); // Nghỉ trước khi sang bước FAQ

            // =========================================================
            // BƯỚC 6/6: THÊM BỘ 4 CÂU HỎI THƯỜNG GẶP (FAQ)
            // =========================================================
            statusText.textContent = '⏳ [6/6] Đang kiểm tra & thêm bộ 4 FAQ...';
            statusText.style.color = '#38bdf8';

            const faqResult = await fillFAQs();
            if (!faqResult.skipped && faqResult.total > 0) report.push(`FAQ: ${faqResult.added}/${faqResult.total}`);
            else if (faqResult.skipped) report.push('FAQ: already done');

            // =========================================================
            // VÒNG 1: TỰ ĐỘNG KIỂM ĐỊNH THỰC TẾ (POST-RUN AUDIT)
            // =========================================================
            statusText.textContent = '🔍 [Vòng 1] Đang kiểm định lại toàn bộ form thực tế...';
            statusText.style.color = '#fbbf24';

            let audit = await auditActualFormResult(m);

            // =========================================================
            // VÒNG 2: CƠ CHẾ TỰ ĐỘNG VÁ LỖI & ĐIỀN BỔ SUNG (SELF-HEALING)
            // =========================================================
            if (audit.passed < 7) {
                const missingNames = [];
                if (!audit.details.category) missingNames.push('Category');
                if (!audit.details.title) missingNames.push('Title');
                if (!audit.details.desc) missingNames.push('Mô tả');
                if (!audit.details.licenses) missingNames.push('Bản quyền/AI');
                if (!audit.details.pricePersonal || !audit.details.priceProfessional) missingNames.push('Giá');
                if (!audit.details.tags) missingNames.push(`Tags (${audit.tagCount}/15)`);
                if (!audit.details.faqs) missingNames.push(`FAQ (${audit.faqCount}/4)`);

                console.log(`[WT3D] ⚠️ Phát hiện thiếu: ${missingNames.join(', ')} -> Bắt đầu tự động dặm bổ sung...`);
                statusText.textContent = `🔄 Phát hiện thiếu [${missingNames.join(', ')}] -> Đang tự động điền dặm bổ sung...`;
                statusText.style.color = '#f59e0b';
                await randomDelay(600, 1000);

                // Dặm Category nếu thiếu
                if (!audit.details.category && m.category) {
                    statusText.textContent = '🔄 Đang dặm lại Category...';
                    await selectFabCategory(m.category);
                    await randomDelay(400, 700);
                }

                // Dặm Title nếu thiếu
                if (!audit.details.title) {
                    statusText.textContent = '🔄 Đang dặm lại Title...';
                    await fillTitle(m.title);
                    await randomDelay(300, 500);
                }

                // Dặm Description nếu thiếu
                if (!audit.details.desc) {
                    statusText.textContent = '🔄 Đang dặm lại Mô tả...';
                    await fillDescription(m.description);
                    await randomDelay(400, 600);
                }

                // Dặm License/AI nếu thiếu
                if (!audit.details.licenses) {
                    statusText.textContent = '🔄 Đang dặm lại Bản quyền & AI...';
                    await clickElementByText('Standard License');
                    await randomDelay(150, 250);
                    await ensureGenerativeAICheckboxTicked();
                    await randomDelay(150, 250);
                    await clickElementByText('No, this listing does not contain mature content');
                    await randomDelay(150, 250);
                    await clickElementByText('No, it was not partly or fully created with generative AI');
                    await randomDelay(300, 500);
                }

                // Dặm Giá nếu thiếu
                if (!audit.details.pricePersonal) {
                    statusText.textContent = `🔄 Đang dặm lại Giá Personal $${m.personal_price}...`;
                    await selectFabDropdownPrice('Personal price', m.personal_price);
                    await randomDelay(350, 600);
                }
                if (!audit.details.priceProfessional) {
                    statusText.textContent = `🔄 Đang dặm lại Giá Pro $${m.professional_price}...`;
                    await selectFabDropdownPrice('Professional price', m.professional_price);
                    await randomDelay(350, 600);
                }

                // Dặm Tags nếu thiếu
                if (!audit.details.tags) {
                    statusText.textContent = '🔄 Đang dặm bổ sung Tags còn thiếu...';
                    await fillTags(m.tags);
                    await randomDelay(400, 600);
                }

                // Dặm FAQ nếu thiếu
                if (!audit.details.faqs) {
                    statusText.textContent = '🔄 Đang dặm bổ sung FAQ còn thiếu...';
                    await fillFAQs();
                    await randomDelay(500, 800);
                }

                // Kiểm định lần 2 sau khi đã tự động dặm bổ sung
                statusText.textContent = '🔍 [Vòng 2] Đang thẩm định lại sau khi dặm...';
                audit = await auditActualFormResult(m);
            }

            // =========================================================
            // KẾT LUẬN BÁO CÁO CUỐI CÙNG
            // =========================================================
            if (audit.passed >= 6) {
                statusText.textContent = `✅ HOÀN TẤT & ĐÃ TỰ ĐỘNG VÁ ĐỦ (${audit.passed}/${audit.total} mục): ${m.name}! (${audit.tagCount} Tags, ${audit.faqCount} FAQ)`;
                statusText.style.color = '#10b981';
            } else {
                const stillMissing = [];
                if (!audit.details.category) stillMissing.push('Category');
                if (!audit.details.title) stillMissing.push('Title');
                if (!audit.details.desc) stillMissing.push('Desc');
                if (!audit.details.licenses) stillMissing.push('License');
                if (!audit.details.pricePersonal || !audit.details.priceProfessional) stillMissing.push('Price');
                if (!audit.details.tags) stillMissing.push(`Tags (${audit.tagCount}/15)`);
                if (!audit.details.faqs) stillMissing.push(`FAQ (${audit.faqCount}/4)`);

                statusText.textContent = `⚠️ ĐÃ ĐIỀN (${audit.passed}/${audit.total} mục). Vui lòng xem lại: ${stillMissing.join(', ')}`;
                statusText.style.color = '#f59e0b';
            }
            fillBtn.disabled = false;
            fillBtn.style.opacity = '1';
            fillBtn.style.cursor = 'pointer';

            const catKey = folderSelect.value;
            const idx = parseInt(modelSelect.value, 10) || 0;
            if (idx + 1 < WT3D_DATABASE[catKey].length) {
                modelSelect.value = idx + 1;
                updateModelInfo();
            }
        });
        document.getElementById('wt3d-close-btn').addEventListener('click', () => {
            panel.style.display = 'none';
        });
    }

    const observer = new MutationObserver(() => {
        if (window.location.href.includes('/portal/listings')) {
            createFloatingPanel();
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });

    window.addEventListener('load', () => {
        setTimeout(createFloatingPanel, 1500);
    });
})();
