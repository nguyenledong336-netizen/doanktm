import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

from models.phong import (
    TrangThaiPhong,
    LoaiPhong,
    PhongTieuChuan,
    PhongVIP,
    PhongSuite
)
from models.KhachHang import KhachHang
from services.quan_ly_phong import QuanLyPhong
from services.quan_ly_dat_phong import QuanLyDatPhong
from services.luu_tru_du_lieu import LuuTruDuLieu
from gui.luoi_phong import LuoiPhong
from gui.box_dat_phong import HopThoaiDatPhong
from gui.box_thong_ke import HopThoaiThongKe


class CuaSoChinh:
    """Cửa sổ chính của ứng dụng"""
    
    # gui/cua_so_chinh.py - Phần __init__
    def __init__(self, root):
        self.root = root
        self.root.title("🏨 Hệ thống quản lý khách sạn")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f0f0')
        
        # Khởi tạo services
        self.quan_ly_phong = QuanLyPhong()
        self.quan_ly_dat_phong = QuanLyDatPhong(self.quan_ly_phong)
        self.luu_tru = LuuTruDuLieu()
        
        # Tải dữ liệu từ file, nếu không có thì tạo mới
        print("📂 Đang tải dữ liệu...")
        if not self.luu_tru.tai_du_lieu(self.quan_ly_phong, self.quan_ly_dat_phong):
            print("📁 Không có dữ liệu, tạo mới...")
            self.tao_du_lieu_mau()
            self.luu_tru.luu_du_lieu(self.quan_ly_phong, self.quan_ly_dat_phong)
        
        # Debug: In số lượng phòng
        so_phong = len(self.quan_ly_phong.lay_tat_ca_phong())
        print(f"📊 Tổng số phòng: {so_phong}")
        
        # Tạo giao diện
        self.tao_menu()
        self.tao_khung_chinh()
        self.tao_thanh_trang_thai()
        
        # Làm mới hiển thị
        self.lam_moi()
        
        # Thiết lập sự kiện đóng cửa sổ
        self.root.protocol("WM_DELETE_WINDOW", self.thoat_chuong_trinh)
    
    def tao_du_lieu_mau(self):
        """Tạo dữ liệu mẫu 6 tầng, mỗi tầng 8 phòng"""
        # Tạo 6 tầng
        for tang in range(1, 7):
            self.quan_ly_phong.them_tang(tang)
        
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
                
                self.quan_ly_phong.them_phong(phong)
    
    def tao_menu(self):
        """Tạo thanh menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📁 File", menu=file_menu)
        file_menu.add_command(label="💾 Lưu dữ liệu", command=self.luu_du_lieu, accelerator="Ctrl+S")
        file_menu.add_command(label="📂 Tải dữ liệu", command=self.tai_du_lieu)
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Thoát", command=self.thoat_chuong_trinh, accelerator="Ctrl+Q")
        
        # Menu Quản lý
        quan_ly_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🔧 Quản lý", menu=quan_ly_menu)
        quan_ly_menu.add_command(label="📊 Xem thống kê", command=self.xem_thong_ke)
        quan_ly_menu.add_command(label="📜 Lịch sử đặt phòng", command=self.xem_lich_su)
        quan_ly_menu.add_separator()
        quan_ly_menu.add_command(label="🔄 Làm mới", command=self.lam_moi, accelerator="F5")
        
        # Menu Trợ giúp
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ Trợ giúp", menu=help_menu)
        help_menu.add_command(label="📖 Hướng dẫn", command=self.hien_thi_huong_dan)
        help_menu.add_command(label="ℹ️ Thông tin", command=self.hien_thi_thong_tin)
        
        # Phím tắt
        self.root.bind('<Control-s>', lambda e: self.luu_du_lieu())
        self.root.bind('<F5>', lambda e: self.lam_moi())
        self.root.bind('<Control-q>', lambda e: self.thoat_chuong_trinh())
    
    def tao_khung_chinh(self):
        """Tạo khung chính"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # === Khung trái: Sơ đồ phòng ===
        # ĐÃ SỬA: Xóa tham số font
        left_frame = ttk.LabelFrame(main_frame, text="📋 Sơ đồ phòng khách sạn")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Thanh công cụ lọc
        toolbar_frame = ttk.Frame(left_frame)
        toolbar_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(toolbar_frame, text="🔍 Lọc:").pack(side=tk.LEFT, padx=5)
        
        self.loai_phong_var = tk.StringVar(value="Tất cả")
        loai_combo = ttk.Combobox(toolbar_frame, textvariable=self.loai_phong_var,
                                  values=["Tất cả"] + [l.value for l in LoaiPhong],
                                  width=15, state="readonly")
        loai_combo.pack(side=tk.LEFT, padx=5)
        loai_combo.bind('<<ComboboxSelected>>', self.loc_phong_theo_loai)
        
        ttk.Button(toolbar_frame, text="🔄 Làm mới", 
                   command=self.lam_moi).pack(side=tk.RIGHT, padx=5)
        
        # Sơ đồ phòng
        self.luoi_phong = LuoiPhong(left_frame, self.quan_ly_phong, self.khi_click_phong)
        self.luoi_phong.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # === Khung phải: Thông tin và chức năng ===
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # ĐÃ SỬA: Xóa tham số font
        self.detail_frame = ttk.LabelFrame(right_frame, text="📝 Chi tiết phòng")
        self.detail_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.detail_text = tk.Text(self.detail_frame, height=12, width=35,
                                   font=('Arial', 10), wrap=tk.WORD)
        self.detail_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ĐÃ SỬA: Xóa tham số font
        booking_frame = ttk.LabelFrame(right_frame, text="📌 Đặt phòng đang hoạt động")
        booking_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.booking_list = tk.Listbox(booking_frame, height=10, font=('Arial', 9))
        self.booking_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Nút chức năng
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="✅ Check-in", 
                   command=self.check_in, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="💳 Check-out", 
                   command=self.check_out, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="📊 Thống kê", 
                   command=self.xem_thong_ke, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="🔄 Làm mới", 
                   command=self.lam_moi, width=12).pack(side=tk.LEFT, padx=2)
    
    def tao_thanh_trang_thai(self):
        """Tạo thanh trạng thái"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_bar = ttk.Label(status_frame, text="🟢 Sẵn sàng", 
                                    relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.status_time = ttk.Label(status_frame, 
                                     text=datetime.now().strftime("%H:%M:%S"),
                                     relief=tk.SUNKEN, anchor=tk.E, width=10)
        self.status_time.pack(side=tk.RIGHT)
        
        # Cập nhật thời gian
        self.update_time()
    
    def update_time(self):
        """Cập nhật thời gian trên thanh trạng thái"""
        self.status_time.config(text=datetime.now().strftime("%H:%M:%S"))
        self.root.after(1000, self.update_time)
    
    def loc_phong_theo_loai(self, event=None):
        """Lọc phòng theo loại"""
        loai = self.loai_phong_var.get()
        if loai == "Tất cả":
            self.luoi_phong.loc_loai = None
        else:
            for l in LoaiPhong:
                if l.value == loai:
                    self.luoi_phong.loc_loai = l
                    break
        self.luoi_phong.lam_moi()
    
    def khi_click_phong(self, phong):
        """Xử lý khi click vào phòng"""
        if phong:
            self.hien_thi_chi_tiet_phong(phong)
            self.status_bar.config(text=f"🟢 Đã chọn phòng {phong.so_phong} (Tầng {phong.tang})")
    
    def hien_thi_chi_tiet_phong(self, phong):
        """Hiển thị chi tiết phòng"""
        self.detail_text.delete(1.0, tk.END)
        
        trang_thai_icons = {
            TrangThaiPhong.TRONG: "🟢",
            TrangThaiPhong.DANG_O: "🔴",
            TrangThaiPhong.DANG_DON: "🟡",
            TrangThaiPhong.BAO_TRI: "⚪"
        }
        
        try:
            gia_1_dem = phong.tinh_gia_theo_ngay()
        except:
            gia_1_dem = phong.gia_niem_yet
        
        details = f"""
🏨 PHÒNG: {phong.so_phong}
📌 Tầng: {phong.tang}
⭐ Loại: {phong.loai_phong.value}
💵 Giá niêm yết: {phong.gia_niem_yet:,.0f} VNĐ/đêm
💲 Giá thực tế: {gia_1_dem:,.0f} VNĐ/đêm
📊 Trạng thái: {trang_thai_icons.get(phong.trang_thai, '')} {phong.trang_thai.value}

📝 Mô tả:
{phong.mo_ta if hasattr(phong, 'mo_ta') else 'Không có mô tả'}

🔧 Tiện ích:
{chr(10).join(['• ' + item for item in phong.tien_ich])}
        """
        
        if hasattr(phong, 'he_so'):
            details += f"\n📈 Hệ số: {phong.he_so}"
        
        if hasattr(phong, 'phi_dich_vu'):
            details += f"\n💰 Phí dịch vụ: {phong.phi_dich_vu * 100:.0f}%"
        
        if hasattr(phong, 'phi_phuc_vu_phong'):
            details += f"\n🧹 Phí phục vụ phòng: {phong.phi_phuc_vu_phong:,.0f} VNĐ/đêm"
        
        self.detail_text.insert(1.0, details)
    
    def check_in(self):
        """Xử lý check-in"""
        phong_chon = self.luoi_phong.lay_phong_chon()
        if not phong_chon:
            messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng chọn một phòng từ sơ đồ")
            return
        
        if phong_chon.trang_thai != TrangThaiPhong.TRONG:
            messagebox.showerror("❌ Lỗi", 
                f"Phòng {phong_chon.so_phong} không sẵn sàng!\n"
                f"Trạng thái hiện tại: {phong_chon.trang_thai.value}")
            return
        
        # Mở hộp thoại đặt phòng
        dialog = HopThoaiDatPhong(self.root, phong_chon)
        self.root.wait_window(dialog)
        
        if dialog.ket_qua:
            khach_hang, ngay_nhan, ngay_tra = dialog.ket_qua
            try:
                dat_phong = self.quan_ly_dat_phong.tao_dat_phong(
                    khach_hang,
                    phong_chon.so_phong,
                    ngay_nhan,
                    ngay_tra
                )
                
                messagebox.showinfo("✅ Thành công", 
                    f"Check-in thành công!\n\n"
                    f"📋 Mã đặt phòng: #{dat_phong.ma_dat_phong}\n"
                    f"👤 Khách hàng: {khach_hang.ho_ten}\n"
                    f"🏨 Phòng: {phong_chon.so_phong}\n"
                    f"📅 Ngày nhận: {ngay_nhan.strftime('%d/%m/%Y')}\n"
                    f"📅 Ngày trả: {ngay_tra.strftime('%d/%m/%Y')}\n"
                    f"💰 Tổng tiền: {dat_phong.tong_tien:,.0f} VNĐ"
                )
                self.lam_moi()
                self.luu_du_lieu()
                
            except Exception as e:
                messagebox.showerror("❌ Lỗi", f"Không thể thực hiện check-in:\n{str(e)}")
    
    def check_out(self):
        """Xử lý check-out và thanh toán"""
        selection = self.booking_list.curselection()
        if not selection:
            messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng chọn đặt phòng từ danh sách")
            return
        
        booking_text = self.booking_list.get(selection[0])
        if booking_text == "📭 Không có đặt phòng nào":
            messagebox.showwarning("⚠️ Cảnh báo", "Không có đặt phòng nào để check-out")
            return
        
        try:
            ma_dat_phong = int(booking_text.split("#")[1].split(" - ")[0])
        except:
            messagebox.showerror("❌ Lỗi", "Không thể lấy mã đặt phòng")
            return
        
        dat_phong = self.quan_ly_dat_phong.lay_dat_phong(ma_dat_phong)
        if not dat_phong:
            messagebox.showerror("❌ Lỗi", "Không tìm thấy đặt phòng")
            return
        
        # Lấy thông tin thanh toán
        thong_tin = dat_phong.lay_thong_tin_thanh_toan()
        
        # Tạo cửa sổ thanh toán
        self.hien_thi_thanh_toan(dat_phong, thong_tin)
    
    def hien_thi_thanh_toan(self, dat_phong, thong_tin):
        """Hiển thị cửa sổ thanh toán"""
        window = tk.Toplevel(self.root)
        window.title("💳 Thanh toán")
        window.geometry("500x600")
        window.transient(self.root)
        window.grab_set()
        window.resizable(False, False)
        
        main_frame = ttk.Frame(window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tiêu đề
        ttk.Label(main_frame, text="💳 THANH TOÁN", 
                  font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Khung thông tin
        info_frame = ttk.LabelFrame(main_frame, text="📋 Chi tiết đặt phòng")
        info_frame.pack(fill=tk.X, pady=10)
        
        cac_thong_tin = [
            ("Mã đặt phòng:", f"#{thong_tin['ma_dat_phong']}"),
            ("Khách hàng:", thong_tin['khach_hang']),
            ("Phòng:", thong_tin['so_phong']),
            ("Hạng phòng:", thong_tin['hang_phong']),
            ("Ngày nhận:", thong_tin['ngay_nhan']),
            ("Ngày trả:", thong_tin['ngay_tra']),
            ("Số đêm:", str(thong_tin['so_dem'])),
            ("Giá/đêm:", f"{thong_tin['gia_moi_dem']:,.0f} VNĐ"),
        ]
        
        for i, (label, value) in enumerate(cac_thong_tin):
            ttk.Label(info_frame, text=label, font=('Arial', 9, 'bold')).grid(
                row=i, column=0, sticky=tk.W, padx=10, pady=3)
            ttk.Label(info_frame, text=value, font=('Arial', 9)).grid(
                row=i, column=1, sticky=tk.W, padx=10, pady=3)
        
        # Tổng tiền
        tong_frame = ttk.LabelFrame(main_frame, text="💰 Tổng cộng")
        tong_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(tong_frame, text=f"{thong_tin['tong_tien']:,.0f} VNĐ", 
                  font=('Arial', 20, 'bold'), foreground='red').pack(pady=10)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        def xac_nhan_thanh_toan():
            if messagebox.askyesno("Xác nhận", "Xác nhận thanh toán và trả phòng?"):
                ket_qua = self.quan_ly_dat_phong.tra_phong(dat_phong.ma_dat_phong)
                if ket_qua:
                    messagebox.showinfo("✅ Thành công", 
                        f"Thanh toán thành công!\n\n"
                        f"💵 Tổng tiền: {ket_qua['tong_tien']:,.0f} VNĐ\n"
                        f"👤 Khách hàng: {ket_qua['khach_hang']}\n"
                        f"🏨 Phòng: {ket_qua['so_phong']}"
                    )
                    window.destroy()
                    self.lam_moi()
                    self.luu_du_lieu()
        
        ttk.Button(button_frame, text="✅ Xác nhận thanh toán", 
                   command=xac_nhan_thanh_toan, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Hủy", 
                   command=window.destroy, width=10).pack(side=tk.LEFT, padx=5)
    
    def xem_thong_ke(self):
        """Xem thống kê"""
        dialog = HopThoaiThongKe(self.root, self.quan_ly_phong, self.quan_ly_dat_phong)
        self.root.wait_window(dialog)
    
    def xem_lich_su(self):
        """Xem lịch sử đặt phòng"""
        window = tk.Toplevel(self.root)
        window.title("📜 Lịch sử đặt phòng")
        window.geometry("900x500")
        window.transient(self.root)
        window.grab_set()
        
        main_frame = ttk.Frame(window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="📜 LỊCH SỬ ĐẶT PHÒNG", 
                  font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Treeview
        columns = ('Mã', 'Khách hàng', 'Phòng', 'Loại', 'Ngày nhận', 'Ngày trả', 'Tổng tiền', 'Trạng thái')
        tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
        
        column_widths = {
            'Mã': 60,
            'Khách hàng': 150,
            'Phòng': 70,
            'Loại': 100,
            'Ngày nhận': 100,
            'Ngày trả': 100,
            'Tổng tiền': 120,
            'Trạng thái': 100
        }
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=column_widths.get(col, 100))
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Hiển thị dữ liệu
        if len(self.quan_ly_dat_phong.danh_sach_dat_phong) == 0:
            tree.insert('', 'end', values=('', 'Chưa có dữ liệu', '', '', '', '', '', ''))
        else:
            for dat_phong in self.quan_ly_dat_phong.danh_sach_dat_phong:
                tree.insert('', 'end', values=(
                    f"#{dat_phong.ma_dat_phong}",
                    dat_phong.khach_hang.ho_ten,
                    dat_phong.phong.so_phong,
                    dat_phong.phong.loai_phong.value,
                    dat_phong.ngay_nhan.strftime('%d/%m/%Y'),
                    dat_phong.ngay_tra.strftime('%d/%m/%Y'),
                    f"{dat_phong.tong_tien:,.0f}",
                    dat_phong.trang_thai
                ))
        
        ttk.Button(main_frame, text="Đóng", 
                   command=window.destroy).pack(pady=10)
    
    def lam_moi(self):
        """Làm mới toàn bộ giao diện"""
        # Cập nhật sơ đồ phòng
        self.luoi_phong.lam_moi()
        
        # Cập nhật danh sách đặt phòng
        self.booking_list.delete(0, tk.END)
        dat_phong_dang_hoat_dong = self.quan_ly_dat_phong.lay_dat_phong_dang_hoat_dong()
        
        if len(dat_phong_dang_hoat_dong) == 0:
            self.booking_list.insert(tk.END, "📭 Không có đặt phòng nào")
        else:
            for dp in dat_phong_dang_hoat_dong:
                self.booking_list.insert(tk.END, 
                    f"#{dp.ma_dat_phong} - {dp.khach_hang.ho_ten} - Phòng {dp.phong.so_phong} - {dp.ngay_tra.strftime('%d/%m')}"
                )
        
        # Cập nhật thanh trạng thái
        tong_phong = len(self.quan_ly_phong.lay_tat_ca_phong())
        phong_trong = len(self.quan_ly_phong.tim_phong_trong().to_list())
        phong_dang_o = len([p for p in self.quan_ly_phong.lay_tat_ca_phong() 
                           if p.trang_thai == TrangThaiPhong.DANG_O])
        
        self.status_bar.config(
            text=f"🏨 Tổng: {tong_phong} phòng | 🟢 Trống: {phong_trong} | 🔴 Đang ở: {phong_dang_o} | 🟡 Đang dọn: {len(dat_phong_dang_hoat_dong)} đặt phòng"
        )
    
    def luu_du_lieu(self):
        """Lưu dữ liệu"""
        try:
            self.luu_tru.luu_du_lieu(self.quan_ly_phong, self.quan_ly_dat_phong)
            self.status_bar.config(text="✅ Đã lưu dữ liệu thành công!")
        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Không thể lưu dữ liệu:\n{str(e)}")
    
    def tai_du_lieu(self):
        """Tải dữ liệu"""
        try:
            self.luu_tru.tai_du_lieu(self.quan_ly_phong, self.quan_ly_dat_phong)
            self.lam_moi()
            messagebox.showinfo("✅ Thành công", "Đã tải dữ liệu thành công!")
        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Không thể tải dữ liệu:\n{str(e)}")
    
    def thoat_chuong_trinh(self):
        """Thoát chương trình và giải phóng bộ nhớ"""
        if messagebox.askyesno("Xác nhận", "Bạn có muốn lưu dữ liệu trước khi thoát không?"):
            self.luu_du_lieu()
        
        # Giải phóng bộ nhớ
        self.quan_ly_phong.xoa_het()
        self.quan_ly_dat_phong.danh_sach_dat_phong.clear()
        
        self.root.destroy()
    
    def hien_thi_huong_dan(self):
        """Hiển thị hướng dẫn sử dụng"""
        huong_dan = """
📖 HƯỚNG DẪN SỬ DỤNG

1️⃣ CHỌN PHÒNG
   • Click vào phòng trên sơ đồ để xem chi tiết
   • Màu sắc: 🟢 Trống | 🔴 Đang ở | 🟡 Đang dọn | ⚪ Bảo trì

2️⃣ CHECK-IN
   • Chọn phòng trống (🟢)
   • Click nút "Check-in"
   • Nhập thông tin khách hàng
   • Xác nhận đặt phòng

3️⃣ CHECK-OUT & THANH TOÁN
   • Chọn đặt phòng trong danh sách
   • Click nút "Check-out"
   • Xem thông tin thanh toán
   • Xác nhận thanh toán

4️⃣ THỐNG KÊ
   • Click nút "Thống kê" để xem
   • Biểu đồ hiển thị tỷ lệ phòng
   • Thống kê doanh thu

5️⃣ LƯU DỮ LIỆU
   • Menu File → Lưu dữ liệu
   • Dữ liệu được lưu vào file JSON

⌨️ PHÍM TẮT
   • Ctrl+S: Lưu dữ liệu
   • F5: Làm mới
   • Ctrl+Q: Thoát
        """
        messagebox.showinfo("📖 Hướng dẫn sử dụng", huong_dan)
    
    def hien_thi_thong_tin(self):
        """Hiển thị thông tin về chương trình"""
        thong_tin = """
🏨 HỆ THỐNG ĐẶT CHỖ VÀ QUẢN LÝ PHÒNG KHÁCH SẠN

📌 Phiên bản: 2.0
📅 Ngày: 2024

🔧 Công nghệ sử dụng:
   • Python 3.x
   • Tkinter (GUI)
   • JSON (Lưu trữ)
   • OOP (Lập trình hướng đối tượng)

📊 Tính năng nâng cao:
   • Danh sách liên kết lồng nhau
   • Merge Sort
   • Xử lý ngoại lệ
   • Quản lý bộ nhớ động
   • Đa hình (Polymorphism)

👨‍💻 Phát triển bởi: Nhóm sinh viên
        """
        messagebox.showinfo("ℹ️ Thông tin", thong_tin)