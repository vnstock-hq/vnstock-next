from datetime import datetime, timedelta
import pandas as pd
import requests

entrade_headers = {
    'authority':
    'services.entrade.com.vn',
    'accept':
    'application/json, text/plain, */*',
    'accept-language':
    'en-US,en;q=0.9',
    'dnt':
    '1',
    'origin':
    'https://banggia.dnse.com.vn',
    'referer':
    'https://banggia.dnse.com.vn/',
    'sec-ch-ua':
    '"Edge";v="114", "Chromium";v="114", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile':
    '?0',
    'sec-ch-ua-platform':
    '"Windows"',
    'sec-fetch-dest':
    'empty',
    'sec-fetch-mode':
    'cors',
    'sec-fetch-site':
    'cross-site',
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0'
}

def _dnse_get_history(symbol: str,
             start_date: str = '2023-06-01',
             end_date: str = '2023-06-17',
             resolution: str = '1D',
            ) -> pd.DataFrame:
  """
        Download historical price data from entrade.com.vn. The unit price is VND.
        Parameters:
        - start_date (str): Start date of the historical price data.
        - end_date (str): End date of the historical price data.
        - resolution (str): Resolution of the historical price data (e.g., '1D').
        - type (str): Type of data (e.g., 'stock').
        - headers (dict): Headers for the HTTP request.
        Returns:
        - pd.DataFrame: Historical price data in DataFrame format.
        """
  # add one more day to end_date
  end_date = (datetime.strptime(end_date, '%Y-%m-%d') +
              timedelta(days=1)).strftime('%Y-%m-%d')
  # convert from_date, to_date to timestamp
  start_timestamp = int(
      datetime.strptime(start_date, '%Y-%m-%d').timestamp())
  end_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())
  # if resolution is not 1D, then calculate the start date is last 90 days from end_date
  if resolution != '1D':
    new_start_timestamp = int(
        datetime.now().timestamp()) - 90 * 24 * 60 * 60
    new_end_timestamp = int(datetime.now().timestamp()) - 90 * 24 * 60 * 60
    # if new_from_timestamp > from_timestamp, then print a notice to user that data is limit to 90 days
    if end_timestamp < new_end_timestamp:
      print(
          "The 'end_date' value in the report should be no more than 90 days from today for all resolutions shorter than 1 day.",
          "\n")
    elif new_start_timestamp > start_timestamp:
      start_timestamp = new_start_timestamp
      print(
          "The retrieval of stock data is restricted to the most recent 90 days from today for all resolutions shorter than 1 day.",
          "\n")
      
  url = f"https://services.entrade.com.vn/chart-api/v2/ohlcs/stock?from={start_timestamp}&to={end_timestamp}&symbol={symbol}&resolution={resolution}"
  response = requests.request("GET", url, headers=entrade_headers)
  if response.status_code == 200:
    response_data = response.json()
    df = pd.DataFrame(response_data)
    df['t'] = pd.to_datetime(df['t'],
                             unit='s')  # convert timestamp to datetime
    df = df.rename(
        columns={
            't': 'time',
            'o': 'open',
            'h': 'high',
            'l': 'low',
            'c': 'close',
            'v': 'volume'
        }).drop(columns=['nextTime'])
    # add symbol column
    df['ticker'] = symbol
    df['time'] = df['time'].dt.tz_localize('UTC').dt.tz_convert(
        'Asia/Ho_Chi_Minh')
    # if resolution is 1D, then convert time to date
    if resolution == '1D':
      df['time'] = df['time'].dt.date
    else:
      # format df['time'] to datetime string with format %Y-%m-%d %H:%M:%S
      df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    # convert df columns open, high, low, close, volume to float, volume to int
    df[['open', 'high', 'low',
        'close']] = df[['open', 'high', 'low', 'close']].astype(float)
    df['volume'] = df['volume'].astype(int)
  else:
    print(f"Error in API response {response.text}", "\n")
    df = None
  return df