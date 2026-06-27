from datetime import datetime
from utils.ngoai_le import NgayKhongHopLe

class DonDatPhong:
    def __init__(self, ma_dat_phong, khach_hang, phong, ngay_nhan, ngay_tra):
        self.ma_dat_phong = ma_dat_phong
        self.khach_hang = khach_hang
        self.phong = phong
        self.ngay_nhan = ngay_nhan
        self.ngay_tra = ngay_tra
        self.tong_tien = 0
        self.trang_thai = "Đã đặt"
        self.ngay_tao = datetime.now()
        self.tinh_tong_tien()
    
    def tinh_tong_tien(self):
        so_dem = (self.ngay_tra - self.ngay_nhan).days
        if so_dem > 0:
            self.tong_tien = self.phong.tinh_gia_phong(so_dem)
        else:
            raise NgayKhongHopLe("Ngày trả phòng phải sau ngày nhận phòng")
    
    def lay_so_dem(self):
        return (self.ngay_tra - self.ngay_nhan).days
    
    def __str__(self):
        return f"Đặt phòng #{self.ma_dat_phong} - {self.khach_hang.ho_ten}"
       