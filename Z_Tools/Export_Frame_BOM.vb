' ==============================================================================
' iLogic Rule: TỔNG HỢP VÀ CHI TIẾT CẮT THÉP HÌNH (MẶC ĐỊNH ĐỘ DÀY T = 1.5)
' File name: Export_Frame_BOM.vb
' Vị trí: D:\WT3D_Project\Z_Tools\Export_Frame_BOM.vb
' ==============================================================================

Sub Main()
    ' 1. Kiem tra moi truong chay Rule
    Dim oDoc As Document = ThisApplication.ActiveDocument
    If oDoc.DocumentType <> DocumentTypeEnum.kAssemblyDocumentObject Then
        MessageBox.Show("Vui long chay Rule nay trong moi truong Assembly (.iam)!", "iLogic Canh bao", MessageBoxButtons.OK, MessageBoxIcon.Warning)
        Return
    End If
    
    Dim oAssyDoc As AssemblyDocument = oDoc
    Dim oCompDef As AssemblyComponentDefinition = oAssyDoc.ComponentDefinition
    
    ' Dictionary 1: Gom nhom tong hop (Key = W | H | T | Vat lieu | Ty trong)
    Dim summaryDict As New System.Collections.Generic.Dictionary(Of String, Double())
    
    ' Dictionary 2: Chi tiet tung doan cat (Key = W | H | T | Vat lieu | Ty trong | Chieu dai cat)
    Dim cutListDict As New System.Collections.Generic.Dictionary(Of String, Double())
    
    ' 2. Duyet de quy qua toan bo mo hinh lap rap
    For Each oOcc As ComponentOccurrence In oCompDef.Occurrences
        ProcessOccurrence(oOcc, summaryDict, cutListDict)
    Next
    
    ' 3. Xuat ket qua ra Excel (Gom 2 Sheet va dinh dang kho in A4)
    ExportToExcel(summaryDict, cutListDict, oAssyDoc)
End Sub

''' <summary>
''' Duyet de quy qua cac linh kien (Occurrence)
''' </summary>
Sub ProcessOccurrence(oOcc As ComponentOccurrence, ByRef summaryDict As System.Collections.Generic.Dictionary(Of String, Double()), ByRef cutListDict As System.Collections.Generic.Dictionary(Of String, Double()))
    ' --- BỘ LỌC POKA-YOKE ---
    If oOcc.Suppressed Then Return
    If Not oOcc.Visible Then Return
    If oOcc.BOMStructure = Inventor.BOMStructureEnum.kReferenceBOMStructure Then Return
    
    ' Neu la Sub-Assembly, duyet sau xuong cac cap con
    If oOcc.DefinitionDocumentType = DocumentTypeEnum.kAssemblyDocumentObject Then
        For Each oSubOcc As ComponentOccurrence In oOcc.SubOccurrences
            ProcessOccurrence(oSubOcc, summaryDict, cutListDict)
        Next
        Return
    End If
    
    ' Neu la Part (.ipt), tien hanh kiem tra thong tin thep hinh
    If oOcc.DefinitionDocumentType = DocumentTypeEnum.kPartDocumentObject Then
        Dim oPartDoc As PartDocument = oOcc.Definition.Document
        Dim oPartDef As PartComponentDefinition = oPartDoc.ComponentDefinition
        
        Dim partNum As String = ""
        Dim stockNum As String = ""
        Dim desc As String = ""
        Dim mat As String = ""
        
        Dim oDesignProps As PropertySet = oPartDoc.PropertySets.Item("Design Tracking Properties")
        
        Try : partNum = oDesignProps.Item("Part Number").Value : Catch : End Try
        Try : stockNum = oDesignProps.Item("Stock Number").Value : Catch : End Try
        Try : desc = oDesignProps.Item("Description").Value : Catch : End Try
        Try : mat = oDesignProps.Item("Material").Value : Catch : End Try
        
        If partNum Is Nothing Then partNum = ""
        If stockNum Is Nothing Then stockNum = ""
        If desc Is Nothing Then desc = ""
        If mat Is Nothing Then mat = ""
        
        ' --- MẶC ĐỊNH VẬT LIỆU INOX 304 NẾU KHÔNG CÓ HOẶC LÀ GENERIC ---
        Dim matLower As String = mat.ToLower().Trim()
        If String.IsNullOrEmpty(matLower) OrElse matLower = "generic" OrElse matLower = "default" OrElse matLower = "vật liệu chung" OrElse matLower = "vat lieu chung" Then
            mat = "Inox 304"
            matLower = "inox 304"
        End If
        
        ' --- TÍNH TỶ TRỌNG CHÍNH XÁC TUYỆT ĐỐI (DENSITY IN g/cm3) ---
        Dim density As Double = 7.93 ' Mac dinh inox
        Try
            Dim massProps = oPartDoc.ComponentDefinition.MassProperties
            Dim partMass As Double = massProps.Mass ' kg
            Dim partVolume As Double = massProps.Volume ' cm3
            
            If partVolume > 0 Then
                density = (partMass * 1000.0) / partVolume
                density = Math.Round(density, 3)
            End If
        Catch
            If matLower.Contains("steel") Then
                density = 7.85
            Else
                density = 7.93
            End If
        End Try
        
        ' Kiem tra xem co phai cau kien Thep hinh (Frame Generator) khong
        Dim length As Double = 0
        Dim isFrame As Boolean = False
        
        ' Kiem tra trong bang Parameters truoc (G_L)
        Try
            Dim oParam As Parameter = oPartDef.Parameters.Item("G_L")
            length = oParam.Value * 10 ' cm sang mm
            isFrame = True
        Catch
            ' Kiem tra Custom iProperties (G_L)
            Try
                Dim oCustomProps As PropertySet = oPartDoc.PropertySets.Item("Inventor User Defined Properties")
                Dim oProp As Inventor.Property = oCustomProps.Item("G_L")
                Dim valStr As String = oProp.Value.ToString().Replace(",", ".")
                length = Double.Parse(valStr, System.Globalization.CultureInfo.InvariantCulture)
                isFrame = True
            Catch
            End Try
        End Try
        
        ' Neu xac dinh dung la Thép hình
        If isFrame Then
            Dim profileName As String = stockNum
            If String.IsNullOrEmpty(profileName) Then profileName = desc
            If String.IsNullOrEmpty(profileName) Then profileName = partNum
            
            ' Parse kich thuoc Rong (W), Cao (H), Do day (T) tu ten tiet dien
            Dim W As Double = 0
            Dim H As Double = 0
            Dim T As Double = 0
            Dim parsed As Boolean = ParseProfile(profileName, W, H, T)
            
            ' --- MẶC ĐỊNH ĐỘ DÀY LÀ 1.5 nếu không parse được hoặc độ dày bằng 0 ---
            If T <= 0 Then T = 1.5
            
            ' A. Gom nhom tong hop
            ' Key: W | H | T | Material | Density
            Dim summaryKey As String = W.ToString(System.Globalization.CultureInfo.InvariantCulture) & "|" & _
                                       H.ToString(System.Globalization.CultureInfo.InvariantCulture) & "|" & _
                                       T.ToString(System.Globalization.CultureInfo.InvariantCulture) & "|" & _
                                       mat & "|" & _
                                       density.ToString(System.Globalization.CultureInfo.InvariantCulture)
            Dim summaryValues() As Double = Nothing
            If summaryDict.TryGetValue(summaryKey, summaryValues) Then
                summaryValues(0) += 1.0 ' So luong
                summaryValues(1) += length ' Tong chieu dai
            Else
                summaryValues = New Double() {1.0, length}
                summaryDict.Add(summaryKey, summaryValues)
            End If
            
            ' B. Gom nhom chi tiet cat
            ' Key: W | H | T | Material | Density | Length
            Dim roundedLength As Double = Math.Round(length, 1)
            Dim cutKey As String = W.ToString(System.Globalization.CultureInfo.InvariantCulture) & "|" & _
                                   H.ToString(System.Globalization.CultureInfo.InvariantCulture) & "|" & _
                                   T.ToString(System.Globalization.CultureInfo.InvariantCulture) & "|" & _
                                   mat & "|" & _
                                   density.ToString(System.Globalization.CultureInfo.InvariantCulture) & "|" & _
                                   roundedLength.ToString(System.Globalization.CultureInfo.InvariantCulture)
            Dim cutValues() As Double = Nothing
            If cutListDict.TryGetValue(cutKey, cutValues) Then
                cutValues(0) += 1.0 ' Tang so luong doan
            Else
                cutValues = New Double() {1.0}
                cutListDict.Add(cutKey, cutValues)
            End If
        End If
    End If
End Sub

''' <summary>
''' Khoi tao Excel va ghi du lieu tong hop & chi tiet cat vao 2 tab, thiet lap in A4
''' </summary>
Sub ExportToExcel(ByRef summaryDict As System.Collections.Generic.Dictionary(Of String, Double()), ByRef cutListDict As System.Collections.Generic.Dictionary(Of String, Double()), oAssyDoc As AssemblyDocument)
    If summaryDict.Count = 0 Then
        MessageBox.Show("Khong tim thay cau kien thep hinh (Frame Generator) nao trong cum lap rap nay!", "Thong bao", MessageBoxButtons.OK, MessageBoxIcon.Information)
        Return
    End If
    
    Dim excelApp As Object = Nothing
    Dim workbook As Object = Nothing
    
    Dim profileNameOnly As String = ""
    Dim rowColor As Integer = 15
    
    Try
        excelApp = CreateObject("Excel.Application")
        excelApp.Visible = True
        workbook = excelApp.Workbooks.Add
        
        ' Palette mau 5S cho tung tiet dien
        Dim profileColorMap As New System.Collections.Generic.Dictionary(Of String, Integer)
        Dim colorPalette() As Integer = New Integer() {34, 35, 40, 39, 38, 24} 
        Dim colorIndex As Integer = 0
        
        ' --- TAB 1: TỔNG HỢP ---
        Dim worksheet1 As Object = workbook.Sheets(1)
        worksheet1.Name = "Tong Hop"
        
        worksheet1.Cells(1, 1).Value = "STT"
        worksheet1.Cells(1, 2).Value = "Tiet Dien Thép"
        worksheet1.Cells(1, 3).Value = "Vat Lieu"
        worksheet1.Cells(1, 4).Value = "Chieu Rong W (mm)"
        worksheet1.Cells(1, 5).Value = "Chieu Cao H (mm)"
        worksheet1.Cells(1, 6).Value = "Do Day T (mm) - NHẬP TẠI ĐÂY"
        worksheet1.Cells(1, 7).Value = "So Luong (Thanh)"
        worksheet1.Cells(1, 8).Value = "Ty Trong (g/cm3) - NHẬP TẠI ĐÂY"
        worksheet1.Cells(1, 9).Value = "Tong Chieu Dai (mm)"
        worksheet1.Cells(1, 10).Value = "Tong Khoi Luong (kg) - CONG THUC"
        
        ' Dinh dang hang tieu de Sheet 1 (Bat tu dong xuong dong WrapText)
        Dim headerRange1 As Object = worksheet1.Range("A1:J1")
        headerRange1.Font.Bold = True
        headerRange1.Font.Size = 11
        headerRange1.Interior.ColorIndex = 15 
        headerRange1.HorizontalAlignment = -4108 
        headerRange1.VerticalAlignment = -4108 
        headerRange1.WrapText = True 
        worksheet1.Rows(1).RowHeight = 35 
        
        Dim rowIndex1 As Integer = 2
        Dim stt1 As Integer = 1
        
        For Each kvp As System.Collections.Generic.KeyValuePair(Of String, Double()) In summaryDict
            Dim keyParts() As String = kvp.Key.Split("|"c)
            Dim W As Double = Double.Parse(keyParts(0), System.Globalization.CultureInfo.InvariantCulture)
            Dim H As Double = Double.Parse(keyParts(1), System.Globalization.CultureInfo.InvariantCulture)
            Dim T As Double = Double.Parse(keyParts(2), System.Globalization.CultureInfo.InvariantCulture)
            Dim material As String = keyParts(3)
            Dim density As Double = Double.Parse(keyParts(4), System.Globalization.CultureInfo.InvariantCulture)
            
            Dim values() As Double = kvp.Value
            Dim count As Integer = Convert.ToInt32(values(0))
            Dim totalLength As Double = values(1)
            
            profileNameOnly = "Hộp " & W & "x" & H
            
            ' Lấy màu 5S tương ứng với tiết diện này
            rowColor = 15
            If Not profileColorMap.TryGetValue(profileNameOnly, rowColor) Then
                rowColor = colorPalette(colorIndex Mod colorPalette.Length)
                profileColorMap.Add(profileNameOnly, rowColor)
                colorIndex += 1
            End If
            
            worksheet1.Cells(rowIndex1, 1).Value = stt1
            worksheet1.Cells(rowIndex1, 2).Value = profileNameOnly
            worksheet1.Cells(rowIndex1, 3).Value = material
            worksheet1.Cells(rowIndex1, 4).Value = W
            worksheet1.Cells(rowIndex1, 5).Value = H
            worksheet1.Cells(rowIndex1, 6).Value = T 
            worksheet1.Cells(rowIndex1, 7).Value = count
            worksheet1.Cells(rowIndex1, 8).Value = density
            worksheet1.Cells(rowIndex1, 9).Value = Math.Round(totalLength, 1) 
            
            ' Cong thuc Excel cho Khoi Luong: = (2 * T * (W + H - 2*T) * Length_mm * Density) / 1,000,000
            Dim r As String = rowIndex1.ToString()
            worksheet1.Cells(rowIndex1, 10).Formula = "= (2 * F" & r & " * (D" & r & " + E" & r & " - 2 * F" & r & ") * I" & r & " * H" & r & ") / 1000000"
            
            worksheet1.Cells(rowIndex1, 1).HorizontalAlignment = -4108 
            worksheet1.Cells(rowIndex1, 4).HorizontalAlignment = -4108 
            worksheet1.Cells(rowIndex1, 5).HorizontalAlignment = -4108 
            worksheet1.Cells(rowIndex1, 6).HorizontalAlignment = -4108 
            worksheet1.Cells(rowIndex1, 7).HorizontalAlignment = -4108 
            worksheet1.Cells(rowIndex1, 8).HorizontalAlignment = -4108 
            worksheet1.Cells(rowIndex1, 9).HorizontalAlignment = -4108 
            
            ' To màu
            Dim rowRange As Object = worksheet1.Range("A" & rowIndex1 & ":J" & rowIndex1)
            rowRange.Interior.ColorIndex = rowColor
            rowRange.Borders.LineStyle = 1
            worksheet1.Cells(rowIndex1, 6).Interior.ColorIndex = 2
            worksheet1.Cells(rowIndex1, 8).Interior.ColorIndex = 2
            
            rowIndex1 += 1
            stt1 += 1
        Next
        
        ' --- GHI HÀNG TỔNG CỘNG TOÀN BỘ CHO TAB 1 ---
        Dim grandRow1 As String = rowIndex1.ToString()
        worksheet1.Cells(rowIndex1, 2).Value = "TỔNG CỘNG TOÀN BỘ"
        
        ' Tổng số lượng thanh (cột G)
        worksheet1.Cells(rowIndex1, 7).Formula = "=SUM(G2:G" & (rowIndex1 - 1) & ")"
        ' Tổng chiều dài mm (cột I)
        worksheet1.Cells(rowIndex1, 9).Formula = "=SUM(I2:I" & (rowIndex1 - 1) & ")"
        ' Tổng khối lượng (cột J)
        worksheet1.Cells(rowIndex1, 10).Formula = "=SUM(J2:J" & (rowIndex1 - 1) & ")"
        
        worksheet1.Cells(rowIndex1, 7).HorizontalAlignment = -4108
        worksheet1.Cells(rowIndex1, 9).HorizontalAlignment = -4108
        
        ' Định dạng hàng tổng cộng
        Dim grandTotalRange1 As Object = worksheet1.Range("A" & grandRow1 & ":J" & grandRow1)
        grandTotalRange1.Font.Bold = True
        grandTotalRange1.Interior.ColorIndex = 40 
        grandTotalRange1.Borders.LineStyle = 1
        
        Dim grandTotalRowIdx1 As Integer = rowIndex1
        rowIndex1 += 1
        
        ' Dat do rong cac cot Sheet 1
        worksheet1.Columns("A").ColumnWidth = 6   
        worksheet1.Columns("B").ColumnWidth = 15  
        worksheet1.Columns("C").ColumnWidth = 14  
        worksheet1.Columns("D").ColumnWidth = 9   
        worksheet1.Columns("E").ColumnWidth = 9   
        worksheet1.Columns("F").ColumnWidth = 11  
        worksheet1.Columns("G").ColumnWidth = 9   
        worksheet1.Columns("H").ColumnWidth = 10  
        worksheet1.Columns("I").ColumnWidth = 11  
        worksheet1.Columns("J").ColumnWidth = 11  
        
        WriteReferenceTable(worksheet1, 13)
        worksheet1.Columns("M").ColumnWidth = 20  
        worksheet1.Columns("N").ColumnWidth = 15  
        
        ' --- THIẾT LẬP IN A4 KHỔ NGANG ---
        Dim ps1 As Object = worksheet1.PageSetup
        ps1.PaperSize = 9 
        ps1.Orientation = 2 
        ps1.Zoom = False
        ps1.FitToPagesWide = 1
        ps1.FitToPagesTall = False 
        ps1.LeftMargin = 28.35 
        ps1.RightMargin = 28.35
        ps1.TopMargin = 28.35
        ps1.BottomMargin = 28.35
        ps1.PrintGridlines = True
        
        ' --- TAB 2: CHI TIẾT CẮT ---
        Dim worksheet2 As Object = Nothing
        Try
            If workbook.Sheets.Count >= 2 Then
                worksheet2 = workbook.Sheets(2)
            Else
                worksheet2 = workbook.Sheets.Add()
            End If
            worksheet2.Name = "Chi Tiet Cat"
        Catch
            worksheet2 = workbook.Sheets.Add()
            worksheet2.Name = "Chi Tiet Cat"
        End Try
        
        worksheet2.Cells(1, 1).Value = "STT"
        worksheet2.Cells(1, 2).Value = "Tiet Dien Thép"
        worksheet2.Cells(1, 3).Value = "Vat Lieu"
        worksheet2.Cells(1, 4).Value = "Chieu Rong W (mm)"
        worksheet2.Cells(1, 5).Value = "Chieu Cao H (mm)"
        worksheet2.Cells(1, 6).Value = "Do Day T (mm) - TU DONG LINK"
        worksheet2.Cells(1, 7).Value = "Chieu Dai Cat L (mm)"
        worksheet2.Cells(1, 8).Value = "So Luong (Doan)"
        worksheet2.Cells(1, 9).Value = "Ty Trong (g/cm3) - TU DONG LINK"
        worksheet2.Cells(1, 10).Value = "Tong Chieu Dai (mm) - CONG THUC"
        worksheet2.Cells(1, 11).Value = "Khoi Luong 1 Doan (kg) - CONG THUC"
        worksheet2.Cells(1, 12).Value = "Tong Khoi Luong (kg) - CONG THUC"
        
        Dim headerRange2 As Object = worksheet2.Range("A1:L1")
        headerRange2.Font.Bold = True
        headerRange2.Font.Size = 11
        headerRange2.Interior.ColorIndex = 15 
        headerRange2.HorizontalAlignment = -4108 
        headerRange2.VerticalAlignment = -4108 
        headerRange2.WrapText = True 
        worksheet2.Rows(1).RowHeight = 35
        
        ' Sap xep danh sach cat
        Dim sortedKeys As New System.Collections.Generic.List(Of String)(cutListDict.Keys)
        sortedKeys.Sort(Function(x, y)
                            Dim partsX() As String = x.Split("|"c)
                            Dim partsY() As String = y.Split("|"c)
                            
                            Dim wX As Double = Double.Parse(partsX(0), System.Globalization.CultureInfo.InvariantCulture)
                            Dim wY As Double = Double.Parse(partsY(0), System.Globalization.CultureInfo.InvariantCulture)
                            Dim compW As Integer = wX.CompareTo(wY)
                            If compW <> 0 Then Return compW
                            
                            Dim hX As Double = Double.Parse(partsX(1), System.Globalization.CultureInfo.InvariantCulture)
                            Dim hY As Double = Double.Parse(partsY(1), System.Globalization.CultureInfo.InvariantCulture)
                            Dim compH As Integer = hX.CompareTo(hY)
                            If compH <> 0 Then Return compH
                            
                            Dim tX As Double = Double.Parse(partsX(2), System.Globalization.CultureInfo.InvariantCulture)
                            Dim tY As Double = Double.Parse(partsY(2), System.Globalization.CultureInfo.InvariantCulture)
                            Dim compT As Integer = tX.CompareTo(tY)
                            If compT <> 0 Then Return compT
                            
                            Dim compMat As Integer = String.Compare(partsX(3), partsY(3))
                            If compMat <> 0 Then Return compMat
                            
                            Dim lenX As Double = Double.Parse(partsX(5), System.Globalization.CultureInfo.InvariantCulture)
                            Dim lenY As Double = Double.Parse(partsY(5), System.Globalization.CultureInfo.InvariantCulture)
                            Return lenY.CompareTo(lenX)
                        End Function)
        
        Dim rowIndex2 As Integer = 2
        Dim stt2 As Integer = 1
        Dim startRowIndex As Integer = 2
        Dim prevGroupKey As String = ""
        
        For i As Integer = 0 To sortedKeys.Count - 1
            Dim key As String = sortedKeys(i)
            Dim keyParts() As String = key.Split("|"c)
            Dim W As Double = Double.Parse(keyParts(0), System.Globalization.CultureInfo.InvariantCulture)
            Dim H As Double = Double.Parse(keyParts(1), System.Globalization.CultureInfo.InvariantCulture)
            Dim T As Double = Double.Parse(keyParts(2), System.Globalization.CultureInfo.InvariantCulture)
            Dim material As String = keyParts(3)
            Dim density As Double = Double.Parse(keyParts(4), System.Globalization.CultureInfo.InvariantCulture)
            Dim cutLength As Double = Double.Parse(keyParts(5), System.Globalization.CultureInfo.InvariantCulture)
            
            Dim currentGroupKey As String = W.ToString(System.Globalization.CultureInfo.InvariantCulture) & "|" & H.ToString(System.Globalization.CultureInfo.InvariantCulture) & "|" & material
            
            ' Neu doi nhom tiet dien
            If prevGroupKey <> "" AndAlso prevGroupKey <> currentGroupKey Then
                WriteSubtotalRow(worksheet2, startRowIndex, rowIndex2 - 1, rowIndex2, prevGroupKey)
                rowIndex2 += 1
                startRowIndex = rowIndex2
            End If
            
            Dim values() As Double = cutListDict(key)
            Dim count As Integer = Convert.ToInt32(values(0))
            Dim r2 As String = rowIndex2.ToString()
            
            profileNameOnly = "Hộp " & W & "x" & H
            
            ' Lấy màu 5S tương ứng (đồng bộ màu với Sheet 1)
            rowColor = 15
            If Not profileColorMap.TryGetValue(profileNameOnly, rowColor) Then
                rowColor = colorPalette(colorIndex Mod colorPalette.Length)
                profileColorMap.Add(profileNameOnly, rowColor)
                colorIndex += 1
            End If
            
            worksheet2.Cells(rowIndex2, 1).Value = stt2
            worksheet2.Cells(rowIndex2, 2).Value = profileNameOnly
            worksheet2.Cells(rowIndex2, 3).Value = material
            worksheet2.Cells(rowIndex2, 4).Value = W
            worksheet2.Cells(rowIndex2, 5).Value = H
            
            worksheet2.Cells(rowIndex2, 6).Formula = "=VLOOKUP(B" & r2 & ", 'Tong Hop'!B:F, 5, FALSE)"
            worksheet2.Cells(rowIndex2, 7).Value = cutLength
            worksheet2.Cells(rowIndex2, 8).Value = count
            worksheet2.Cells(rowIndex2, 9).Formula = "=VLOOKUP(B" & r2 & ", 'Tong Hop'!B:H, 7, FALSE)"
            
            worksheet2.Cells(rowIndex2, 10).Formula = "= G" & r2 & " * H" & r2
            worksheet2.Cells(rowIndex2, 11).Formula = "= (2 * F" & r2 & " * (D" & r2 & " + E" & r2 & " - 2 * F" & r2 & ") * G" & r2 & " * I" & r2 & ") / 1000000"
            worksheet2.Cells(rowIndex2, 12).Formula = "= K" & r2 & " * H" & r2
            
            worksheet2.Cells(rowIndex2, 1).HorizontalAlignment = -4108 
            worksheet2.Cells(rowIndex2, 4).HorizontalAlignment = -4108 
            worksheet2.Cells(rowIndex2, 5).HorizontalAlignment = -4108 
            worksheet2.Cells(rowIndex2, 6).HorizontalAlignment = -4108 
            worksheet2.Cells(rowIndex2, 7).HorizontalAlignment = -4108 
            worksheet2.Cells(rowIndex2, 8).HorizontalAlignment = -4108 
            worksheet2.Cells(rowIndex2, 9).HorizontalAlignment = -4108 
            
            ' To màu
            Dim rowRange2 As Object = worksheet2.Range("A" & rowIndex2 & ":L" & rowIndex2)
            rowRange2.Interior.ColorIndex = rowColor
            rowRange2.Borders.LineStyle = 1
            worksheet2.Cells(rowIndex2, 6).Interior.ColorIndex = 2
            worksheet2.Cells(rowIndex2, 9).Interior.ColorIndex = 2
            
            rowIndex2 += 1
            stt2 += 1
            prevGroupKey = currentGroupKey
        Next
        
        ' Ghi dong Tong cong cho nhom cuoi cung
        If prevGroupKey <> "" Then
            WriteSubtotalRow(worksheet2, startRowIndex, rowIndex2 - 1, rowIndex2, prevGroupKey)
            rowIndex2 += 1
        End If
        
        ' --- GHI HÀNG TỔNG CỘNG TOÀN BỘ CHO TAB 2 (LINK SANG TAB 1) ---
        Dim grandRow2 As String = rowIndex2.ToString()
        worksheet2.Cells(rowIndex2, 2).Value = "TỔNG CỘNG TOÀN BỘ"
        
        worksheet2.Cells(rowIndex2, 8).Formula = "='Tong Hop'!G" & grandTotalRowIdx1
        worksheet2.Cells(rowIndex2, 10).Formula = "='Tong Hop'!I" & grandTotalRowIdx1
        worksheet2.Cells(rowIndex2, 12).Formula = "='Tong Hop'!J" & grandTotalRowIdx1
        
        worksheet2.Cells(rowIndex2, 8).HorizontalAlignment = -4108
        worksheet2.Cells(rowIndex2, 10).HorizontalAlignment = -4108
        
        ' Định dạng hàng tổng cộng toàn bộ
        Dim grandTotalRange2 As Object = worksheet2.Range("A" & grandRow2 & ":L" & grandRow2)
        grandTotalRange2.Font.Bold = True
        grandTotalRange2.Interior.ColorIndex = 40 
        grandTotalRange2.Borders.LineStyle = 1
        
        rowIndex2 += 1
        
        ' Dat do rong cac cot Sheet 2
        worksheet2.Columns("A").ColumnWidth = 6   
        worksheet2.Columns("B").ColumnWidth = 15  
        worksheet2.Columns("C").ColumnWidth = 14  
        worksheet2.Columns("D").ColumnWidth = 9   
        worksheet2.Columns("E").ColumnWidth = 9   
        worksheet2.Columns("F").ColumnWidth = 11  
        worksheet2.Columns("G").ColumnWidth = 10  
        worksheet2.Columns("H").ColumnWidth = 9   
        worksheet2.Columns("I").ColumnWidth = 10  
        worksheet2.Columns("J").ColumnWidth = 11  
        worksheet2.Columns("K").ColumnWidth = 11  
        worksheet2.Columns("L").ColumnWidth = 11  
        
        WriteReferenceTable(worksheet2, 15)
        worksheet2.Columns("O").ColumnWidth = 20  
        worksheet2.Columns("P").ColumnWidth = 15  
        
        ' --- THIẾT LẬP IN A4 KHỔ NGANG CHO TAB 2 ---
        Dim ps2 As Object = worksheet2.PageSetup
        ps2.PaperSize = 9 
        ps2.Orientation = 2 
        ps2.Zoom = False
        ps2.FitToPagesWide = 1
        ps2.FitToPagesTall = False 
        ps2.LeftMargin = 28.35 
        ps2.RightMargin = 28.35
        ps2.TopMargin = 28.35
        ps2.BottomMargin = 28.35
        ps2.PrintGridlines = True
        
        ' Kich hoat tab Tong Hop khi mo file
        Try
            worksheet1.Activate()
        Catch
        End Try
        
        ' Luu file tu dong
        Dim assyPath As String = ""
        Try
            assyPath = System.IO.Path.GetDirectoryName(oAssyDoc.FullFileName)
        Catch
        End Try
        
        If String.IsNullOrEmpty(assyPath) Then
            assyPath = System.Environment.GetFolderPath(System.Environment.SpecialFolder.MyDocuments)
        End If
        
        Dim assyName As String = System.IO.Path.GetFileNameWithoutExtension(oAssyDoc.FullFileName)
        If String.IsNullOrEmpty(assyName) Then assyName = "Assembly_BOM"
        
        Dim excelFileName As String = System.IO.Path.Combine(assyPath, assyName & "_Frame_BOM.xlsx")
        
        Try
            If System.IO.File.Exists(excelFileName) Then
                System.IO.File.Delete(excelFileName)
            End If
            workbook.SaveAs(excelFileName)
            MessageBox.Show("Xuat bao cao thanh cong!" & vbCrLf & _
                            "File duoc luu tai: " & excelFileName, "iLogic Export", MessageBoxButtons.OK, MessageBoxIcon.Information)
        Catch ex As Exception
            MessageBox.Show("Bang tinh Excel da mo hoac loi quyen ghi. Vui long kiem tra Excel va luu thu cong." & vbCrLf & _
                            "Chi tiet: " & ex.Message, "iLogic Canh bao", MessageBoxButtons.OK, MessageBoxIcon.Warning)
        End Try
        
    Catch ex As Exception
        MessageBox.Show("Co loi xay ra khi xuat du lieu sang Excel: " & ex.Message, "Loi He Thong", MessageBoxButtons.OK, MessageBoxIcon.Error)
        If excelApp IsNot Nothing Then
            excelApp.Visible = True
        End If
    End Try
End Sub

''' <summary>
''' Ghi dong Tong cong cho mot nhom tiet dien thep tai Sheet Chi tiet cat
''' </summary>
Sub WriteSubtotalRow(ByRef worksheet As Object, startRow As Integer, endRow As Integer, targetRow As Integer, groupKey As String)
    Dim keyParts() As String = groupKey.Split("|"c)
    Dim W As Double = Double.Parse(keyParts(0), System.Globalization.CultureInfo.InvariantCulture)
    Dim H As Double = Double.Parse(keyParts(1), System.Globalization.CultureInfo.InvariantCulture)
    
    Dim tRow As String = targetRow.ToString()
    
    worksheet.Cells(targetRow, 2).Value = "TỔNG CỘNG HỘP " & W & "x" & H
    
    ' Tinh tong so doan: Cot H (Cot 8)
    worksheet.Cells(targetRow, 8).Formula = "=SUM(H" & startRow & ":H" & endRow & ")"
    
    ' Tinh tong chieu dai (mm): Cot J (Cot 10)
    worksheet.Cells(targetRow, 10).Formula = "=SUM(J" & startRow & ":J" & endRow & ")"
    
    ' Tinh tong khoi luong (kg): Cot L (Cot 12)
    worksheet.Cells(targetRow, 12).Formula = "=SUM(L" & startRow & ":L" & endRow & ")"
    
    ' Dinh dang hang tong cong phân doan: Font in dam, nen xam dam de phan dinh ro rang, chu trang
    Dim subtotalRange As Object = worksheet.Range("A" & tRow & ":L" & tRow)
    subtotalRange.Font.Bold = True
    subtotalRange.Interior.ColorIndex = 16 
    subtotalRange.Font.ColorIndex = 2 
    subtotalRange.Borders.LineStyle = 1
    
    worksheet.Cells(targetRow, 8).HorizontalAlignment = -4108
End Sub

''' <summary>
''' Ghi Bảng tra cứu tỷ trọng ở các cột trống phía bên phải bảng dữ liệu chính
''' </summary>
Sub WriteReferenceTable(ByRef worksheet As Object, startCol As Integer)
    Dim colLetter1 As String = GetExcelColumnName(startCol)
    Dim colLetter2 As String = GetExcelColumnName(startCol + 1)
    
    worksheet.Cells(1, startCol).Value = "BẢNG TRA CỨU TỶ TRỌNG"
    worksheet.Cells(2, startCol).Value = "Vật Liệu"
    worksheet.Cells(2, startCol + 1).Value = "Tỷ trọng (g/cm3)"
    
    worksheet.Cells(3, startCol).Value = "Inox 304"
    worksheet.Cells(3, startCol + 1).Value = 7.93
    
    worksheet.Cells(4, startCol).Value = "Inox 316"
    worksheet.Cells(4, startCol + 1).Value = 8.00
    
    worksheet.Cells(5, startCol).Value = "Inox 201"
    worksheet.Cells(5, startCol + 1).Value = 7.86
    
    worksheet.Cells(6, startCol).Value = "Sắt / Thép thường"
    worksheet.Cells(6, startCol + 1).Value = 7.85
    
    worksheet.Cells(7, startCol).Value = "Nhôm"
    worksheet.Cells(7, startCol + 1).Value = 2.70
    
    ' Định dạng tiêu đề bảng tra cứu
    Dim titleRange As Object = worksheet.Range(colLetter1 & "1:" & colLetter2 & "1")
    titleRange.Merge()
    titleRange.Font.Bold = True
    titleRange.HorizontalAlignment = -4108
    titleRange.Interior.ColorIndex = 40 
    titleRange.Borders.LineStyle = 1
    
    Dim headerRange As Object = worksheet.Range(colLetter1 & "2:" & colLetter2 & "2")
    headerRange.Font.Bold = True
    headerRange.Interior.ColorIndex = 15
    headerRange.Borders.LineStyle = 1
    
    ' Định dạng đường viền và căn chỉnh cho dữ liệu bảng tra cứu
    Dim dataRange As Object = worksheet.Range(colLetter1 & "3:" & colLetter2 & "7")
    dataRange.Borders.LineStyle = 1
    
    ' Căn giữa cột số tỷ trọng
    worksheet.Range(colLetter2 & "3:" & colLetter2 & "7").HorizontalAlignment = -4108
End Sub

''' <summary>
''' Đổi số thứ tự cột Excel thành ký tự chữ cái (Vd: 13 -> M, 15 -> O)
''' </summary>
Function GetExcelColumnName(columnNumber As Integer) As String
    Dim columnName As String = ""
    Dim temp As Integer
    While columnNumber > 0
        temp = (columnNumber - 1) Mod 26
        columnName = Convert.ToChar(65 + temp) & columnName
        columnNumber = (columnNumber - temp) \ 26
    End While
    Return columnName
End Function

''' <summary>
''' Ham Helper de parse kich thuoc Rong, Cao, Day tu ten Profile
''' </summary>
Function ParseProfile(profileName As String, ByRef W As Double, ByRef H As Double, ByRef T As Double) As Boolean
    W = 0 : H = 0 : T = 0
    If String.IsNullOrEmpty(profileName) Then Return False
    Try
        Dim s As String = profileName.ToLower().Replace(" ", "").Replace("*", "x").Replace(",", ".")
        Dim parts() As String = s.Split("x"c)
        
        If parts.Length >= 3 Then
            Dim tStr : tStr = parts(parts.Length - 1)
            Dim hStr : hStr = parts(parts.Length - 2)
            Dim wStr : wStr = parts(parts.Length - 3)
            
            T = GetFirstNumber(tStr)
            H = GetFirstNumber(hStr)
            W = GetLastNumber(wStr)
            Return True
        ElseIf parts.Length = 2 Then
            Dim tStr : tStr = parts(1)
            Dim wStr : wStr = parts(0)
            
            Dim val1 As Double = GetLastNumber(wStr)
            Dim val2 As Double = GetFirstNumber(tStr)
            
            ' Nếu số thứ hai lớn hơn 6, nó là chiều cao H của hộp chữ nhật/vuông chứ không phải độ dày T
            If val2 > 6 Then
                W = val1
                H = val2
                T = 0 ' Để mặc định là 1.5 ở ngoài
            Else
                W = val1
                H = val1
                T = val2
            End If
            Return True
        ElseIf parts.Length = 1 Then
            Dim val1 As Double = GetLastNumber(parts(0))
            If val1 > 0 Then
                W = val1
                H = val1
                T = 0 ' Để mặc định là 1.5 ở ngoài
                Return True
            End If
        End If
    Catch
    End Try
    Return False
End Function

Function GetFirstNumber(s As String) As Double
    Dim m As System.Text.RegularExpressions.Match = System.Text.RegularExpressions.Regex.Match(s, "([0-9]+(?:\.[0-9]+)?)")
    If m.Success Then
        Return Double.Parse(m.Value, System.Globalization.CultureInfo.InvariantCulture)
    End If
    Return 0
End Function

Function GetLastNumber(s As String) As Double
    Dim ms As System.Text.RegularExpressions.MatchCollection = System.Text.RegularExpressions.Regex.Matches(s, "([0-9]+(?:\.[0-9]+)?)")
    If ms.Count > 0 Then
        Return Double.Parse(ms(ms.Count - 1).Value, System.Globalization.CultureInfo.InvariantCulture)
    End If
    Return 0
End Function
