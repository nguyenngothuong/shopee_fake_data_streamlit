# BÁO CÁO PHÂN TÍCH DỮ LIỆU SHOPEE

## TỔNG QUAN
Báo cáo này phân tích 50,000 đơn hàng từ dữ liệu Shopee, tập trung vào các chỉ số hoàn hủy và hiệu suất theo nhiều khía cạnh. Dựa trên nghiên cứu chính sách hoàn hủy của Shopee và các vấn đề thực tế, báo cáo đã được cập nhật để phản ánh thông tin mới nhất, bao gồm các thảo luận trên Facebook và bài báo khiếu nại. Dưới đây là những phát hiện chính:

- Đã giao thành công: 70.19% (35,095 đơn)
- Tỷ lệ đơn hàng hoàn/hủy: 24.83% (12,413 đơn) 
- Danh mục sản phẩm lớn nhất: Trang điểm (40.17%)

![Biểu đồ phân bố trạng thái đơn hàng](bieu_do_phan_tich/phan_bo_trang_thai.png)
![Biểu đồ phân bố danh mục sản phẩm](bieu_do_phan_tich/phan_bo_danh_muc.png)

## PHÂN TÍCH ĐƠN HÀNG HOÀN HỦY
Theo [Chính sách trả hàng và hoàn tiền của Shopee](https://help.shopee.vn/portal/4/article/77251), từ ngày 8/3/2024, Shopee cho phép trả hàng trong 15 ngày kể từ ngày nhận hàng, bao gồm lý do đổi ý. Tỷ lệ đơn hàng hoàn/hủy chiếm 24.83% tổng số đơn hàng, với các lý do chính:

- Tìm được sản phẩm tốt hơn/rẻ hơn (20.58%)
- Sản phẩm không phù hợp với làn da (19.37%)
- Màu sắc/mùi hương khác với mong đợi (19.20%)

[Các thảo luận trên Facebook và bài báo khiếu nại](https://www.trustpilot.com/review/shopee.vn) cho thấy nhiều khách hàng phàn nàn về chậm trễ trong xử lý hoàn tiền và quy trình trả hàng phức tạp.

![Biểu đồ lý do hoàn hủy hàng](bieu_do_phan_tich/ly_do_hoan_huy.png)

### TOP 10 THƯƠNG HIỆU CÓ TỶ LỆ HOÀN HỦY CAO NHẤT

Dựa trên dữ liệu, top 10 thương hiệu có tỷ lệ hoàn hủy cao nhất, có thể phản ánh vấn đề chất lượng hoặc kỳ vọng khách hàng, như sau:

| Xếp hạng | Thương hiệu    | Tỷ lệ hoàn hủy (%) |
|----------|----------------|---------------------|
| 1        | Magic Casa     | 28.79               |
| 2        | Colorkey       | 27.88               |
| 3        | DEGO PHARMA    | 27.63               |
| 4        | Eyelash Curlen | 26.81               |
| 5        | TWG            | 26.60               |
| 6        | UCM            | 26.53               |
| 7        | Electric Brush | 26.49               |
| 8        | Dove           | 26.29               |
| 9        | MINSHZEE       | 26.28               |
| 10       | Eye Cover      | 26.07               |

![Biểu đồ thương hiệu có tỷ lệ hoàn hủy cao](bieu_do_phan_tich/top_10_thuong_hieu_hoan_huy.png)

### PHÂN TÍCH THEO KHOẢNG GIÁ

Sản phẩm có giá >300k có tỷ lệ hoàn hủy cao nhất (26.26%), trong khi các khoảng giá khác dao động từ 24.61% đến 25.03%, cho thấy khách hàng có xu hướng cẩn trọng hơn với sản phẩm giá cao.

### XU HƯỚNG THEO THỜI GIAN

Tỷ lệ hoàn hủy theo tháng dao động từ 23.10% (thấp nhất vào 2024-07) đến 26.72% (cao nhất vào 2023-07).

![Biểu đồ tỷ lệ hoàn hủy theo tháng](bieu_do_phan_tich/ty_le_hoan_huy_theo_thang.png)

Phân tích theo quý:
- 2023Q1: 26.09% (cao nhất)
- 2024Q3: 24.12% (thấp nhất)

![Biểu đồ tỷ lệ hoàn hủy theo quý](bieu_do_phan_tich/ty_le_hoan_huy_theo_quy.png)

### PHÂN TÍCH THEO GIÁ TRỊ ĐƠN HÀNG

Đơn hàng có giá trị cao nhất (>1M) có tỷ lệ hoàn hủy cao nhất (26.71%), trong khi đơn hàng <100k có tỷ lệ thấp nhất (24.33%), phản ánh xu hướng khách hàng yêu cầu cao hơn với đơn hàng giá trị lớn.

![Biểu đồ tỷ lệ hoàn hủy theo giá trị đơn hàng](bieu_do_phan_tich/ty_le_hoan_huy_theo_gia_tri_don_hang.png)

### PHÂN TÍCH THEO PHƯƠNG THỨC THANH TOÁN

Tỷ lệ hoàn hủy cao nhất thuộc về phương thức "Chuyển khoản ngân hàng" (25.23%), thấp nhất là "Thanh toán qua Momo" (24.46%), có thể do hành vi mua sắm khác nhau giữa các phương thức thanh toán.

![Biểu đồ tỷ lệ hoàn hủy theo phương thức thanh toán](bieu_do_phan_tich/ty_le_hoan_huy_theo_phuong_thuc_thanh_toan.png)

### PHÂN TÍCH THEO ĐƠN VỊ VẬN CHUYỂN

"Giao hàng tiết kiệm" có tỷ lệ hoàn hủy cao nhất (25.07%), trong khi "Giao hàng nhanh" có tỷ lệ thấp nhất (24.61%), có thể do thời gian giao hàng dài hơn gây ra thay đổi ý định.

![Biểu đồ tỷ lệ hoàn hủy theo đơn vị vận chuyển](bieu_do_phan_tich/ty_le_hoan_huy_theo_don_vi_van_chuyen.png)

## PHÂN TÍCH SÂU VÀ NHẬN ĐỊNH AI
Từ dữ liệu phân tích và các nguồn thông tin đáng tin cậy, AI xác định một số điểm đáng chú ý:

## THỜI VỤ VÀ BIẾN ĐỘNG
Theo [Tỷ lệ hoàn tiền theo mùa](https://thoughtmetric.io/define/refund-rate), tỷ lệ hoàn hủy có xu hướng tăng cao vào các tháng có nhiều chương trình khuyến mãi. Cụ thể trong dữ liệu:
- Tháng 7/2023: 26.72% (cao nhất)
- Tháng 4/2024: 26.26%
- Tháng 7/2024: 23.10% (thấp nhất)
- Tháng 5/2024: 23.18%

### VẤN ĐỀ VỀ THÔNG TIN SẢN PHẨM

Ba lý do hàng đầu dẫn đến hoàn hủy đều liên quan đến kỳ vọng của khách hàng không khớp với sản phẩm thực tế:
- Tìm được sản phẩm tốt hơn/rẻ hơn (20.58%), phù hợp với chính sách đổi ý của Shopee, nhưng có thể gây áp lực cho người bán, như phản ánh trên X ([X post](https://x.com/anisaniesa/status/1790345474094035142)).
- Sản phẩm không phù hợp với làn da (19.37%), có thể được xem là sản phẩm lỗi nếu gây phản ứng, cần cải thiện thông tin thành phần, theo [Reducing E-commerce Returns](https://thegood.com/insights/reduce-ecommerce-returns/).
- Màu sắc/mùi hương khác với mong đợi (19.20%), cho thấy cần cải thiện hình ảnh và mô tả sản phẩm, theo [E-commerce Return Strategies](https://www.sendcloud.com/how-to-reduce-returns-in-ecommerce/).

### MỐI QUAN HỆ GIỮA GIÁ TRỊ ĐƠN HÀNG VÀ TỶ LỆ HOÀN HỦY

Có mối tương quan tích cực giữa giá trị đơn hàng và tỷ lệ hoàn hủy - đơn hàng giá trị càng cao thì tỷ lệ hoàn hủy càng lớn:
- <100k: 24.33%
- >1M: 26.71%

Điều này gợi ý rằng khách hàng có xu hướng cẩn trọng hơn và yêu cầu cao hơn với các sản phẩm giá trị lớn, cần chính sách hậu mãi đặc biệt.

### THƯƠNG HIỆU VÀ VẤN ĐỀ CHẤT LƯỢNG

Top 10 thương hiệu có tỷ lệ hoàn hủy cao nhất (từ 26.07% đến 28.79%) đều cao hơn đáng kể so với tỷ lệ trung bình (24.83%). Điều này cho thấy có vấn đề nhất quán về chất lượng hoặc kỳ vọng sản phẩm với các thương hiệu này, cần chương trình cải thiện chất lượng.

### PHƯƠNG THỨC THANH TOÁN VÀ HÀNH VI NGƯỜI DÙNG

Phương thức "Chuyển khoản ngân hàng" có tỷ lệ hoàn hủy cao nhất (25.23%), trong khi "Thanh toán qua Momo" thấp nhất (24.46%). Điều này có thể phản ánh sự khác biệt trong hành vi người dùng theo phương thức thanh toán, với người dùng ví điện tử có thể cẩn thận hơn khi đặt hàng, cần phân tích sâu hơn.

## KHUYẾN NGHỊ CHIẾN LƯỢC

Dựa trên phân tích, AI đề xuất các biện pháp cải thiện sau, kết hợp với thông tin từ các nguồn e-commerce:

### CẢI THIỆN THÔNG TIN SẢN PHẨM

- Bổ sung chi tiết hơn về màu sắc, mùi hương thực tế, theo [E-commerce Return Strategies](https://www.sendcloud.com/how-to-reduce-returns-in-ecommerce/).
- Thêm đánh giá phù hợp với loại da, cung cấp thông tin thành phần để giảm hoàn hủy do không phù hợp, theo [Reducing E-commerce Returns](https://thegood.com/insights/reduce-ecommerce-returns/).
- Cung cấp so sánh kích thước/dung tích trực quan, sử dụng hình ảnh chất lượng cao và video để thể hiện sản phẩm.

### CHƯƠNG TRÌNH "THƯƠNG HIỆU ĐÁNG TIN CẬY"

- Làm việc với top 10 thương hiệu có tỷ lệ hoàn hủy cao để cải thiện chất lượng, cung cấp chương trình đánh giá và phản hồi từ khách hàng.
- Phát triển tiêu chuẩn chất lượng và cam kết rõ ràng, giảm áp lực từ chính sách đổi ý, như phản ánh trên X ([X post](https://x.com/anisaniesa/status/1790345474094035142)).

### CHIẾN LƯỢC ỨNG XỬ THEO GIÁ TRỊ

- Với đơn hàng >300k: tăng cường thông tin, dịch vụ tư vấn trước mua, cung cấp hỗ trợ cá nhân hóa.
- Với đơn hàng >1M: cân nhắc chính sách bảo hành/đổi trả đặc biệt, theo [E-commerce Return Best Practices](https://redstagfulfillment.com/best-practices-e-commerce-returns/).

### TỐI ƯU HÓA THEO MÙA VỤ

- Tăng cường kiểm soát chất lượng vào các tháng cao điểm (tháng 7, tháng 4), phân tích dữ liệu bán hàng để quản lý kỳ vọng, theo [Seasonal Refund Rates](https://thoughtmetric.io/define/refund-rate).
- Đưa ra các chiến dịch marketing và giao tiếp khách hàng nhằm giảm hoàn hủy trong mùa vụ bận rộn.

### CẢI THIỆN QUY TRÌNH LOGISTIC

- Làm việc với "Giao hàng tiết kiệm" để giảm tỷ lệ hoàn hủy, cung cấp thông tin theo dõi và ước tính thời gian giao hàng, theo [Logistic Impact on Returns](https://www.sendcloud.co.uk/how-to-reduce-returns-in-ecommerce/).
- Học hỏi từ quy trình của "Giao hàng nhanh" có tỷ lệ hoàn hủy thấp nhất, cải thiện trải nghiệm giao hàng.

## KẾT LUẬN

Theo [Báo cáo của BigSeller](https://www.bigseller.com/blog/articleDetails/1639.htm), chính sách mới của Shopee về đổi trả trong 15 ngày đang tạo áp lực lớn cho người bán. Tuy nhiên, với tỷ lệ giao hàng thành công 70.19%, Shopee vẫn có nền tảng vững chắc để cải thiện. Bằng cách áp dụng các giải pháp đề xuất, có thể nâng cao tỷ lệ thành công lên 75-80% trong những quý tới.

### Key Citations
- [Shopee Refund Policy Detailed Terms and Conditions](https://help.shopee.com.my/portal/4/article/77221-Refunds-and-Return-Policy)
- [Shopee Cancellation Policy for Buyers Basic Guide](https://help.shopee.com.my/portal/4/article/78918-%255BBuyer-Basics%255D-How-do-I-cancel-my-order)
- [Shopee Return Conditions for Original Sealed Products](https://help.shopee.ph/portal/4/article/97776-What-is-Change-of-Mind-Returns)
- [Shopee Change of Mind Policy Platform-wide Implementation](https://seller.shopee.sg/edu/article/20197/Platform-wide-Change-of-Mind-Policy)
- [Reducing E-commerce Returns Expert Strategies and Insights](https://thegood.com/insights/reduce-ecommerce-returns/)
- [E-commerce Return Strategies Ten Effective Methods](https://www.sendcloud.com/how-to-reduce-returns-in-ecommerce/)
- [E-commerce Return Best Practices Comprehensive Guide](https://redstagfulfillment.com/best-practices-e-commerce-returns/)
- [Seasonal Refund Rates E-Commerce Explained](https://thoughtmetric.io/define/refund-rate)
- [Logistic Impact on Returns Strategies for Retailers](https://www.sendcloud.co.uk/how-to-reduce-returns-in-ecommerce/)