import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np
import os

# Đặt font chữ hỗ trợ tiếng Việt cho matplotlib
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# Hàm đọc và phân tích dữ liệu
def analyze_shopee_data(csv_file="shopee_fake_data.csv"):
    print("Đang đọc dữ liệu từ file CSV...")
    
    # Kiểm tra xem file có tồn tại không
    if not os.path.exists(csv_file):
        print(f"Lỗi: File {csv_file} không tồn tại!")
        print("Vui lòng chạy file generate_fake_data.py trước để tạo dữ liệu.")
        return
    
    # Đọc dữ liệu
    df = pd.read_csv(csv_file)
    
    # Chuyển đổi cột ngày thành định dạng datetime
    df['Ngày đặt hàng'] = pd.to_datetime(df['Ngày đặt hàng'], format='%d/%m/%Y')
    if 'Ngày giao/hủy/hoàn' in df.columns:
        df['Ngày giao/hủy/hoàn'] = pd.to_datetime(df['Ngày giao/hủy/hoàn'], format='%d/%m/%Y', errors='coerce')
    
    # Tạo thư mục để lưu biểu đồ
    if not os.path.exists('bieu_do_phan_tich'):
        os.makedirs('bieu_do_phan_tich')
    
    # Phân tích tổng quan
    analyze_overview(df)
    
    # Phân tích hàng hoàn hủy
    analyze_canceled_orders(df)
    
    # Phân tích theo thời gian
    analyze_time_trends(df)
    
    # Phân tích theo giá trị đơn hàng
    analyze_order_value(df)
    
    # Phân tích theo phương thức thanh toán
    analyze_payment_methods(df)
    
    # Phân tích theo đơn vị vận chuyển
    analyze_shipping_methods(df)
    
    # Thêm phân tích đơn bán theo tháng
    analyze_monthly_sales(df)
    
    print("\nPhân tích hoàn tất! Các biểu đồ đã được lưu trong thư mục 'bieu_do_phan_tich'")

def analyze_overview(df):
    print("\n===== PHÂN TÍCH TỔNG QUAN =====")
    
    # Đếm số lượng đơn hàng duy nhất
    unique_orders = df['Mã đơn hàng'].nunique()
    print(f"Tổng số đơn hàng: {unique_orders}")
    
    # Phân bố trạng thái đơn hàng
    status_counts = df.groupby('Trạng thái đơn hàng')['Mã đơn hàng'].nunique()
    print("\nPhân bố trạng thái đơn hàng:")
    for status, count in status_counts.items():
        print(f"{status}: {count} đơn ({count/unique_orders*100:.2f}%)")
    
    # Vẽ biểu đồ phân bố trạng thái
    plt.figure(figsize=(10, 6))
    ax = status_counts.plot(kind='bar', color=sns.color_palette("Set3"))
    plt.title('Phân bố trạng thái đơn hàng', fontsize=14)
    plt.xlabel('Trạng thái', fontsize=12)
    plt.ylabel('Số lượng đơn hàng', fontsize=12)
    plt.xticks(rotation=45)
    
    # Thêm số lượng và phần trăm lên đầu mỗi cột
    for i, v in enumerate(status_counts):
        ax.text(i, v + 0.1, f"{v}\n({v/unique_orders*100:.1f}%)", 
                ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('bieu_do_phan_tich/phan_bo_trang_thai.png')
    
    # Phân tích danh mục sản phẩm
    category_counts = df['Danh mục sản phẩm'].value_counts()
    print("\nPhân bố danh mục sản phẩm:")
    total_products = len(df)
    for category, count in category_counts.items():
        print(f"{category}: {count} sản phẩm ({count/total_products*100:.2f}%)")
    
    # Vẽ biểu đồ phân bố danh mục
    plt.figure(figsize=(12, 7))
    ax = category_counts.plot(kind='bar', color=sns.color_palette("Set2"))
    plt.title('Phân bố danh mục sản phẩm', fontsize=14)
    plt.xlabel('Danh mục', fontsize=12)
    plt.ylabel('Số lượng sản phẩm', fontsize=12)
    plt.xticks(rotation=45)
    
    # Thêm số lượng và phần trăm lên đầu mỗi cột
    for i, v in enumerate(category_counts):
        ax.text(i, v + 0.1, f"{v}\n({v/total_products*100:.1f}%)", 
                ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('bieu_do_phan_tich/phan_bo_danh_muc.png')

def analyze_canceled_orders(df):
    print("\n===== PHÂN TÍCH HÀNG HOÀN HỦY =====")
    
    # Lọc dữ liệu các đơn hoàn hủy
    canceled_orders = df[(df['Trạng thái đơn hàng'] == 'Đã hủy') | (df['Trạng thái đơn hàng'] == 'Đã hoàn trả')].copy()
    
    # Tính tổng số đơn hàng
    total_orders = df['Mã đơn hàng'].nunique()
    canceled_count = canceled_orders['Mã đơn hàng'].nunique()
    
    print(f"Tổng số đơn hàng: {total_orders}")
    print(f"Số đơn hàng bị hủy/hoàn: {canceled_count} ({canceled_count/total_orders*100:.2f}%)")
    
    # 1. Phân tích lý do hoàn hủy
    reason_counts = canceled_orders['Lý do hoàn hủy'].value_counts()
    print("\n=== LÝ DO HOÀN HỦY HÀNG ===")
    for reason, count in reason_counts.items():
        print(f"{reason}: {count} đơn ({count/canceled_count*100:.2f}%)")
    
    # 2. Phân tích theo danh mục sản phẩm
    category_canceled = canceled_orders['Danh mục sản phẩm'].value_counts()
    all_categories = df['Danh mục sản phẩm'].value_counts()
    
    print("\n=== TỶ LỆ HOÀN HỦY THEO DANH MỤC ===")
    for category in all_categories.index:
        total_cat = all_categories[category]
        canceled_cat = category_canceled.get(category, 0)
        print(f"{category}: {canceled_cat}/{total_cat} ({canceled_cat/total_cat*100:.2f}%)")
    
    # 3. Phân tích theo thương hiệu
    brand_canceled = canceled_orders.groupby('Thương hiệu')['Mã đơn hàng'].nunique()
    all_brands = df.groupby('Thương hiệu')['Mã đơn hàng'].nunique()
    
    # Tính tỷ lệ hoàn hủy cho mỗi thương hiệu
    brand_rates = []
    for brand in all_brands.index:
        if all_brands[brand] >= 50:  # Chỉ xét các thương hiệu có >= 50 đơn hàng
            total_brand = all_brands[brand]
            canceled_brand = brand_canceled.get(brand, 0)
            rate = canceled_brand / total_brand * 100
            brand_rates.append({
                'Thương hiệu': brand,
                'Tỷ lệ hoàn hủy': rate,
                'Số đơn hủy': canceled_brand,
                'Tổng số đơn': total_brand
            })
    
    # Tạo DataFrame và sắp xếp theo tỷ lệ hoàn hủy
    top_brands_df = pd.DataFrame(brand_rates).sort_values('Tỷ lệ hoàn hủy', ascending=False).head(10)
    
    print("\n=== TOP 10 THƯƠNG HIỆU CÓ TỶ LỆ HOÀN HỦY CAO NHẤT ===")
    for _, row in top_brands_df.iterrows():
        print(f"{row['Thương hiệu']}: {row['Tỷ lệ hoàn hủy']:.2f}%")
    
    # Vẽ biểu đồ top 10 thương hiệu có tỷ lệ hoàn hủy cao nhất
    plt.figure(figsize=(12, 7))
    sns.barplot(data=top_brands_df, x='Thương hiệu', y='Tỷ lệ hoàn hủy')
    plt.title('Top 10 thương hiệu có tỷ lệ hoàn hủy cao nhất', fontsize=14)
    plt.xlabel('Thương hiệu', fontsize=12)
    plt.ylabel('Tỷ lệ hoàn hủy (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    # Thêm giá trị phần trăm lên đầu mỗi cột
    for i, v in enumerate(top_brands_df['Tỷ lệ hoàn hủy']):
        plt.text(i, v + 0.1, f'{v:.1f}%', ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('bieu_do_phan_tich/top_10_thuong_hieu_hoan_huy.png')
    
    # 4. Phân tích theo khoảng giá
    price_bins = [0, 50000, 100000, 200000, 300000, float('inf')]
    price_labels = ['<50k', '50k-100k', '100k-200k', '200k-300k', '>300k']
    
    # Tạo bản sao của DataFrame để tránh SettingWithCopyWarning
    df_copy = df.copy()
    df_copy['Khoảng giá'] = pd.cut(df_copy['Giá gốc'], bins=price_bins, labels=price_labels)
    canceled_orders['Khoảng giá'] = pd.cut(canceled_orders['Giá gốc'], bins=price_bins, labels=price_labels)
    
    # Phân tích theo khoảng giá với observed=True
    price_canceled = canceled_orders.groupby('Khoảng giá', observed=True)['Mã đơn hàng'].nunique()
    all_prices = df_copy.groupby('Khoảng giá', observed=True)['Mã đơn hàng'].nunique()
    
    print("\n=== TỶ LỆ HOÀN HỦY THEO KHOẢNG GIÁ ===")
    for price in price_labels:
        total_price = all_prices[price]
        canceled_price = price_canceled.get(price, 0)
        print(f"{price}: {canceled_price}/{total_price} ({canceled_price/total_price*100:.2f}%)")

def analyze_time_trends(df):
    print("\n===== PHÂN TÍCH XU HƯỚNG THEO THỜI GIAN =====")
    
    # Thêm cột tháng và quý
    df['Tháng'] = df['Ngày đặt hàng'].dt.strftime('%Y-%m')
    df['Quý'] = df['Ngày đặt hàng'].dt.to_period('Q').astype(str)
    
    # Lọc dữ liệu các đơn hoàn hủy
    canceled_orders = df[(df['Trạng thái đơn hàng'] == 'Đã hủy') | (df['Trạng thái đơn hàng'] == 'Đã hoàn trả')]
    
    # Phân tích theo tháng
    monthly_all = df.groupby('Tháng')['Mã đơn hàng'].nunique()
    monthly_canceled = canceled_orders.groupby('Tháng')['Mã đơn hàng'].nunique()
    
    monthly_rates = {}
    print("\n=== TỶ LỆ HOÀN HỦY THEO THÁNG ===")
    for month in sorted(monthly_all.index):
        total_month = monthly_all[month]
        canceled_month = monthly_canceled.get(month, 0)
        rate = canceled_month / total_month * 100
        monthly_rates[month] = rate
        print(f"{month}: {canceled_month}/{total_month} ({rate:.2f}%)")
    
    # Vẽ biểu đồ tỷ lệ hoàn hủy theo tháng
    monthly_rates_series = pd.Series(monthly_rates)
    plt.figure(figsize=(14, 7))
    ax = monthly_rates_series.plot(kind='line', marker='o', color='#1f77b4')
    plt.title('Tỷ lệ hoàn hủy theo tháng', fontsize=14)
    plt.xlabel('Tháng', fontsize=12)
    plt.ylabel('Tỷ lệ hoàn hủy (%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    
    # Thêm tỷ lệ phần trăm lên mỗi điểm
    for i, v in enumerate(monthly_rates_series):
        ax.text(i, v + 0.2, f"{v:.1f}%", ha='center', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('bieu_do_phan_tich/ty_le_hoan_huy_theo_thang.png')
    
    # Phân tích theo quý
    quarterly_all = df.groupby('Quý')['Mã đơn hàng'].nunique()
    quarterly_canceled = canceled_orders.groupby('Quý')['Mã đơn hàng'].nunique()
    
    quarterly_rates = {}
    print("\n=== TỶ LỆ HOÀN HỦY THEO QUÝ ===")
    for quarter in sorted(quarterly_all.index):
        total_quarter = quarterly_all[quarter]
        canceled_quarter = quarterly_canceled.get(quarter, 0)
        rate = canceled_quarter / total_quarter * 100
        quarterly_rates[quarter] = rate
        print(f"{quarter}: {canceled_quarter}/{total_quarter} ({rate:.2f}%)")
    
    # Vẽ biểu đồ tỷ lệ hoàn hủy theo quý
    quarterly_rates_series = pd.Series(quarterly_rates)
    plt.figure(figsize=(12, 7))
    ax = quarterly_rates_series.plot(kind='bar', color=sns.color_palette("viridis", len(quarterly_rates)))
    plt.title('Tỷ lệ hoàn hủy theo quý', fontsize=14)
    plt.xlabel('Quý', fontsize=12)
    plt.ylabel('Tỷ lệ hoàn hủy (%)', fontsize=12)
    
    # Thêm tỷ lệ phần trăm lên đầu mỗi cột
    for i, v in enumerate(quarterly_rates_series):
        ax.text(i, v + 0.1, f"{v:.1f}%", ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('bieu_do_phan_tich/ty_le_hoan_huy_theo_quy.png')

def analyze_order_value(df):
    print("\n===== PHÂN TÍCH THEO GIÁ TRỊ ĐƠN HÀNG =====")
    
    # Tính tổng giá trị đơn hàng (giá sau giảm * số lượng)
    df_copy = df.copy()
    df_copy['Giá trị sản phẩm'] = df_copy['Giá sau giảm'] * df_copy['Số lượng']
    
    # Tính tổng giá trị cho mỗi đơn hàng
    order_values = df_copy.groupby('Mã đơn hàng')['Giá trị sản phẩm'].sum().reset_index()
    
    # Thêm thông tin trạng thái đơn hàng
    order_status = df_copy[['Mã đơn hàng', 'Trạng thái đơn hàng']].drop_duplicates()
    order_values = order_values.merge(order_status, on='Mã đơn hàng')
    
    # Tạo cột đánh dấu đơn hàng bị hủy/hoàn
    order_values['Bị hủy/hoàn'] = order_values['Trạng thái đơn hàng'].isin(['Đã hủy', 'Đã hoàn trả'])
    
    # Tạo các khoảng giá trị đơn hàng
    value_bins = [0, 100000, 200000, 500000, 1000000, float('inf')]
    value_labels = ['<100k', '100k-200k', '200k-500k', '500k-1M', '>1M']
    
    order_values['Khoảng giá trị'] = pd.cut(order_values['Giá trị sản phẩm'], bins=value_bins, labels=value_labels)
    
    # Phân tích tỷ lệ hủy/hoàn theo khoảng giá trị với observed=True
    value_groups = order_values.groupby('Khoảng giá trị', observed=True)
    
    value_rates = {}
    print("\n=== TỶ LỆ HOÀN HỦY THEO GIÁ TRỊ ĐƠN HÀNG ===")
    for value_range, group in value_groups:
        total = len(group)
        canceled = group['Bị hủy/hoàn'].sum()
        rate = canceled / total * 100
        value_rates[value_range] = rate
        print(f"{value_range}: {canceled}/{total} ({rate:.2f}%)")
    
    # Vẽ biểu đồ tỷ lệ hoàn hủy theo giá trị đơn hàng
    value_rates_series = pd.Series(value_rates)
    plt.figure(figsize=(10, 6))
    ax = value_rates_series.plot(kind='bar', color=sns.color_palette("Greens_d", len(value_rates)))
    plt.title('Tỷ lệ hoàn hủy theo giá trị đơn hàng', fontsize=14)
    plt.xlabel('Giá trị đơn hàng', fontsize=12)
    plt.ylabel('Tỷ lệ hoàn hủy (%)', fontsize=12)
    
    # Thêm tỷ lệ phần trăm lên đầu mỗi cột
    for i, v in enumerate(value_rates_series):
        ax.text(i, v + 0.1, f"{v:.1f}%", ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('bieu_do_phan_tich/ty_le_hoan_huy_theo_gia_tri_don_hang.png')

def analyze_payment_methods(df):
    print("\n===== PHÂN TÍCH THEO PHƯƠNG THỨC THANH TOÁN =====")
    
    # Lọc dữ liệu các đơn hoàn hủy
    canceled_orders = df[(df['Trạng thái đơn hàng'] == 'Đã hủy') | (df['Trạng thái đơn hàng'] == 'Đã hoàn trả')]
    
    # Phân tích theo phương thức thanh toán
    payment_all = df.groupby('Phương thức thanh toán')['Mã đơn hàng'].nunique()
    payment_canceled = canceled_orders.groupby('Phương thức thanh toán')['Mã đơn hàng'].nunique()
    
    payment_rates = {}
    print("\n=== TỶ LỆ HOÀN HỦY THEO PHƯƠNG THỨC THANH TOÁN ===")
    for payment in payment_all.index:
        total_payment = payment_all[payment]
        canceled_payment = payment_canceled.get(payment, 0)
        rate = canceled_payment / total_payment * 100
        payment_rates[payment] = rate
        print(f"{payment}: {canceled_payment}/{total_payment} ({rate:.2f}%)")
    
    # Vẽ biểu đồ tỷ lệ hoàn hủy theo phương thức thanh toán
    payment_rates_series = pd.Series(payment_rates)
    plt.figure(figsize=(12, 7))
    ax = payment_rates_series.plot(kind='bar', color=sns.color_palette("Purples_d", len(payment_rates)))
    plt.title('Tỷ lệ hoàn hủy theo phương thức thanh toán', fontsize=14)
    plt.xlabel('Phương thức thanh toán', fontsize=12)
    plt.ylabel('Tỷ lệ hoàn hủy (%)', fontsize=12)
    plt.xticks(rotation=45)
    
    # Thêm tỷ lệ phần trăm lên đầu mỗi cột
    for i, v in enumerate(payment_rates_series):
        ax.text(i, v + 0.1, f"{v:.1f}%", ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('bieu_do_phan_tich/ty_le_hoan_huy_theo_phuong_thuc_thanh_toan.png')

def analyze_shipping_methods(df):
    print("\n===== PHÂN TÍCH THEO ĐƠN VỊ VẬN CHUYỂN =====")
    
    # Lọc dữ liệu các đơn hoàn hủy
    canceled_orders = df[(df['Trạng thái đơn hàng'] == 'Đã hủy') | (df['Trạng thái đơn hàng'] == 'Đã hoàn trả')]
    
    # Phân tích theo đơn vị vận chuyển
    shipping_all = df.groupby('Đơn vị vận chuyển')['Mã đơn hàng'].nunique()
    shipping_canceled = canceled_orders.groupby('Đơn vị vận chuyển')['Mã đơn hàng'].nunique()
    
    shipping_rates = {}
    print("\n=== TỶ LỆ HOÀN HỦY THEO ĐƠN VỊ VẬN CHUYỂN ===")
    for shipping in shipping_all.index:
        total_shipping = shipping_all[shipping]
        canceled_shipping = shipping_canceled.get(shipping, 0)
        rate = canceled_shipping / total_shipping * 100
        shipping_rates[shipping] = rate
        print(f"{shipping}: {canceled_shipping}/{total_shipping} ({rate:.2f}%)")
    
    # Vẽ biểu đồ tỷ lệ hoàn hủy theo đơn vị vận chuyển
    shipping_rates_series = pd.Series(shipping_rates)
    plt.figure(figsize=(12, 7))
    ax = shipping_rates_series.plot(kind='bar', color=sns.color_palette("Blues_d", len(shipping_rates)))
    plt.title('Tỷ lệ hoàn hủy theo đơn vị vận chuyển', fontsize=14)
    plt.xlabel('Đơn vị vận chuyển', fontsize=12)
    plt.ylabel('Tỷ lệ hoàn hủy (%)', fontsize=12)
    plt.xticks(rotation=45)
    
    # Thêm tỷ lệ phần trăm lên đầu mỗi cột
    for i, v in enumerate(shipping_rates_series):
        ax.text(i, v + 0.1, f"{v:.1f}%", ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('bieu_do_phan_tich/ty_le_hoan_huy_theo_don_vi_van_chuyen.png')

# Thêm hàm phân tích đơn bán theo tháng
def analyze_monthly_sales(df):
    print("\n===== PHÂN TÍCH ĐƠN BÁN THEO THÁNG =====")
    
    # Thêm cột tháng
    df['Tháng'] = df['Ngày đặt hàng'].dt.strftime('%Y-%m')
    
    # Phân tích số lượng đơn hàng theo tháng
    monthly_orders = df.groupby('Tháng')['Mã đơn hàng'].nunique()
    
    print("\n=== SỐ LƯỢNG ĐƠN HÀNG THEO THÁNG ===")
    for month, count in monthly_orders.items():
        print(f"{month}: {count} đơn")
    
    # Vẽ biểu đồ số lượng đơn hàng theo tháng
    plt.figure(figsize=(15, 7))
    ax = monthly_orders.plot(kind='bar', color='skyblue')
    plt.title('Số lượng đơn hàng theo tháng', fontsize=14)
    plt.xlabel('Tháng', fontsize=12)
    plt.ylabel('Số lượng đơn hàng', fontsize=12)
    plt.xticks(rotation=45)
    
    # Thêm số lượng lên đầu mỗi cột
    for i, v in enumerate(monthly_orders):
        ax.text(i, v + 1, f'{v:,}', ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('bieu_do_phan_tich/don_hang_theo_thang.png')
    
    # Phân tích doanh thu theo tháng
    df['Doanh thu'] = df['Giá sau giảm'] * df['Số lượng']
    monthly_revenue = df.groupby('Tháng')['Doanh thu'].sum()
    
    print("\n=== DOANH THU THEO THÁNG ===")
    for month, revenue in monthly_revenue.items():
        print(f"{month}: {revenue:,.0f} VNĐ")
    
    # Vẽ biểu đồ doanh thu theo tháng
    plt.figure(figsize=(15, 7))
    ax = monthly_revenue.plot(kind='line', marker='o', color='green')
    plt.title('Doanh thu theo tháng', fontsize=14)
    plt.xlabel('Tháng', fontsize=12)
    plt.ylabel('Doanh thu (VNĐ)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    
    # Thêm giá trị doanh thu lên mỗi điểm
    for i, v in enumerate(monthly_revenue):
        ax.text(i, v, f'{v:,.0f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('bieu_do_phan_tich/doanh_thu_theo_thang.png')
    
    # Phân tích sản phẩm bán chạy theo tháng
    print("\n=== TOP 5 SẢN PHẨM BÁN CHẠY THEO THÁNG ===")
    for month in sorted(df['Tháng'].unique()):
        month_data = df[df['Tháng'] == month]
        top_products = month_data.groupby('Tên sản phẩm')['Số lượng'].sum().nlargest(5)
        print(f"\nTháng {month}:")
        for product, quantity in top_products.items():
            print(f"{product}: {quantity} sản phẩm")
        
        # Vẽ biểu đồ top 5 sản phẩm bán chạy cho mỗi tháng
        plt.figure(figsize=(12, 6))
        ax = top_products.plot(kind='bar', color=sns.color_palette("husl", 5))
        plt.title(f'Top 5 sản phẩm bán chạy tháng {month}', fontsize=14)
        plt.xlabel('Sản phẩm', fontsize=12)
        plt.ylabel('Số lượng bán', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        
        # Thêm số lượng lên đầu mỗi cột
        for i, v in enumerate(top_products):
            ax.text(i, v, f'{v:,}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(f'bieu_do_phan_tich/top_5_san_pham_{month}.png')

# Gọi hàm phân tích khi chạy trực tiếp
if __name__ == "__main__":
    analyze_shopee_data()
    print("Để xem kết quả phân tích chi tiết, hãy mở thư mục 'bieu_do_phan_tich'")