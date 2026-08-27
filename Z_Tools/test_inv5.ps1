$inv = [System.Runtime.InteropServices.Marshal]::GetActiveObject("Inventor.Application")
$doc = $inv.ActiveDocument
$def = $doc.ComponentDefinition
$def | Get-Member -MemberType Properties | Out-String | Set-Content "D:\WT3D_Project\Z_Tools\def_props.txt"
