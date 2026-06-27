# utils/ngoai_le.py
class PhongKhongSanCo(Exception):
    """Lỗi khi phòng không có sẵn"""
    pass

class NgayKhongHopLe(Exception):
    """Lỗi khi ngày tháng không hợp lệ"""
    pass

class KhachHangKhongTimThay(Exception):
    """Lỗi khi không tìm thấy khách hàng"""
    pass

class DatPhongKhongTimThay(Exception):
    """Lỗi khi không tìm thấy đặt phòng"""
    pass