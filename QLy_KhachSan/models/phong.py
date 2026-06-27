from abc import ABC, abstractmethod
from enum import Enum

class TrangThaiPhong(Enum):
    TRONG = "Trống"
    DANG_O = "Đang ở"
    DANG_DON = "Đang dọn dẹp"
    BAO_TRI = "Bảo trì"

class LoaiPhong(Enum):
    TIEU_CHUAN = "Tiêu chuẩn"
    VIP = "VIP"
    SUITE = "Suite"

class Phong(ABC):
    def __init__(self, so_phong, tang, loai_phong, gia_niem_yet):
        self.so_phong = so_phong
        self.tang = tang
        self.loai_phong = loai_phong
        self.gia_niem_yet = gia_niem_yet
        self.trang_thai = TrangThaiPhong.TRONG
        self.mo_ta = ""
        self.tien_ich = []
    
    @abstractmethod
    def tinh_gia_phong(self, so_dem):
        pass
    
    def __str__(self):
        return f"Phòng {self.so_phong} (Tầng {self.tang}) - {self.trang_thai.value}"

class PhongTieuChuan(Phong):
    def __init__(self, so_phong, tang, gia_niem_yet=500000):
        super().__init__(so_phong, tang, LoaiPhong.TIEU_CHUAN, gia_niem_yet)
        self.tien_ich = ["WiFi", "TV", "Điều hòa", "Giường đôi"]
        
    def tinh_gia_phong(self, so_dem):
        return self.gia_niem_yet * so_dem

class PhongVIP(Phong):
    def __init__(self, so_phong, tang, gia_niem_yet=800000):
        super().__init__(so_phong, tang, LoaiPhong.VIP, gia_niem_yet)
        self.tien_ich = ["WiFi", "TV", "Điều hòa","Giường đôi", "Mini bar", "View đẹp","Miễn phí bữa sáng"]
        
    def tinh_gia_phong(self, so_dem):
        return self.gia_niem_yet * so_dem * 1.1

class PhongSuite(Phong):
    def __init__(self, so_phong, tang, gia_niem_yet=1500000):
        super().__init__(so_phong, tang, LoaiPhong.SUITE, gia_niem_yet)
        self.tien_ich = [
            "WiFi", "TV", "Điều hòa","Giường King", "Mini bar", "Miễn phí bữa sáng",
            "View đẹp nhất", "Bồn tắm massage", "Phòng khách riêng"]
        
    def tinh_gia_phong(self, so_dem):
        return self.gia_niem_yet * so_dem * 1.2
    
    def thong_tin(self):
        return {
            "Số phòng": self.so_phong,
            "Tầng": self.tang,
            "Loại": self.loai_phong.value,
            "Giá": self.gia_niem_yet,
            "Trạng thái": self.trang_thai.value,
            "Tiện ích": self.tien_ich
    }