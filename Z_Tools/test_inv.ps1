$inv = [System.Runtime.InteropServices.Marshal]::GetActiveObject("Inventor.Application")
$doc = $inv.ActiveDocument
$def = $doc.ComponentDefinition

try {
    $rep = $def.RepresentationsManager.ActiveDesignViewRepresentation
	$tg = $inv.TransientGeometry
	
	$mathPlane = $tg.CreatePlane($tg.CreatePoint(0,0,10), $tg.CreateUnitVector(0,0,1))
	
	try {
	    $msv = $rep.ModelSectionViews
		$secView = $msv.AddHalfSectionView($mathPlane)
		Write-Host "Added HalfSectionView with Math Plane successfully!"
		$secView.Delete()
	} catch {
	    Write-Host "Failed AddHalfSectionView with Math Plane: " $_.Exception.Message
	}
} catch {
    Write-Host "Failed: " $_.Exception.Message
}
