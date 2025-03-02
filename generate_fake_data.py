import csv
import random
import datetime
import re
from faker import Faker
from faker.providers import person, address, phone_number, internet
from random import choice, randint, uniform, sample, choices
from datetime import datetime, timedelta

# Khởi tạo Faker với địa phương Việt Nam
fake = Faker('vi_VN')
fake.add_provider(person)
fake.add_provider(address)
fake.add_provider(phone_number)
fake.add_provider(internet)

# Dữ liệu metadata tiếng Việt
# Trạng thái đơn hàng
trang_thai_don_hang = [
    "Đã giao thành công",
    "Đã hủy",
    "Đã hoàn trả",
    "Đang giao",
    "Đang xử lý"
]

# Cập nhật tỷ lệ trạng thái theo yêu cầu mới
weights_trang_thai = [78, 15, 7, 0, 0]  # 78% thành công, 22% hoàn/hủy (15% hủy, 7% trả)

# Lý do hoàn hủy
ly_do_huy = [
    "Tìm được sản phẩm tốt hơn/rẻ hơn",
    "Màu sắc/mùi hương khác mong đợi",
    "Sản phẩm không phù hợp với làn da",
    "Không còn nhu cầu",
    "Người bán tư vấn chậm"
]

ly_do_tra = [
    "Giao sai hàng",
    "Không như mong đợi",
    "Giao thiếu hàng",
    "Giao sai màu, đặt đỏ giao hồng",
    "Hàng móp, không dùng được"
]

# Phương thức thanh toán
phuong_thuc_thanh_toan = {
    "Thanh toán khi nhận hàng (COD)": 60,
    "Ví ShopeePay": 20, 
    "SPayLater": 12,
    "Thẻ tín dụng/ghi nợ": 8
}

# Đơn vị vận chuyển
don_vi_van_chuyen = {
    "Nhanh-SPX Express": 65,
    "Nhanh-Giao Hàng Nhanh": 20,
    "Hỏa Tốc": 10,
    "Tiết kiệm-Viettel Post": 5
}

# Danh mục sản phẩm
danh_muc_san_pham = [
    "Trang điểm",
    "Chăm sóc da mặt",
    "Chăm sóc cơ thể",
    "Chăm sóc tóc",
    "Nước hoa",
    "Dụng cụ làm đẹp",
    "Chăm sóc răng miệng"
]

# Thương hiệu
thuong_hieu = [
    "XIXI", "GOGO TALES", "Colorkey", "Flowery", "HUNMUI", "VEECCI", 
    "Lameila", "Sweet Mint", "HERORANGE", "My Smile", "The Ordinary",
    "DEGO PHARMA", "Openeyes", "SEOMOU", "Eyelash Curlen", "Dikalu",
    "AHA Skinmenu", "YONGU", "HEYXI", "Maffick", "Maigoole", "INOD"
]

# Tạo danh sách sản phẩm từ dữ liệu đã cung cấp
san_pham = [
    {"ten": "XIXI Phấn Má Hồng 4 ô Nhũ Sáng Highlight", "gia_goc": 41000, "danh_muc": "Trang điểm", "thuong_hieu": "XIXI"},
    {"ten": "Mặt Nạ Vitamin B5 Colorkey 10 Miếng Hổ Trợ Dưỡng Trắng", "gia_goc": 139000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "Colorkey"},
    {"ten": "Combo dầu gội, dầu xả nước hoa muối biển Flowery 500ml", "gia_goc": 136000, "danh_muc": "Chăm sóc tóc", "thuong_hieu": "Flowery"},
    {"ten": "Bộ Trang Điểm 17 Món Xixi Phiên Bản Nâng Cấp", "gia_goc": 387000, "danh_muc": "Trang điểm", "thuong_hieu": "XIXI"},
    {"ten": "VEECCI Phấn Tạo Khối Phấn Má Hồng Kèm Highlight", "gia_goc": 90000, "danh_muc": "Trang điểm", "thuong_hieu": "VEECCI"},
    {"ten": "Combo sữa dưỡng thể, sữa tắm dưỡng trắng Niacinamide 500ml", "gia_goc": 56000, "danh_muc": "Chăm sóc cơ thể", "thuong_hieu": "HUNMUI"},
    {"ten": "Cushion Phấn Phủ Kết Hợp 2 Tầng GOGO TALES Vitality", "gia_goc": 67500, "danh_muc": "Trang điểm", "thuong_hieu": "GOGO TALES"},
    {"ten": "Set kem nền 4 món MSMEESHU chính hãng", "gia_goc": 120000, "danh_muc": "Trang điểm", "thuong_hieu": "MSMEESHU"},
    {"ten": "Serum hiệu chỉnh trắng răng MY SMILE - Công nghệ V34", "gia_goc": 39500, "danh_muc": "Chăm sóc răng miệng", "thuong_hieu": "My Smile"},
    {"ten": "Bộ 13 Cọ Trang Điểm Lông Mềm", "gia_goc": 38400, "danh_muc": "Dụng cụ làm đẹp", "thuong_hieu": "Lameila"},
    {"ten": "XỊT KHÓA NỀN MAKEUP FIXER SPRAY GIỮ CHẶT LỚP TRANG ĐIỂM", "gia_goc": 42500, "danh_muc": "Trang điểm", "thuong_hieu": "GOGO TALES"},
    {"ten": "Set trang điểm đầy đủ 16 món bản nâng cấp 2024", "gia_goc": 350000, "danh_muc": "Trang điểm", "thuong_hieu": "XIXI"},
    {"ten": "Bút kẻ mắt XIXI ngòi mảnh 0.1mm", "gia_goc": 11500, "danh_muc": "Trang điểm", "thuong_hieu": "XIXI"},
    {"ten": "Dầu gội nước hoa muối biển Flowery 500ml", "gia_goc": 79800, "danh_muc": "Chăm sóc tóc", "thuong_hieu": "Flowery"},
    {"ten": "Dầu Gội Đầu DEGO PHARMA 80ml Dứt Điểm Gàu Ngứa", "gia_goc": 320000, "danh_muc": "Chăm sóc tóc", "thuong_hieu": "DEGO PHARMA"},
    {"ten": "Sữa tắm dưỡng trắng Niacinamide - Unisex 500ml", "gia_goc": 110000, "danh_muc": "Chăm sóc cơ thể", "thuong_hieu": "HUNMUI"},
    {"ten": "Mặt nạ dưỡng da LAB 101 Provitamin B5", "gia_goc": 93500, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "LAB 101"},
    {"ten": "Serum hiệu chỉnh trắng răng My Smile", "gia_goc": 124500, "danh_muc": "Chăm sóc răng miệng", "thuong_hieu": "My Smile"},
    {"ten": "Kem Đánh Răng HUNMUI Dạng Gel Lỏng", "gia_goc": 150000, "danh_muc": "Chăm sóc răng miệng", "thuong_hieu": "HUNMUI"},
    {"ten": "Bảng mắt 9 ô secret garden GOGO TALES", "gia_goc": 99000, "danh_muc": "Trang điểm", "thuong_hieu": "GOGO TALES"},
    {"ten": "Combo 2 tẩy da chết body Dove", "gia_goc": 60000, "danh_muc": "Chăm sóc cơ thể", "thuong_hieu": "Dove"},
    {"ten": "Kem Tan Quầng Thâm Bọng Mắt Openeyes", "gia_goc": 180000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "Openeyes"},
    {"ten": "Kem lót Xixi, kem lót kiềm dầu dưỡng ẩm", "gia_goc": 70000, "danh_muc": "Trang điểm", "thuong_hieu": "XIXI"},
    {"ten": "Kẹp Mi Eyelash Curlen Nội địa Trung", "gia_goc": 35000, "danh_muc": "Dụng cụ làm đẹp", "thuong_hieu": "Eyelash Curlen"},
    {"ten": "Sữa Dưỡng Thể AHA Skinmenu 500ml", "gia_goc": 49500, "danh_muc": "Chăm sóc cơ thể", "thuong_hieu": "AHA Skinmenu"},
    {"ten": "Kem Ủ Trắng - Tắm Trắng HUNMUI", "gia_goc": 42500, "danh_muc": "Chăm sóc cơ thể", "thuong_hieu": "HUNMUI"},
    {"ten": "Phấn Phủ Bột GOGO TALES RAPT Kiềm Dầu", "gia_goc": 110000, "danh_muc": "Trang điểm", "thuong_hieu": "GOGO TALES"},
    {"ten": "Lược gỡ rối, tạo phồng tóc bán nguyệt", "gia_goc": 38000, "danh_muc": "Dụng cụ làm đẹp", "thuong_hieu": "Beauty Tools"},
    {"ten": "Mặt Nạ Sủi Bọt Thải Độc Cà Rốt (12 Gói)", "gia_goc": 69000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "SEOMOU"},
    {"ten": "Viên kích trắng alpha arbutin Thái Lan", "gia_goc": 75000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "Alpha Arbutin"},
    {"ten": "Combo 2 Hộp Kem Đánh Răng HUNMUI", "gia_goc": 300000, "danh_muc": "Chăm sóc răng miệng", "thuong_hieu": "HUNMUI"},
    {"ten": "Xixi Cọ Trang Điểm Đầu Dẹt", "gia_goc": 20000, "danh_muc": "Dụng cụ làm đẹp", "thuong_hieu": "XIXI"},
    {"ten": "Kem nền Xixi, kem nền nội địa trung", "gia_goc": 70000, "danh_muc": "Trang điểm", "thuong_hieu": "XIXI"},
    {"ten": "Chì kẻ mày SUAKE không trôi", "gia_goc": 17000, "danh_muc": "Trang điểm", "thuong_hieu": "SUAKE"},
    {"ten": "Phấn mắt nhũ MINSHZEE và highlight", "gia_goc": 20000, "danh_muc": "Trang điểm", "thuong_hieu": "MINSHZEE"},
    {"ten": "Mascara GlamColour Living Colorful", "gia_goc": 60000, "danh_muc": "Trang điểm", "thuong_hieu": "GlamColour"},
    {"ten": "Kem Giảm Nám, Chống Nhăn UCM Nhật Bản", "gia_goc": 169000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "UCM"},
    {"ten": "Tuýp Tẩy da Tế Bào Chết Môi HEYXI", "gia_goc": 45000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "HEYXI"},
    {"ten": "Bàn Chải Điện Tự Động Đánh Răng 5 Chế Độ", "gia_goc": 99000, "danh_muc": "Chăm sóc răng miệng", "thuong_hieu": "Electric Brush"},
    {"ten": "Hộp 50 cây tăm chỉ nha khoa", "gia_goc": 30000, "danh_muc": "Chăm sóc răng miệng", "thuong_hieu": "Dental Care"},
    {"ten": "Kem Chống Nắng Trắng Da HEYXI SPF 50+", "gia_goc": 75000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "HEYXI"},
    {"ten": "Mút tán kem nền, mút trang điểm", "gia_goc": 11000, "danh_muc": "Dụng cụ làm đẹp", "thuong_hieu": "Beauty Puff"},
    {"ten": "Dầu xả nước hoa muối biển Flowery 500ml", "gia_goc": 136666, "danh_muc": "Chăm sóc tóc", "thuong_hieu": "Flowery"},
    {"ten": "Set 3 cây son kem lì Hero Orange", "gia_goc": 60000, "danh_muc": "Trang điểm", "thuong_hieu": "HERORANGE"},
    {"ten": "Kẹo mầm sâm tố nữ Xmax Thảo Mộc 37", "gia_goc": 120000, "danh_muc": "Thực phẩm chức năng", "thuong_hieu": "Xmax"},
    {"ten": "Kem Đất Sét Amide Làm Sạch Sâu", "gia_goc": 29000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "Amide"},
    {"ten": "Mặt Nạ Nâng Cơ SEOMOU", "gia_goc": 75000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "SEOMOU"},
    {"ten": "Tinh Chất Peel da The Ordinary AHA 30%+BHA 2%", "gia_goc": 165000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "The Ordinary"},
    {"ten": "Mặt nạ mắt bioaqua 60 miếng", "gia_goc": 85000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "Bioaqua"},
    {"ten": "Cọ Trang Điểm Son Môi Đầu Tròn", "gia_goc": 12500, "danh_muc": "Dụng cụ làm đẹp", "thuong_hieu": "Beauty Tools"},
    {"ten": "Bảng phấn mắt Dikalu 20 ô", "gia_goc": 40000, "danh_muc": "Trang điểm", "thuong_hieu": "Dikalu"},
    {"ten": "Xịt Thơm Miệng Heyxi Vị Đào, Bạc hà", "gia_goc": 45000, "danh_muc": "Chăm sóc răng miệng", "thuong_hieu": "HEYXI"},
    {"ten": "Son kem lì Gogotales Rapt Zero Velvet Tint", "gia_goc": 75000, "danh_muc": "Trang điểm", "thuong_hieu": "GOGO TALES"},
    {"ten": "Bút Kẻ Mắt Sweet Mint Siêu Mịn", "gia_goc": 65000, "danh_muc": "Trang điểm", "thuong_hieu": "Sweet Mint"},
    {"ten": "Kem Dưỡng Trắng Da Huyết Rồng Linh Chi", "gia_goc": 35000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "Dragon Blood"},
    {"ten": "Giảm thâm quầng mắt The Ordinary Caffeine 5%", "gia_goc": 265000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "The Ordinary"},
    {"ten": "Serum hôi nách INOD Huyền Phi", "gia_goc": 230000, "danh_muc": "Chăm sóc cơ thể", "thuong_hieu": "INOD"},
    {"ten": "Phấn phủ dạng bột Maffick", "gia_goc": 45000, "danh_muc": "Trang điểm", "thuong_hieu": "Maffick"},
    {"ten": "Lược massage da đầu kích thích mọc tóc", "gia_goc": 25000, "danh_muc": "Dụng cụ làm đẹp", "thuong_hieu": "Hair Tools"},
    {"ten": "Kem dưỡng thể trắng da HUNMUI Body Cream", "gia_goc": 75000, "danh_muc": "Chăm sóc cơ thể", "thuong_hieu": "HUNMUI"},
    {"ten": "Combo 5 hộp kẹo mầm sâm tố nữ Xmax", "gia_goc": 480000, "danh_muc": "Thực phẩm chức năng", "thuong_hieu": "Xmax"},
    {"ten": "Chì Kẻ Mày Double Effect Lameila", "gia_goc": 30000, "danh_muc": "Trang điểm", "thuong_hieu": "Lameila"},
    {"ten": "Phấn Phủ Lameila - Phấn Nền Che Khuyết", "gia_goc": 85000, "danh_muc": "Trang điểm", "thuong_hieu": "Lameila"},
    {"ten": "Son lì HERORANGE mềm mịn như nhung", "gia_goc": 95000, "danh_muc": "Trang điểm", "thuong_hieu": "HERORANGE"},
    {"ten": "Gel đào thải mụn nghệ đỏ YONGU", "gia_goc": 180000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "YONGU"},
    {"ten": "Son Môi GOGOTALES Dưỡng Ẩm", "gia_goc": 80000, "danh_muc": "Trang điểm", "thuong_hieu": "GOGO TALES"},
    {"ten": "Son kem lì GOGO TALES Powder Yarn", "gia_goc": 105000, "danh_muc": "Trang điểm", "thuong_hieu": "GOGO TALES"},
    {"ten": "Mascara Siêu Mảnh tơi mi Lameila", "gia_goc": 90000, "danh_muc": "Trang điểm", "thuong_hieu": "Lameila"},
    {"ten": "Bộ 5 mảnh Set Kẹp Tóc Đính Đá", "gia_goc": 36000, "danh_muc": "Dụng cụ làm đẹp", "thuong_hieu": "Hair Clips"},
    {"ten": "Bình xịt chống nắng Maigoole SPF50", "gia_goc": 120000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "Maigoole"},
    {"ten": "Kem dưỡng da tay Hyaluronic Acid HIH", "gia_goc": 150000, "danh_muc": "Chăm sóc cơ thể", "thuong_hieu": "HIH"},
    {"ten": "Bộ Trang Điểm Lameila 20 món", "gia_goc": 380000, "danh_muc": "Trang điểm", "thuong_hieu": "Lameila"},
    {"ten": "Phấn Mắt Xixi 6 Màu Bắt Sáng", "gia_goc": 35000, "danh_muc": "Trang điểm", "thuong_hieu": "XIXI"},
    {"ten": "Tinh Chất Hút Nám Tàn Nhang Houmal", "gia_goc": 150000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "Houmal"},
    {"ten": "Bảng phấn mắt 9 ô Coco Venus Dikalu", "gia_goc": 90000, "danh_muc": "Trang điểm", "thuong_hieu": "Dikalu"},
    {"ten": "Bảng Phấn Tạo Khối Sweet Mint 4 ô", "gia_goc": 35000, "danh_muc": "Trang điểm", "thuong_hieu": "Sweet Mint"},
    {"ten": "Combo 2 Hộp Mặt Nạ Nâng Cơ SEOMOU", "gia_goc": 175000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "SEOMOU"},
    {"ten": "Sữa Dưỡng Thể Alpha Arbutin 3 Plus Collagen", "gia_goc": 199000, "danh_muc": "Chăm sóc cơ thể", "thuong_hieu": "Alpha Arbutin"},
    {"ten": "Cọ Đắp Mặt Nạ Silicon", "gia_goc": 19000, "danh_muc": "Dụng cụ làm đẹp", "thuong_hieu": "Mask Brush"},
    {"ten": "Dung Dịch Vệ Sinh Phụ Nữ Ume Tía Tô", "gia_goc": 250000, "danh_muc": "Chăm sóc cơ thể", "thuong_hieu": "Ume"},
    {"ten": "Xịt dưỡng thể trắng da TWG", "gia_goc": 180000, "danh_muc": "Chăm sóc cơ thể", "thuong_hieu": "TWG"},
    {"ten": "Miếng Che Mắt Chống Chói hình thú", "gia_goc": 25000, "danh_muc": "Dụng cụ làm đẹp", "thuong_hieu": "Eye Cover"},
    {"ten": "Phấn Phủ Bột Kiềm Dầu Lameila", "gia_goc": 65000, "danh_muc": "Trang điểm", "thuong_hieu": "Lameila"},
    {"ten": "Kem bôi nấm ngứa Dego Pharma 30g", "gia_goc": 250000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "DEGO PHARMA"},
    {"ten": "Heart Beauty Cải Thiện Nội Tiết Tố Nữ", "gia_goc": 260000, "danh_muc": "Thực phẩm chức năng", "thuong_hieu": "Heart Beauty"},
    {"ten": "Kem Thanh Che Khuyết Điểm LAMEILA", "gia_goc": 95000, "danh_muc": "Trang điểm", "thuong_hieu": "Lameila"},
    {"ten": "Kem Bơ YAQINUO Dưỡng Ẩm Săn Chắc", "gia_goc": 120000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "YAQINUO"},
    {"ten": "Kem nền trang điểm Lameila Bb cream", "gia_goc": 95000, "danh_muc": "Trang điểm", "thuong_hieu": "Lameila"},
    {"ten": "Kem Ủ Tóc Pinky Pinky Dưỡng Tóc", "gia_goc": 150000, "danh_muc": "Chăm sóc tóc", "thuong_hieu": "Pinky Pinky"},
    {"ten": "Phấn bắt sáng tạo khối 4 ô Gogo Tales", "gia_goc": 99000, "danh_muc": "Trang điểm", "thuong_hieu": "GOGO TALES"},
    {"ten": "Son môi lì mịn mượt như nhung lâu trôi", "gia_goc": 95000, "danh_muc": "Trang điểm", "thuong_hieu": "HERORANGE"},
    {"ten": "Nước Hoa Karri lưu hương cực lâu", "gia_goc": 120000, "danh_muc": "Nước hoa", "thuong_hieu": "Karri"},
    {"ten": "Combo 5 Bao Lì xì 2024 tết GIÁP THÌN", "gia_goc": 15000, "danh_muc": "Phụ kiện", "thuong_hieu": "Lucky Dragon"},
    {"ten": "Thanh Lăn Massage Mắt JOMTAM", "gia_goc": 120000, "danh_muc": "Dụng cụ làm đẹp", "thuong_hieu": "JOMTAM"},
    {"ten": "Set 6 Cây Son Kem Gấu Trúc Magic Casa", "gia_goc": 120000, "danh_muc": "Trang điểm", "thuong_hieu": "Magic Casa"},
    {"ten": "Bảng Phấn Má Hồng Sweet Mint 2 Màu", "gia_goc": 35000, "danh_muc": "Trang điểm", "thuong_hieu": "Sweet Mint"},
    {"ten": "Mặt nạ sủi bọt thải độc GINBI", "gia_goc": 35000, "danh_muc": "Chăm sóc da mặt", "thuong_hieu": "GINBI"},
    {"ten": "Bảng mắt 8 ô Gogotales Garden Bear", "gia_goc": 200000, "danh_muc": "Trang điểm", "thuong_hieu": "GOGO TALES"},
    {"ten": "Bảng Phấn Mắt 7 Ô GOGO TALES Oẳn Tù Tì", "gia_goc": 130000, "danh_muc": "Trang điểm", "thuong_hieu": "GOGO TALES"},
    {"ten": "Gel khóa màu son siêu bền màu T2", "gia_goc": 65000, "danh_muc": "Trang điểm", "thuong_hieu": "T2 Cosmetics"}
]

# Một số tỉnh/thành và quận/huyện ở Việt Nam
tinh_thanh = [
    "Hà Nội", "TP. Hồ Chí Minh", "Đà Nẵng", "Hải Phòng", "Cần Thơ", "Bình Dương", 
    "Đồng Nai", "Khánh Hòa", "Hải Dương", "Bà Rịa - Vũng Tàu", "Đắk Lắk", "Lâm Đồng", 
    "Thái Nguyên", "Quảng Ninh", "Hưng Yên", "Nam Định", "Thanh Hóa", "Nghệ An", 
    "Bắc Ninh", "Hà Tĩnh", "Quảng Ngãi", "Bình Thuận"
]

quan_huyen = {
    "Hà Nội": ["Cầu Giấy", "Ba Đình", "Hoàn Kiếm", "Đống Đa", "Hai Bà Trưng", "Thanh Xuân", "Hà Đông", "Nam Từ Liêm", "Bắc Từ Liêm", "Tây Hồ", "Long Biên", "Hoàng Mai"],
    "TP. Hồ Chí Minh": ["Quận 1", "Quận 3", "Quận 4", "Quận 5", "Quận 6", "Quận 7", "Quận 10", "Quận 11", "Bình Thạnh", "Phú Nhuận", "Gò Vấp", "Tân Bình", "Tân Phú", "Bình Tân", "Thủ Đức"],
    "Đà Nẵng": ["Hải Châu", "Thanh Khê", "Liên Chiểu", "Ngũ Hành Sơn", "Sơn Trà", "Cẩm Lệ"],
    "Hải Phòng": ["Hồng Bàng", "Ngô Quyền", "Lê Chân", "Kiến An", "Hải An", "Đồ Sơn", "Dương Kinh"],
    "Cần Thơ": ["Ninh Kiều", "Cái Răng", "Bình Thủy", "Ô Môn", "Thốt Nốt"],
    "Bình Dương": ["Thủ Dầu Một", "Thuận An", "Dĩ An", "Tân Uyên", "Bến Cát", "Bàu Bàng", "Phú Giáo", "Dầu Tiếng"],
    "Đồng Nai": ["Biên Hòa", "Long Khánh", "Nhơn Trạch", "Vĩnh Cửu", "Trảng Bom", "Thống Nhất", "Cẩm Mỹ", "Long Thành", "Xuân Lộc", "Định Quán"],
    "Khánh Hòa": ["Nha Trang", "Cam Ranh", "Ninh Hòa", "Vạn Ninh", "Diên Khánh", "Khánh Vĩnh", "Khánh Sơn", "Trường Sa"],
    "Hải Dương": ["Thành phố Hải Dương", "Chí Linh", "Nam Sách", "Kinh Môn", "Gia Lộc", "Tứ Kỳ", "Thanh Miện", "Ninh Giang", "Cẩm Giàng", "Thanh Hà"],
    "Bà Rịa - Vũng Tàu": ["Vũng Tàu", "Bà Rịa", "Phú Mỹ", "Xuyên Mộc", "Long Điền", "Đất Đỏ", "Châu Đức", "Côn Đảo"],
    "Đắk Lắk": ["Buôn Ma Thuột", "Buôn Hồ", "Cư M'gar", "Ea H'leo", "Ea Súp", "Krông Buk", "Krông Năng"],
    "Lâm Đồng": ["Đà Lạt", "Bảo Lộc", "Đức Trọng", "Di Linh", "Đơn Dương", "Lạc Dương", "Đam Rông"],
    "Thái Nguyên": ["Thành phố Thái Nguyên", "Sông Công", "Phổ Yên", "Phú Bình", "Đồng Hỷ", "Võ Nhai", "Định Hóa", "Đại Từ"],
    "Quảng Ninh": ["Hạ Long", "Móng Cái", "Cẩm Phả", "Uông Bí", "Quảng Yên", "Đông Triều", "Vân Đồn", "Tiên Yên"],
    "Hưng Yên": ["Thành phố Hưng Yên", "Mỹ Hào", "Ân Thi", "Khoái Châu", "Yên Mỹ", "Tiên Lữ", "Phù Cừ", "Kim Động"],
    "Nam Định": ["Thành phố Nam Định", "Vụ Bản", "Ý Yên", "Mỹ Lộc", "Nam Trực", "Trực Ninh", "Xuân Trường", "Giao Thủy"],
    "Thanh Hóa": ["Thành phố Thanh Hóa", "Bỉm Sơn", "Sầm Sơn", "Đông Sơn", "Quảng Xương", "Tĩnh Gia", "Nông Cống", "Như Xuân"],
    "Nghệ An": ["Vinh", "Cửa Lò", "Thái Hòa", "Hoàng Mai", "Quỳnh Lưu", "Diễn Châu", "Yên Thành", "Đô Lương"],
    "Bắc Ninh": ["Thành phố Bắc Ninh", "Từ Sơn", "Tiên Du", "Yên Phong", "Quế Võ", "Gia Bình", "Lương Tài", "Thuận Thành"],
    "Hà Tĩnh": ["Thành phố Hà Tĩnh", "Hồng Lĩnh", "Hương Sơn", "Đức Thọ", "Vũ Quang", "Nghi Xuân", "Can Lộc", "Thạch Hà"],
    "Quảng Ngãi": ["Thành phố Quảng Ngãi", "Bình Sơn", "Sơn Tịnh", "Tư Nghĩa", "Nghĩa Hành", "Mộ Đức", "Đức Phổ", "Ba Tơ"],
    "Bình Thuận": ["Phan Thiết", "La Gi", "Tuy Phong", "Bắc Bình", "Hàm Thuận Bắc", "Hàm Thuận Nam", "Tánh Linh", "Đức Linh"]
}

# Các phường xã (mẫu cho mỗi quận/huyện)
phuong_xa = {
    "Cầu Giấy": ["Dịch Vọng", "Dịch Vọng Hậu", "Mai Dịch", "Nghĩa Đô", "Nghĩa Tân", "Quan Hoa", "Trung Hòa", "Yên Hòa"],
    "Quận 1": ["Bến Nghé", "Bến Thành", "Cầu Kho", "Cầu Ông Lãnh", "Đa Kao", "Nguyễn Cư Trinh", "Nguyễn Thái Bình", "Phạm Ngũ Lão", "Tân Định"],
    "Hải Châu": ["Hải Châu I", "Hải Châu II", "Nam Dương", "Phước Ninh", "Bình Hiên", "Bình Thuận", "Hòa Thuận Đông", "Hòa Thuận Tây"],
    "Hồng Bàng": ["Hoàng Văn Thụ", "Minh Khai", "Quang Trung", "Sở Dầu", "Thượng Lý", "Trại Chuối"],
    "Ninh Kiều": ["An Bình", "An Cư", "An Hòa", "An Khánh", "An Nghiệp", "An Phú", "Cái Khế", "Hưng Lợi", "Tân An"],
}

# Hàm tạo địa chỉ ngẫu nhiên
def tao_dia_chi():
    tinh = random.choice(tinh_thanh)
    huyen = random.choice(quan_huyen.get(tinh, ["Quận/Huyện"]))
    
    # Tạo số nhà và tên đường ngẫu nhiên
    so_nha = random.randint(1, 999)
    ten_duong = fake.street_name()
    
    # Nếu có dữ liệu phường xã thì chọn, không thì tạo ngẫu nhiên
    if huyen in phuong_xa:
        phuong = random.choice(phuong_xa[huyen])
    else:
        phuong = f"Phường/Xã {random.randint(1, 20)}"
    
    return f"Số {so_nha}, {ten_duong}, {phuong}, {huyen}, {tinh}"

# Hàm tạo tên khách hàng kiểu username
def tao_ten_khach_hang():
    prefix = random.choice(['thai', 'nguyen', 'tran', 'le', 'pham', 'vu', 'dao', 'ngo', 'ho', 'dang'])
    name = random.choice(['kim', 'thu', 'hong', 'lan', 'huong', 'mai', 'loan', 'thao', 'trang', 'linh'])
    number = random.randint(100, 999)
    return f"{prefix}{name}{number}"

# Thêm hàm tạo phân bố theo nguyên tắc 80/20
def create_pareto_weights(n, factor=2):
    """
    Tạo trọng số theo phân bố Pareto
    n: số lượng phần tử
    factor: độ chênh lệch (càng lớn càng tập trung vào top)
    """
    weights = [1/(i**factor) for i in range(1, n+1)]
    total = sum(weights)
    return [w/total for w in weights]

# Cập nhật phân bố sản phẩm (20% sản phẩm chiếm 80% doanh số)
def get_product_weights():
    n_products = len(san_pham)
    weights = create_pareto_weights(n_products)
    return weights

# Cập nhật phân bố theo thời gian
def tao_ngay_trong_2_nam():
    # Tạo ngày cơ bản
    ngay_bat_dau = datetime(2023, 5, 1)
    ngay_ket_thuc = datetime(2024, 4, 30)
    
    # Xác định các ngày đặc biệt và trọng số
    ngay_dac_biet = {
        # Sale 2023
        datetime(2023, 9, 9): 10,    # 9.9
        datetime(2023, 10, 10): 8,   # 10.10
        datetime(2023, 11, 11): 15,  # 11.11 (cao điểm)
        datetime(2023, 12, 12): 12,  # 12.12
        # Tết 2024
        datetime(2024, 1, 20): 5,    # Cận Tết
        datetime(2024, 1, 21): 5,
        datetime(2024, 1, 22): 5,
        datetime(2024, 1, 23): 3,
        datetime(2024, 1, 24): 2,    # Giảm dần trong Tết
        # Sale 2024
        datetime(2024, 3, 3): 8,     # 3.3
        datetime(2024, 4, 4): 8,     # 4.4
    }
    
    # 40% khả năng rơi vào ngày đặc biệt
    if random.random() < 0.4:
        dates, weights = zip(*ngay_dac_biet.items())
        return random.choices(dates, weights=weights)[0]
    
    # Ngày thường: phân bố không đều theo tháng
    month_weights = {
        5: 3,   # Tháng 5/2023: ít đơn
        6: 4,
        7: 5,
        8: 6,
        9: 7,
        10: 8,
        11: 10, # Tăng dần
        12: 12, # Cao điểm cuối năm
        1: 8,   # Đầu năm 2024
        2: 4,   # Tháng Tết ít đơn
        3: 6,
        4: 7
    }
    
    # Chọn tháng theo trọng số
    month = random.choices(list(month_weights.keys()), 
                         weights=list(month_weights.values()))[0]
    # Chọn ngày trong tháng (tập trung vào đầu và cuối tháng)
    day_weights = [2 if i < 5 or i > 25 else 1 for i in range(1, 29)]
    day = random.choices(range(1, 29), weights=day_weights)[0]
    
    year = 2024 if month < 5 else 2023
    return datetime(year, month, day)

# Hàm tạo mã đơn hàng
def tao_ma_don_hang():
    prefix = "SPVN"
    digits = ''.join(random.choices('0123456789', k=10))
    return f"{prefix}{digits}"

# Hàm tạo mã giảm giá
def tao_ma_giam_gia():
    ma = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
    return f"SHOP{ma}"

# Tạo lý do hoàn hủy dựa trên trạng thái
def tao_ly_do_hoan_huy(trang_thai):
    if trang_thai in ["Đã hủy", "Đã hoàn trả"]:
        return random.choice(ly_do_huy if trang_thai == "Đã hủy" else ly_do_tra)
    return ""

# Tạo giá sau giảm giá
def tao_gia_sau_giam(gia_goc):
    # 70% sản phẩm có giảm giá
    if random.random() < 0.7:
        phan_tram_giam = random.choice([5, 10, 15, 20, 25, 30, 40, 50, 60])
        gia_sau_giam = int(gia_goc * (100 - phan_tram_giam) / 100)
        return gia_sau_giam
    return gia_goc

# Tạo ngày giao/hủy/hoàn dựa trên ngày đặt hàng và trạng thái
def tao_ngay_giao_huy_hoan(ngay_dat_hang, trang_thai):
    if trang_thai == "Đang xử lý":
        return ""
    elif trang_thai == "Đang giao":
        return ""
    else:
        # Tạo ngày ngẫu nhiên sau ngày đặt hàng từ 1-14 ngày
        ngay_sau = ngay_dat_hang + timedelta(days=random.randint(1, 14))
        # Đảm bảo không vượt quá thời gian hiện tại
        return min(ngay_sau, datetime.now()).strftime("%d/%m/%Y")

# Tạo đánh giá sao dựa trên trạng thái
def tao_danh_gia_sao(trang_thai):
    if trang_thai == "Đã giao thành công":
        # Phần lớn đánh giá 4-5 sao
        return random.choices([1, 2, 3, 4, 5], weights=[5, 5, 10, 40, 40])[0]
    return ""

# Tạo trọng số hoàn hủy cho thương hiệu (20% thương hiệu chiếm 80% hoàn hủy)
def get_brand_cancel_weights():
    brands = list(set([sp["thuong_hieu"] for sp in san_pham]))
    # Sắp xếp thương hiệu để đảm bảo kết quả nhất quán
    brands.sort()
    weights = create_pareto_weights(len(brands), factor=1.8)
    return dict(zip(brands, weights))

# Tạo trọng số hoàn hủy cho danh mục (20% danh mục chiếm 80% hoàn hủy)
def get_category_cancel_weights():
    categories = list(set([sp["danh_muc"] for sp in san_pham]))
    # Sắp xếp danh mục để đảm bảo kết quả nhất quán
    categories.sort()
    weights = create_pareto_weights(len(categories), factor=1.5)
    return dict(zip(categories, weights))

# Cập nhật hàm tạo dữ liệu đơn hàng
def tao_du_lieu_don_hang(so_luong=50000, output_file="shopee_fake_data.csv"):
    # Tạo header cho file CSV
    headers = [
        "Mã đơn hàng", "Ngày đặt hàng", "Ngày giao/hủy/hoàn", "Trạng thái đơn hàng", 
        "Lý do hoàn hủy", "Phương thức thanh toán", "Đơn vị vận chuyển", "Phí vận chuyển",
        "Mã giảm giá", "Tên khách hàng", "Số điện thoại", "Email", "Địa chỉ",
        "Tên sản phẩm", "Mã sản phẩm", "Thương hiệu", "Danh mục sản phẩm", 
        "Giá gốc", "Giá sau giảm", "Số lượng", "Đánh giá sao", "Ghi chú"
    ]
    
    # Tạo trọng số cho sản phẩm
    product_weights = get_product_weights()
    
    # Tạo trọng số hoàn hủy cho thương hiệu và danh mục
    brand_cancel_weights = get_brand_cancel_weights()
    category_cancel_weights = get_category_cancel_weights()
    
    # Tạo danh sách và trọng số từ dictionary để dùng random.choices
    pt_thanh_toan = list(phuong_thuc_thanh_toan.keys())
    weights_thanh_toan = list(phuong_thuc_thanh_toan.values())
    
    # Tương tự cho đơn vị vận chuyển
    dv_van_chuyen = list(don_vi_van_chuyen.keys())
    weights_van_chuyen = list(don_vi_van_chuyen.values())
    
    # Mở file để ghi dữ liệu
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        
        # Tạo các dòng dữ liệu
        for _ in range(so_luong):
            # Tạo ngày đặt hàng
            ngay_dat_hang = tao_ngay_trong_2_nam()
            ngay_dat_hang_str = ngay_dat_hang.strftime("%d/%m/%Y")
            
            # Chọn sản phẩm theo phân bố Pareto
            so_san_pham = random.choices([1, 2, 3, 4, 5], 
                                       weights=[60, 25, 10, 3, 2])[0]
            san_pham_list = random.choices(san_pham, 
                                         weights=product_weights, 
                                         k=so_san_pham)
            
            # Điều chỉnh tỷ lệ hoàn hủy theo thời gian
            # Tháng cao điểm (11, 12) có tỷ lệ hoàn hủy cao hơn
            if ngay_dat_hang.month in [11, 12]:
                weights_trang_thai_adjusted = [70, 20, 10, 0, 0]  # Tăng tỷ lệ hoàn hủy
            # Tháng Tết (1, 2) có tỷ lệ hoàn hủy thấp hơn
            elif ngay_dat_hang.month in [1, 2]:
                weights_trang_thai_adjusted = [85, 10, 5, 0, 0]  # Giảm tỷ lệ hoàn hủy
            # Ngày sale có tỷ lệ hoàn hủy cao hơn
            elif ngay_dat_hang.day == ngay_dat_hang.month:  # Ngày sale (ví dụ: 9/9, 11/11)
                weights_trang_thai_adjusted = [65, 25, 10, 0, 0]  # Tăng tỷ lệ hoàn hủy nhiều
            else:
                weights_trang_thai_adjusted = weights_trang_thai
            
            # Tạo trạng thái đơn hàng theo phân bố đã điều chỉnh
            trang_thai = random.choices(trang_thai_don_hang, weights=weights_trang_thai_adjusted)[0]
            
            # Điều chỉnh tỷ lệ hoàn hủy theo thương hiệu và danh mục
            # Nếu sản phẩm thuộc thương hiệu/danh mục có tỷ lệ hoàn hủy cao
            for sp in san_pham_list:
                brand_weight = brand_cancel_weights.get(sp["thuong_hieu"], 0.01)
                category_weight = category_cancel_weights.get(sp["danh_muc"], 0.01)
                
                # Thương hiệu và danh mục có trọng số cao sẽ có tỷ lệ hoàn hủy cao hơn
                if random.random() < (brand_weight * 5) or random.random() < (category_weight * 5):
                    if random.random() < 0.7:  # 70% là hủy, 30% là hoàn trả
                        trang_thai = "Đã hủy"
                    else:
                        trang_thai = "Đã hoàn trả"
            
            # Tạo dữ liệu cơ bản cho đơn hàng
            ma_don_hang = tao_ma_don_hang()
            ngay_giao_huy_hoan = tao_ngay_giao_huy_hoan(ngay_dat_hang, trang_thai)
            ly_do = tao_ly_do_hoan_huy(trang_thai)
            phuong_thuc_tt = random.choices(pt_thanh_toan, weights=weights_thanh_toan)[0]
            dvvc = random.choices(dv_van_chuyen, weights=weights_van_chuyen)[0]
            phi_van_chuyen = random.choice([0, 15000, 22000, 30000, 35000, 40000])
            
            # Có 30% đơn hàng sử dụng mã giảm giá
            ma_giam_gia = tao_ma_giam_gia() if random.random() < 0.3 else ""
            
            # Tạo thông tin khách hàng
            ten_khach_hang = tao_ten_khach_hang()
            so_dien_thoai = fake.phone_number()
            email = fake.email()
            dia_chi = tao_dia_chi()
            
            # Điều chỉnh giá theo thời gian
            if ngay_dat_hang.month == 2:  # Tháng Tết
                gia_tang = random.uniform(1.2, 1.3)  # Tăng 20-30%
            elif ngay_dat_hang.day in [1, 2, 3, 4, 5]:  # Đầu tháng
                gia_tang = random.uniform(0.9, 0.95)  # Giảm 5-10%
            elif ngay_dat_hang.day in [25, 26, 27, 28, 29, 30]:  # Cuối tháng
                gia_tang = random.uniform(0.85, 0.9)  # Giảm 10-15%
            else:
                gia_tang = 1.0
            
            # Với mỗi sản phẩm trong đơn hàng
            for sp in san_pham_list:
                # Tạo mã sản phẩm
                ma_san_pham = f"SP{random.randint(100000, 999999)}"
                
                # Tạo giá sau giảm
                gia_goc = sp["gia_goc"]
                gia_sau_giam = tao_gia_sau_giam(gia_goc)
                
                # Điều chỉnh giá theo thời điểm
                gia_goc = int(gia_goc * gia_tang)
                
                # Tăng số lượng cho sản phẩm hot
                if sp in san_pham[:int(len(san_pham)*0.2)]:  # Top 20% sản phẩm
                    so_luong_sp = random.choices([1, 2, 3, 4, 5], 
                                               weights=[50, 25, 15, 7, 3])[0]
                else:
                    so_luong_sp = random.choices([1, 2], weights=[90, 10])[0]
                
                # Tạo đánh giá sao
                danh_gia_sao = tao_danh_gia_sao(trang_thai)
                
                # Thêm logic xử lý COD và hoàn hủy
                if phuong_thuc_tt == "Thanh toán khi nhận hàng (COD)" and trang_thai in ["Đã hủy", "Đã hoàn trả"]:
                    # Tăng tỷ lệ hủy cho COD
                    if random.random() < 0.76:  # 76% đơn hủy từ COD
                        ly_do = random.choice(ly_do_huy if trang_thai == "Đã hủy" else ly_do_tra)
                
                # Ghi dòng dữ liệu vào file CSV
                row = [
                    ma_don_hang, ngay_dat_hang_str, ngay_giao_huy_hoan, trang_thai, 
                    ly_do, phuong_thuc_tt, dvvc, phi_van_chuyen,
                    ma_giam_gia, ten_khach_hang, so_dien_thoai, email, dia_chi,
                    sp["ten"], ma_san_pham, sp["thuong_hieu"], sp["danh_muc"], 
                    gia_goc, gia_sau_giam, so_luong_sp, danh_gia_sao, ""
                ]
                writer.writerow(row)

if __name__ == "__main__":
    # Tạo 50.000 dòng dữ liệu
    tao_du_lieu_don_hang(50000, "shopee_fake_data.csv")
    print("Đã tạo xong dữ liệu giả lập! File: shopee_fake_data.csv")