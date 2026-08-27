import sys
import re

file_path = r'd:\WT3D_Project\Z_Tools\MAXSKILLS_Studio_Shorts_9_16.iLogicVb'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Logic to remove duplicate 'Public Function SolveUpVector'
# We define it once clearly.
solve_vector_code = """
Public Function SolveUpVector(eyeP As Inventor.Point, tarP As Inventor.Point, tg As TransientGeometry) As Inventor.UnitVector
    Dim dirV As Inventor.Vector = tg.CreateVector(tarP.X - eyeP.X, tarP.Y - eyeP.Y, tarP.Z - eyeP.Z)
    Dim rightV As Inventor.Vector = dirV.CrossProduct(tg.CreateVector(0, 1, 0))
    If rightV.Length < 0.001 Then rightV = tg.CreateVector(1, 0, 0)
    Dim dynamicUp As Inventor.Vector = rightV.CrossProduct(dirV)
    dynamicUp.Normalize()
    Return tg.CreateUnitVector(dynamicUp.X, dynamicUp.Y, dynamicUp.Z)
End Function
"""

# Remove all occurrences of SolveUpVector function
text = re.sub(r'Public Function SolveUpVector\(.*?\r?\nEnd Function', '', text, flags=re.DOTALL)

# Re-append it clean at the end
text = text.strip() + "\n\n" + solve_vector_code.strip()

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Duplicates cleaned.")
