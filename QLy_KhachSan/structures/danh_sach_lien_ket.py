class Nut:
    def __init__(self, du_lieu):
        self.du_lieu = du_lieu
        self.tiep_theo = None

class DanhSachLienKet:
    def __init__(self):
        self.dau = None
        self.kich_thuoc = 0
    
    def them(self, du_lieu):
        nut_moi = Nut(du_lieu)
        if not self.dau:
            self.dau = nut_moi
        else:
            hien_tai = self.dau
            while hien_tai.tiep_theo:
                hien_tai = hien_tai.tiep_theo
            hien_tai.tiep_theo = nut_moi
        self.kich_thuoc += 1
    
    def xoa(self, du_lieu):
        if not self.dau:
            return False
        
        if self.dau.du_lieu == du_lieu:
            self.dau = self.dau.tiep_theo
            self.kich_thuoc -= 1
            return True
        
        hien_tai = self.dau
        while hien_tai.tiep_theo:
            if hien_tai.tiep_theo.du_lieu == du_lieu:
                hien_tai.tiep_theo = hien_tai.tiep_theo.tiep_theo
                self.kich_thuoc -= 1
                return True
            hien_tai = hien_tai.tiep_theo
        return False
    
    def tim(self, dieu_kien):
        hien_tai = self.dau
        while hien_tai:
            if dieu_kien(hien_tai.du_lieu):
                return hien_tai.du_lieu
            hien_tai = hien_tai.tiep_theo
        return None
    
    def loc(self, dieu_kien):
        ket_qua = DanhSachLienKet()
        hien_tai = self.dau
        while hien_tai:
            if dieu_kien(hien_tai.du_lieu):
                ket_qua.them(hien_tai.du_lieu)
            hien_tai = hien_tai.tiep_theo
        return ket_qua
    
    def to_list(self):
        ket_qua = []
        hien_tai = self.dau
        while hien_tai:
            ket_qua.append(hien_tai.du_lieu)
            hien_tai = hien_tai.tiep_theo
        return ket_qua
    
    def __iter__(self):
        hien_tai = self.dau
        while hien_tai:
            yield hien_tai.du_lieu
            hien_tai = hien_tai.tiep_theo
    
    def __len__(self):
        return self.kich_thuoc
    
    def xoa_het(self):
        self.dau = None
        self.kich_thuoc = 0