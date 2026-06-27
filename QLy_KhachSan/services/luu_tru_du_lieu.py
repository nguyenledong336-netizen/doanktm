# services/luu_tru_du_lieu.py
import json
import os
from datetime import datetime
from models import phong
from models.phong import PhongTieuChuan, PhongVIP, PhongSuite, TrangThaiPhong, LoaiPhong
from models.KhachHang import KhachHang
from models.don_dat_phong import DonDatPhong

class LuuTruDuLieu:
    """Lưu trữ và tải dữ liệu từ file JSON"""
    
    def __init__(self, ten_file="data/khach_san_data.json"):
        self.ten_file = ten_file
    
    def luu_du_lieu(self, quan_ly_phong, quan_ly_dat_phong):
        """Lưu dữ liệu vào file JSON"""
        du_lieu = {
            "phong": [],
            "dat_phong": [],
            "bo_dem_dat_phong": quan_ly_dat_phong.bo_dem_dat_phong if quan_ly_dat_phong else 1
        }
        
        # Lưu thông tin phòng
        for phong in quan_ly_phong.lay_tat_ca_phong():
            phong_data = {
                "so_phong": phong.so_phong,
                "tang": phong.tang,
                "loai_phong": phong.loai_phong.value,
                "gia_niem_yet": phong.gia_niem_yet,
                "trang_thai": phong.trang_thai.value,
                "mo_ta": phong.mo_ta,
                "tien_ich": phong.tien_ich
            }
            du_lieu["phong"].append(phong_data)
        
        # Lưu thông tin đặt phòng
        if quan_ly_dat_phong:
            for dat_phong in quan_ly_dat_phong.danh_sach_dat_phong:
                dat_phong_data = {
                    "ma_dat_phong": dat_phong.ma_dat_phong,
                    "khach_hang": {
                        "ho_ten": dat_phong.khach_hang.ho_ten,
                        "so_cmnd": dat_phong.khach_hang.so_cmnd,
                        "so_dien_thoai": dat_phong.khach_hang.so_dien_thoai,
                        "email": dat_phong.khach_hang.email
                    },
                    "so_phong": dat_phong.phong.so_phong,
                    "ngay_nhan": dat_phong.ngay_nhan.isoformat(),
                    "ngay_tra": dat_phong.ngay_tra.isoformat(),
                    "tong_tien": dat_phong.tong_tien,
                    "trang_thai": dat_phong.trang_thai,
                    "ngay_tao": dat_phong.ngay_tao.isoformat()
                }
                du_lieu["dat_phong"].append(dat_phong_data)
        
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(os.path.dirname(self.ten_file), exist_ok=True)
        
        with open(self.ten_file, 'w', encoding='utf-8') as f:
            json.dump(du_lieu, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Đã lưu {len(du_lieu['phong'])} phòng vào {self.ten_file}")
        return True
    
    def tai_du_lieu(self, quan_ly_phong, quan_ly_dat_phong):
        """Tải dữ liệu từ file JSON"""
        if not os.path.exists(self.ten_file):
            print(f"ℹ️ File {self.ten_file} không tồn tại")
            return False
        
        try:
            with open(self.ten_file, 'r', encoding='utf-8') as f:
                du_lieu = json.load(f)
            
            # Kiểm tra dữ liệu
            if len(du_lieu.get("phong", [])) == 0:
                print("⚠️ File JSON không có dữ liệu phòng")
                return False
            
            # Xóa dữ liệu cũ
            quan_ly_phong.xoa_het()
            
            # Tạo lại cấu trúc các tầng
            cac_tang = set()
            for phong_data in du_lieu["phong"]:
               cac_tang.add(int(phong_data["tang"]))
            
            for tang in cac_tang:
                quan_ly_phong.them_tang(tang)
            
            # Ánh xạ loại phòng
            loai_phong_map = {
                "Tiêu chuẩn": PhongTieuChuan,
                "VIP": PhongVIP,
                "Suite": PhongSuite
            }
            
            # Ánh xạ trạng thái
            trang_thai_map = {
                "Trống": TrangThaiPhong.TRONG,
                "Đang ở": TrangThaiPhong.DANG_O,
                "Đang dọn dẹp": TrangThaiPhong.DANG_DON,
                "Bảo trì": TrangThaiPhong.BAO_TRI
            }
            
            # Tạo lại các phòng
            for phong_data in du_lieu["phong"]:
                lop_phong = loai_phong_map.get(phong_data["loai_phong"], PhongTieuChuan)
                phong = lop_phong(
                  phong_data["so_phong"],
                  int(phong_data["tang"]),
                 phong_data["gia_niem_yet"]
                 )
                phong.trang_thai = trang_thai_map.get(phong_data["trang_thai"], TrangThaiPhong.TRONG)
                phong.mo_ta = phong_data.get("mo_ta", "")
                phong.tien_ich = phong_data.get("tien_ich", [])
                quan_ly_phong.them_phong(phong)
            
            # Khôi phục đặt phòng
            if quan_ly_dat_phong:
                quan_ly_dat_phong.bo_dem_dat_phong = du_lieu.get("bo_dem_dat_phong", 1)
                
                for dat_phong_data in du_lieu.get("dat_phong", []):
                    khach_hang = KhachHang(
                        dat_phong_data["khach_hang"]["ho_ten"],
                        dat_phong_data["khach_hang"]["so_cmnd"],
                        dat_phong_data["khach_hang"]["so_dien_thoai"],
                        dat_phong_data["khach_hang"].get("email", "")
                    )
                    
                    phong = quan_ly_phong.lay_phong(dat_phong_data["so_phong"])
                    if phong:
                        ngay_nhan = datetime.fromisoformat(dat_phong_data["ngay_nhan"]).date()
                        ngay_tra = datetime.fromisoformat(dat_phong_data["ngay_tra"]).date()
                        
                        dat_phong = DonDatPhong(
                            dat_phong_data["ma_dat_phong"],
                            khach_hang,
                            phong,
                            ngay_nhan,
                            ngay_tra
                        )
                        dat_phong.tong_tien = dat_phong_data["tong_tien"]
                        dat_phong.trang_thai = dat_phong_data["trang_thai"]
                        dat_phong.ngay_tao = datetime.fromisoformat(dat_phong_data["ngay_tao"])
                        
                        quan_ly_dat_phong.danh_sach_dat_phong.append(dat_phong)
            
            so_phong = len(quan_ly_phong.lay_tat_ca_phong())
            print(f"✅ Đã tải {so_phong} phòng từ {self.ten_file}")
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ Lỗi đọc JSON: {e}")
            return False
        except Exception as e:
            print(f"❌ Lỗi khi tải dữ liệu: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def tao_du_lieu_mau(self, quan_ly_phong):
        """Tạo dữ liệu mẫu cho khách sạn"""
        print("📁 Đang tạo dữ liệu mẫu...")
        
        # Xóa dữ liệu cũ
        quan_ly_phong.xoa_het()
        
        # Tạo 6 tầng
        for tang in range(1, 7):
            quan_ly_phong.them_tang(tang)
        
        # Tạo phòng cho mỗi tầng
        for tang in range(1, 7):
            for i in range(1, 9):  # 8 phòng mỗi tầng
                so_phong = f"{tang:02d}{i:02d}"
                
                # Phân bố: 1-4 Thường, 5-7 VIP, 8 Suite
                if i <= 4:
                    phong = PhongTieuChuan(so_phong, tang)
                elif i <= 7:
                    phong = PhongVIP(so_phong, tang)
                else:
                    phong = PhongSuite(so_phong, tang)
                
                print("Đang thêm:", phong.so_phong)
                print("Kết quả:", quan_ly_phong.them_phong(phong))
        
        so_phong = len(quan_ly_phong.lay_tat_ca_phong())
        print(f"✅ Đã tạo {so_phong} phòng mẫu")
        return so_phong