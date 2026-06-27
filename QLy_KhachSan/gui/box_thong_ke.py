import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models.phong import TrangThaiPhong, LoaiPhong

class HopThoaiThongKe(tk.Toplevel):
    
    def __init__(self, parent, quan_ly_phong, quan_ly_dat_phong):
        super().__init__(parent)
        self.quan_ly_phong = quan_ly_phong
        self.quan_ly_dat_phong = quan_ly_dat_phong
        self.title(" Thống kê khách sạn")
        self.geometry("950x700")
        self.transient(parent)
        self.grab_set()
        
        try:
            self.iconbitmap('icon.ico')
        except:
            pass
        
        self.tao_widgets()
        self.hien_thi_thong_ke()
    
    def tao_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=" THỐNG KÊ KHÁCH SẠN", 
                  font=('Arial', 16, 'bold')).pack(pady=5)
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.tab_phong = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_phong, text=" Thống kê phòng")
        
        self.tab_bieu_do = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_bieu_do, text=" Biểu đồ")
        
        self.tab_doanh_thu = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_doanh_thu, text=" Doanh thu")
        
        ttk.Button(main_frame, text="Đóng", command=self.destroy, width=10).pack(pady=5)
    
    def hien_thi_thong_ke(self):
        self.hien_thi_thong_ke_phong()
        self.hien_thi_bieu_do()
        self.hien_thi_doanh_thu()
    
    def hien_thi_thong_ke_phong(self):
        main_frame = ttk.Frame(self.tab_phong)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tong_quan = ttk.LabelFrame(main_frame, text="📊 Tổng quan")
        tong_quan.pack(fill=tk.X, pady=5)
        
        all_rooms = self.quan_ly_phong.lay_tat_ca_phong()
        tong = len(all_rooms)
        
        trong = len([r for r in all_rooms if r.trang_thai == TrangThaiPhong.TRONG])
        dang_o = len([r for r in all_rooms if r.trang_thai == TrangThaiPhong.DANG_O])
        dang_don = len([r for r in all_rooms if r.trang_thai == TrangThaiPhong.DANG_DON])
        bao_tri = len([r for r in all_rooms if r.trang_thai == TrangThaiPhong.BAO_TRI])
        
        stats_frame = ttk.Frame(tong_quan)
        stats_frame.pack(pady=10)
        
        cac_thong_ke = [
            ("Tổng số phòng", tong, "#2196F3"),
            ("🟢 Phòng trống", trong, "#4CAF50"),
            ("🔴 Phòng đang ở", dang_o, "#F44336"),
            ("🟡 Phòng đang dọn", dang_don, "#FF9800"),
            ("⚪ Phòng bảo trì", bao_tri, "#9E9E9E"),
        ]
        
        for i, (label, value, color) in enumerate(cac_thong_ke):
            frame = ttk.Frame(stats_frame)
            frame.grid(row=i//3, column=i%3, padx=20, pady=5, sticky=tk.W)
            
            if i > 0:
                canvas = tk.Canvas(frame, width=20, height=20, bg=color, highlightthickness=1)
                canvas.pack(side=tk.LEFT)
            
            ttk.Label(frame, text=f"{label}: {value}", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        loai_frame = ttk.LabelFrame(main_frame, text=" Thống kê theo loại phòng")
        loai_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ('Loại phòng', 'Tổng', 'Trống', 'Đang ở', 'Đang dọn', 'Bảo trì', 'Tỷ lệ lấp đầy')
        tree = ttk.Treeview(loai_frame, columns=columns, show='headings', height=6)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == 'Loại phòng':
                tree.column(col, width=120)
            elif col == 'Tỷ lệ lấp đầy':
                tree.column(col, width=100)
            else:
                tree.column(col, width=80)
        
        scrollbar = ttk.Scrollbar(loai_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        thong_ke = self.quan_ly_phong.thong_ke_theo_loai()
        
        for loai, data in thong_ke.items():
            tong_loai = data['tong']
            trong_loai = data['trong']
            dang_o_loai = data['dang_o']
            
            if tong_loai > 0:
                ty_le_lap_day = ((dang_o_loai) / tong_loai) * 100
            else:
                ty_le_lap_day = 0
            
            tree.insert('', 'end', values=(
                loai.value,
                tong_loai,
                trong_loai,
                dang_o_loai,
                data['dang_don'],
                data['bao_tri'],
                f"{ty_le_lap_day:.1f}%"
            ))
    
    def hien_thi_bieu_do(self):
        main_frame = ttk.Frame(self.tab_bieu_do)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        
        all_rooms = self.quan_ly_phong.lay_tat_ca_phong()
        
        trang_thai = {
            'Trống': len([r for r in all_rooms if r.trang_thai == TrangThaiPhong.TRONG]),
            'Đang ở': len([r for r in all_rooms if r.trang_thai == TrangThaiPhong.DANG_O]),
            'Đang dọn': len([r for r in all_rooms if r.trang_thai == TrangThaiPhong.DANG_DON]),
            'Bảo trì': len([r for r in all_rooms if r.trang_thai == TrangThaiPhong.BAO_TRI])
        }
        
        mau_sac = ['#4CAF50', '#F44336', '#FF9800', '#9E9E9E']
        explode = (0.05, 0.05, 0.05, 0.05)
        
        ax1.pie(trang_thai.values(), labels=trang_thai.keys(), 
                autopct='%1.1f%%', colors=mau_sac, explode=explode,
                shadow=True, startangle=90)
        ax1.set_title(' Tỷ lệ trạng thái phòng', fontsize=12, fontweight='bold')
        
        thong_ke = self.quan_ly_phong.thong_ke_theo_loai()
        
        loai_phong = []
        tong_so = []
        dang_o = []
        
        for loai, data in thong_ke.items():
            loai_phong.append(loai.value)
            tong_so.append(data['tong'])
            dang_o.append(data['dang_o'])
        
        x = range(len(loai_phong))
        width = 0.35
        
        bars1 = ax2.bar([i - width/2 for i in x], tong_so, width, label='Tổng số', color='#2196F3')
        bars2 = ax2.bar([i + width/2 for i in x], dang_o, width, label='Đang ở', color='#F44336')
        
        ax2.set_xlabel('Loại phòng', fontsize=10)
        ax2.set_ylabel('Số lượng', fontsize=10)
        ax2.set_title(' Thống kê theo loại phòng', fontsize=12, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(loai_phong)
        ax2.legend()
        
        for bar in bars1:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        for bar in bars2:
            height = bar.get_height()
            if height > 0:
                ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def hien_thi_doanh_thu(self):
        main_frame = ttk.Frame(self.tab_doanh_thu)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tong_doanh_thu = self.quan_ly_dat_phong.tinh_doanh_thu()
        
        frame = ttk.LabelFrame(main_frame, text="💰 Tổng doanh thu")
        frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(frame, text=f"{tong_doanh_thu:,.0f} VNĐ", 
                  font=('Arial', 24, 'bold'), foreground='#4CAF50').pack(pady=20)
        
        doanh_thu_frame = ttk.LabelFrame(main_frame, text="📊 Doanh thu theo loại phòng")
        doanh_thu_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ('Loại phòng', 'Số lượt đặt', 'Doanh thu', 'Tỷ lệ')
        tree = ttk.Treeview(doanh_thu_frame, columns=columns, show='headings', height=5)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == 'Loại phòng':
                tree.column(col, width=150)
            elif col == 'Doanh thu':
                tree.column(col, width=200)
            else:
                tree.column(col, width=100)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        doanh_thu_theo_loai = {}
        so_luot_dat_theo_loai = {}
        
        for dat_phong in self.quan_ly_dat_phong.danh_sach_dat_phong:
            if dat_phong.trang_thai == "Đã trả phòng":
                loai = dat_phong.phong.loai_phong
                doanh_thu_theo_loai[loai] = doanh_thu_theo_loai.get(loai, 0) + dat_phong.tong_tien
                so_luot_dat_theo_loai[loai] = so_luot_dat_theo_loai.get(loai, 0) + 1
        
        for loai, doanh_thu in doanh_thu_theo_loai.items():
            so_luot = so_luot_dat_theo_loai.get(loai, 0)
            ty_le = (doanh_thu / tong_doanh_thu * 100) if tong_doanh_thu > 0 else 0
            
            tree.insert('', 'end', values=(
                loai.value,
                so_luot,
                f"{doanh_thu:,.0f} VNĐ",
                f"{ty_le:.1f}%"
            ))
        
        if len(doanh_thu_theo_loai) == 0:
            tree.insert('', 'end', values=('Chưa có dữ liệu', 0, '0 VNĐ', '0%'))