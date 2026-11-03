import os, zipfile, re, sys, io

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def inspect_component_package(component_dir):
    """
    Kiểm tra tự động gói sản phẩm trước khi xuất bản lên sàn 3D
    """
    mod_name = os.path.basename(component_dir)
    print("="*80)
    print(f"🔍 KIỂM ĐỊNH CHẤT LƯỢNG & PHÁP LÝ SÀN 3D: [{mod_name}]")
    print("="*80)
    
    issues = []
    passes = []
    
    # 1. Kiểm tra cấu trúc thư mục con bắt buộc
    expected_subdirs = ["06_Renders_and_Media"]
    for s in expected_subdirs:
        sp = os.path.join(component_dir, s)
        if os.path.exists(sp):
            passes.append(f"Cấu trúc thư mục '{s}' hợp lệ")
        else:
            issues.append(f"Thiếu thư mục '{s}'")
            
    # 2. Kiểm tra bộ tài liệu SEO & Publishing Studio (Hỗ trợ cả tên Folder lẫn tên Model Assembly)
    docs_dir = os.path.join(component_dir, r"06_Renders_and_Media\05_SEO_and_Marketing_Docs")
    studio_file = None
    
    cand1 = os.path.join(docs_dir, f"Publishing_Studio_{mod_name}.html")
    if os.path.exists(cand1):
        studio_file = cand1
    elif os.path.exists(docs_dir):
        for f in os.listdir(docs_dir):
            if f.startswith("Publishing_Studio_") and f.endswith(".html"):
                studio_file = os.path.join(docs_dir, f)
                break
    
    if studio_file and os.path.exists(studio_file):
        passes.append(f"Có file Publishing Studio 1-Chạm ({os.path.basename(studio_file)})")
        with open(studio_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Kiểm tra Zero-Link trên tab sàn (CGTrader, Fab, TurboSquid)
        cg_match = re.search(r'id="cgDesc">(.*?)</div>', content, re.DOTALL)
        fab_match = re.search(r'id="fabDesc">(.*?)</div>', content, re.DOTALL)
        ts_match = re.search(r'id="tsDesc">(.*?)</div>', content, re.DOTALL)
        
        marketplace_texts = []
        if cg_match: marketplace_texts.append(("CGTrader", cg_match.group(1)))
        if fab_match: marketplace_texts.append(("Fab", fab_match.group(1)))
        if ts_match: marketplace_texts.append(("TurboSquid", ts_match.group(1)))
        
        for platform, text in marketplace_texts:
            if re.search(r'\+84|\d{10}|\b09\d{8}\b', text):
                issues.append(f"Vi phạm Zero-Link: Tab [{platform}] có chứa Số Điện Thoại!")
            if re.search(r'http[s]?://|www\.|zalo|facebook', text, re.IGNORECASE):
                issues.append(f"Vi phạm Zero-Link: Tab [{platform}] có chứa Link ngoài!")
            if "@" in text:
                issues.append(f"Vi phạm Zero-Link: Tab [{platform}] có chứa ký tự '@'!")
                
        if not any("Vi phạm Zero-Link" in iss for iss in issues):
            passes.append("Tuân thủ 100% Zero-Link Policy trên các Tab Sàn Quốc Tế")
    else:
        issues.append("Thiếu file Publishing Studio HTML")
        
    # 3. Kiểm tra file nén ZIP bán sàn (nếu đã đóng gói)
    upload_pkg_dir = os.path.join(component_dir, r"06_Renders_and_Media\01_Marketplace_Upload_Package")
    if os.path.exists(upload_pkg_dir):
        zip_files = [f for f in os.listdir(upload_pkg_dir) if f.endswith('.zip')]
        if zip_files:
            for zf in zip_files:
                zpath = os.path.join(upload_pkg_dir, zf)
                try:
                    with zipfile.ZipFile(zpath, 'r') as z:
                        namelist = z.namelist()
                        nested = [n for n in namelist if "/" in n and not n.endswith("/")]
                        if nested:
                            issues.append(f"File ZIP '{zf}' bị lồng thư mục con: {nested[:3]}")
                        else:
                            passes.append(f"File ZIP '{zf}' chuẩn Flat File Structure (CheckMate Pro)")
                            
                        forbidden = [n for n in namelist if n.endswith(('.iam', '.ipt', '.idw'))]
                        if forbidden:
                            issues.append(f"CẢNH BÁO NGUY HIỂM: File ZIP '{zf}' bị lộ file gốc Autodesk: {forbidden}")
                        else:
                            passes.append(f"File ZIP '{zf}' bảo vệ bản quyền 100% (Không chứa file gốc .iam/.ipt)")
                            
                        junk = [n for n in namelist if any(j in n for j in ["OldVersions", "Thumbs.db", ".DS_Store"])]
                        if junk:
                            issues.append(f"File ZIP '{zf}' chứa file rác: {junk}")
                        else:
                            passes.append(f"File ZIP '{zf}' sạch sẽ 100% không rác hệ thống")
                except Exception as e:
                    issues.append(f"Lỗi đọc file ZIP '{zf}': {e}")
        else:
            passes.append("Chưa đóng gói ZIP (Sẵn sàng xuất file)")

    print("\n✅ CÁC TIÊU CHÍ ĐÃ ĐẠT (PASS):")
    for p in passes:
        print(f"  ✔️ {p}")
        
    if issues:
        print("\n❌ CÁC LỖI CẦN SỬA (FAIL):")
        for iss in issues:
            print(f"  ⚠️ {iss}")
        print("\n🔴 KẾT QUẢ: CHƯA ĐẠT CHUẨN XUẤT BẢN")
    else:
        print("\n💎 KẾT QUẢ: 100% PASS - HOÀN TOÀN ĐỦ TIÊU CHUẨN ĐĂNG BÁN TRÊN FAB, CGTRADER, TURBOSQUID!")
    print("="*80)

if __name__ == "__main__":
    test_dir = r"D:\INVENTOR_DATA\05_STANDARD_COMPONENTS\01_Pumps_and_Motors\BlueWhite_C630P_Chemical_Dosing_Pump"
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    inspect_component_package(test_dir)
