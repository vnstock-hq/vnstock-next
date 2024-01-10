# vnstock-next
> Không gian làm việc của dự án phát triển phiên bản tiếp theo, kế thừa các yếu tố mang lại thành công của vnstock đến hiện tại.

## Triết lý thiết kế
> Dễ dàng để phổ cập tới số đông, đáp ứng nhu cầu đa dạng của người dùng

- Tham khảo mô tả [tại đây](https://docs.vnstock.site/community/contribute/?h=tri%E1%BA%BFt+l%C3%BD#triet-ly-thiet-ke)

## Mục tiêu phát triển
> Tạo dựng kiến trúc mã nguồn chặt chẽ, có tính kế thừa để dễ dàng nâng cấp và mở rộng tính năng trong giai đoạn tới.

## Nhận diện nhu cầu
- **Cấu trúc hàm phân cấp, dễ nhớ và áp dụng cho nhiều lớp tài sản khác nhau**. Ví dụ: `stock.price.some_function()` | `commodity.price.some_function()`) thay vì các hàm đơn lẻ thiếu trật tự và cần phải tra cứu mỗi khi dùng.
- **Mô hình dữ liệu đầu ra cố định & chặt chẽ** giúp dễ dàng lưu trữ vào cơ sở dữ liệu hoặc chuyển làm nguồn cấp cho các ứng dụng được liên kết để mở rộng tính năng. Ví dụ kết hợp các ứng dụng TA, Backtest, phân tích portfolio hiện có. Cân nhắc naming convention sử dụng `snake_case`
- **Hỗ trợ automation testing** giúp giảm thời gian kiểm tra, dễ phát hiện lỗi để đẩy nhanh thời gian phát hành khi quy mô của thư viện được mở rộng.
- **Tối ưu cho performance**. Cân nhắc sử dụng kết hợp với [Polar](https://pola.rs/) cho các thành phần tính toán ưu tiên tốc độ xử lý và đa luồng.


## Cấu trúc thư viện
- vnstock-next
- docs
- tests
- data (optional)


## Phân tích mẫu (ưu tiên)
### Phân loại
Nhu cầu | Nhóm dữ liệu | Tên tiêu chuẩn | Mô tả
--- | --- | --- | ---
Phân tích kỹ thuật | Giá cổ phiếu | Quote | Cả realtime lẫn dữ liệu lịch sử
Phân tích kỹ thuật | Giá cổ phiếu | Quote | Cả realtime lẫn dữ liệu lịch sử
Phân tích kỹ thuật | Giá cổ phiếu | Quote | Cả realtime lẫn dữ liệu lịch sử
Phân tích cơ bản | 

## Nhóm dữ liệu

Các nhóm chính:
- Stock & ETFs
- Index
- Future
- Commodity
- Forex
- Crypto
- CW
- Mutual Funds

- Company Fundamental
- Economics
- 
- News
- ESG

### Dữ liệu qua xử lý
- Chỉ báo

## Dữ liệu mẫu
> Xem chi tiết trong thư mục [docs](./docs)

## Nguồn ý tưởng
### Thư viện
Tên | Stars | Folks | Mô tả
--- | :---: | :---: | :-
[OpenBB](https://github.com/OpenBB-finance/OpenBBTerminal)  | 25.3k | 2.5k | -
[yfinance](https://github.com/ranaroussi/yfinance) | 11k | 2.1k | -
[pandas_reader](https://github.com/pydata/pandas-datareader/tree/main/pandas_datareader) | 2.8k | 676 | -
[Nasdaq Data Link python](https://github.com/Nasdaq/data-link-python) | 333 | 59 | 

### Nguồn cấp dữ liệu
> Cách cấu trúc dữ liệu cho thấy một bức tranh toàn cảnh về các loại dữ liệu và đầu ra tiêu chuẩn của chúng.
#### Quốc tế
> Tiêu chuẩn đang áp dụng trên các thị trường sôi động nhất thế giới.

Tên | Mô tả
--- | ---
[FinancialModelingPrep](https://site.financialmodelingprep.com/developer/docs) | 
[Alpha Vantage](https://www.alphavantage.co/#about) | 
[Polygon](https://polygon.io/docs/stocks/getting-started) | Mô tả cụ thể data type
[Barchart](https://www.barchart.com/ondemand/api) | Mô tả cụ thể input/output
[Tradier](https://documentation.tradier.com/brokerage-api/overview/market-data) | Tham khảo API document
[IEX Cloud](https://iexcloud.io/docs/core/QUOTE) | Tham khảo cách cấu trúc các nhóm dữ liệu
[Nasdaq DataLink](https://docs.data.nasdaq.com/docs/data-organization) | 
[Refinitive](https://www.lseg.com/en/data-analytics/financial-data) | Microsoft 365 tích hợp sẵn cho Excel

#### Việt Nam
- Wefeed
- Fiintrade
- Vietstock
- FireAnt
- Fialda


### Phân tích

Tên | Stars | Folks | Mô tả
--- | :---: | :---: | :-
[pyfolio](https://github.com/quantopian/pyfolio) | 5.3k | 1.7k | Quản lý danh mục
[pandas_ta](https://github.com/twopirllc/pandas-ta/tree/main) | 4.3k | 871 | Phân tích kỹ thuật


