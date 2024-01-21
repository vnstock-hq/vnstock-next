# OOP functions refactor

Trong file này mô tả ví dụ mẫu về đoạn code được tổ chức lại theo hướng OOP

```
from vnstock-next import *
```

```python
TCBS = TCBS()

# Instantiate Candles with specific parameters
candles_instance = TCBS.Candles(
    symbol='TCB',
    start_time='2023-12-01',
    end_time='2024-01-02',
    resolution='1D',
    type='stock',
    decor=True,
    format='df'
)

df = candles_instance.download(headers=tcbs_headers)
df
```

```python
# Instantiate DNSE with a specific symbol
DNSE = DNSE(symbol='TCB')

# Set parameters for data retrieval
start_date = '2023-06-01'
end_date = '2023-06-17'
resolution = '1D'
type = 'stock'

# Call the download method to retrieve historical price data
DNSE.candles.download(start_date=start_date, end_date=end_date, resolution=resolution, type=type)
```
