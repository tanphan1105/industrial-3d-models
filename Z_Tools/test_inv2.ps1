try {
    $inv = [System.Runtime.InteropServices.Marshal]::GetActiveObject("Inventor.Application")
    $doc = $inv.ActiveDocument
    $def = $doc.ComponentDefinition
    $rep = $def.RepresentationsManager.ActiveDesignViewRepresentation
	$tg = $inv.TransientGeometry
	
	try {
	    $pt = $inv.GetType().InvokeMember("TransientGeometry", [System.Reflection.BindingFlags]::GetProperty, $null, $inv, $null).CreatePoint(0,0,10)
        $vec = $inv.TransientGeometry.CreateUnitVector(0,0,1)
        $mathPlane = $inv.TransientGeometry.CreatePlane($pt, $vec)
	} catch {
	    Write-Host "Create plane failed: " $_.Exception.Message
        exit
	}
	
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
