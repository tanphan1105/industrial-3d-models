import os, re
version_tag = "V6.4.9"
START_TAG = f"' ===== {version_tag} LEARNING GOVERNOR START ====="
END_TAG   = f"' ===== {version_tag} LEARNING GOVERNOR END ====="
PRE_TAG   = f"' ===== {version_tag} PRE-FLIGHT SIMULATION ====="

with open(r'd:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb', 'r', encoding='utf-8') as f:
    text = f.read()

# Simulate execution of V6.4.9 exactly as it is in patch_v6_4_9_fixed.py
text = re.sub(
    r"' ===== V6\.\d+(?:\.\d+)? LEARNING GOVERNOR START =====[\s\S]*?' ===== V6\.\d+(?:\.\d+)? LEARNING GOVERNOR END =====",
    "",
    text
)
text = re.sub(
    r"Sub\s+ApplyLearningGovernor\s*\([\s\S]*?End Sub\s*",
    "",
    text
)
text = re.sub(
    r"' ===== V6\.\d+(?:\.\d+)? PRE-FLIGHT SIMULATION =====[\s\S]*?If RiskScore[\s\S]*?End If",
    "",
    text
)

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

if "ApplyLearningGovernor(" not in text:
    text = text.rstrip() + "\n\n" + governor.strip()

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
        text = text + "\n\n" + sim_block.strip()

print("START_TAG in text:", START_TAG in text)
print("END_TAG in text:", END_TAG in text)
print("PRE_TAG in text:", PRE_TAG in text)
print("func count:", len(re.findall(r"Sub\s+ApplyLearningGovernor\s*\(", text)))
print("End Sub in text:", "End Sub" in text)
