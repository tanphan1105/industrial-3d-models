import os
import shutil
import hashlib

file_path = r'd:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb'
backup_path = file_path + ".bak_v62"

# ===============================
# 1. LOAD FILE SAFELY
# ===============================
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

original_text = text

# ===============================
# 2. BACKUP (ROLLBACK SAFETY)
# ===============================
if not os.path.exists(backup_path):
    shutil.copy(file_path, backup_path)

# ===============================
# 3. REMOVE OLD FUNCTION (SAFE ANCHOR)
# ===============================
# We remove the Sub version if it exists from V6.1 turn
start_tag = "Sub ApplyLearningGovernor"
end_tag = "End Sub"

if start_tag in text and end_tag in text:
    start = text.find(start_tag)
    end = text.find(end_tag, start) + len(end_tag)
    text = text[:start] + text[end:]

# Also check for old Function version just in case
start_tag_f = "Function ApplyLearningGovernor"
end_tag_f = "End Function"
if start_tag_f in text and end_tag_f in text:
    start = text.find(start_tag_f)
    end = text.find(end_tag_f, start) + len(end_tag_f)
    text = text[:start] + text[end:]

# ===============================
# 4. INSERT NEW GOVERNOR (IDEMPOTENT)
# ===============================
governor_sub = """
Sub ApplyLearningGovernor(ByRef prof As ModelProfile, partCount As Integer, _
    ByRef rScore As Double, ByRef rPattern As String, ByRef over As Boolean)

    rScore = 0.0

    ' V6.2 Risk Weights (Stable Model)
    Dim wDense As Double = 0.6
    Dim wPart As Double = 0.4

    If prof.Name = "Dense_Piping" Then rScore += wDense
    If partCount > 450 Then rScore += wPart

    If rScore >= 0.7 Then
        prof.AllowDeepZoom = False
        prof.MaxAngularSpeed *= 0.8
        over = True
        rPattern = "DENSE_PIPE_HIGH_PART"
    End If

End Sub
"""

if "Sub ApplyLearningGovernor" not in text:
    text = text.strip() + "\n\n" + governor_sub.strip()

# ===============================
# 5. FIX CALL SITE (SAFE REPLACE)
# ===============================
# Ensure it's the procedure call version
text = text.replace(
    "activeProfile = ApplyLearningGovernor(activeProfile, partCount, RiskScore, RiskPattern, chk_LearningOverride)",
    "ApplyLearningGovernor(activeProfile, partCount, RiskScore, RiskPattern, chk_LearningOverride)"
)

# ===============================
# 6. SIMULATION LAYER (IDEMPOTENT)
# ===============================
sim_block = """
    ' [V6.2] PRE-FLIGHT SIMULATION LAYER
    If RiskScore >= 0.9 Then
        EngineHealthScore -= 10
        logReport.AppendLine("PRE_FLIGHT: HIGH RISK DETECTED")
    End If
"""

# Clean up older simulation layers if present to keep it idempotent
if "' [V6.1] PRE-FLIGHT RISK SIMULATION (Shadow Mode)" in text:
    # Find start and end of that block
    s_idx = text.find("' Layer 4: [V6.1] PRE-FLIGHT RISK SIMULATION (Shadow Mode)")
    e_idx = text.find("End If", s_idx) + 6
    if s_idx != -1:
        text = text[:s_idx] + text[e_idx:]

if "PRE-FLIGHT SIMULATION LAYER" not in text:
    text = text.replace(
        'Dim vWeight As String = If(activeProfile.Name = "Dense_Piping", "Heavy", "Light")',
        sim_block + '\n    Dim vWeight As String = If(activeProfile.Name = "Dense_Piping", "Heavy", "Light")'
    )

# ===============================
# 7. PATCH VALIDATION (LIGHT CHECK)
# ===============================
required_tokens = [
    "ApplyLearningGovernor",
    "PRE-FLIGHT",
    "ModelProfile"
]

valid = all(token in text for token in required_tokens)

# ===============================
# 8. WRITE SAFELY + HASH TRACKING
# ===============================
if valid:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

    patch_id = hashlib.md5(text.encode()).hexdigest()
    print(f"V6.2 PATCH APPLIED OK | HASH: {patch_id}")
else:
    print("PATCH FAILED VALIDATION - ROLLBACK SUGGESTED")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(original_text)
