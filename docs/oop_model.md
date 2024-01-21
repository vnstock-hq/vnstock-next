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


# STOCK

## Folder structure

```
├─stocks/
│ ├─mappings/
│ ├─insider/
│ ├─__init__.py
│ ├─stocks_view.py
│ ├─technical_analysis/
│ ├─cboe_model.py
│ ├─databento_model.py
│ ├─behavioural_analysis/
│ ├─tradinghours/
│ ├─README.md
│ ├─stocks_model.py
│ ├─cboe_view.py
│ ├─fundamental_analysis/
│ ├─options/
│ ├─government/
│ ├─stock_statics.py
│ ├─discovery/
│ ├─comparison_analysis/
│ ├─research/
│ ├─quantitative_analysis/
│ ├─backtesting/
│ ├─stocks_helper.py
│ ├─dark_pool_shorts/
│ ├─stocks_controller.py
│ └─screener/
```

## Object model

### Attributes

### Methods

- class TCBS

  - `__init__`

  - `class candles`

    - `def __init__`

    - `def download`

- class Ticker

  - `__init__`

  - `def candles`

  - `def download`

  - `def to_`

    - to_json

    - to_csv

    - to_ami

    - to_gsheet

### Common process

- Input validation

- Request

- Handle request result

  - Status check

  - Raise Error

  - Read data

  - Return desired data in json format

  - Read to pandas

    - Rename: snakecase

    - Set data type

    - Rearrange columns

- Output format

  - Export to JSON for Pollars from Pandas

  - Export to CSV from Pandas

  - Export to Amibroker csv

  - Save to Google Sheets
