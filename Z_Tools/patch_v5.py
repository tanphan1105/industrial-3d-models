import sys
import re

file_path = r'd:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Structure Definitions and Checklists
struct_def = """
Public Structure ModelProfile
    Public Name As String
    Public MaxAngularSpeed As Double
    Public CameraRadiusFactor As Double
    Public MinZoomRatio As Double
    Public AllowTopFlip As Boolean
    Public AllowVertigo As Boolean
    Public AllowSpeedRamp As Boolean
    Public AllowIBLSweep As Boolean
    Public AllowMacro As Boolean
    Public AllowDeepZoom As Boolean
    Public AllowDynamicSection As Boolean
End Structure
"""

content = re.sub(
    r'Imports System\.Windows\.Forms\s*Sub Main\(\)',
    f'Imports System.Windows.Forms\n{struct_def}\nSub Main()\n'
    f'    \' [V5.0] GLOBAL CHECKLIST FLAGS\n'
    f'    Dim chk_ProfileDetected As Boolean = False\n'
    f'    Dim chk_ShotBlocked As Boolean = False\n'
    f'    Dim chk_ParamScaled As Boolean = False\n'
    f'    Dim chk_IBLAllowed As Boolean = False\n'
    f'    Dim blockedShotCount As Integer = 0\n'
    f'    Dim EngineHealthScore As Integer = 100\n'
    f'    Dim logReport As New System.Text.StringBuilder()\n',
    content
)

# 2. SmartClassifyAI Call Update
content = re.sub(
    r'Dim shapeClass As String = "".*?Dim funcClass As String = "".*?Dim vWeight As String = "".*?SmartClassifyAI\(oDoc, shapeClass, funcClass, vWeight\)',
    'Dim activeProfile As ModelProfile = SmartClassifyAI(oDoc)\n'
    '    If activeProfile.Name <> "SafeProfile" Then\n'
    '        chk_ProfileDetected = True\n'
    '    Else\n'
    '        EngineHealthScore -= 30\n'
    '    End If\n'
    '    Dim vWeight As String = If(activeProfile.Name = "Dense_Piping", "Heavy", "Light")',
    content, flags=re.DOTALL
)

content = re.sub(
    r'ThisApplication\.StatusBarText = "\[MAXSKILLS 4\.2( AI)?\] Shape: " & shapeClass.*?vWeight',
    'ThisApplication.StatusBarText = "[MAXSKILLS V5.0] Profile: " & activeProfile.Name\n'
    '    logReport.AppendLine("=== MAXSKILLS V5.0 REPORT ===")\n'
    '    logReport.AppendLine("ProfileDetected: " & activeProfile.Name)',
    content
)

content = content.replace(
    'Dim cameraPresets As List(Of String) = SelectCinematicCameraAI(shapeClass, funcClass, vWeight, commercialIntent)',
    'Dim cameraPresets As List(Of String) = SelectCinematicCameraAI(activeProfile.Name, "General_Part", vWeight, commercialIntent)'
)

# 3. Governor inside `For Each`
governor_block = """
        ' =============================================================
        ' [V5.0] SHOT GOVERNOR – LUẬT THÉP BẢO VỆ ENGINE
        ' =============================================================
        Dim blockMsg As String = ""
        If shotType = "Dolly_Vertigo" AndAlso Not activeProfile.AllowVertigo Then blockMsg = "Vertigo Disabled"
        If shotType = "Phase_Shift_Orbit" AndAlso Not activeProfile.AllowTopFlip Then blockMsg = "TopFlip Disabled"
        If shotType = "Top_Orbit_Zoom" AndAlso Not activeProfile.AllowTopFlip Then blockMsg = "TopFlip Disabled"
        If shotType = "Internal_Core_Sweep" AndAlso Not activeProfile.AllowDeepZoom Then blockMsg = "DeepZoom Disabled"
        If shotType = "Tesla_Speed_Ramp" AndAlso Not activeProfile.AllowSpeedRamp Then blockMsg = "SpeedRamp Disabled"
        If shotType = "FPV_Drone_Dive" AndAlso Not activeProfile.AllowTopFlip Then blockMsg = "TopFlip Disabled"
        If shotType = "Dynamic_Section_MRI" AndAlso Not activeProfile.AllowDynamicSection Then blockMsg = "DynSection Disabled"

        If blockMsg <> "" Then
            blockedShotCount += 1
            chk_ShotBlocked = True
            logReport.AppendLine("ShotBlocked: TRUE - " & shotType & " (" & blockMsg & ")")
            EngineHealthScore -= 5
            ThisApplication.StatusBarText = "[MAXSKILLS V5.0] BỎ QUA: " & shotType & " | Lý do: " & blockMsg
            Continue For
        End If
"""
content = content.replace(
    'ThisApplication.StatusBarText = "[AI Director] " & shotType & " | Thước phim: " & baseName',
    'ThisApplication.StatusBarText = "[AI Director] " & shotType & " | Thước phim: " & baseName\n' + governor_block
)

# 4. Status Bar per loop
content = content.replace(
    'Dim curTier As String = "Rhythm"',
    'ThisApplication.StatusBarText = "[MAXSKILLS V5.0] Profile=" & activeProfile.Name & " | Blocked=" & chk_ShotBlocked & " | ParamScaled=" & chk_ParamScaled & " | Shot=" & shotType\n        Dim curTier As String = "Rhythm"'
)

# 5. Dynamic Params
content = content.replace('curR = maxDim * ', 'curR = maxDim * activeProfile.CameraRadiusFactor * ')
content = content.replace('theta = Math.PI * ', 'theta = Math.PI * activeProfile.MaxAngularSpeed * ')
content = content.replace('curR = maxDim * activeProfile.CameraRadiusFactor *', 'chk_ParamScaled = True\n                    curR = maxDim * activeProfile.CameraRadiusFactor *')

# 6. SmartClassifyAI Replacement
classify_ai = """
Function SmartClassifyAI(oDoc As Document) As ModelProfile
    Dim prof As New ModelProfile()
    ' Safe Fallback
    prof.Name = "SafeProfile"
    prof.MaxAngularSpeed = 0.5
    prof.CameraRadiusFactor = 1.5
    prof.MinZoomRatio = 0.8
    prof.AllowTopFlip = False
    prof.AllowVertigo = False
    prof.AllowSpeedRamp = False
    prof.AllowIBLSweep = False
    prof.AllowMacro = False
    prof.AllowDeepZoom = False
    prof.AllowDynamicSection = False

    If oDoc.DocumentType <> DocumentTypeEnum.kAssemblyDocumentObject Then Return prof

    Dim oAsm As AssemblyDocument = CType(oDoc, AssemblyDocument)
    Dim ptsCount As Integer = oAsm.ComponentDefinition.Occurrences.AllLeafOccurrences.Count
    Dim rB As Box = oAsm.ComponentDefinition.RangeBox
    Dim dx As Double = rB.MaxPoint.X - rB.MinPoint.X
    Dim dy As Double = rB.MaxPoint.Y - rB.MinPoint.Y
    Dim dz As Double = rB.MaxPoint.Z - rB.MinPoint.Z

    If dy > 1.8 * Math.Max(dx, dz) Then
        prof.Name = "Vertical_Tall"
        prof.MaxAngularSpeed = 0.6
        prof.CameraRadiusFactor = 1.6
        prof.MinZoomRatio = 0.45
        prof.AllowTopFlip = False
        prof.AllowVertigo = False
        prof.AllowDynamicSection = True
        prof.AllowMacro = True
    ElseIf Math.Max(dx, dz) > 2.0 * dy Then
        prof.Name = "Horizontal_Long"
        prof.MaxAngularSpeed = 1.2
        prof.CameraRadiusFactor = 1.3
        prof.MinZoomRatio = 0.35
        prof.AllowVertigo = True
        prof.AllowSpeedRamp = True
        prof.AllowDynamicSection = True
        prof.AllowMacro = True
    ElseIf ptsCount > 300 Then
        prof.Name = "Dense_Piping"
        prof.MaxAngularSpeed = 0.5
        prof.CameraRadiusFactor = 1.8
        prof.MinZoomRatio = 0.6
        prof.AllowDeepZoom = False
        prof.AllowDynamicSection = True
    Else
        prof.Name = "Compact_Block"
        prof.MaxAngularSpeed = 1.5
        prof.CameraRadiusFactor = 1.1
        prof.MinZoomRatio = 0.25
        prof.AllowIBLSweep = True
        prof.AllowMacro = True
        prof.AllowDeepZoom = True
        prof.AllowDynamicSection = True
    End If
    Return prof
End Function
"""
content = re.sub(r'Sub SmartClassifyAI\(oDoc As Document.*?End Sub', classify_ai, content, flags=re.DOTALL)

# 7. Write Log at End
log_write = """
    ' [V5.0] WRITE CHECKLIST REPORT
    If chk_ProfileDetected Then logReport.AppendLine("[CHECK] Profile Detection : PASS") Else logReport.AppendLine("[CHECK] Profile Detection : FAIL")
    If chk_ShotBlocked Then logReport.AppendLine("[CHECK] Shot Governor : PASS - " & blockedShotCount & " shots blocked") Else logReport.AppendLine("[CHECK] Shot Governor : WARN - No shots blocked")
    If chk_ParamScaled Then logReport.AppendLine("[CHECK] Dynamic Params : PASS") Else logReport.AppendLine("[CHECK] Dynamic Params : FAIL")
    logReport.AppendLine("EngineHealthScore: " & EngineHealthScore & "/100")
    logReport.AppendLine("FinalStatus: " & If(EngineHealthScore > 50, "SAFE", "CRITICAL"))
    
    Try
        System.IO.File.WriteAllText(exportDir & "\MAXSKILLS_V5_ProfileReport_" & baseName & ".txt", logReport.ToString())
    Catch : End Try
"""
content = content.replace("' Thực thi trạm kết xuất FFmpeg", log_write + "\n    ' Thực thi trạm kết xuất FFmpeg")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Success')
