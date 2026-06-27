class KhachHang:
    def __init__(self, ho_ten, so_cccd, so_dien_thoai,):
        self.ho_ten = ho_ten
        self.so_cmnd = so_cccd
        self.so_dien_thoai = so_dien_thoai
        self.lich_su_dat_phong = []
    
    def them_dat_phong(self, dat_phong):
        self.lich_su_dat_phong.append(dat_phong)
    
    def __str__(self):
        return f"{self.ho_ten} - {self.so_cccd}"