Add-Type -Path "C:\Program Files\Autodesk\Inventor 2021\Bin\Public Assemblies\Autodesk.Inventor.Interop.dll"
[Enum]::GetNames([Autodesk.Inventor.DisplayModeEnum]) | Out-String | Set-Content "D:\WT3D_Project\Z_Tools\enums.txt"
