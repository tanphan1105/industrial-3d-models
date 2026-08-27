import os
import shutil
import hashlib
import re
from datetime import datetime

file_path = r'd:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb'
tmp_path = file_path + ".tmp"
version_tag = "V6.4.8"

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
# 2. BACKUP ENGINE
# ===============================
backup_path = file_path + f".bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
if os.path.exists(file_path):
    shutil.copy2(file_path, backup_path)

# ===============================
# 3. VERSION LOCK
# ===============================
if version_tag in text:
    print(f"PATCH SKIPPED - ALREADY {version_tag}")
    raise SystemExit()

# ===============================
# 4. CLEAN OLD GOVERNOR
# ===============================
text = re.sub(
    r"' ===== V6\.\d+(?:\.\d+)? LEARNING GOVERNOR START =====[\s\S]*?' ===== V6\.\d+(?:\.\d+)? LEARNING GOVERNOR END =====",
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
# 5. CLEAN OLD PRE-FLIGHT
# ===============================
text = re.sub(
    r"' ===== V6\.\d+(?:\.\d+)? PRE-FLIGHT SIMULATION =====[\s\S]*?logReport\.AppendLine.*?End If[\n\r]*",
    "",
    text,
    flags=re.MULTILINE
)

# ===============================
# 6. GOVERNOR ENGINE
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

gov_signature = "ApplyLearningGovernor(ByRef prof As ModelProfile"

if gov_signature not in text:
    text = text.rstrip() + "\n\n" + governor.strip()

# ===============================
# 7. SAFE CALL PATCH
# ===============================
text = re.sub(
    r"activeProfile\s*=\s*ApplyLearningGovernor\s*\((.*?)\)",
    r"ApplyLearningGovernor(\1)",
    text
)

# ===============================
# 8. PRE-FLIGHT BLOCK
# ===============================
sim_block = f"""
    ' ===== {version_tag} PRE-FLIGHT SIMULATION =====
    If RiskScore >= 0.9 Then
        EngineHealthScore -= 10
        logReport.AppendLine("PRE_FLIGHT: HIGH RISK DETECTED")
    End If
"""

anchor_pattern = r"(Dim\s+vWeight\s*=\s*If\s*\(activeProfile\.Name.*?\))"

if f"{version_tag} PRE-FLIGHT SIMULATION" not in text:
    match = re.search(anchor_pattern, text)
    if match:
        # Chèn an toàn ngay sát trên cụm khai báo vWeight ở khu vực xử lý profile
        text = re.sub(anchor_pattern, sim_block + r"\n    \1", text, count=1)
    else:
        # SAFE FALLBACK STRATEGY: Chèn bên dưới việc gán commercialIntent (vẫn đảm bảo an toàn nằm trong Sub Main)
        safe_anchor = re.search(r"(Dim\s+commercialIntent\s*=\s*\".*?\")", text)
        if safe_anchor:
            text = text.replace(safe_anchor.group(0), safe_anchor.group(0) + "\n" + sim_block, 1)

# ===============================
# 9. VALIDATION ENGINE
# ===============================
def validate(code: str) -> bool:
    gov_blocks = len(re.findall(r"Sub\s+ApplyLearningGovernor\b", code))
    end_blocks = len(re.findall(r"\bEnd Sub\b", code))

    start_tag = f"' ===== {version_tag} LEARNING GOVERNOR START ====="
    end_tag = f"' ===== {version_tag} LEARNING GOVERNOR END ====="

    structure_ok = (
        gov_blocks == 1 and
        end_blocks >= 1 and
        code.count(start_tag) == 1 and
        code.count(end_tag) == 1
    )

    start_pos = code.find("Sub ApplyLearningGovernor")
    end_pos = code.rfind("End Sub")

    # Hàm nằm phải có End Sub nằm phía dưới nó
    structure_ok = structure_ok and (0 <= start_pos < end_pos)

    # Đảm bảo PRE-FLIGHT được ném vào không bị văng ra ngoài Sub Main
    # Code phải chứa PreFlight và chứa Biến tham chiếu Sub Main
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
