import os
import shutil
import hashlib
import re
from datetime import datetime

file_path = r'd:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb'
tmp_path = file_path + ".tmp"
version_tag = "V6.4.9"

START_TAG = f"' ===== {version_tag} LEARNING GOVERNOR START ====="
END_TAG   = f"' ===== {version_tag} LEARNING GOVERNOR END ====="
PRE_TAG   = f"' ===== {version_tag} PRE-FLIGHT SIMULATION ====="

# ===============================
# 0. INIT
# ===============================
os.makedirs(os.path.dirname(file_path), exist_ok=True)

if not os.path.exists(file_path):
    raise FileNotFoundError(file_path)

with open(file_path, "r", encoding="utf-8") as f:
    original_text = f.read()

text = original_text

# ===============================
# 1. BACKUP
# ===============================
backup_path = file_path + f".bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
shutil.copy2(file_path, backup_path)

# ===============================
# 2. VERSION GUARD (STRONG)
# ===============================
if START_TAG in text and END_TAG in text:
    print("SKIP - ALREADY PATCHED")
    raise SystemExit()

# ===============================
# 3. SAFE BLOCK REMOVAL (CROSS-VERSION SCOPE)
# ===============================
# Xóa sạch các Block Governor của mọi version trước
text = re.sub(
    r"' ===== V6\.\d+(?:\.\d+)? LEARNING GOVERNOR START =====[\s\S]*?' ===== V6\.\d+(?:\.\d+)? LEARNING GOVERNOR END =====",
    "",
    text
)

# Xóa thân hàm ApplyLearningGovernor
text = re.sub(
    r"Sub\s+ApplyLearningGovernor\s*\([\s\S]*?End Sub\s*",
    "",
    text
)

# Xóa sạch PRE-FLIGHT của các bản trước
text = re.sub(
    r"' ===== V6\.\d+(?:\.\d+)? PRE-FLIGHT SIMULATION =====[\s\S]*?If RiskScore[\s\S]*?End If",
    "",
    text
)

# ===============================
# 4. GOVERNOR
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

if "Sub ApplyLearningGovernor" not in text:
    text = text.rstrip() + "\n\n" + governor.strip()

# ===============================
# 5. SAFE CALL PATCH (IMPROVED)
# ===============================
# handle nested parentheses better (light heuristic)
text = re.sub(
    r"ApplyLearningGovernor\s*\((.*?)\)",
    r"ApplyLearningGovernor(\1)",
    text
)

# ===============================
# 6. PRE-FLIGHT (SAFE SCOPE INJECTION)
# ===============================
sim_block = f"""
    {PRE_TAG}
    If RiskScore >= 0.9 Then
        EngineHealthScore -= 10
        logReport.AppendLine("PRE_FLIGHT: HIGH RISK DETECTED")
    End If
"""

anchors = [
    r"(Dim\s+vWeight\s*=.*)",
    r"(Dim\s+commercialIntent\s*=.*)"
]

if PRE_TAG not in text:
    injected = False

    for a in anchors:
        m = re.search(a, text)
        if m:
            text = re.sub(a, sim_block + r"\n    \1", text, count=1)
            injected = True
            break

    if not injected:
        # safer fallback: inject at bottom (though risky in iLogic if out of Main)
        text = text + "\n\n" + sim_block.strip()

# ===============================
# 7. VALIDATION (STRICTER)
# ===============================
def validate(code):
    return (
        START_TAG in code and
        END_TAG in code and
        PRE_TAG in code and
        len(re.findall(r"Sub\s+ApplyLearningGovernor\s*\(", code)) == 1 and
        "End Sub" in code
    )

valid = validate(text)

# ===============================
# 8. HASH
# ===============================
def hash_code(code):
    return hashlib.sha256(
        re.sub(r"\s+", "", code + version_tag).encode()
    ).hexdigest()[:16]

# ===============================
# 9. WRITE ATOMIC
# ===============================
def atomic_write(path, content):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp, path)

# ===============================
# 10. EXEC
# ===============================
if valid:
    atomic_write(file_path, text)
    print(f"{version_tag} OK | {hash_code(text)} | {datetime.now()}")
else:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(original_text)
    raise SystemExit("ENGINE_ABORT")
