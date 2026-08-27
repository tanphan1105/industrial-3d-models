import sys
import re

file_path = r'd:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add chk_SafeProfileUsed
content = content.replace(
    'Dim chk_IBLAllowed As Boolean = False',
    'Dim chk_IBLAllowed As Boolean = False\n    Dim chk_SafeProfileUsed As Boolean = False'
)

# 2. Update If statement setting
content = content.replace(
    'Else\n        EngineHealthScore -= 30',
    'Else\n        chk_SafeProfileUsed = True\n        EngineHealthScore -= 30'
)

# 3. Phanh Sinh Tồn in the Shot Governor
health_brake = """        ' [V5.0] PHANH SINH TỒN HEALTH SCORE
        If EngineHealthScore < 60 Then
            activeProfile.AllowIBLSweep = False
            activeProfile.AllowSpeedRamp = False
        End If

        ' =============================================================
        ' [V5.0] SHOT GOVERNOR – LUẬT THÉP BẢO VỆ ENGINE
        ' =============================================================
"""
content = content.replace(
    """        ' =============================================================
        ' [V5.0] SHOT GOVERNOR – LUẬT THÉP BẢO VỆ ENGINE
        ' =============================================================\n""",
    health_brake
)

# 4. Status Bar Format update
content = content.replace(
    'ThisApplication.StatusBarText = "[MAXSKILLS V5.0] BỎ QUA: " & shotType & " | Lý do: " & blockMsg',
    'ThisApplication.StatusBarText = "[MAXSKILLS V5.0] Profile=" & activeProfile.Name & " | Shot=" & shotType & " | Blocked=True | Health=" & EngineHealthScore'
)
content = content.replace(
    'ThisApplication.StatusBarText = "[MAXSKILLS V5.0] Profile=" & activeProfile.Name & " | Blocked=" & chk_ShotBlocked & " | ParamScaled=" & chk_ParamScaled & " | Shot=" & shotType',
    'ThisApplication.StatusBarText = "[MAXSKILLS V5.0] Profile=" & activeProfile.Name & " | Shot=" & shotType & " | Blocked=" & chk_ShotBlocked & " | Health=" & EngineHealthScore'
)

# 5. File Log Format Update
log_write_old = """    ' [V5.0] WRITE CHECKLIST REPORT
    If chk_ProfileDetected Then logReport.AppendLine("[CHECK] Profile Detection : PASS") Else logReport.AppendLine("[CHECK] Profile Detection : FAIL")
    If chk_ShotBlocked Then logReport.AppendLine("[CHECK] Shot Governor : PASS - " & blockedShotCount & " shots blocked") Else logReport.AppendLine("[CHECK] Shot Governor : WARN - No shots blocked")
    If chk_ParamScaled Then logReport.AppendLine("[CHECK] Dynamic Params : PASS") Else logReport.AppendLine("[CHECK] Dynamic Params : FAIL")
    logReport.AppendLine("EngineHealthScore: " & EngineHealthScore & "/100")
    logReport.AppendLine("FinalStatus: " & If(EngineHealthScore > 50, "SAFE", "CRITICAL"))"""

log_write_new = """    ' [V5.0] WRITE CHECKLIST REPORT
    Dim finalLog As New System.Text.StringBuilder()
    finalLog.AppendLine("ProfileDetected: " & activeProfile.Name)
    finalLog.AppendLine("SafeProfileUsed: " & chk_SafeProfileUsed)
    finalLog.AppendLine("BlockedShots: " & blockedShotCount)
    finalLog.AppendLine("IBLSweep: " & If(activeProfile.AllowIBLSweep, "Allowed", "Blocked"))
    finalLog.AppendLine("EngineHealthScore: " & EngineHealthScore)
    finalLog.AppendLine("FinalStatus: " & If(EngineHealthScore >= 60, "SAFE", "CRITICAL"))
    logReport.AppendLine()
    logReport.AppendLine(finalLog.ToString())"""

content = content.replace(log_write_old, log_write_new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Final Spec Applied Successfully.")
