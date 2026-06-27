from datetime import datetime, date
from models.don_dat_phong import DonDatPhong
from models.phong import TrangThaiPhong
from utils.ngoai_le import PhongKhongSanCo, NgayKhongHopLe

class QuanLyDatPhong:
    def __init__(self, quan_ly_phong):
        self.quan_ly_phong = quan_ly_phong
        self.danh_sach_dat_phong = []
        self.bo_dem_dat_phong = 1
    
    def tao_dat_phong(self, khach_hang, so_phong, ngay_nhan, ngay_tra):

        if isinstance(ngay_nhan, str):
            ngay_nhan = datetime.strptime(ngay_nhan, "%Y-%m-%d").date()
        elif isinstance(ngay_nhan, datetime):
            ngay_nhan = ngay_nhan.date()
            
        if isinstance(ngay_tra, str):
            ngay_tra = datetime.strptime(ngay_tra, "%Y-%m-%d").date()
        elif isinstance(ngay_tra, datetime):
            ngay_tra = ngay_tra.date()

        hom_nay = date.today()

        if ngay_nhan >= ngay_tra:
            raise NgayKhongHopLe("Ngày nhận phòng phải trước ngày trả phòng!")
        
        if ngay_nhan < hom_nay:
            raise NgayKhongHopLe("Ngày nhận phòng không thể trong quá khứ!")
        
        # 3. Kiểm tra sự tồn tại của phòng
        phong = self.quan_ly_phong.lay_phong(so_phong)
        if not phong:
            raise PhongKhongSanCo(f"Phòng {so_phong} không tồn tại trên hệ thống!")
        
      
        if phong.trang_thai != TrangThaiPhong.TRONG:
            raise PhongKhongSanCo(
                f"Phòng {so_phong} hiện không sẵn sàng (Trạng thái: {phong.trang_thai.value})"
            )
      
        dat_phong = DonDatPhong(
            ma_dat_phong=self.bo_dem_dat_phong,
            khach_hang=khach_hang,
            phong=phong,
            ngay_nhan=ngay_nhan,
            ngay_tra=ngay_tra
        )
        
   
        dat_phong.trang_thai = "Đã đặt" 
        
        self.danh_sach_dat_phong.append(dat_phong)
        self.bo_dem_dat_phong += 1
        
        # 6. Cập nhật trạng thái phòng dựa trên ngày nhận
        # Nếu đặt nhận phòng ngay hôm nay thì chuyển sang ĐANG_O, nếu đặt trước thì giữ nguyên TRONG
        if ngay_nhan == hom_nay:
            phong.trang_thai = TrangThaiPhong.DANG_O
        
        return dat_phong
    
    def tra_phong(self, ma_dat_phong):
        dat_phong = self.lay_dat_phong(ma_dat_phong)
        if not dat_phong:
            return None
        
       
        dat_phong.phong.trang_thai = TrangThaiPhong.DANG_DON
        dat_phong.trang_thai = "Đã trả phòng"
        
        return dat_phong.tong_tien
    
    def lay_dat_phong(self, ma_dat_phong):

        try:
            ma_dat_phong = int(ma_dat_phong)
        except ValueError:
            return None

        for dat_phong in self.danh_sach_dat_phong:
            if int(dat_phong.ma_dat_phong) == ma_dat_phong:
                return dat_phong
        return None
    
    def lay_dat_phong_theo_khach(self, so_cmnd):
        return [d for d in self.danh_sach_dat_phong if str(d.khach_hang.so_cmnd) == str(so_cmnd)]
    
    def lay_dat_phong_dang_hoat_dong(self):
    
        return [d for d in self.danh_sach_dat_phong if d.trang_thai == "Đã đặt"]