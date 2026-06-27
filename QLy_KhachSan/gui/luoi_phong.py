import tkinter as tk
from tkinter import ttk
from models.phong import TrangThaiPhong, LoaiPhong

class LuoiPhong(ttk.Frame):
    
    def __init__(self, parent, quan_ly_phong, on_click_callback=None):
        super().__init__(parent)
        self.quan_ly_phong = quan_ly_phong
        self.on_click_callback = on_click_callback
        self.nut_bam = {}
        self.phong_chon = None
        self.loc_loai = None
        
        print(f"LuoiPhong init: {len(self.quan_ly_phong.lay_tat_ca_phong())} phòng")
        
        self.tao_luoi()
    
    def tao_luoi(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        self.nut_bam = {}
        
        tat_ca_phong = self.quan_ly_phong.lay_tat_ca_phong()
        
        print(f"TaoLuoi: {len(tat_ca_phong)} phòng")
        
        if len(tat_ca_phong) == 0:
            label = ttk.Label(self, text="⚠️ Không có phòng nào!\nVui lòng tạo dữ liệu mới.", 
                             font=('Arial', 14), foreground='red')
            label.pack(expand=True)
            return
        
        if self.loc_loai:
            tat_ca_phong = [p for p in tat_ca_phong if p.loai_phong == self.loc_loai]
            print(f"🔍 Sau lọc: {len(tat_ca_phong)} phòng")
        
        cac_tang = {}
        for phong in tat_ca_phong:
            if phong.tang not in cac_tang:
                cac_tang[phong.tang] = []
            cac_tang[phong.tang].append(phong)
        
        print(f"🔍 Số tầng: {len(cac_tang)}")
        
        self.tao_chu_thich()
        
        for so_tang in sorted(cac_tang.keys()):
            phong_tang = cac_tang[so_tang]
            
            tang_frame = ttk.Frame(self)
            tang_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=3)
            
            ttk.Label(tang_frame, text=f" Tầng {so_tang}", 
                     font=('Arial', 10, 'bold'), width=12).pack(side=tk.LEFT, padx=5)
            
            phong_frame = ttk.Frame(tang_frame)
            phong_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            for phong in sorted(phong_tang, key=lambda x: x.so_phong):
                ten_loai = {
                    LoaiPhong.TIEU_CHUAN: "T",
                    LoaiPhong.VIP: "V",
                    LoaiPhong.SUITE: "S"
                }.get(phong.loai_phong, "")
                
                mau_nen = self.lay_mau_trang_thai(phong.trang_thai)
                mau_chu = self.lay_mau_chu(phong.trang_thai)
                
                btn = tk.Button(
                    phong_frame,
                    text=f"{phong.so_phong}\n{ten_loai}",
                    width=7,
                    height=2,
                    bg=mau_nen,
                    fg=mau_chu,
                    relief=tk.RAISED,
                    font=('Arial', 8, 'bold'),
                    command=lambda p=phong: self.xu_ly_click_phong(p)
                )
                btn.pack(side=tk.LEFT, padx=2, pady=2)
                self.nut_bam[phong.so_phong] = btn
        
        print(f" Đã hiển thị {len(self.nut_bam)} phòng")
    
    def tao_chu_thich(self):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(frame, text="📌 Chú thích:  ", font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        
        ttk.Label(frame, text="T=Thường  ", font=('Arial', 9)).pack(side=tk.LEFT)
        ttk.Label(frame, text="V=VIP  ", font=('Arial', 9)).pack(side=tk.LEFT)
        ttk.Label(frame, text="S=Suite  ", font=('Arial', 9)).pack(side=tk.LEFT)
        
        ttk.Label(frame, text="  |  ").pack(side=tk.LEFT)
        
        mau_sac = [
            ("🟢", TrangThaiPhong.TRONG, "#90EE90"),
            ("🔴", TrangThaiPhong.DANG_O, "#FF6B6B"),
            ("🟡", TrangThaiPhong.DANG_DON, "#FFD93D"),
            ("⚪", TrangThaiPhong.BAO_TRI, "#C0C0C0"),
        ]
        
        for ky_hieu, trang_thai, mau in mau_sac:
            frame_con = ttk.Frame(frame)
            frame_con.pack(side=tk.LEFT, padx=3)
            
            canvas = tk.Canvas(frame_con, width=12, height=12, bg=mau, highlightthickness=1)
            canvas.pack(side=tk.LEFT)
            
            ttk.Label(frame_con, text=ky_hieu, font=('Arial', 8)).pack(side=tk.LEFT, padx=2)
    
    def lay_mau_trang_thai(self, trang_thai):
        mau_sac = {
            TrangThaiPhong.TRONG: "#90EE90",   
            TrangThaiPhong.DANG_O: "#FF6B6B",    
            TrangThaiPhong.DANG_DON: "#FFD93D",  
            TrangThaiPhong.BAO_TRI: "#C0C0C0"    
        }
        return mau_sac.get(trang_thai, "#FFFFFF")
    
    def lay_mau_chu(self, trang_thai):
        mau_sac = {
            TrangThaiPhong.TRONG: "#006400",     
            TrangThaiPhong.DANG_O: "#8B0000",      
            TrangThaiPhong.DANG_DON: "#8B7500",   
            TrangThaiPhong.BAO_TRI: "#4A4A4A"    
        }
        return mau_sac.get(trang_thai, "#000000")
    
    def xu_ly_click_phong(self, phong):
        self.phong_chon = phong
        if self.on_click_callback:
            self.on_click_callback(phong)
    
    def lay_phong_chon(self):
        """Lấy phòng đang được chọn"""
        return self.phong_chon
    
    def lam_moi(self):
        print("🔄 Làm mới LuoiPhong")
        self.tao_luoi()