import os
import shutil
import hashlib
import re
from datetime import datetime

file_path = r'd:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb'
tmp_path = file_path + ".tmp"
version_tag = "V6.4.8"

START_TAG = f"' ===== {version_tag} LEARNING GOVERNOR START ====="
END_TAG   = f"' ===== {version_tag} LEARNING GOVERNOR END ====="
PRE_TAG   = f"' ===== {version_tag} PRE-FLIGHT SIMULATION ====="

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
# 2. BACKUP ENGINE (SMART)
# ===============================
def file_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

current_hash = file_hash(original_text)
backup_path = file_path + f".bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

if not os.path.exists(backup_path):
    shutil.copy2(file_path, backup_path)

# ===============================
# 3. VERSION LOCK (SAFE MODE)
# ===============================
if START_TAG in text and END_TAG in text:
    print(f"PATCH SKIPPED - ALREADY {version_tag}")
    raise SystemExit()

# ===============================
# 4. CLEAN OLD GOVERNOR (SAFE BLOCK REMOVE)
# ===============================
text = re.sub(
    r"' ===== V6\.\d+(?:\.\d+)? LEARNING GOVERNOR START =====[\s\S]*?' ===== V6\.\d+(?:\.\d+)? LEARNING GOVERNOR END =====",
    "",
    text
)

text = re.sub(
    r"Sub\s+ApplyLearningGovernor\s*\([\s\S]*?End Sub",
    "",
    text
)

# ===============================
# 5. CLEAN PRE-FLIGHT BLOCK
# ===============================
text = re.sub(
    r"' ===== V6\.\d+(?:\.\d+)? PRE-FLIGHT SIMULATION =====[\s\S]*?If RiskScore[\s\S]*?End If",
    "",
    text
)

# ===============================
# 6. GOVERNOR ENGINE (IDEMPOTENT)
# ===============================
governor = f"""
{START_TAG}
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
{END_TAG}
"""

# inject only if missing
if "Sub ApplyLearningGovernor" not in text:
    text = text.rstrip() + "\n\n" + governor.strip()

# ===============================
# 7. SAFE CALL PATCH (NON-GREEDY)
# ===============================
text = re.sub(
    r"ApplyLearningGovernor\s*\(([^()]*)\)",
    r"ApplyLearningGovernor(\1)",
    text
)

# ===============================
# 8. PRE-FLIGHT BLOCK (SAFE ANCHOR INSERTION)
# ===============================
sim_block = f"""
    {PRE_TAG}
    If RiskScore >= 0.9 Then
        EngineHealthScore -= 10
        logReport.AppendLine("PRE_FLIGHT: HIGH RISK DETECTED")
    End If
"""

# better anchors (multi-option strategy)
anchor_candidates = [
    r"(Dim\s+vWeight\s*=\s*If\s*\(activeProfile\.Name.*\))",
    r"(Dim\s+commercialIntent\s*=\s*\".*?\")"
]

if PRE_TAG not in text:
    injected = False

    for anchor in anchor_candidates:
        match = re.search(anchor, text)
        if match:
            text = re.sub(anchor, sim_block + r"\n    \1", text, count=1)
            injected = True
            break

    # fallback safe append (last resort)
    if not injected:
        text = text.rstrip() + "\n\n" + sim_block.strip()

# ===============================
# 9. VALIDATION ENGINE (STRICT MODE)
# ===============================
def validate(code: str) -> bool:
    has_governor = START_TAG in code and END_TAG in code
    has_preflight = PRE_TAG in code

    func_ok = len(re.findall(r"Sub\s+ApplyLearningGovernor\s*\(", code)) == 1

    # ensure correct order
    start_pos = code.find("Sub ApplyLearningGovernor")
    end_pos = code.rfind("End Sub")

    structure_ok = start_pos != -1 and end_pos > start_pos

    return all([has_governor, has_preflight, func_ok, structure_ok])

valid = validate(text)

# ===============================
# 10. HASH ENGINE (STABLE)
# ===============================
def generate_hash(code: str):
    normalized = re.sub(r"\s+", "", code + version_tag)
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]

# ===============================
# 11. ATOMIC WRITE
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
