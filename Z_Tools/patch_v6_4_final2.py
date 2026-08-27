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
# 0. SAFE INIT
# ===============================
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# ===============================
# 1. LOAD FILE
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
# 3. VERSION LOCK (ANTI REPATCH)
# ===============================
if version_tag in text:
    print("PATCH SKIPPED - ALREADY V6.4")
    raise SystemExit()

# ===============================
# 4. CLEAN OLD GOVERNOR (STRICT BOUNDARY SAFE)
# ===============================
text = re.sub(
    r"' ===== V6\.\d+ LEARNING GOVERNOR START =====[\s\S]*?' ===== V6\.\d+ LEARNING GOVERNOR END =====",
    "",
    text
)

text = re.sub(
    r"Sub\s+ApplyLearningGovernor[\s\S]*?End Sub",
    "",
    text,
    flags=re.MULTILINE
)

# ===============================
# 5. INSERT GOVERNOR (IDEMPOTENT LOCK)
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

if f"{version_tag} LEARNING GOVERNOR START" not in text:
    text = text.rstrip() + "\n\n" + governor.strip()

# ===============================
# 6. SAFE CALL PATCH (STRUCTURAL)
# ===============================
text = re.sub(
    r"activeProfile\s*=\s*ApplyLearningGovernor\s*\((.*?)\)",
    r"ApplyLearningGovernor(\1)",
    text
)

# ===============================
# 7. PRE-FLIGHT CLEAN (BOUNDARY SAFE)
# ===============================
text = re.sub(
    r"' ===== V6\.\d+ PRE-FLIGHT SIMULATION =====[\s\S]*?(?=Dim\s|Sub\s|Function\s|$)",
    "",
    text
)

# ===============================
# 8. PRE-FLIGHT INSERT (SINGLE INSTANCE ONLY)
# ===============================
anchor_pattern = r'(Dim\s+vWeight\s*=\s*If\s*\(activeProfile\.Name\s*=\s*"Dense_Piping".*?\))'

sim_block = f"""
' ===== {version_tag} PRE-FLIGHT SIMULATION =====
If RiskScore >= 0.9 Then
    EngineHealthScore -= 10
    logReport.AppendLine("PRE_FLIGHT: HIGH RISK DETECTED")
End If
"""

if "V6.4 PRE-FLIGHT SIMULATION" not in text:
    if re.search(anchor_pattern, text):
        text = re.sub(anchor_pattern, sim_block + r"\n\1", text, count=1)

# ===============================
# 9. STRONG STRUCTURAL VALIDATION (ENGINE SAFE MODE)
# ===============================
def validate(code: str) -> bool:
    governor_count = code.count("Sub ApplyLearningGovernor")
    endsub_count = code.count("End Sub")

    return all([
        governor_count == 1,
        endsub_count == 1,
        "PRE-FLIGHT SIMULATION" in code,
        "ModelProfile" in code,
        f"{version_tag} LEARNING GOVERNOR" in code
    ])

valid = validate(text)

# ===============================
# 10. HASH ENGINE (NORMALIZED SIGNATURE)
# ===============================
def generate_hash(code: str):
    normalized = re.sub(r"\s+", "", code)
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]

# ===============================
# 11. ATOMIC WRITE
# ===============================
def write_atomic(path, content):
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp_path, path)

# ===============================
# 12. EXECUTION GATE (FAIL SAFE)
# ===============================
if valid:
    write_atomic(file_path, text)

    patch_id = generate_hash(text)
    print(f"{version_tag} PATCH SUCCESS | {patch_id} | {datetime.now()}")

else:
    print(f"{version_tag} PATCH FAILED -> SAFE ROLLBACK")

    if os.path.exists(tmp_path):
        os.remove(tmp_path)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(original_text)
