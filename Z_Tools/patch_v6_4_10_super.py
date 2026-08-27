import os
import re
import logging
from datetime import datetime
import shutil
import hashlib

# ===============================
# CONFIG
# ===============================
file_path = r'd:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb'
version_tag = "V6.4.10"

START_TAG = f"' ===== {version_tag} LEARNING GOVERNOR START ====="
END_TAG   = f"' ===== {version_tag} LEARNING GOVERNOR END ====="
PRE_TAG   = f"' ===== {version_tag} PRE-FLIGHT SIMULATION ====="

# ===============================
# LOGGING SETUP
# ===============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("patch_engine.log", encoding="utf-8")
    ]
)
log = logging.getLogger(__name__)

# ===============================
# 0. LOAD
# ===============================
log.info(f"Loading file: {file_path}")
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

original_text = text

# ===============================
# 1. CLEAN OLD BLOCKS (SAFE SCOPED)
# ===============================
log.info("Step 1: Cleaning old blocks...")

# Remove old GOVERNOR block (versioned)
text = re.sub(
    r"' ===== V6\.\d+(?:\.\d+)? LEARNING GOVERNOR START =====[\s\S]*?' ===== V6\.\d+(?:\.\d+)? LEARNING GOVERNOR END =====\n?",
    "",
    text
)

# Remove ApplyLearningGovernor Sub (word-boundary safe)
text = re.sub(
    r"\bSub\s+ApplyLearningGovernor\s*\([\s\S]*?End Sub\s*",
    "",
    text
)

# Remove old PRE-FLIGHT block (versioned)
text = re.sub(
    r"' ===== V6\.\d+(?:\.\d+)? PRE-FLIGHT SIMULATION =====[\s\S]*?End If\n?",
    "",
    text
)

# ===============================
# 2. GOVERNOR BLOCK
# ===============================
log.info("Step 2: Preparing governor block...")

governor = f"""
{START_TAG}
Sub ApplyLearningGovernor(ByRef prof As ModelProfile, partCount As Integer, _
    ByRef rScore As Double, ByRef rPattern As String, ByRef over As Boolean)

    ' --- Weight definitions ---
    ' wDense: weight applied when profile is Dense_Piping (dominant factor)
    ' wPart:  weight applied when part count exceeds threshold (secondary factor)
    Dim wDense As Double = 0.6
    Dim wPart  As Double = 0.4

    rScore = 0.0
    over   = False
    rPattern = ""

    If prof.Name = "Dense_Piping" Then rScore += wDense
    If partCount > 450 Then rScore += wPart

    If rScore >= 0.7 Then
        prof.AllowDeepZoom = False
        prof.MaxAngularSpeed *= 0.8
        over     = True
        rPattern = "DENSE_PIPE_HIGH_PART"
    End If

End Sub
{END_TAG}
"""

# Inject only if Sub is missing (strict detection)
if not re.search(r"\bSub\s+ApplyLearningGovernor\s*\(", text):
    text = text.rstrip() + "\n\n" + governor.strip()
    log.info("Governor block injected.")
else:
    log.info("Governor block already present, skipping inject.")

# ===============================
# 3. SAFE CALL PATCH (NORMALIZE WHITESPACE)
# ===============================
log.info("Step 3: Normalizing ApplyLearningGovernor call sites...")

# Normalize: collapse extra whitespace between args in call sites
text = re.sub(
    r"\bApplyLearningGovernor\s*\(\s*([^()\n]+?)\s*\)",
    lambda m: "ApplyLearningGovernor(" + re.sub(r"\s*,\s*", ", ", m.group(1).strip()) + ")",
    text
)

# ===============================
# 4. PRE-FLIGHT INJECTION (SUB-AWARE SAFE)
# ===============================
log.info("Step 4: Injecting pre-flight simulation block...")

sim_block = f"""
    {PRE_TAG}
    If RiskScore >= 0.9 Then
        EngineHealthScore -= 10
        logReport.AppendLine("PRE_FLIGHT: HIGH RISK DETECTED")
    End If
"""

def find_sub_end(code: str, sub_start: int) -> int:
    """
    From sub_start, walk line-by-line tracking Sub/End Sub nesting depth.
    Returns the index of the matching 'End Sub', or -1 if not found.
    Fixes the naive code.find("End Sub") which could match a wrong End Sub.
    """
    depth = 0
    pos = sub_start
    lines = code[sub_start:].splitlines(keepends=True)
    cursor = sub_start

    for line in lines:
        stripped = line.strip()
        # count Sub openings (exclude End Sub, Function, etc.)
        if re.match(r'\bSub\s+\w+', stripped) and not stripped.startswith("End"):
            depth += 1
        if re.match(r'\bEnd\s+Sub\b', stripped):
            depth -= 1
            if depth == 0:
                return cursor + len(line)
        cursor += len(line)

    return -1


def inject_preflight(code: str) -> str:
    if PRE_TAG in code:
        log.info("Pre-flight block already present, skipping inject.")
        return code

    # Find Sub Main with word boundary to avoid matching Sub MainSetup etc.
    match = re.search(r'\bSub\s+Main\b', code)

    if match:
        sub_start = match.start()
        sub_end   = find_sub_end(code, sub_start)

        if sub_end != -1:
            sub_block   = code[sub_start:sub_end]
            # Insert sim_block right after "Sub Main" header line
            header_end  = sub_block.index("\n") + 1
            injected    = sub_block[:header_end] + sim_block + sub_block[header_end:]
            result      = code[:sub_start] + injected + code[sub_end:]
            log.info("Pre-flight block injected inside Sub Main.")
            return result
        else:
            log.warning("Could not find matching End Sub for Sub Main. Falling back to append.")
    else:
        log.warning("Sub Main not found. Falling back to append.")

    return code + "\n\n" + sim_block.strip()


text = inject_preflight(text)

# ===============================
# 5. VALIDATION (STRICT REAL CHECK)
# ===============================
log.info("Step 5: Validating patched code...")

def validate(code: str) -> bool:
    # Must have exactly 1 ApplyLearningGovernor Sub
    func_blocks = len(re.findall(r"\bSub\s+ApplyLearningGovernor\s*\(", code))

    has_start = START_TAG in code
    has_end   = END_TAG in code
    has_pre   = PRE_TAG in code

    # Nesting-aware Sub/End Sub balance check
    sub_opens  = len(re.findall(r'^\s*Sub\s+\w+', code, re.MULTILINE))
    sub_closes = len(re.findall(r'^\s*End\s+Sub\b', code, re.MULTILINE))
    balanced   = (sub_opens == sub_closes)

    # Structural pairing: find ApplyLearningGovernor, then its matching End Sub
    gov_match = re.search(r"\bSub\s+ApplyLearningGovernor\s*\(", code)
    if gov_match:
        end_idx = find_sub_end(code, gov_match.start())
        correct_structure = (end_idx != -1)
    else:
        correct_structure = False

    results = {
        "func_blocks == 1": func_blocks == 1,
        "has_start":        has_start,
        "has_end":          has_end,
        "has_pre":          has_pre,
        "sub_balanced":     balanced,
        "correct_structure":correct_structure,
    }

    for check, passed in results.items():
        status = "OK" if passed else "FAIL"
        log.info(f"  Validate [{status}] {check}")

    return all(results.values())


valid = validate(text)

# ===============================
# 6. WRITE SAFELY (ATOMIC)
# ===============================
def write_atomic(path: str, content: str) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp, path)
    log.info(f"File written atomically: {path}")

# ===============================
# 7. EXECUTION GATE
# ===============================
if valid:
    write_atomic(file_path, text)
    log.info(f"{version_tag} PATCH OK ✓")
    print(f"{version_tag} PATCH OK")
else:
    # Rollback: restore original content
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(original_text)
    log.error("ENGINE_ABORT: INVALID STRUCTURE — original file restored.")
    raise SystemExit("ENGINE_ABORT: INVALID STRUCTURE")
