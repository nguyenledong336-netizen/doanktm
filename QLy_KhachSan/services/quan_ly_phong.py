from models import phong
from structures.danh_sach_lien_ket import DanhSachLienKet
from models.phong import TrangThaiPhong, LoaiPhong, PhongTieuChuan, PhongVIP, PhongSuite

class Tang:
    def __init__(self, so_tang):
        self.so_tang = so_tang
        self.danh_sach_phong = DanhSachLienKet()

class QuanLyPhong:
    def __init__(self):
        self.cac_tang = DanhSachLienKet()  
    
    def them_tang(self, so_tang):
        try:
            so_tang = int(so_tang)
        except ValueError:
            pass
            
        tang = self.cac_tang.tim(lambda t: t.so_tang == so_tang)
        if tang:
            return False
        self.cac_tang.them(Tang(so_tang))
        return True
        
    def them_phong(self, phong):
        try:
            phong_tang = int(phong.tang)
        except ValueError:
            phong_tang = phong.tang

        tang = self.cac_tang.tim(lambda t: t.so_tang == phong_tang)
        if tang is None:
            print("Không tìm thấy tầng", phong.tang)
            return False

        tang.danh_sach_phong.them(phong)
        return True

    def tim_phong_trong(self, loai_phong=None):
        phong_trong = DanhSachLienKet()
        # Đã sửa lỗi: Duyệt chuẩn qua từng tầng rồi mới đến phòng
        for tang in self.cac_tang:
            for p in tang.danh_sach_phong:
                if p.trang_thai == TrangThaiPhong.TRONG:
                    if loai_phong is None or p.loai_phong == loai_phong:
                        phong_trong.them(p)
        return phong_trong

    def lay_phong(self, so_phong):
        so_phong = str(so_phong).strip()
        for tang in self.cac_tang:
            for p in tang.danh_sach_phong:
                if str(p.so_phong).strip() == so_phong:
                    return p
        return None

    def cap_nhat_trang_thai_phong(self, so_phong, trang_thai):
        phong = self.lay_phong(so_phong)
        if phong:
            phong.trang_thai = trang_thai
            return True
        return False

    def sap_xep_phong_theo_gia(self, danh_sach_phong, tang_dan=True):
        if len(danh_sach_phong) <= 1:
            return danh_sach_phong

        mid = len(danh_sach_phong) // 2
        trai = danh_sach_phong[:mid]
        phai = danh_sach_phong[mid:]

        trai = self.sap_xep_phong_theo_gia(trai, tang_dan)
        phai = self.sap_xep_phong_theo_gia(phai, tang_dan)

        return self._tron_theo_gia(trai, phai, tang_dan)

    def _tron_theo_gia(self, trai, phai, tang_dan=True):
        ket_qua = []
        i = j = 0

        while i < len(trai) and j < len(phai):
            if tang_dan:
                if trai[i].gia_niem_yet <= phai[j].gia_niem_yet:
                    ket_qua.append(trai[i])
                    i += 1
                else:
                    ket_qua.append(phai[j])
                    j += 1
            else:
                if trai[i].gia_niem_yet >= phai[j].gia_niem_yet:
                    ket_qua.append(trai[i])
                    i += 1
                else:
                    ket_qua.append(phai[j])
                    j += 1

        ket_qua.extend(trai[i:])
        ket_qua.extend(phai[j:])
        return ket_qua

    def sap_xep_phong_theo_tang(self, danh_sach_phong, tang_dan=True):
        if len(danh_sach_phong) <= 1:
            return danh_sach_phong

        mid = len(danh_sach_phong) // 2
        trai = danh_sach_phong[:mid]
        phai = danh_sach_phong[mid:]

        trai = self.sap_xep_phong_theo_tang(trai, tang_dan)
        phai = self.sap_xep_phong_theo_tang(phai, tang_dan)

        return self._tron_theo_tang(trai, phai, tang_dan)

    def _tron_theo_tang(self, trai, phai, tang_dan=True):
        ket_qua = []
        i = j = 0

        while i < len(trai) and j < len(phai):
            try:
                tang_trai = int(trai[i].tang)
                tang_phai = int(phai[j].tang)
            except ValueError:
                tang_trai = trai[i].tang
                tang_phai = phai[j].tang

            if tang_dan:
                if tang_trai <= tang_phai:
                    ket_qua.append(trai[i])
                    i += 1
                else:
                    ket_qua.append(phai[j])
                    j += 1
            else:
                if tang_trai >= tang_phai:
                    ket_qua.append(trai[i])
                    i += 1
                else:
                    ket_qua.append(phai[j])
                    j += 1

        ket_qua.extend(trai[i:])
        ket_qua.extend(phai[j:])
        return ket_qua

    def sap_xep_phong_da_tieu_chi(self, danh_sach_phong, tieu_chi="gia", tang_dan=True):
        if tieu_chi == "gia":
            return self.sap_xep_phong_theo_gia(danh_sach_phong, tang_dan)
        elif tieu_chi == "tang":
            return self.sap_xep_phong_theo_tang(danh_sach_phong, tang_dan)
        else:
            return danh_sach_phong

    def lay_tat_ca_phong(self):
        tat_ca_phong = []
        for tang in self.cac_tang:
            if hasattr(tang.danh_sach_phong, 'to_list'):
                tat_ca_phong.extend(tang.danh_sach_phong.to_list())
            else:
                for p in tang.danh_sach_phong:
                    tat_ca_phong.append(p)
        return tat_ca_phong

    def hien_thi_phong_sap_xep(self, tieu_chi="gia", tang_dan=True):
        tat_ca = self.lay_tat_ca_phong()
        return self.sap_xep_phong_da_tieu_chi(tat_ca, tieu_chi, tang_dan)

    def xoa_het(self):
        for tang in self.cac_tang:
            if hasattr(tang.danh_sach_phong, 'xoa_het'):
                tang.danh_sach_phong.xoa_het()
        if hasattr(self.cac_tang, 'xoa_het'):
            self.cac_tang.xoa_het()