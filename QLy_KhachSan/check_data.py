import json
import os

def check_data():
    os.makedirs("data", exist_ok=True)
    file_path = "data/khach_san_data.json"
    
    print("=" * 60)
    print("🚀 TIẾN HÀNH RESET & KHỞI TẠO 48 PHÒNG MẪU CHUẨN")
    print("=" * 60)
    
    # Khởi tạo khung dữ liệu
    du_lieu_mau = {
        "phong": [],
        "dat_phong": [],
        "bo_dem_dat_phong": 1
    }
    
    # Vòng lặp tự động tạo dữ liệu cho 6 tầng (từ tầng 1 đến tầng 6)
    for tang in range(1, 7):
        # Mỗi tầng có 8 phòng (từ phòng 1 đến phòng 8)
        for i in range(1, 9):
            # Định dạng số phòng dạng chuỗi, ví dụ: "101", "102", ..., "108" hoặc "601", ..., "608"
            so_phong = f"{tang}{i:02d}"  # Kết quả: "101", "102", ..., "108"
            
            # Phân bổ loại phòng và giá niêm yết theo đúng thiết kế của bạn:
            if i <= 4:
                loai_phong = "Tiêu chuẩn"
                gia_niem_yet = 300000.0
                mo_ta = "Phòng tiêu chuẩn đơn giản, sạch sẽ thoải mái"
                tien_ich = ["Wifi", "Tivi", "Quạt điện"]
            elif i <= 7:
                loai_phong = "VIP"
                gia_niem_yet = 600000.0
                mo_ta = "Phòng VIP không gian rộng rãi, tiện nghi cao cấp"
                tien_ich = ["Wifi", "Tivi", "Điều hòa", "Tủ lạnh"]
            else:
                loai_phong = "Suite"
                gia_niem_yet = 1200000.0
                mo_ta = "Phòng Suite sang trọng, đẳng cấp thượng lưu"
                tien_ich = ["Wifi", "Tivi", "Điều hòa", "Tủ lạnh", "Bồn tắm mini"]
                
            # Đóng gói thông tin một phòng đúng định dạng đối tượng
            phong_data = {
                "so_phong": so_phong,
                "tang": tang,             # Kiểu int để khớp với set(phong_data["tang"])
                "loai_phong": loai_phong, # Đúng từ khóa Tiếng Việt có dấu
                "gia_niem_yet": gia_niem_yet,
                "trang_thai": "Trống",     # Đúng trạng thái map phòng trống
                "mo_ta": mo_ta,
                "tien_ich": tien_ich
            }
            du_lieu_mau["phong"].append(phong_data)
            
    # Xóa file cũ để tránh xung đột cấu trúc lỗi
    if os.path.exists(file_path):
        os.remove(file_path)
        print("🗑️ Đã giải phóng file dữ liệu cũ cũ.")
        
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(du_lieu_mau, f, ensure_ascii=False, indent=2)
            
        print("✅ Khởi tạo bộ dữ liệu 48 phòng THÀNH CÔNG!")
        print(f"📊 Tổng số phòng vừa ghi file: {len(du_lieu_mau['phong'])} phòng.")
        print("   -> Tầng 1 đến tầng 6 (mỗi tầng: 4 Tiêu chuẩn, 3 VIP, 1 Suite).")
        return True
    except Exception as e:
        print(f"❌ Lỗi ghi file: {e}")
        return False

if __name__ == "__main__":
    check_data()