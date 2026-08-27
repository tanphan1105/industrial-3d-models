import os
import shutil
import hashlib
import re
from datetime import datetime

file_path = r'd:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb'

backup_path = file_path + ".bak_v63"
tmp_path = file_path + ".tmp"

# ===============================
# 0. SAFE ENV CHECK
# ===============================
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# ===============================
# 1. LOAD
# ===============================
with open(file_path, 'r', encoding='utf-8') as f:
    original_text = f.read()

text = original_text

# ===============================
# 2. BACKUP (ONLY ONCE)
# ===============================
if not os.path.exists(backup_path):
    shutil.copy(file_path, backup_path)

# ===============================
# 3. REMOVE OLD GOVERNOR (REGEX SAFE)
# ===============================
pattern_sub = r"Sub\s+ApplyLearningGovernor[\s\S]*?End Sub"
pattern_func = r"Function\s+ApplyLearningGovernor[\s\S]*?End Function"

text = re.sub(pattern_sub, "", text, flags=re.MULTILINE)
text = re.sub(pattern_func, "", text, flags=re.MULTILINE)

# ===============================
# 4. INSERT GOVERNOR (IDEMPOTENT BLOCK MARKER)
# ===============================
governor_sub = """
' ===== V6.3 LEARNING GOVERNOR START =====
Sub ApplyLearningGovernor(ByRef prof As ModelProfile, partCount As Integer, _
    ByRef rScore As Double, ByRef rPattern As String, ByRef over As Boolean)

    rScore = 0.0

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
' ===== V6.3 LEARNING GOVERNOR END =====
"""

if "V6.3 LEARNING GOVERNOR" not in text:
    text += "\n\n" + governor_sub.strip()

# ===============================
# 5. SAFE CALL PATCH (REGEX)
# ===============================
text = re.sub(
    r"activeProfile\s*=\s*ApplyLearningGovernor\s*\((.*?)\)",
    r"ApplyLearningGovernor(\1)",
    text
)

# ===============================
# 6. PRE-FLIGHT SIMULATION PATCH (IDEMPOTENT)
# ===============================
sim_block = """
' ===== V6.3 PRE-FLIGHT SIMULATION =====
If RiskScore >= 0.9 Then
    EngineHealthScore -= 10
    logReport.AppendLine("PRE_FLIGHT: HIGH RISK DETECTED")
End If
' =======================================
"""

if "V6.3 PRE-FLIGHT SIMULATION" not in text:
    text = text.replace(
        'Dim vWeight As String = If(activeProfile.Name = "Dense_Piping", "Heavy", "Light")',
        sim_block + '\n    Dim vWeight As String = If(activeProfile.Name = "Dense_Piping", "Heavy", "Light")'
    )

# ===============================
# 7. VALIDATION ENGINE
# ===============================
required_tokens = [
    "ApplyLearningGovernor",
    "PRE-FLIGHT",
    "ModelProfile"
]

valid = all(t in text for t in required_tokens)

# ===============================
# 8. ATOMIC WRITE + HASH TRACKING
# ===============================
def write_atomic(path, content):
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp_path, path)

if valid:
    write_atomic(file_path, text)

    patch_id = hashlib.sha256(text.encode()).hexdigest()[:16]
    log_line = f"{datetime.now()} | PATCH_OK | {patch_id}"

    print("V6.3 PATCH SUCCESS")
    print(log_line)
else:
    print("PATCH FAILED -> ROLLBACK INITIATED")
    write_atomic(file_path, original_text)
