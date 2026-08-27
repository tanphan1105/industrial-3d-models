import re

file_path = r'd:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb'

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. CLEAN UP PRE-FLIGHT BLOCKS (incl. Orphaned)
# Remove all PRE-FLIGHT blocks completely (orphaned and tagged)
text = re.sub(
    r"\n*[ \t]*If\s+RiskScore\s*>=\s*0\.9\s*Then[\s\S]*?End\s+If[ \t]*\n*",
    "\n",
    text
)
# Remove the old V6 tags that might have been left hanging
text = re.sub(r"[ \t]*' ===== V6\.\d+(?:\.\d+)? PRE-FLIGHT SIMULATION =====\n", "", text)
text = re.sub(r"[ \t]*' Layer 4: \[V6\.1\] PRE-FLIGHT RISK SIMULATION \(Shadow Mode\)\n", "", text)
text = re.sub(r"[ \t]*' \[V6\.2\] PRE-FLIGHT SIMULATION LAYER\n", "", text)

# 2. INJECT NEW PRE-FLIGHT BLOCK AT THE CORRECT LOCATION
# It must be AFTER ApplyLearningGovernor(...)
preflight_block = """
    ' ===== V6.4.12 PRE-FLIGHT SIMULATION =====
    If RiskScore >= 0.9 Then
        EngineHealthScore -= 10
        logReport.AppendLine("PRE_FLIGHT: HIGH RISK DETECTED")
    End If
"""

# Check if it was already injected
if "' ===== V6.4.12 PRE-FLIGHT SIMULATION =====" not in text:
    # Find ApplyLearningGovernor(...) call and inject after it
    text = re.sub(
        r"(\bApplyLearningGovernor\s*\([^()]+\)\s*\n)",
        r"\1" + preflight_block + "\n",
        text,
        count=1
    )

# 3. CLEAN UP DUPLICATE "[V5.0] CORE ENGINE FUNCTIONS"
core_header = (
    r"' ==============================================================================\n"
    r"' \[V5\.0\] CORE ENGINE FUNCTIONS \(Shot Governor & Anti-Gimbal\)\n"
    r"' ==============================================================================\n"
)
# Find all occurrences
matches = list(re.finditer(core_header, text))
# Only keep the last occurrence if there are multiple.
# Actually, wait. It's usually placed at the very end before the functions.
# Let's just keep the last one. Or we can strip them all and add it once before "Function SolveUpVector".
text = re.sub(core_header, "", text)

# Now, ensure it exists exactly once before SolveUpVector
if "Function SolveUpVector" in text:
    target = r"\n(Function\s+SolveUpVector\b)"
    replacement = (
        r"\n\n' ==============================================================================\n"
        r"' [V5.0] CORE ENGINE FUNCTIONS (Shot Governor & Anti-Gimbal)\n"
        r"' ==============================================================================\n\1"
    )
    text = re.sub(target, replacement, text)

# Write back
with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("MAXSKILLS cleaned up perfectly!")
