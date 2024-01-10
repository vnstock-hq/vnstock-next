

# Danh sách mã cổ phiếu
> Danh sách mã cổ phiếu có sẵn trong cơ sở dữ liệu. Hierarchy: stock.list

# Thông tin mã cổ phiếu
> Thông tin ngắn gọn của mã CP từ API đồ thị nến. Hierarchy: stock.info

# Candlestick
> Hierarchy: stock.quote

- time (datetime)
- open (float)
- high (float)
- low (float)
- close (float)
- volume (int)


## Tick (Intraday)
Tên | Kiểu dữ liệu| Ý nghĩa | Dữ liệu mẫu
--- | --- | --- | ---
time | datetime | Thời gian | "2024-01-10 14:45:00", dữ liệu gốc không kèm thông tin ngày.
price | float | Giá khớp | 20.50
volume | int | KLGD | 100
side | str | Mua hay Bán
change_pct | float | Phần trăm thay đổi | -0.5


- SSI intraday
```
{
    "_id": "1445001704872708158",
    "stockSymbol": "SSI",
    "accumulatedVol": 23828800,
    "accumulatedVal": 802664.2,
    "vol": 1019200,
    "changeType": "D",
    "price": 33700,
    "priceChange": -300,
    "priceChangePercent": -0.88,
    "ref": 34000,
    "side": "unknown",
    "time": "14:45:00"
}
```

- TCBS Intraday

```
{
    "p": 34400,
    "v": 169600,
    "cp": -100,
    "rcp": 0,
    "a": "",
    "ba": 3582500,
    "sa": 3403900,
    "hl": false,
    "pcp": -100,
    "t": "14:45:02"
}
```
và 

```
{
    "ap": 34500,
    "v": 200,
    "cp": 0,
    "rcp": 0,
    "a": "SD",
    "type": "SHEEP",
    "n": 1,
    "t": "14:29:52",
    "pcp": -50
}
```

# EOD


