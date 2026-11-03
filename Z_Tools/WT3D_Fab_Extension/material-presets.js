// WT3D Material Presets - danh sách 20 vật liệu chuẩn WT3D do người dùng cung cấp (hiện trong bảng với dấu ★).
// Mỗi mẫu: { name, hex | rgb, roughness, metalness, channels?, keepTexturedColorHex?, note? }
//   name      : tên dễ nhớ (bắt buộc, không trùng nhau)
//   hex       : "#RRGGBB"  (hoặc rgb: [r, g, b] với mỗi giá trị 0..1)
//   roughness : 0..1  (độ nhám thật như hiển thị ở thanh Roughness của Fab; 0 = bóng gương, 1 = nhám hoàn toàn)
//   metalness : 0..1  (0 = không kim loại, 1 = kim loại hoàn toàn)
//   channels  : các trường PBR mở rộng của Fab (transmission.*, thickness.*, opacity.*, basecolor.factor, normal.*)
//   note      : ghi chú tùy chọn
// Thêm mẫu mới: chép một dòng vào mảng dưới đây, Reload extension, rồi Ctrl+Shift+R trên tab Fab.
window.WT3D_MATERIAL_PRESETS = [
  // 15 mẫu ghi nhận trực tiếp từ Fab 3D Editor (Mục 1 -> 15)
  { name: "Khung skid",              hex: "#EA8304", roughness: 0.200, metalness: 0.000, note: "R 0.2 / G 0.8" },
  {
    name: "Ống uPVC clear",          hex: "#4DCAFF", roughness: 0.000, metalness: 0.000,
    channels: {
      "transmission.enabled": true,
      "transmission.factor": 1.0,
      "transmission.ior": 1.0,
      "transmission.attenuationdistance": 1.111,
      "transmission.attenuationcolor": [1, 1, 1],
      "thickness.enabled": true,
      "thickness.factor": 1.111,
      "opacity.enabled": false
    },
    note: "Transmission ON • Volume Thickness 1.111 • IOR 1.0"
  },
  {
    name: "Thân phin lọc trong suốt", hex: "#72E9F5", roughness: 0.350, metalness: 0.046,
    channels: {
      "opacity.enabled": true,
      "opacity.type": "blending",
      "opacity.factor": 0.320,
      "opacity.invert": false,
      "transmission.enabled": false
    },
    note: "Opacity Blending 0.320"
  },
  { name: "Nhựa trắng",              hex: "#EBEBEB", roughness: 0.800, metalness: 0.000, note: "XID_SmoothWhite" },
  { name: "uPVC đậm",                hex: "#5E5E61", roughness: 0.279, metalness: 0.000, note: "XID_SmoothMediumGray" },
  { name: "Inox bóng",               hex: "#C8C8C8", roughness: 0.366, metalness: 0.655, note: "XID_TitaniumPolished" },
  { name: "Nhựa xanh",               hex: "#1825F8", roughness: 0.480, metalness: 0.000, note: "XID_BlueWallPaint" },
  { name: "Xanh bơm",                hex: "#0068AD", roughness: 0.225, metalness: 0.000, note: "XID_BlueWallPaint" },
  {
    name: "Đen bơm",                 hex: "#1F1F22", roughness: 0.290, metalness: 0.000,
    keepTexturedColorHex: "#FFFFFF",
    channels: {
      "normal.enabled": true,
      "normal.factor": 1.0,
      "normal.flipY": false
    },
    note: "XID_BlackCast_16 (giữ Texture + Normal OpenGL nếu có)"
  },
  {
    name: "FRP cột lọc",             hex: "#919673", roughness: 0.249, metalness: 0.000,
    channels: {
      "normal.enabled": true,
      "normal.factor": 1.0,
      "normal.flipY": false
    },
    note: "CarbonFiber1 (Normal OpenGL 1.0)"
  },
  { name: "Đen autovalve",           hex: "#050505", roughness: 0.222, metalness: 0.000, note: "SmoothBlack" },
  {
    name: "Xanh skid",               hex: "#0180AB", roughness: 0.202, metalness: 0.000,
    channels: {
      "basecolor.factor": 0.415
    },
    note: "Base Color Intensity 0.415"
  },
  { name: "uPVC nhạt",               hex: "#7C7E82", roughness: 0.219, metalness: 0.398 },
  { name: "Thau van điện",           hex: "#B29864", roughness: 0.775, metalness: 1.000, note: "BrassSatin" },
  { name: "Bulong",                  hex: "#BEBCBA", roughness: 0.273, metalness: 1.000, note: "SemiPolished" },

  // 5 mẫu từ luồng PROCESS (Mục 16 -> 20)
  { name: "Nhựa PPR",                hex: "#0D512B", roughness: 0.219, metalness: 0.000 },
  { name: "Thân van",                hex: "#222735", roughness: 0.132, metalness: 0.000 },
  { name: "PVC xám",                 hex: "#474747", roughness: 0.200, metalness: 0.000 },
  { name: "Tay van đỏ",              hex: "#B20000", roughness: 0.425, metalness: 0.000 },
  { name: "Vỏ RO FRP trắng",         hex: "#FFFFFF", roughness: 0.029, metalness: 0.000 },
  ...(Array.isArray(window.WT3D_MATERIAL_PRESETS) ? window.WT3D_MATERIAL_PRESETS : [])
];
