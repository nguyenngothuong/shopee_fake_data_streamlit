import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Thiết lập trang
st.set_page_config(
    page_title="Phân tích dữ liệu Shopee",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hàm đọc dữ liệu
@st.cache_data
def load_data(file_path="shopee_fake_data.csv"):
    df = pd.read_csv(file_path)
    # Chuyển đổi cột ngày thành định dạng datetime
    df['Ngày đặt hàng'] = pd.to_datetime(df['Ngày đặt hàng'], format='%d/%m/%Y')
    if 'Ngày giao/hủy/hoàn' in df.columns:
        df['Ngày giao/hủy/hoàn'] = pd.to_datetime(df['Ngày giao/hủy/hoàn'], format='%d/%m/%Y', errors='coerce')
    
    # Thêm cột tháng
    df['Tháng'] = df['Ngày đặt hàng'].dt.strftime('%Y-%m')
    
    # Thêm cột doanh thu
    df['Doanh thu'] = df['Giá sau giảm'] * df['Số lượng']
    
    return df

# Tiêu đề trang
st.title("🛍️ Phân tích dữ liệu Shopee")
st.markdown("Dashboard phân tích dữ liệu đơn hàng và tỷ lệ hoàn hủy")

# Tải dữ liệu
try:
    df = load_data()
    st.success("Đã tải dữ liệu thành công!")
except Exception as e:
    st.error(f"Lỗi khi tải dữ liệu: {e}")
    st.info("Vui lòng đảm bảo file 'shopee_fake_data.csv' đã được tạo bằng cách chạy file generate_fake_data.py")
    st.stop()

# Tạo tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Tổng quan", 
    "Phân tích hoàn hủy", 
    "Phân tích theo thời gian",
    "Phân tích theo giá trị",
    "Phân tích theo phương thức thanh toán",
    "Phân tích theo vận chuyển"
])

# Tab 1: Tổng quan
with tab1:
    st.header("Tổng quan dữ liệu")
    
    # Tạo 2 cột
    col1, col2 = st.columns(2)
    
    with col1:
        # Phân bố trạng thái đơn hàng
        st.subheader("Phân bố trạng thái đơn hàng")
        status_counts = df.groupby('Trạng thái đơn hàng')['Mã đơn hàng'].nunique()
        unique_orders = df['Mã đơn hàng'].nunique()
        
        # Tạo biểu đồ tròn với Plotly
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Phân bố trạng thái đơn hàng",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        
        # Thêm phần trăm vào biểu đồ
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='%{label}: %{value} đơn<br>%{percent}'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Hiển thị số liệu
        for status, count in status_counts.items():
            st.write(f"- {status}: {count} đơn ({count/unique_orders*100:.2f}%)")
    
    with col2:
        # Phân bố danh mục sản phẩm
        st.subheader("Phân bố danh mục sản phẩm")
        category_counts = df['Danh mục sản phẩm'].value_counts()
        total_products = len(df)
        
        # Tạo biểu đồ cột với Plotly
        fig = px.bar(
            x=category_counts.index,
            y=category_counts.values,
            title="Phân bố danh mục sản phẩm",
            labels={'x': 'Danh mục', 'y': 'Số lượng sản phẩm'},
            color=category_counts.values,
            color_continuous_scale=px.colors.sequential.Viridis
        )
        
        # Thêm phần trăm lên đầu mỗi cột
        fig.update_traces(
            text=[f"{count} ({count/total_products*100:.1f}%)" for count in category_counts.values],
            textposition='outside'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Thông tin tổng quan
    st.subheader("Thông tin tổng quan")
    
    # Tạo 4 cột cho các metrics
    metric1, metric2, metric3, metric4 = st.columns(4)
    
    with metric1:
        st.metric(
            label="Tổng số đơn hàng", 
            value=f"{unique_orders:,}"
        )
    
    with metric2:
        total_revenue = df['Doanh thu'].sum()
        st.metric(
            label="Tổng doanh thu", 
            value=f"{total_revenue:,.0f} VNĐ"
        )
    
    with metric3:
        canceled_rate = status_counts.get('Đã hủy', 0) / unique_orders * 100
        st.metric(
            label="Tỷ lệ hủy đơn", 
            value=f"{canceled_rate:.2f}%"
        )
    
    with metric4:
        returned_rate = status_counts.get('Đã hoàn trả', 0) / unique_orders * 100
        st.metric(
            label="Tỷ lệ hoàn trả", 
            value=f"{returned_rate:.2f}%"
        )

# Tab 2: Phân tích hoàn hủy
with tab2:
    st.header("Phân tích đơn hàng hoàn hủy")
    
    # Lọc dữ liệu các đơn hoàn hủy
    canceled_orders = df[(df['Trạng thái đơn hàng'] == 'Đã hủy') | (df['Trạng thái đơn hàng'] == 'Đã hoàn trả')]
    
    # Tạo 2 cột
    col1, col2 = st.columns(2)
    
    with col1:
        # Lý do hoàn hủy
        st.subheader("Lý do hoàn hủy")
        reason_counts = canceled_orders['Lý do hoàn hủy'].value_counts()
        
        # Tạo biểu đồ cột ngang với Plotly
        fig = px.bar(
            y=reason_counts.index,
            x=reason_counts.values,
            title="Lý do hoàn hủy đơn hàng",
            labels={'y': 'Lý do', 'x': 'Số lượng đơn hàng'},
            orientation='h',
            color=reason_counts.values,
            color_continuous_scale=px.colors.sequential.Reds
        )
        
        # Thêm số lượng và phần trăm
        fig.update_traces(
            text=[f"{count} ({count/len(canceled_orders)*100:.1f}%)" for count in reason_counts.values],
            textposition='outside'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top 10 thương hiệu có tỷ lệ hoàn hủy cao nhất
        st.subheader("Top 10 thương hiệu có tỷ lệ hoàn hủy cao nhất")
        
        # Tính tỷ lệ hoàn hủy theo thương hiệu
        brand_all = df.groupby('Thương hiệu')['Mã đơn hàng'].nunique()
        brand_canceled = canceled_orders.groupby('Thương hiệu')['Mã đơn hàng'].nunique()
        
        brand_rates = {}
        for brand in brand_all.index:
            total_brand = brand_all[brand]
            canceled_brand = brand_canceled.get(brand, 0)
            if total_brand >= 50:  # Chỉ xét thương hiệu có ít nhất 50 đơn
                rate = canceled_brand / total_brand * 100
                brand_rates[brand] = rate
        
        # Sắp xếp và lấy top 10
        brand_rates_series = pd.Series(brand_rates).sort_values(ascending=False).head(10)
        
        # Tạo biểu đồ cột với Plotly
        fig = px.bar(
            x=brand_rates_series.index,
            y=brand_rates_series.values,
            title="Top 10 thương hiệu có tỷ lệ hoàn hủy cao nhất",
            labels={'x': 'Thương hiệu', 'y': 'Tỷ lệ hoàn hủy (%)'},
            color=brand_rates_series.values,
            color_continuous_scale=px.colors.sequential.Oranges
        )
        
        # Thêm tỷ lệ phần trăm lên đầu mỗi cột
        fig.update_traces(
            text=[f"{rate:.1f}%" for rate in brand_rates_series.values],
            textposition='outside'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tỷ lệ hoàn hủy theo danh mục sản phẩm
    st.subheader("Tỷ lệ hoàn hủy theo danh mục sản phẩm")
    
    # Tính tỷ lệ hoàn hủy theo danh mục
    category_all = df.groupby('Danh mục sản phẩm')['Mã đơn hàng'].nunique()
    category_canceled = canceled_orders.groupby('Danh mục sản phẩm')['Mã đơn hàng'].nunique()
    
    category_rates = {}
    for category in category_all.index:
        total_category = category_all[category]
        canceled_category = category_canceled.get(category, 0)
        rate = canceled_category / total_category * 100
        category_rates[category] = rate
    
    category_rates_series = pd.Series(category_rates)
    
    # Tạo biểu đồ cột với Plotly
    fig = px.bar(
        x=category_rates_series.index,
        y=category_rates_series.values,
        title="Tỷ lệ hoàn hủy theo danh mục sản phẩm",
        labels={'x': 'Danh mục', 'y': 'Tỷ lệ hoàn hủy (%)'},
        color=category_rates_series.values,
        color_continuous_scale=px.colors.sequential.Purples
    )
    
    # Thêm tỷ lệ phần trăm lên đầu mỗi cột
    fig.update_traces(
        text=[f"{rate:.1f}%" for rate in category_rates_series.values],
        textposition='outside'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Tab 3: Phân tích theo thời gian
with tab3:
    st.header("Phân tích theo thời gian")
    
    # Tạo 2 cột
    col1, col2 = st.columns(2)
    
    with col1:
        # Số lượng đơn hàng theo tháng
        st.subheader("Số lượng đơn hàng theo tháng")
        monthly_orders = df.groupby('Tháng')['Mã đơn hàng'].nunique()
        
        # Tạo biểu đồ cột với Plotly
        fig = px.bar(
            x=monthly_orders.index,
            y=monthly_orders.values,
            title="Số lượng đơn hàng theo tháng",
            labels={'x': 'Tháng', 'y': 'Số lượng đơn hàng'},
            color=monthly_orders.values,
            color_continuous_scale=px.colors.sequential.Blues
        )
        
        # Thêm số lượng lên đầu mỗi cột
        fig.update_traces(
            text=[f"{count:,}" for count in monthly_orders.values],
            textposition='outside'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Doanh thu theo tháng
        st.subheader("Doanh thu theo tháng")
        monthly_revenue = df.groupby('Tháng')['Doanh thu'].sum()
        
        # Tạo biểu đồ đường với Plotly
        fig = px.line(
            x=monthly_revenue.index,
            y=monthly_revenue.values,
            title="Doanh thu theo tháng",
            labels={'x': 'Tháng', 'y': 'Doanh thu (VNĐ)'},
            markers=True,
        )
        
        # Thêm giá trị doanh thu lên mỗi điểm
        fig.update_traces(
            text=[f"{revenue:,.0f}" for revenue in monthly_revenue.values],
            textposition='top center'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tỷ lệ hoàn hủy theo tháng
    st.subheader("Tỷ lệ hoàn hủy theo tháng")
    
    # Tính tỷ lệ hoàn hủy theo tháng
    monthly_all = df.groupby('Tháng')['Mã đơn hàng'].nunique()
    monthly_canceled = canceled_orders.groupby('Tháng')['Mã đơn hàng'].nunique()
    
    monthly_rates = {}
    for month in monthly_all.index:
        total_month = monthly_all[month]
        canceled_month = monthly_canceled.get(month, 0)
        rate = canceled_month / total_month * 100
        monthly_rates[month] = rate
    
    monthly_rates_series = pd.Series(monthly_rates)
    
    # Tạo biểu đồ cột với Plotly
    fig = px.bar(
        x=monthly_rates_series.index,
        y=monthly_rates_series.values,
        title="Tỷ lệ hoàn hủy theo tháng",
        labels={'x': 'Tháng', 'y': 'Tỷ lệ hoàn hủy (%)'},
        color=monthly_rates_series.values,
        color_continuous_scale=px.colors.sequential.Greens
    )
    
    # Thêm tỷ lệ phần trăm lên đầu mỗi cột
    fig.update_traces(
        text=[f"{rate:.1f}%" for rate in monthly_rates_series.values],
        textposition='outside'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top 5 sản phẩm bán chạy theo tháng
    st.subheader("Top 5 sản phẩm bán chạy theo tháng")
    
    # Chọn tháng để hiển thị
    selected_month = st.selectbox(
        "Chọn tháng để xem top 5 sản phẩm bán chạy:",
        sorted(df['Tháng'].unique())
    )
    
    # Lọc dữ liệu theo tháng đã chọn
    month_data = df[df['Tháng'] == selected_month]
    top_products = month_data.groupby('Tên sản phẩm')['Số lượng'].sum().nlargest(5)
    
    # Tạo biểu đồ cột với Plotly
    fig = px.bar(
        x=top_products.index,
        y=top_products.values,
        title=f"Top 5 sản phẩm bán chạy tháng {selected_month}",
        labels={'x': 'Sản phẩm', 'y': 'Số lượng bán'},
        color=top_products.values,
        color_continuous_scale=px.colors.sequential.Viridis
    )
    
    # Thêm số lượng lên đầu mỗi cột
    fig.update_traces(
        text=[f"{quantity:,}" for quantity in top_products.values],
        textposition='outside'
    )
    
    # Điều chỉnh layout để hiển thị tên sản phẩm dài
    fig.update_layout(
        xaxis={'tickangle': 45},
        margin={'b': 100}
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Tab 4: Phân tích theo giá trị
with tab4:
    st.header("Phân tích theo giá trị đơn hàng")
    
    # Tạo các khoảng giá trị đơn hàng
    df['Giá trị đơn hàng'] = df.groupby('Mã đơn hàng')['Doanh thu'].transform('sum')
    
    # Tạo các nhóm giá trị
    def categorize_order_value(value):
        if value < 100000:
            return "Dưới 100K"
        elif value < 200000:
            return "100K-200K"
        elif value < 500000:
            return "200K-500K"
        elif value < 1000000:
            return "500K-1M"
        else:
            return "Trên 1M"
    
    df['Nhóm giá trị'] = df['Giá trị đơn hàng'].apply(categorize_order_value)
    
    # Tạo 2 cột
    col1, col2 = st.columns(2)
    
    with col1:
        # Phân bố đơn hàng theo giá trị
        st.subheader("Phân bố đơn hàng theo giá trị")
        value_counts = df.drop_duplicates('Mã đơn hàng')['Nhóm giá trị'].value_counts()
        
        # Tạo biểu đồ tròn với Plotly
        fig = px.pie(
            values=value_counts.values,
            names=value_counts.index,
            title="Phân bố đơn hàng theo giá trị",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.4
        )
        
        # Thêm phần trăm vào biểu đồ
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='%{label}: %{value} đơn<br>%{percent}'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Tỷ lệ hoàn hủy theo giá trị đơn hàng
        st.subheader("Tỷ lệ hoàn hủy theo giá trị đơn hàng")
        
        # Tính tỷ lệ hoàn hủy theo giá trị
        value_all = df.drop_duplicates('Mã đơn hàng').groupby('Nhóm giá trị')['Mã đơn hàng'].count()
        value_canceled = df[df['Trạng thái đơn hàng'].isin(['Đã hủy', 'Đã hoàn trả'])].drop_duplicates('Mã đơn hàng').groupby('Nhóm giá trị')['Mã đơn hàng'].count()
        
        value_rates = {}
        for value in value_all.index:
            total_value = value_all[value]
            canceled_value = value_canceled.get(value, 0)
            rate = canceled_value / total_value * 100
            value_rates[value] = rate
        
        value_rates_series = pd.Series(value_rates)
        
        # Tạo biểu đồ cột với Plotly
        fig = px.bar(
            x=value_rates_series.index,
            y=value_rates_series.values,
            title="Tỷ lệ hoàn hủy theo giá trị đơn hàng",
            labels={'x': 'Giá trị đơn hàng', 'y': 'Tỷ lệ hoàn hủy (%)'},
            color=value_rates_series.values,
            color_continuous_scale=px.colors.sequential.Reds
        )
        
        # Thêm tỷ lệ phần trăm lên đầu mỗi cột
        fig.update_traces(
            text=[f"{rate:.1f}%" for rate in value_rates_series.values],
            textposition='outside'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Giá trị đơn hàng trung bình theo tháng
    st.subheader("Giá trị đơn hàng trung bình theo tháng")
    
    # Tính giá trị đơn hàng trung bình theo tháng
    avg_order_value = df.drop_duplicates('Mã đơn hàng').groupby('Tháng')['Giá trị đơn hàng'].mean()
    
    # Tạo biểu đồ đường với Plotly
    fig = px.line(
        x=avg_order_value.index,
        y=avg_order_value.values,
        title="Giá trị đơn hàng trung bình theo tháng",
        labels={'x': 'Tháng', 'y': 'Giá trị trung bình (VNĐ)'},
        markers=True,
    )
    
    # Thêm giá trị lên mỗi điểm
    fig.update_traces(
        text=[f"{value:,.0f}" for value in avg_order_value.values],
        textposition='top center'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Tab 5: Phân tích theo phương thức thanh toán
with tab5:
    st.header("Phân tích theo phương thức thanh toán")
    
    # Tạo 2 cột
    col1, col2 = st.columns(2)
    
    with col1:
        # Phân bố đơn hàng theo phương thức thanh toán
        st.subheader("Phân bố đơn hàng theo phương thức thanh toán")
        payment_counts = df.drop_duplicates('Mã đơn hàng')['Phương thức thanh toán'].value_counts()
        
        # Tạo biểu đồ tròn với Plotly
        fig = px.pie(
            values=payment_counts.values,
            names=payment_counts.index,
            title="Phân bố đơn hàng theo phương thức thanh toán",
            color_discrete_sequence=px.colors.qualitative.Pastel1,
            hole=0.4
        )
        
        # Thêm phần trăm vào biểu đồ
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='%{label}: %{value} đơn<br>%{percent}'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Tỷ lệ hoàn hủy theo phương thức thanh toán
        st.subheader("Tỷ lệ hoàn hủy theo phương thức thanh toán")
        
        # Tính tỷ lệ hoàn hủy theo phương thức thanh toán
        payment_all = df.drop_duplicates('Mã đơn hàng').groupby('Phương thức thanh toán')['Mã đơn hàng'].count()
        payment_canceled = df[df['Trạng thái đơn hàng'].isin(['Đã hủy', 'Đã hoàn trả'])].drop_duplicates('Mã đơn hàng').groupby('Phương thức thanh toán')['Mã đơn hàng'].count()
        
        payment_rates = {}
        for payment in payment_all.index:
            total_payment = payment_all[payment]
            canceled_payment = payment_canceled.get(payment, 0)
            rate = canceled_payment / total_payment * 100
            payment_rates[payment] = rate
        
        payment_rates_series = pd.Series(payment_rates)
        
        # Tạo biểu đồ cột với Plotly
        fig = px.bar(
            x=payment_rates_series.index,
            y=payment_rates_series.values,
            title="Tỷ lệ hoàn hủy theo phương thức thanh toán",
            labels={'x': 'Phương thức thanh toán', 'y': 'Tỷ lệ hoàn hủy (%)'},
            color=payment_rates_series.values,
            color_continuous_scale=px.colors.sequential.Purples
        )
        
        # Thêm tỷ lệ phần trăm lên đầu mỗi cột
        fig.update_traces(
            text=[f"{rate:.1f}%" for rate in payment_rates_series.values],
            textposition='outside'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Giá trị đơn hàng trung bình theo phương thức thanh toán
    st.subheader("Giá trị đơn hàng trung bình theo phương thức thanh toán")
    
    # Tính giá trị đơn hàng trung bình theo phương thức thanh toán
    avg_payment_value = df.drop_duplicates('Mã đơn hàng').groupby('Phương thức thanh toán')['Giá trị đơn hàng'].mean()
    
    # Tạo biểu đồ cột với Plotly
    fig = px.bar(
        x=avg_payment_value.index,
        y=avg_payment_value.values,
        title="Giá trị đơn hàng trung bình theo phương thức thanh toán",
        labels={'x': 'Phương thức thanh toán', 'y': 'Giá trị trung bình (VNĐ)'},
        color=avg_payment_value.values,
        color_continuous_scale=px.colors.sequential.Blues
    )
    
    # Thêm giá trị lên đầu mỗi cột
    fig.update_traces(
        text=[f"{value:,.0f}" for value in avg_payment_value.values],
        textposition='outside'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Tab 6: Phân tích theo vận chuyển
with tab6:
    st.header("Phân tích theo đơn vị vận chuyển")
    
    # Tạo 2 cột
    col1, col2 = st.columns(2)
    
    with col1:
        # Phân bố đơn hàng theo đơn vị vận chuyển
        st.subheader("Phân bố đơn hàng theo đơn vị vận chuyển")
        shipping_counts = df.drop_duplicates('Mã đơn hàng')['Đơn vị vận chuyển'].value_counts()
        
        # Tạo biểu đồ tròn với Plotly
        fig = px.pie(
            values=shipping_counts.values,
            names=shipping_counts.index,
            title="Phân bố đơn hàng theo đơn vị vận chuyển",
            color_discrete_sequence=px.colors.qualitative.Pastel2,
            hole=0.4
        )
        
        # Thêm phần trăm vào biểu đồ
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='%{label}: %{value} đơn<br>%{percent}'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Tỷ lệ hoàn hủy theo đơn vị vận chuyển
        st.subheader("Tỷ lệ hoàn hủy theo đơn vị vận chuyển")
        
        # Tính tỷ lệ hoàn hủy theo đơn vị vận chuyển
        shipping_all = df.drop_duplicates('Mã đơn hàng').groupby('Đơn vị vận chuyển')['Mã đơn hàng'].count()
        shipping_canceled = df[df['Trạng thái đơn hàng'].isin(['Đã hủy', 'Đã hoàn trả'])].drop_duplicates('Mã đơn hàng').groupby('Đơn vị vận chuyển')['Mã đơn hàng'].count()
        
        shipping_rates = {}
        for shipping in shipping_all.index:
            total_shipping = shipping_all[shipping]
            canceled_shipping = shipping_canceled.get(shipping, 0)
            rate = canceled_shipping / total_shipping * 100
            shipping_rates[shipping] = rate
        
        shipping_rates_series = pd.Series(shipping_rates)
        
        # Tạo biểu đồ cột với Plotly
        fig = px.bar(
            x=shipping_rates_series.index,
            y=shipping_rates_series.values,
            title="Tỷ lệ hoàn hủy theo đơn vị vận chuyển",
            labels={'x': 'Đơn vị vận chuyển', 'y': 'Tỷ lệ hoàn hủy (%)'},
            color=shipping_rates_series.values,
            color_continuous_scale=px.colors.sequential.Blues
        )
        
        # Thêm tỷ lệ phần trăm lên đầu mỗi cột
        fig.update_traces(
            text=[f"{rate:.1f}%" for rate in shipping_rates_series.values],
            textposition='outside'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Thời gian giao hàng trung bình theo đơn vị vận chuyển
    st.subheader("Thời gian giao hàng trung bình theo đơn vị vận chuyển")
    
    # Tính thời gian giao hàng
    delivered_orders = df[df['Trạng thái đơn hàng'] == 'Đã giao thành công'].drop_duplicates('Mã đơn hàng')
    delivered_orders['Thời gian giao hàng'] = (delivered_orders['Ngày giao/hủy/hoàn'] - delivered_orders['Ngày đặt hàng']).dt.days
    
    # Tính thời gian giao hàng trung bình theo đơn vị vận chuyển
    avg_delivery_time = delivered_orders.groupby('Đơn vị vận chuyển')['Thời gian giao hàng'].mean()
    
    # Tạo biểu đồ cột với Plotly
    fig = px.bar(
        x=avg_delivery_time.index,
        y=avg_delivery_time.values,
        title="Thời gian giao hàng trung bình theo đơn vị vận chuyển",
        labels={'x': 'Đơn vị vận chuyển', 'y': 'Thời gian giao hàng (ngày)'},
        color=avg_delivery_time.values,
        color_continuous_scale=px.colors.sequential.Greens
    )
    
    # Thêm giá trị lên đầu mỗi cột
    fig.update_traces(
        text=[f"{value:.1f} ngày" for value in avg_delivery_time.values],
        textposition='outside'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Phí vận chuyển trung bình theo đơn vị vận chuyển
    st.subheader("Phí vận chuyển trung bình theo đơn vị vận chuyển")
    
    # Tính phí vận chuyển trung bình theo đơn vị vận chuyển
    avg_shipping_fee = df.drop_duplicates('Mã đơn hàng').groupby('Đơn vị vận chuyển')['Phí vận chuyển'].mean()
    
    # Tạo biểu đồ cột với Plotly
    fig = px.bar(
        x=avg_shipping_fee.index,
        y=avg_shipping_fee.values,
        title="Phí vận chuyển trung bình theo đơn vị vận chuyển",
        labels={'x': 'Đơn vị vận chuyển', 'y': 'Phí vận chuyển (VNĐ)'},
        color=avg_shipping_fee.values,
        color_continuous_scale=px.colors.sequential.Oranges
    )
    
    # Thêm giá trị lên đầu mỗi cột
    fig.update_traces(
        text=[f"{value:,.0f}" for value in avg_shipping_fee.values],
        textposition='outside'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Sidebar với các bộ lọc
st.sidebar.title("Bộ lọc dữ liệu")

# Lọc theo khoảng thời gian
st.sidebar.header("Khoảng thời gian")
min_date = df['Ngày đặt hàng'].min().date()
max_date = df['Ngày đặt hàng'].max().date()
start_date = st.sidebar.date_input("Từ ngày", min_date)
end_date = st.sidebar.date_input("Đến ngày", max_date)

# Lọc theo trạng thái đơn hàng
st.sidebar.header("Trạng thái đơn hàng")
status_options = df['Trạng thái đơn hàng'].unique()
selected_status = st.sidebar.multiselect("Chọn trạng thái", status_options, default=status_options)

# Lọc theo danh mục sản phẩm
st.sidebar.header("Danh mục sản phẩm")
category_options = df['Danh mục sản phẩm'].unique()
selected_categories = st.sidebar.multiselect("Chọn danh mục", category_options, default=category_options)

# Lọc theo phương thức thanh toán
st.sidebar.header("Phương thức thanh toán")
payment_options = df['Phương thức thanh toán'].unique()
selected_payments = st.sidebar.multiselect("Chọn phương thức thanh toán", payment_options, default=payment_options)

# Lọc theo đơn vị vận chuyển
st.sidebar.header("Đơn vị vận chuyển")
shipping_options = df['Đơn vị vận chuyển'].unique()
selected_shipping = st.sidebar.multiselect("Chọn đơn vị vận chuyển", shipping_options, default=shipping_options)

# Nút áp dụng bộ lọc
if st.sidebar.button("Áp dụng bộ lọc"):
    # Lọc dữ liệu theo các điều kiện đã chọn
    filtered_df = df[
        (df['Ngày đặt hàng'].dt.date >= start_date) &
        (df['Ngày đặt hàng'].dt.date <= end_date) &
        (df['Trạng thái đơn hàng'].isin(selected_status)) &
        (df['Danh mục sản phẩm'].isin(selected_categories)) &
        (df['Phương thức thanh toán'].isin(selected_payments)) &
        (df['Đơn vị vận chuyển'].isin(selected_shipping))
    ]
    
    # Hiển thị thông tin về dữ liệu đã lọc
    st.sidebar.success(f"Đã lọc: {filtered_df['Mã đơn hàng'].nunique()} đơn hàng")
    
    # Lưu dữ liệu đã lọc vào session state để sử dụng trong toàn bộ ứng dụng
    st.session_state['filtered_data'] = filtered_df
    
    # Sử dụng st.rerun thay vì st.experimental_rerun (đã bị deprecated)
    st.rerun()
else:
    # Nếu chưa áp dụng bộ lọc, sử dụng dữ liệu gốc hoặc dữ liệu đã lọc từ session state
    if 'filtered_data' in st.session_state:
        df = st.session_state['filtered_data']
        st.sidebar.info(f"Đang hiển thị dữ liệu đã lọc: {df['Mã đơn hàng'].nunique()} đơn hàng")

# Thêm thông tin về dự án
st.sidebar.markdown("---")
st.sidebar.info(
    """
    **Dự án phân tích dữ liệu Shopee**
    
    Phân tích 50,000 đơn hàng từ dữ liệu Shopee, tập trung vào các chỉ số hoàn hủy và hiệu suất theo nhiều khía cạnh.
    
    Dữ liệu được tạo bằng file generate_fake_data.py
    """
)

# Thêm tính năng tải xuống dữ liệu
st.sidebar.markdown("---")
st.sidebar.header("Tải xuống dữ liệu")

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df_to_csv(df)
st.sidebar.download_button(
    label="Tải xuống dữ liệu CSV",
    data=csv,
    file_name='shopee_data_export.csv',
    mime='text/csv',
)

# Thêm tính năng xem dữ liệu thô
st.sidebar.markdown("---")
if st.sidebar.checkbox("Xem dữ liệu thô"):
    st.subheader("Dữ liệu thô")
    st.dataframe(df) 