import pandas as pd
import requests
from datetime import datetime, timedelta

tcbs_headers = {
    'sec-ch-ua':
    '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'DNT': '1',
    'Accept-language': 'vi',
    'sec-ch-ua-mobile': '?0',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Referer': 'https://tcinvest.tcbs.com.vn/',
    'sec-ch-ua-platform': '"Windows"'
}

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


class TCBS:

  def __init__(self, symbol='TCB'):
    """
        Initialize TCBS object with a default symbol.

        Parameters:
        - symbol (str): The default symbol for TCBS.
        """
    self.symbol = symbol
    self.candles = self.Candles(symbol)

  class Candles:

    def __init__(self,
                 symbol,
                 start_time='2024-01-02',
                 end_time='2024-01-10',
                 resolution='1D',
                 type='stock',
                 decor=True,
                 format='df',
                 headers=tcbs_headers):
      """
            Initialize Candles object with parameters for data retrieval.

            Parameters:
            - start_time (str): Start time for data retrieval.
            - end_time (str): End time for data retrieval.
            - resolution (str): Resolution of the data (e.g., '1D').
            - type (str): Type of data (e.g., 'stock').
            - decor (bool): Flag for additional decoration (default is True).
            - format (str): Format of the retrieved data (e.g., 'df' for DataFrame).

            """
      self.symbol = symbol
      self.start_time = start_time
      self.end_time = end_time
      if resolution == '1D':
        self.resolution = 'D'
      else:
        self.resolution = resolution
      self.type = type
      self.decor = decor
      self.format = format
      self.headers = headers

    def download(self, headers):
      """
            Download longterm OHLC data from TCBS.

            Parameters:
            - headers (dict): Headers for the HTTP request.

            Returns:
            - pd.DataFrame: Longterm OHLC data in DataFrame format.
            """
      # convert date difference to number of days
      start_date = datetime.strptime(self.start_time, '%Y-%m-%d')
      end_date = datetime.strptime(self.end_time, '%Y-%m-%d')
      delta = (end_date - start_date).days
      headers = self.headers

      # convert end_date to timestamp
      end_date_stp = int(end_date.timestamp())

      print(
          f'Time range is {delta} days. Looping through {delta // 365 + 1} requests'
      )

      # if delta is greater than 365 days loop through multiple requests to get full data
      if delta > 365:
        df = pd.DataFrame()
        while delta > 365:
          url = self._construct_url(end_date_stp)
          print(url)
          response = requests.request("GET", url, headers=headers)
          status_code = response.status_code

          if status_code == 200:
            data = response.json()
            df_temp = pd.DataFrame(data['data'])
            df_temp['time'] = pd.to_datetime(
                df_temp['tradingDate']).dt.strftime('%Y-%m-%d')
            df_temp.drop('tradingDate', axis=1, inplace=True)
            df = pd.concat([df_temp, df], ignore_index=True)
            end_date_stp = int(
                datetime.strptime(df['time'].min(), '%Y-%m-%d').timestamp())
            delta = delta - 365
          else:
            print(f'Error {status_code}. {response.text}')

        # get the remaining data
        url = self._construct_url(end_date_stp, delta)
        response = requests.request("GET", url, headers=headers)
        status_code = response.status_code

        if status_code == 200:
          data = response.json()
          df_temp = pd.DataFrame(data['data'])
          df_temp['time'] = pd.to_datetime(
              df_temp['tradingDate']).dt.strftime('%Y-%m-%d')
          df_temp.drop('tradingDate', axis=1, inplace=True)
          df = pd.concat([df_temp, df], ignore_index=True)
        else:
          print(f'Error {status_code}. {response.text}')

        # select data from start_date to end_date
        df = df[(df['time'] >= start_date.strftime('%Y-%m-%d'))
                & (df['time'] <= end_date.strftime('%Y-%m-%d'))]

        # devide price by 1000
        df['ticker'] = self.symbol

        # filter data from df to get data from start_date to end_date
        df = df[(df['time'] >= start_date.strftime('%Y-%m-%d'))
                & (df['time'] <= end_date.strftime('%Y-%m-%d'))]

        if self.type == 'stock':
          df[['open', 'high', 'low',
              'close']] = round(df[['open', 'high', 'low', 'close']] / 1000, 2)

        # convert df columns open, high, low, close, volume to float, volume to int
        df[['open', 'high', 'low',
            'close']] = df[['open', 'high', 'low', 'close']].astype(float)
        df['volume'] = df['volume'].astype(int)

        return df
      else:
        # Handle the case when delta is less than or equal to 365
        url = self._construct_url(end_date_stp, delta)
        response = requests.request("GET", url, headers=headers)
        status_code = response.status_code

        if status_code == 200:
          data = response.json()
          df = pd.DataFrame(data['data'])
          df['time'] = pd.to_datetime(
              df['tradingDate']).dt.strftime('%Y-%m-%d')
          df.drop('tradingDate', axis=1, inplace=True)
          df = df[(df['time'] >= start_date.strftime('%Y-%m-%d'))
                  & (df['time'] <= end_date.strftime('%Y-%m-%d'))]

          if self.type == 'stock':
            df[['open', 'high', 'low',
                'close']] = round(df[['open', 'high', 'low', 'close']] / 1000,
                                  2)

          df[['open', 'high', 'low',
              'close']] = df[['open', 'high', 'low', 'close']].astype(float)
          df['volume'] = df['volume'].astype(int)
          # rearrange time column to the first column
          cols = list(df.columns)
          cols = [cols[-1]] + cols[:-1]
          df = df[cols]
          print(f'Candles data downloaded successfully for {self.symbol}')
          return df
        else:
          print(f'Error {status_code}. {response.text}')
          return None

    def _construct_url(self, end_date_stp, delta=None):
      """
            Construct the TCBS API URL for data retrieval.

            Parameters:
            - end_date_stp (int): End date timestamp.
            - delta (int): Number of days for countBack parameter.

            Returns:
            - str: TCBS API URL.
            """
      if delta is None:
        delta = 365

      if self.type in ['stock', 'index']:
        return f"https://apipubaws.tcbs.com.vn/stock-insight/v2/stock/bars-long-term?ticker={self.symbol}&type={self.type}&resolution={self.resolution}&to={end_date_stp}&countBack={delta}"
      elif self.type == 'derivative':
        return f'https://apipubaws.tcbs.com.vn/futures-insight/v2/stock/bars-long-term?ticker={self.symbol}&type=derivative&resolution={self.resolution}&to={end_date_stp}&countBack={delta}'


class DNSE:

  def __init__(self, symbol='TCB'):
    """
        Initialize DNSE object with a default symbol.

        Parameters:
        - symbol (str): The default symbol for DNSE.
        """
    self.symbol = symbol
    self.candles = self.Candles(symbol)

  class Candles:

    def __init__(self, symbol):
      """
            Initialize Candles object with parameters for data retrieval.

            Parameters:
            - symbol (str): The symbol for which to retrieve data.
            """
      self.symbol = symbol

    def download(self,
                 start_date='2023-06-01',
                 end_date='2023-06-17',
                 resolution='1D',
                 type='stock',
                 headers=entrade_headers):
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

      url = f"https://services.entrade.com.vn/chart-api/v2/ohlcs/{type}?from={start_timestamp}&to={end_timestamp}&symbol={self.symbol}&resolution={resolution}"
      response = requests.request("GET", url, headers=headers)

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
        df['ticker'] = self.symbol
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
