import os
import shutil
import hashlib
import re
from datetime import datetime

file_path = r'd:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb'
tmp_path = file_path + ".tmp"
version_tag = "V6.4.7"

# ===============================
# 0. SAFE INIT
# ===============================
os.makedirs(os.path.dirname(file_path), exist_ok=True)

if not os.path.exists(file_path):
    raise FileNotFoundError(f"INPUT FILE NOT FOUND: {file_path}")

# ===============================
# 1. LOAD FILE
# ===============================
with open(file_path, 'r', encoding='utf-8') as f:
    original_text = f.read()

text = original_text

# ===============================
# 2. BACKUP ENGINE (KAIZEN SAFE)
# ===============================
backup_path = file_path + f".bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

if os.path.exists(file_path):
    shutil.copy2(file_path, backup_path)

# ===============================
# 3. VERSION LOCK (ANTI REPATCH)
# ===============================
if version_tag in text:
    print(f"PATCH SKIPPED - ALREADY {version_tag}")
    raise SystemExit()

# ===============================
# 4. CLEAN OLD GOVERNOR (SAFE WIPE)
# ===============================
text = re.sub(
    r"' ===== V6\.\d+\.\d+ LEARNING GOVERNOR START =====[\s\S]*?' ===== V6\.\d+\.\d+ LEARNING GOVERNOR END =====",
    "",
    text,
    flags=re.MULTILINE
)

text = re.sub(
    r"Sub\s+ApplyLearningGovernor[\s\S]*?End Sub",
    "",
    text,
    flags=re.MULTILINE
)

# ===============================
# 5. GOVERNOR ENGINE
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

if text.count("Sub ApplyLearningGovernor") == 0:
    text = text.rstrip() + "\n\n" + governor.strip()

# ===============================
# 6. SAFE CALL PATCH
# ===============================
text = re.sub(
    r"activeProfile\s*=\s*ApplyLearningGovernor\s*\((.*?)\)",
    r"ApplyLearningGovernor(\1)",
    text
)

# ===============================
# 7. PRE-FLIGHT CLEAN
# ===============================
text = re.sub(
    r"' ===== V6\.\d+\.\d+ PRE-FLIGHT SIMULATION =====[\s\S]*?(?=Dim\s|Sub\s|Function\s|$)",
    "",
    text,
    flags=re.MULTILINE
)

# ===============================
# 8. PRE-FLIGHT ENGINE
# ===============================
anchor_pattern = r"(Dim\s+\w+\s*=\s*If\s*\(activeProfile\.Name.*?\))"

sim_block = f"""
' ===== {version_tag} PRE-FLIGHT SIMULATION =====
If RiskScore >= 0.9 Then
    EngineHealthScore -= 10
    logReport.AppendLine("PRE_FLIGHT: HIGH RISK DETECTED")
End If
"""

if f"{version_tag} PRE-FLIGHT SIMULATION" not in text:
    match = re.search(anchor_pattern, text)
    if match:
        text = re.sub(anchor_pattern, sim_block + r"\n\1", text, count=1)
    else:
        safe_anchor = re.search(r"Dim\s+\w+\s*=", text)
        if safe_anchor:
            text = text.replace(safe_anchor.group(0), sim_block + "\n" + safe_anchor.group(0), 1)
        else:
            text = sim_block + "\n\n" + text

# ===============================
# 9. VALIDATION ENGINE (HARD MODE)
# ===============================
def validate(code: str) -> bool:
    gov_blocks = len(re.findall(r"Sub\s+ApplyLearningGovernor\b", code))

    start_tag = f"' ===== {version_tag} LEARNING GOVERNOR START ====="
    end_tag = f"' ===== {version_tag} LEARNING GOVERNOR END ====="

    structure_ok = (
        gov_blocks == 1 and
        code.count(start_tag) == 1 and
        code.count(end_tag) == 1
    )

    start_pos = code.find("Sub ApplyLearningGovernor")
    end_pos = code.rfind("End Sub")

    structure_ok = structure_ok and start_pos != -1 and end_pos != -1 and start_pos < end_pos

    return (
        structure_ok and
        "PRE-FLIGHT SIMULATION" in code and
        "ModelProfile" in code and
        version_tag in code
    )

valid = validate(text)

# ===============================
# 10. HASH ENGINE
# ===============================
def generate_hash(code: str):
    normalized = re.sub(r"\s+", "", code + version_tag)
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]

# ===============================
# 11. ATOMIC WRITE (FAIL-SAFE)
# ===============================
def write_atomic(path, content):
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp_path, path)
    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise RuntimeError(f"ATOMIC_WRITE_FAILED: {e}")

# ===============================
# 12. EXECUTION GATE
# ===============================
if valid:
    write_atomic(file_path, text)

    patch_id = generate_hash(text)
    print(f"{version_tag} PATCH SUCCESS | {patch_id} | {datetime.now()}")

else:
    print(f"{version_tag} PATCH FAILED -> ROLLBACK")

    if os.path.exists(tmp_path):
        os.remove(tmp_path)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(original_text)

    raise SystemExit("ENGINE_ABORT: STRUCTURE INVALID")
