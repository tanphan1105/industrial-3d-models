$inv = [System.Runtime.InteropServices.Marshal]::GetActiveObject("Inventor.Application")
$doc = $inv.ActiveDocument
$rep = $doc.ComponentDefinition.RepresentationsManager.ActiveDesignViewRepresentation
$rep | Get-Member -MemberType Properties | Out-String | Set-Content "D:\WT3D_Project\Z_Tools\rep_props.txt"
