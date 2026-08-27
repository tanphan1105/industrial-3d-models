import os
import shutil
import hashlib
import re
from datetime import datetime

file_path = r'd:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb'

backup_path = file_path + ".bak_v64"
tmp_path = file_path + ".tmp"
version_tag = "V6.4"

# ===============================
# 0. INIT SAFE CHECK
# ===============================
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# ===============================
# 1. LOAD
# ===============================
with open(file_path, 'r', encoding='utf-8') as f:
    original_text = f.read()

text = original_text

# ===============================
# 2. BACKUP (ONCE ONLY)
# ===============================
if not os.path.exists(backup_path):
    shutil.copy(file_path, backup_path)

# ===============================
# 3. VERSION GUARD (ANTI DUPLICATE PATCH)
# ===============================
if version_tag in text:
    print("PATCH SKIPPED - ALREADY V6.4")
    raise SystemExit()

# ===============================
# 4. REMOVE GOVERNOR (SAFE BLOCK)
# ===============================
text = re.sub(
    r"' ===== V6\.\d LEARNING GOVERNOR START =====[\s\S]*?' ===== V6\.\d LEARNING GOVERNOR END =====",
    "",
    text
)

# Also remove standalone Sub if it exists without marker
pattern_sub = r"Sub\s+ApplyLearningGovernor[\s\S]*?End Sub"
text = re.sub(pattern_sub, "", text, flags=re.MULTILINE)

# ===============================
# 5. INSERT GOVERNOR (CONTROLLED BLOCK)
# ===============================
governor = f"""
' ===== {version_tag} LEARNING GOVERNOR START =====
Sub ApplyLearningGovernor(ByRef prof As ModelProfile, partCount As Integer, _
    ByRef rScore As Double, ByRef rPattern As String, ByRef over As Boolean)

    rScore = 0

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
' ===== {version_tag} LEARNING GOVERNOR END =====
"""

text += "\n\n" + governor.strip()

# ===============================
# 6. SAFE CALL PATCH (STRUCTURAL REGEX)
# ===============================
# Clean up any assignment to activeProfile from ApplyLearningGovernor
text = re.sub(
    r"activeProfile\s*=\s*ApplyLearningGovernor\s*\((.*?)\)",
    r"ApplyLearningGovernor(\1)",
    text
)

# ===============================
# 7. PRE-FLIGHT PATCH (ANCHOR BASED)
# ===============================
# Clean up old pre-flight block
text = re.sub(
    r"' ===== V6\.\d PRE-FLIGHT SIMULATION =====[\s\S]*?' =======================================",
    "",
    text
)

anchor_pattern = r'(Dim\s+vWeight\s*=\s*If\s*\(activeProfile\.Name\s*=\s*"Dense_Piping".*?\))'

sim_block = f"""
' ===== {version_tag} PRE-FLIGHT SIMULATION =====
If RiskScore >= 0.9 Then
    EngineHealthScore -= 10
    logReport.AppendLine("PRE_FLIGHT: HIGH RISK DETECTED")
End If
' =======================================
"""

if re.search(anchor_pattern, text):
    text = re.sub(
        anchor_pattern,
        sim_block + r"\1",
        text
    )

# ===============================
# 8. STRUCTURAL VALIDATION (STRONG)
# ===============================
def validate(code: str) -> bool:
    return all([
        "Sub ApplyLearningGovernor" in code,
        "End Sub" in code,
        "PRE-FLIGHT" in code,
        "ModelProfile" in code,
        code.count("Sub ApplyLearningGovernor") == 1
    ])

valid = validate(text)

# ===============================
# 9. ATOMIC WRITE + HASH LOCK
# ===============================
def write_atomic(path, content):
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp_path, path)

if valid:
    write_atomic(file_path, text)

    patch_id = hashlib.sha256(text.encode()).hexdigest()[:16]
    print(f"{version_tag} PATCH SUCCESS | {patch_id} | {datetime.now()}")
else:
    print(f"{version_tag} PATCH FAILED -> ROLLBACK")
    write_atomic(file_path, original_text)
