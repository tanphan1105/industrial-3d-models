import sys
import re

file_path = r'd:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Hotfix: Fix Double Mutation by converting ApplyLearningGovernor to Sub
text = re.sub(r'Function ApplyLearningGovernor\(.*?\r?\nEnd Function', '', text, flags=re.DOTALL)

governor_sub = """
Sub ApplyLearningGovernor(ByRef prof As ModelProfile, partCount As Integer, ByRef rScore As Double, ByRef rPattern As String, ByRef over As Boolean)
    rScore = 0.0
    ' [V6.1] Risk Weight Dictionary (Toyota Style)
    Dim w_DensePipe As Double = 0.6
    Dim w_HighPart As Double = 0.4
    
    If prof.Name = "Dense_Piping" Then rScore += w_DensePipe
    If partCount > 450 Then rScore += w_HighPart
    
    If rScore >= 0.7 Then
        prof.AllowDeepZoom = False
        prof.MaxAngularSpeed *= 0.8
        over = True
        rPattern = "DENSE_PIPE_HIGH_PART"
    End If
End Sub
"""

text = text.strip() + "\n\n" + governor_sub.strip()

# 2. Update all call sites to use Procedure call
text = re.sub(r'activeProfile = ApplyLearningGovernor\(.*?\)', r'ApplyLearningGovernor(activeProfile, partCount, RiskScore, RiskPattern, chk_LearningOverride)', text)

# 3. [V6.1] Implement Buffered Logging
if 'Dim LearningBuffer As New List(Of String)()' not in text:
    text = text.replace(
        'Dim logReport As New System.Text.StringBuilder()',
        'Dim logReport As New System.Text.StringBuilder()\n    Dim LearningBuffer As New List(Of String)()'
    )

# Escaping the replacement string to avoid bad escape errors in re.sub
batch_flush = r"""
    ' [V6.1] TOYOTA BATCH FLUSH (Scale-Safe Logging)
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
            
        LearningBuffer.Add(logLine)
        System.IO.File.AppendAllLines(csvPath, LearningBuffer)
    Catch : End Try
"""

# Instead of re.sub with complex regex, let's use a simpler marker or anchor if possible
# The block starts at "' [V6.0] ADAPTIVE CSV LOGGING"
csv_marker_start = "' [V6.0] ADAPTIVE CSV LOGGING (Toyota Kaizen)"
# Find the start and find the next ' Catch : End Try'
start_idx = text.find(csv_marker_start)
if start_idx != -1:
    end_marker = "Catch : End Try"
    end_idx = text.find(end_marker, start_idx) + len(end_marker)
    text = text[:start_idx] + batch_flush + text[end_idx:]

# 4. [V6.1] Simulation Layer
if 'PRE-FLIGHT RISK SIMULATION' not in text:
    simulation_check = """
    ' Layer 4: [V6.1] PRE-FLIGHT RISK SIMULATION (Shadow Mode)
    If RiskScore >= 0.9 Then
        EngineHealthScore -= 10 ' Cảnh báo sớm
        logReport.AppendLine("PreFlight-Status: HIGH_RISK_DETECTED")
    End If
"""
    text = text.replace(
        'Dim vWeight As String = If(activeProfile.Name = "Dense_Piping", "Heavy", "Light")',
        simulation_check + '\n    Dim vWeight As String = If(activeProfile.Name = "Dense_Piping", "Heavy", "Light")'
    )

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("V6.1 Hotfix & Scaling Applied Successfully.")
