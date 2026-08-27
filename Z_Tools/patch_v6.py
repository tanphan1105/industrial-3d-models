import sys
import re

file_path = r'd:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Sub Main flags
text = text.replace(
    'Dim chk_SafeProfileUsed As Boolean = False',
    'Dim chk_SafeProfileUsed As Boolean = False\n    Dim chk_LearningOverride As Boolean = False\n    Dim RiskScore As Double = 0.0\n    Dim RiskPattern As String = "NONE"\n    Dim OverrideSource As String = "RULE"'
)

# 2. Add ApplyLearningGovernor call and partCount calculation
# We need to get partCount in Main to pass to governor
part_calc = """
    Dim partCount As Integer = 0
    If oDoc.DocumentType = DocumentTypeEnum.kAssemblyDocumentObject Then
        partCount = CType(oDoc, AssemblyDocument).ComponentDefinition.Occurrences.AllLeafOccurrences.Count
    End If
"""

text = re.sub(
    r'Dim vWeight As String = If\(activeProfile\.Name = "Dense_Piping", "Heavy", "Light"\)',
    part_calc + r'\n    activeProfile = ApplyLearningGovernor(activeProfile, partCount)\n    Dim vWeight As String = If(activeProfile.Name = "Dense_Piping", "Heavy", "Light")',
    text
)

# 3. Update Status Bar V6.0
text = text.replace(
    'ThisApplication.StatusBarText = "[MAXSKILLS V5.0] Profile: " & activeProfile.Name',
    'ThisApplication.StatusBarText = "[MAXSKILLS V6.0] Profile: " & activeProfile.Name & " | RiskScore=" & RiskScore'
)

# 4. Update Header in Report
text = text.replace('=== MAXSKILLS V5.0 REPORT ===', '=== MAXSKILLS V6.0 ADAPTIVE REPORT ===')

# 5. Update Loop Status Bar
text = re.sub(
    r'ThisApplication\.StatusBarText = "\[MAXSKILLS V5\.0\] Profile=" & activeProfile\.Name & " \| Shot=" & shotType & " \| Blocked=" & chk_ShotBlocked & " \| Health=" & EngineHealthScore',
    'ThisApplication.StatusBarText = "[MAXSKILLS V6.0] Prof=" & activeProfile.Name & " | Score=" & RiskScore & " | Health=" & EngineHealthScore & " | Override=" & chk_LearningOverride & " | Shot=" & shotType',
    text
)

# 6. Inject ApplyLearningGovernor Function
governor_func = """
Function ApplyLearningGovernor(ByRef prof As ModelProfile, partCount As Integer) As ModelProfile
    Dim rScore As Double = 0.0
    
    ' Layer 1: Deterministic Rules (Weighted)
    If prof.Name = "Dense_Piping" Then rScore += 0.6
    If partCount > 450 Then rScore += 0.4
    
    ' Layer 2: Threshold Activation
    If rScore >= 0.7 Then
        prof.AllowDeepZoom = False
        prof.MaxAngularSpeed *= 0.8
        ' Inject variables into global scope via Side Effects (iLogic allows this if declared in Main)
        ' Note: In iLogic, to modify variables in Main from a Function, they must be passed or accessible.
        ' We will use a shared object or just return the modified profile.
    End If
    
    ' For V6.0 iLogic, we'll set the global risk variables using a simpler trick or just return
    Return prof
End Function
"""

# Actually, iLogic functions can't easily modify Main's local variables unless passed ByRef.
# I will modify the call site to set those variables.

# Update call site to capture risk
text = text.replace(
    'activeProfile = ApplyLearningGovernor(activeProfile, partCount)',
    'activeProfile = ApplyLearningGovernor(activeProfile, partCount, RiskScore, RiskPattern, chk_LearningOverride)'
)

# Update the function definition too
governor_func_final = """
Function ApplyLearningGovernor(ByRef prof As ModelProfile, partCount As Integer, ByRef rScore As Double, ByRef rPattern As String, ByRef over As Boolean) As ModelProfile
    rScore = 0.0
    If prof.Name = "Dense_Piping" Then rScore += 0.6
    If partCount > 450 Then rScore += 0.4
    
    If rScore >= 0.7 Then
        prof.AllowDeepZoom = False
        prof.MaxAngularSpeed *= 0.8
        over = True
        rPattern = "DENSE_PIPE_HIGH_PART"
    End If
    Return prof
End Function
"""

# Append function at the end
text = text.strip() + "\n\n" + governor_func_final

# 7. CSV Logging at the end
# Fields: Timestamp, Model, Profile, PartCount, Blocked, Health, Status, RiskPatternID, OverrideSource
csv_log = """
    ' [V6.0] ADAPTIVE CSV LOGGING (Toyota Kaizen)
    Try
        Dim csvPath As String = "d:\WT3D_Project\Z_Log\MAXSKILLS_Learning_Log.csv"
        If Not System.IO.File.Exists(csvPath) Then
            System.IO.File.WriteAllText(csvPath, "Timestamp,Model,Profile,PartCount,BlockedCount,Health,Status,RiskPattern,OverrideSource" & vbCrLf)
        End If
        Dim logLine As String = String.Format("{0},{1},{2},{3},{4},{5},{6},{7},{8}", _
            DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"), _
            baseName, _
            activeProfile.Name, _
            partCount, _
            blockedShotCount, _
            EngineHealthScore, _
            If(EngineHealthScore >= 60, "SAFE", "CRITICAL"), _
            RiskPattern, _
            OverrideSource)
        System.IO.File.AppendAllText(csvPath, logLine & vbCrLf)
    Catch : End Try
"""

text = text.replace("' Thực thi trạm kết xuất FFmpeg", csv_log + "\n    ' Thực thi trạm kết xuất FFmpeg")

# 8. Update logReport to include new fields
text = text.replace(
    'finalLog.AppendLine("FinalStatus: " & If(EngineHealthScore >= 60, "SAFE", "CRITICAL"))',
    'finalLog.AppendLine("FinalStatus: " & If(EngineHealthScore >= 60, "SAFE", "CRITICAL"))\n'
    '    finalLog.AppendLine("RiskScore: " & RiskScore)\n'
    '    finalLog.AppendLine("RiskPattern: " & RiskPattern)\n'
    '    finalLog.AppendLine("OverrideSource: " & OverrideSource)'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("V6.0 Architecture Applied.")
