import os
import re
import sys
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
# Resolve log path safely even if file_path has no directory component
_file_dir = os.path.dirname(os.path.abspath(file_path))
log_file  = os.path.join(_file_dir, "patch_engine.log")

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
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp, path)
        log.info(f"File written atomically: {path}")
    except Exception as e:
        # Clean up orphaned .tmp if replace failed
        if os.path.exists(tmp):
            os.remove(tmp)
        raise RuntimeError(f"Atomic write failed: {e}") from e


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


# VB line patterns — compiled once, reused everywhere
_RE_SUB_OPEN  = re.compile(
    r'^(?:Private\s+|Public\s+|Friend\s+)?Sub\s+\w+', re.IGNORECASE
)
_RE_SUB_END   = re.compile(r'^End\s+Sub\b', re.IGNORECASE)
_RE_COMMENT   = re.compile(r"^\s*'")          # VB line comment


def _is_code_line(line: str) -> bool:
    """Return True if line is not a VB comment."""
    return not _RE_COMMENT.match(line)


def find_sub_end(code: str, sub_start: int) -> int:
    """
    Walk line-by-line from sub_start tracking Sub/End Sub nesting depth.
    Skips comment lines to avoid false matches like: ' Sub Helper()
    Handles Private/Public/Friend Sub.
    Returns the end index (exclusive) after the matching 'End Sub' line,
    or -1 if not found.
    """
    depth  = 0
    cursor = sub_start

    for line in code[sub_start:].splitlines(keepends=True):
        stripped = line.strip()

        if _is_code_line(stripped):
            if _RE_SUB_OPEN.match(stripped) and not _RE_SUB_END.match(stripped):
                depth += 1
            elif _RE_SUB_END.match(stripped):
                depth -= 1
                if depth == 0:
                    return cursor + len(line)

        cursor += len(line)

    return -1


def remove_sub(code: str, sub_name: str) -> str:
    """
    Remove a named Sub block using nesting-aware end detection.
    Handles optional Private/Public/Friend accessor.
    """
    pattern = re.compile(
        rf'\b(?:Private\s+|Public\s+|Friend\s+)?Sub\s+{re.escape(sub_name)}\s*\(',
        re.IGNORECASE
    )
    match = pattern.search(code)
    if not match:
        log.info(f"Sub '{sub_name}' not found, nothing to remove.")
        return code

    sub_start = match.start()
    sub_end   = find_sub_end(code, sub_start)

    if sub_end == -1:
        log.warning(f"Could not find End Sub for '{sub_name}', skipping removal.")
        return code

    # Consume one trailing newline if present
    if sub_end < len(code) and code[sub_end] == "\n":
        sub_end += 1

    log.info(f"Removed Sub '{sub_name}' (chars {sub_start}–{sub_end})")
    return code[:sub_start] + code[sub_end:]


def inject_preflight(code: str, block: str, pre_tag: str) -> str:
    """
    Inject pre-flight simulation block into Sub Main (nesting-aware).
    Falls back to appending at end-of-file if Sub Main is absent.
    Preserves indentation — does NOT strip the block.
    """
    if pre_tag in code:
        log.info("Pre-flight block already present, skipping inject.")
        return code

    match = re.search(r'\bApplyLearningGovernor\s*\(.*?\)', code, re.IGNORECASE)

    if match:
        insert_idx = code.find("\n", match.end())
        if insert_idx != -1:
            insert_idx += 1
            injected   = code[:insert_idx] + block + code[insert_idx:]
            log.info("Pre-flight block injected after ApplyLearningGovernor.")
            return injected

        log.warning("Could not find newline after ApplyLearningGovernor. Falling back to append.")
    else:
        log.warning("ApplyLearningGovernor call not found. Falling back to append.")

    # Fallback: append without stripping (preserve indent structure)
    return code.rstrip("\n") + "\n\n" + block.rstrip("\n") + "\n"


def validate(code: str, start_tag: str, end_tag: str, pre_tag: str) -> bool:
    """
    Strict structural validation of patched VB code.
    Checks: tag presence, Sub count, Sub/End Sub balance, structural pairing.
    """
    # 1. Exactly 1 ApplyLearningGovernor Sub
    func_blocks = len(re.findall(
        r'\b(?:Private\s+|Public\s+|Friend\s+)?Sub\s+ApplyLearningGovernor\s*\(',
        code, re.IGNORECASE
    ))

    # 2. All version tags present
    has_start = start_tag in code
    has_end   = end_tag   in code
    has_pre   = pre_tag   in code

    # 3. Sub / End Sub balance — skip comment lines
    code_lines  = [ln for ln in code.splitlines() if _is_code_line(ln)]
    code_body   = "\n".join(code_lines)

    sub_opens   = len(re.findall(
        r'^\s*(?:Private\s+|Public\s+|Friend\s+)?Sub\s+\w+\b',
        code_body, re.MULTILINE | re.IGNORECASE
    ))
    sub_closes  = len(re.findall(
        r'^\s*End\s+Sub\b', code_body, re.MULTILINE | re.IGNORECASE
    ))
    balanced    = (sub_opens == sub_closes)

    # 4. ApplyLearningGovernor has a proper matching End Sub
    gov_match = re.search(
        r'\b(?:Private\s+|Public\s+|Friend\s+)?Sub\s+ApplyLearningGovernor\s*\(',
        code, re.IGNORECASE
    )
    correct_structure = False
    if gov_match:
        end_idx           = find_sub_end(code, gov_match.start())
        correct_structure = (end_idx != -1)

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


# ===============================
# 0. LOAD
# ===============================
log.info("=" * 50)
log.info(f"Patch Engine {version_tag} starting...")
log.info(f"Target file : {file_path}")

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

original_text     = text
original_checksum = checksum(original_text)
log.info(f"Original checksum: {original_checksum}")

# ===============================
# 1. BACKUP
# ===============================
backup_path = backup_file(file_path)

# ===============================
# 2. CLEAN OLD BLOCKS
# ===============================
log.info("Step 2: Cleaning old blocks...")

# Remove old GOVERNOR block (any V6.x.x version tag)
text = re.sub(
    r"' ===== V6\.\d+(?:\.\d+)? LEARNING GOVERNOR START =====[\s\S]*?"
    r"' ===== V6\.\d+(?:\.\d+)? LEARNING GOVERNOR END =====\n?",
    "",
    text
)

# Remove ApplyLearningGovernor Sub (nesting-aware)
text = remove_sub(text, "ApplyLearningGovernor")

# Remove old PRE-FLIGHT block (any indent: spaces or tabs, any V6.x.x)
text = re.sub(
    r"[ \t]*' ===== V6\.\d+(?:\.\d+)? PRE-FLIGHT SIMULATION =====[\s\S]*?End If[ \t]*\n?",
    "",
    text
)

# Remove orphaned PRE-FLIGHT blocks (without comment tags)
text = re.sub(
    r"\n*[ \t]*If\s+RiskScore\s*>=\s*0\.9\s*Then[\s\S]*?End\s+If[ \t]*\n*",
    "\n",
    text
)

# ===============================
# 3. INJECT GOVERNOR BLOCK
# ===============================
log.info("Step 3: Preparing and injecting governor block...")

governor = (
    f"\n{START_TAG}\n"
    f"Sub ApplyLearningGovernor(ByRef prof As ModelProfile, partCount As Integer, _\n"
    f"    ByRef rScore As Double, ByRef rPattern As String, ByRef over As Boolean)\n"
    f"\n"
    f"    ' --- Weight definitions ---\n"
    f"    ' wDense : weight applied when profile is Dense_Piping (dominant factor)\n"
    f"    ' wPart  : weight applied when part count exceeds threshold (secondary factor)\n"
    f"    Dim wDense As Double = 0.6\n"
    f"    Dim wPart  As Double = 0.4\n"
    f"\n"
    f"    rScore   = 0.0\n"
    f"    over     = False\n"
    f"    rPattern = \"\"\n"
    f"\n"
    f"    If prof.Name = \"Dense_Piping\" Then rScore += wDense\n"
    f"    If partCount > 450            Then rScore += wPart\n"
    f"\n"
    f"    If rScore >= 0.7 Then\n"
    f"        prof.AllowDeepZoom    = False\n"
    f"        prof.MaxAngularSpeed *= 0.8\n"
    f"        over     = True\n"
    f"        rPattern = \"DENSE_PIPE_HIGH_PART\"\n"
    f"    End If\n"
    f"\n"
    f"End Sub\n"
    f"{END_TAG}\n"
)

pattern_gov = re.compile(
    r'\b(?:Private\s+|Public\s+|Friend\s+)?Sub\s+ApplyLearningGovernor\s*\(',
    re.IGNORECASE
)
if not pattern_gov.search(text):
    text = text.rstrip("\n") + "\n\n" + governor.strip() + "\n"
    log.info("Governor block injected.")
else:
    log.info("Governor block already present, skipping inject.")

# ===============================
# 4. NORMALIZE CALL SITES
# ===============================
log.info("Step 4: Normalizing ApplyLearningGovernor call sites...")

text = re.sub(
    r"\bApplyLearningGovernor\s*\(\s*([^()\n]+?)\s*\)",
    lambda m: "ApplyLearningGovernor("
              + re.sub(r"\s*,\s*", ", ", m.group(1).strip())
              + ")",
    text
)

# ===============================
# 5. INJECT PRE-FLIGHT BLOCK
# ===============================
log.info("Step 5: Injecting pre-flight simulation block...")

# Preserve 4-space indent — do NOT strip when appending as fallback
sim_block = (
    f"\n"
    f"    {PRE_TAG}\n"
    f"    If RiskScore >= 0.9 Then\n"
    f"        EngineHealthScore -= 10\n"
    f'        logReport.AppendLine("PRE_FLIGHT: HIGH RISK DETECTED")\n'
    f"    End If\n"
)

text = inject_preflight(text, sim_block, PRE_TAG)

# ===============================
# 6. VALIDATION
# ===============================
log.info("Step 6: Validating patched code...")
valid = validate(text, START_TAG, END_TAG, PRE_TAG)

# ===============================
# 7. EXECUTION GATE
# ===============================
if valid:
    patched_checksum = checksum(text)
    write_atomic(file_path, text)
    log.info(f"Patched checksum : {patched_checksum}")
    log.info(f"{version_tag} PATCH OK \u2713")
    print(f"{version_tag} PATCH OK")
    sys.exit(0)
else:
    write_atomic(file_path, original_text)
    restored_checksum = checksum(original_text)
    log.error("ENGINE_ABORT: INVALID STRUCTURE")
    log.error(f"Original file restored. Checksum : {restored_checksum}")
    log.error(f"Backup retained at              : {backup_path}")
    raise SystemExit("ENGINE_ABORT: INVALID STRUCTURE")
