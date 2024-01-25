import pandas as pd

from .providers.dnse import _dnse_get_history


class Ticker:
    def __init__(self, symbol):
        self.symbol = symbol.upper()

    def history(
        self,
        interval: str = "1D",
        start_date: str = None,
        end_date: str = None,
        provider: str = "dnse",
    ) -> pd.DataFrame:
        """Get ticker history."""

        if provider == "dnse":
            symbol = self.symbol
            return _dnse_get_history(
                symbol, resolution=interval, start_date=start_date, end_date=end_date
            )
        elif provider == "tcbs":
            pass
        else:
            raise ValueError(f"Provider {provider} is not supported.")
