import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from models.KhachHang import KhachHang
from utils.ngoai_le import NgayKhongHopLe

class HopThoaiDatPhong(tk.Toplevel):
    
    def __init__(self, parent, phong):
        super().__init__(parent)
        self.phong = phong
        self.ket_qua = None
        self.title(f" Check-in - Phòng {phong.so_phong}")
        self.geometry("450x500")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        
        try:
            self.iconbitmap('icon.ico')
        except:
            pass
        
        self.tao_widgets()
        self.cap_nhat_tien()
    
    def tao_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=" CHECK-IN", 
                  font=('Arial', 16, 'bold')).pack(pady=5)
        
        info_frame = ttk.LabelFrame(main_frame, text=" Thông tin phòng")
        info_frame.pack(fill=tk.X, pady=5)
        
        try:
            gia_1_dem = self.phong.tinh_gia_theo_ngay()
        except:
            gia_1_dem = self.phong.gia_niem_yet
        
        thong_tin = [
            ("Số phòng:", self.phong.so_phong),
            ("Tầng:", str(self.phong.tang)),
            ("Loại phòng:", self.phong.loai_phong.value),
            ("Giá/đêm:", f"{gia_1_dem:,.0f} VNĐ"),
        ]
        
        for i, (label, value) in enumerate(thong_tin):
            ttk.Label(info_frame, text=label, font=('Arial', 9, 'bold')).grid(
                row=i, column=0, sticky=tk.W, padx=10, pady=3)
            ttk.Label(info_frame, text=value, font=('Arial', 9)).grid(
                row=i, column=1, sticky=tk.W, padx=10, pady=3)
        
        khach_frame = ttk.LabelFrame(main_frame, text="👤 Thông tin khách hàng")
        khach_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(khach_frame, text="Họ tên *:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.name_entry = ttk.Entry(khach_frame, width=25, font=('Arial', 10))
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(khach_frame, text="CMND/CCCD *:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.id_entry = ttk.Entry(khach_frame, width=25, font=('Arial', 10))
        self.id_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(khach_frame, text="Số điện thoại *:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.phone_entry = ttk.Entry(khach_frame, width=25, font=('Arial', 10))
        self.phone_entry.grid(row=2, column=1, padx=10, pady=5)
        
        dat_frame = ttk.LabelFrame(main_frame, text=" Thông tin đặt phòng")
        dat_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(dat_frame, text="Ngày nhận:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.check_in_entry = ttk.Entry(dat_frame, width=20, font=('Arial', 10))
        self.check_in_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.check_in_entry.grid(row=0, column=1, padx=10, pady=5)
        self.check_in_entry.bind('<KeyRelease>', self.cap_nhat_tien)
        
        ttk.Label(dat_frame, text="Ngày trả:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.check_out_entry = ttk.Entry(dat_frame, width=20, font=('Arial', 10))
        self.check_out_entry.insert(0, (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))
        self.check_out_entry.grid(row=1, column=1, padx=10, pady=5)
        self.check_out_entry.bind('<KeyRelease>', self.cap_nhat_tien)
        
        self.tien_frame = ttk.LabelFrame(main_frame, text=" Tổng tiền")
        self.tien_frame.pack(fill=tk.X, pady=5)
        
        self.tong_tien_label = ttk.Label(self.tien_frame, text="0 VNĐ", 
                                         font=('Arial', 16, 'bold'), foreground='red')
        self.tong_tien_label.pack(pady=5)
        
        self.chi_tiet_label = ttk.Label(self.tien_frame, text="", font=('Arial', 9))
        self.chi_tiet_label.pack(pady=2)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=15)
        
        ttk.Button(button_frame, text=" Xác nhận đặt phòng", 
                   command=self.xac_nhan, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Hủy", 
                   command=self.destroy, width=10).pack(side=tk.LEFT, padx=5)
        
        self.bind('<Return>', lambda e: self.xac_nhan())
        self.bind('<Escape>', lambda e: self.destroy())
    
    def cap_nhat_tien(self, event=None):
        try:
            ngay_nhan = datetime.strptime(self.check_in_entry.get(), "%Y-%m-%d").date()
            ngay_tra = datetime.strptime(self.check_out_entry.get(), "%Y-%m-%d").date()
            so_dem = (ngay_tra - ngay_nhan).days
            
            if so_dem > 0:
                tong_tien = self.phong.tinh_gia_phong(so_dem)
                self.tong_tien_label.config(text=f"{tong_tien:,.0f} VNĐ")
                self.chi_tiet_label.config(
                    text=f"× {so_dem} đêm = {tong_tien:,.0f} VNĐ"
                )
            elif so_dem == 0:
                self.tong_tien_label.config(text=" 0 đêm")
                self.chi_tiet_label.config(text="Ngày trả phải sau ngày nhận")
            else:
                self.tong_tien_label.config(text=" Lỗi")
                self.chi_tiet_label.config(text="Ngày không hợp lệ")
        except ValueError:
            self.tong_tien_label.config(text=" Định dạng sai")
            self.chi_tiet_label.config(text="Vui lòng nhập YYYY-MM-DD")
        except Exception as e:
            self.tong_tien_label.config(text=" Lỗi")
            self.chi_tiet_label.config(text=str(e))
    
    def xac_nhan(self):
        try:
            ho_ten = self.name_entry.get().strip()
            so_cmnd = self.id_entry.get().strip()
            so_dien_thoai = self.phone_entry.get().strip()
            email = self.email_entry.get().strip()
            
            if not ho_ten:
                messagebox.showerror("Lỗi", "Vui lòng nhập họ tên khách hàng")
                self.name_entry.focus()
                return
            
            if not so_cmnd:
                messagebox.showerror("Lỗi", "Vui lòng nhập số CMND/CCCD")
                self.id_entry.focus()
                return
            
            if not so_dien_thoai:
                messagebox.showerror("Lỗi", "Vui lòng nhập số điện thoại")
                self.phone_entry.focus()
                return
            
            ngay_nhan = datetime.strptime(self.check_in_entry.get().strip(), "%Y-%m-%d").date()
            ngay_tra = datetime.strptime(self.check_out_entry.get().strip(), "%Y-%m-%d").date()
            
            if ngay_nhan >= ngay_tra:
                messagebox.showerror("Lỗi", "Ngày trả phòng phải sau ngày nhận phòng")
                return
            
            if ngay_nhan < datetime.now().date():
                messagebox.showerror("Lỗi", "Ngày nhận phòng không thể trong quá khứ")
                return
            
            khach_hang = KhachHang(ho_ten, so_cmnd, so_dien_thoai, email)
            
            so_dem = (ngay_tra - ngay_nhan).days
            tong_tien = self.phong.tinh_gia_phong(so_dem)
            
            confirm = messagebox.askyesno(
                " Xác nhận đặt phòng",
                f" XÁC NHẬN ĐẶT PHÒNG\n\n"
                f" Phòng: {self.phong.so_phong} - {self.phong.loai_phong.value}\n"
                f" Khách hàng: {ho_ten}\n"
                f" Ngày nhận: {ngay_nhan.strftime('%d/%m/%Y')}\n"
                f" Ngày trả: {ngay_tra.strftime('%d/%m/%Y')}\n"
                f" Số đêm: {so_dem}\n"
                f" Tổng tiền: {tong_tien:,.0f} VNĐ\n\n"
                f" Xác nhận đặt phòng này?"
            )
            
            if confirm:
                self.ket_qua = (khach_hang, ngay_nhan, ngay_tra)
                self.destroy()
            
        except ValueError as e:
            messagebox.showerror("Lỗi", f"Định dạng ngày không hợp lệ:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra:\n{str(e)}")