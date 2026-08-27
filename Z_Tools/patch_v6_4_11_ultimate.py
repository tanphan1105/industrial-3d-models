import os
import re
import logging
import shutil
import hashlib
from datetime import datetime

# ===============================
# CONFIG
# ===============================
file_path   = r'd:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb'
version_tag = "V6.4.11"

START_TAG = f"' ===== {version_tag} LEARNING GOVERNOR START ====="
END_TAG   = f"' ===== {version_tag} LEARNING GOVERNOR END ====="
PRE_TAG   = f"' ===== {version_tag} PRE-FLIGHT SIMULATION ====="

# ===============================
# LOGGING SETUP
# ===============================
log_file = os.path.join(os.path.dirname(file_path), "patch_engine.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file, encoding="utf-8")
    ]
)
log = logging.getLogger(__name__)

# ===============================
# HELPERS
# ===============================

def checksum(content: str) -> str:
    """SHA-256 checksum of string content."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def write_atomic(path: str, content: str) -> None:
    """
    Write content to path atomically via a .tmp file.
    Prevents file corruption if process crashes mid-write.
    """
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp, path)
    log.info(f"File written atomically: {path}")


def backup_file(path: str) -> str:
    """
    Create a timestamped backup of the file before patching.
    Returns the backup path.
    """
    ts          = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{path}.{version_tag}.{ts}.bak"
    shutil.copy2(path, backup_path)
    log.info(f"Backup created: {backup_path}")
    return backup_path


def find_sub_end(code: str, sub_start: int) -> int:
    """
    From sub_start, walk line-by-line tracking Sub/End Sub nesting depth.
    Handles Private Sub, Public Sub, Protected Sub correctly.
    Returns the end index (exclusive) of the matching 'End Sub' line,
    or -1 if not found.
    """
    depth  = 0
    cursor = sub_start
    lines  = code[sub_start:].splitlines(keepends=True)

    for line in lines:
        stripped = line.strip()

        # Match Sub openings: optional accessor + Sub keyword
        # Covers: Sub, Private Sub, Public Sub, Friend Sub
        if (re.match(r'^(?:Private\s+|Public\s+|Friend\s+)?Sub\s+\w+', stripped)
                and not re.match(r'^End\s+Sub\b', stripped)):
            depth += 1

        if re.match(r'^End\s+Sub\b', stripped):
            depth -= 1
            if depth == 0:
                return cursor + len(line)

        cursor += len(line)

    return -1


# ===============================
# 0. LOAD
# ===============================
log.info(f"{'='*50}")
log.info(f"Patch Engine {version_tag} starting...")
log.info(f"Target file: {file_path}")

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

original_text     = text
original_checksum = checksum(original_text)
log.info(f"Original file checksum: {original_checksum}")

# ===============================
# 1. BACKUP
# ===============================
backup_path = backup_file(file_path)

# ===============================
# 2. CLEAN OLD BLOCKS (SAFE SCOPED)
# ===============================
log.info("Step 2: Cleaning old blocks...")

# Remove old GOVERNOR block (versioned, any V6.x.x)
text = re.sub(
    r"' ===== V6\.\d+(?:\.\d+)? LEARNING GOVERNOR START =====[\s\S]*?"
    r"' ===== V6\.\d+(?:\.\d+)? LEARNING GOVERNOR END =====\n?",
    "",
    text
)

# Remove ApplyLearningGovernor Sub using nesting-aware find_sub_end
# First locate it, then slice it out cleanly
def remove_sub(code: str, sub_name: str) -> str:
    """Remove a named Sub block using nesting-aware end detection."""
    pattern = rf'\b(?:Private\s+|Public\s+|Friend\s+)?Sub\s+{re.escape(sub_name)}\s*\('
    match   = re.search(pattern, code)
    if not match:
        return code
    sub_start = match.start()
    sub_end   = find_sub_end(code, sub_start)
    if sub_end == -1:
        log.warning(f"Could not find End Sub for '{sub_name}', skipping removal.")
        return code
    # Strip the trailing newline after End Sub if present
    if sub_end < len(code) and code[sub_end] == "\n":
        sub_end += 1
    log.info(f"Removed Sub '{sub_name}' (chars {sub_start}–{sub_end})")
    return code[:sub_start] + code[sub_end:]

text = remove_sub(text, "ApplyLearningGovernor")

# Remove old PRE-FLIGHT block (versioned, any V6.x.x)
text = re.sub(
    r"    ' ===== V6\.\d+(?:\.\d+)? PRE-FLIGHT SIMULATION =====[\s\S]*?End If\n?",
    "",
    text
)

# ===============================
# 3. GOVERNOR BLOCK
# ===============================
log.info("Step 3: Preparing and injecting governor block...")

governor = f"""
{START_TAG}
Sub ApplyLearningGovernor(ByRef prof As ModelProfile, partCount As Integer, _
    ByRef rScore As Double, ByRef rPattern As String, ByRef over As Boolean)

    ' --- Weight definitions ---
    ' wDense : weight applied when profile is Dense_Piping (dominant factor)
    ' wPart  : weight applied when part count exceeds threshold (secondary factor)
    Dim wDense As Double = 0.6
    Dim wPart  As Double = 0.4

    rScore   = 0.0
    over     = False
    rPattern = ""

    If prof.Name = "Dense_Piping" Then rScore += wDense
    If partCount > 450            Then rScore += wPart

    If rScore >= 0.7 Then
        prof.AllowDeepZoom    = False
        prof.MaxAngularSpeed *= 0.8
        over     = True
        rPattern = "DENSE_PIPE_HIGH_PART"
    End If

End Sub
{END_TAG}
"""

# Inject only if Sub is missing (strict detection)
pattern_gov = r'\b(?:Private\s+|Public\s+|Friend\s+)?Sub\s+ApplyLearningGovernor\s*\('
if not re.search(pattern_gov, text):
    text = text.rstrip() + "\n\n" + governor.strip() + "\n"
    log.info("Governor block injected.")
else:
    log.info("Governor block already present, skipping inject.")

# ===============================
# 4. SAFE CALL PATCH (NORMALIZE WHITESPACE)
# ===============================
log.info("Step 4: Normalizing ApplyLearningGovernor call sites...")

# Normalize whitespace around commas in all call sites
text = re.sub(
    r"\bApplyLearningGovernor\s*\(\s*([^()\n]+?)\s*\)",
    lambda m: "ApplyLearningGovernor("
              + re.sub(r"\s*,\s*", ", ", m.group(1).strip())
              + ")",
    text
)

# ===============================
# 5. PRE-FLIGHT INJECTION (NESTING-AWARE)
# ===============================
log.info("Step 5: Injecting pre-flight simulation block...")

sim_block = (
    f"\n"
    f"    {PRE_TAG}\n"
    f"    If RiskScore >= 0.9 Then\n"
    f"        EngineHealthScore -= 10\n"
    f'        logReport.AppendLine("PRE_FLIGHT: HIGH RISK DETECTED")\n'
    f"    End If\n"
)

def inject_preflight(code: str) -> str:
    if PRE_TAG in code:
        log.info("Pre-flight block already present, skipping inject.")
        return code

    # Find Sub Main with strict word boundary
    match = re.search(r'\bSub\s+Main\b', code)

    if match:
        sub_start = match.start()
        sub_end   = find_sub_end(code, sub_start)

        if sub_end != -1:
            sub_block  = code[sub_start:sub_end]
            header_end = sub_block.index("\n") + 1
            injected   = sub_block[:header_end] + sim_block + sub_block[header_end:]
            log.info("Pre-flight block injected inside Sub Main.")
            return code[:sub_start] + injected + code[sub_end:]
        else:
            log.warning("Could not find matching End Sub for Sub Main. Falling back to append.")
    else:
        log.warning("Sub Main not found. Falling back to append.")

    return code + "\n\n" + sim_block.strip()

text = inject_preflight(text)

# ===============================
# 6. VALIDATION (STRICT)
# ===============================
log.info("Step 6: Validating patched code...")

def validate(code: str) -> bool:
    # 1. Exactly 1 ApplyLearningGovernor Sub
    func_blocks = len(re.findall(
        r'\b(?:Private\s+|Public\s+|Friend\s+)?Sub\s+ApplyLearningGovernor\s*\(',
        code
    ))

    # 2. All version tags present
    has_start = START_TAG in code
    has_end   = END_TAG   in code
    has_pre   = PRE_TAG   in code

    # 3. Sub / End Sub balance (handles Private/Public/Friend Sub)
    sub_opens  = len(re.findall(
        r'^\s*(?:Private\s+|Public\s+|Friend\s+)?Sub\s+\w+',
        code, re.MULTILINE
    ))
    sub_closes = len(re.findall(r'^\s*End\s+Sub\b', code, re.MULTILINE))
    balanced   = (sub_opens == sub_closes)

    # 4. ApplyLearningGovernor has a proper matching End Sub
    gov_match = re.search(
        r'\b(?:Private\s+|Public\s+|Friend\s+)?Sub\s+ApplyLearningGovernor\s*\(',
        code
    )
    if gov_match:
        end_idx           = find_sub_end(code, gov_match.start())
        correct_structure = (end_idx != -1)
    else:
        correct_structure = False

    results = {
        "func_blocks == 1":  func_blocks == 1,
        "has_start_tag":     has_start,
        "has_end_tag":       has_end,
        "has_pre_tag":       has_pre,
        "sub_end_balanced":  balanced,
        "correct_structure": correct_structure,
    }

    all_pass = True
    for check, passed in results.items():
        status = "OK  " if passed else "FAIL"
        log.info(f"  [{status}] {check}")
        if not passed:
            all_pass = False

    return all_pass

valid = validate(text)

# ===============================
# 7. EXECUTION GATE
# ===============================
if valid:
    patched_checksum = checksum(text)
    write_atomic(file_path, text)
    log.info(f"Patched file checksum : {patched_checksum}")
    log.info(f"{version_tag} PATCH OK \u2713")
    print(f"{version_tag} PATCH OK")
else:
    # Rollback atomically — avoid plain open() which can corrupt on crash
    write_atomic(file_path, original_text)
    restored_checksum = checksum(original_text)
    log.error("ENGINE_ABORT: INVALID STRUCTURE")
    log.error(f"Original file restored. Checksum: {restored_checksum}")
    log.error(f"Backup retained at: {backup_path}")
    raise SystemExit("ENGINE_ABORT: INVALID STRUCTURE")
