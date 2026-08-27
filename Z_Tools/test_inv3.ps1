$inv = [System.Runtime.InteropServices.Marshal]::GetActiveObject("Inventor.Application")
$doc = $inv.ActiveDocument
$def = $doc.ComponentDefinition

try {
    $rep = $def.RepresentationsManager.ActiveDesignViewRepresentation
	$tg = $inv.TransientGeometry
	
	try {
	    $pt = $inv.GetType().InvokeMember("TransientGeometry", [System.Reflection.BindingFlags]::GetProperty, $null, $inv, $null).CreatePoint(0,0,10)
        $xAxis = $inv.TransientGeometry.CreateUnitVector(1,0,0)
        $yAxis = $inv.TransientGeometry.CreateUnitVector(0,1,0)
        
        $tempPlane = $def.WorkPlanes.AddFixed($pt, $xAxis, $yAxis, $true)
        Write-Host "Created Fixed WorkPlane successfully!"
	} catch {
	    Write-Host "Create fixed plane failed: " $_.Exception.Message
        exit
	}
	
	try {
	    $msv = $rep.ModelSectionViews
		$secView = $msv.AddHalfSectionView($tempPlane)
		Write-Host "Added HalfSectionView with Fixed Plane successfully!"
		$secView.Delete()
        $tempPlane.Delete()
	} catch {
	    Write-Host "Failed AddHalfSectionView: " $_.Exception.Message
        $tempPlane.Delete()
	}
} catch {
    Write-Host "Failed: " $_.Exception.Message
}
