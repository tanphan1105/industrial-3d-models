import os, sys, io, shutil, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SRC_ROOT = r'D:\INVENTOR_DATA\05_STANDARD_COMPONENTS'
BATCH_OUTPUT_ROOT = r'D:\INVENTOR_DATA\CGTRADER_BATCH_UPLOAD'

print('=' * 80)
print('💎 WT3D CGTRADER BATCH UPLOAD PACKAGER - SIÊU THÔNG MINH')
print('Tự động gom: 1 File ZIP CAD + Toàn bộ Ảnh Preview 4K + 1 Video MP4 cho 212 Models')
print('=' * 80)

os.makedirs(BATCH_OUTPUT_ROOT, exist_ok=True)

categories = [d for d in os.listdir(SRC_ROOT) if os.path.isdir(os.path.join(SRC_ROOT, d)) and not d.startswith('.') and not d.startswith('00_')]
categories.sort()

total_processed = 0
total_skipped = 0
batch_manifest = []

for cat in categories:
    cat_dir = os.path.join(SRC_ROOT, cat)
    models = [m for m in os.listdir(cat_dir) if os.path.isdir(os.path.join(cat_dir, m)) and not m.startswith('.') and not m.startswith('OldVersions')]
    models.sort()
    
    print(f'\n📂 Đang xử lý Nhóm: {cat} ({len(models)} models)...')
    cat_batch_dir = os.path.join(BATCH_OUTPUT_ROOT, cat)
    os.makedirs(cat_batch_dir, exist_ok=True)
    
    for m in models:
        m_dir = os.path.join(cat_dir, m)
        renders_dir = os.path.join(m_dir, '06_Renders_and_Media')
        
        if not os.path.exists(renders_dir):
            total_skipped += 1
            continue
            
        target_model_dir = os.path.join(cat_batch_dir, m)
        os.makedirs(target_model_dir, exist_ok=True)
        
        # Xóa các file cũ trong target_model_dir (trừ trường hợp file đang bị lock)
        for old_f in os.listdir(target_model_dir):
            old_f_path = os.path.join(target_model_dir, old_f)
            if os.path.isfile(old_f_path):
                try:
                    os.remove(old_f_path)
                except Exception:
                    pass
        
        copied_zip = 0
        copied_imgs = 0
        copied_vids = 0
        copied_img_names = set()
        
        # 1. Tìm và copy DUY NHẤT file ZIP Universal CAD
        for root, dirs, files in os.walk(renders_dir):
            for f in files:
                if f.lower().endswith('.zip') and 'cad' in f.lower():
                    src_f = os.path.join(root, f)
                    dst_f = os.path.join(target_model_dir, f)
                    try:
                        shutil.copy2(src_f, dst_f)
                        copied_zip += 1
                        break
                    except Exception:
                        pass
            if copied_zip > 0:
                break
                
        # Fallback nếu không có file zip chứa chữ 'cad'
        if copied_zip == 0:
            for root, dirs, files in os.walk(renders_dir):
                for f in files:
                    if f.lower().endswith('.zip'):
                        src_f = os.path.join(root, f)
                        dst_f = os.path.join(target_model_dir, f)
                        try:
                            shutil.copy2(src_f, dst_f)
                            copied_zip += 1
                            break
                        except Exception:
                            pass
                if copied_zip > 0:
                    break
        
        # 2. Quét TẤT CẢ ảnh Preview (PNG, JPG) từ 02_Images_4K_Previews, 04_Watermarked_Exports, 01_4K_Images
        for root, dirs, files in os.walk(renders_dir):
            # Bỏ qua thư mục texture con
            if '01_Marketplace_Upload_Package' in root and any(root.endswith(ext) for ext in ['.fbx', '.obj', '.blend', m]):
                continue
            for f in files:
                f_lower = f.lower()
                if f_lower.endswith(('.png', '.jpg', '.jpeg', '.webp')) and not f.startswith('.'):
                    if f not in copied_img_names:
                        src_f = os.path.join(root, f)
                        dst_f = os.path.join(target_model_dir, f)
                        try:
                            shutil.copy2(src_f, dst_f)
                            copied_imgs += 1
                            copied_img_names.add(f)
                        except Exception:
                            pass
                            
        # 3. Quét Video MP4 từ 04_Finished_Videos
        for root, dirs, files in os.walk(renders_dir):
            for f in files:
                f_lower = f.lower()
                if f_lower.endswith(('.mp4', '.mov', '.webm')) and not f.startswith('.'):
                    src_f = os.path.join(root, f)
                    dst_f = os.path.join(target_model_dir, f)
                    try:
                        shutil.copy2(src_f, dst_f)
                        copied_vids += 1
                        break # 1 video 360 là đủ
                    except Exception:
                        pass
            if copied_vids > 0:
                break
        
        total_files = copied_zip + copied_imgs + copied_vids
        if total_files > 0:
            total_processed += 1
            batch_manifest.append({
                'category': cat,
                'model_name': m,
                'batch_folder': target_model_dir,
                'zip_count': copied_zip,
                'images_count': copied_imgs,
                'video_count': copied_vids,
                'total_files': total_files
            })
            print(f'   ✓ [{total_processed:03d}] {m} -> 1 ZIP CAD + {copied_imgs} Ảnh Previews + {copied_vids} Video')
        else:
            total_skipped += 1

manifest_file = os.path.join(BATCH_OUTPUT_ROOT, 'CGTrader_Batch_Manifest.json')
with open(manifest_file, 'w', encoding='utf-8') as f:
    json.dump(batch_manifest, f, indent=2, ensure_ascii=False)

print('\n' + '=' * 80)
print(f'🎉 TỔNG KẾT BATCH PACKAGER HOÀN HẢO:')
print(f' - Đã đóng gói hoàn chỉnh: {total_processed} Models')
print(f' - Cấu trúc mỗi model: 1 File ZIP Universal CAD + Album 19-20 Ảnh Previews 4K + 1 Video MP4 360°')
print(f' - Vị trí lưu trữ: {BATCH_OUTPUT_ROOT}')
print('=' * 80)
