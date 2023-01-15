import pandas as pd
import requests


class CoinglassAPI:
    """ Unofficial Python client for Coinglass API """

    def __init__(self, api_key: str):
        """
        Args:
            api_key: key from Coinglass, get one at https://www.coinglass.com/pricing
        """
        self.__api_key = api_key
        self.base_url = "https://open-api.coinglass.com/public/v2/indicator/"
        self._session = requests.Session()

    def _get(self, endpoint: str, params: dict = None) -> dict:
        headers = {
            "accept": "application/json",
            "coinglassSecret": self.__api_key
        }
        url = self.base_url + endpoint
        return self._session.request('GET', url, params=params, headers=headers, timeout=30).json()

    @staticmethod
    def _create_dataframe(data: list[dict], time_col: str) -> pd.DataFrame:
        df = pd.DataFrame(data)
        df[time_col] = pd.to_datetime(df[time_col], unit="ms")
        df.set_index(time_col, inplace=True, drop=True)
        return df

    def average_funding(
            self,
            symbol: str,
            interval: str,
            limit: int = None,
            start_time: int = None,
            end_time: int = None
    ) -> pd.DataFrame:
        """
        Average funding rate for a symbol

        Args:
            symbol: symbol to get funding rate for
            interval: interval to get funding rate for (e.g. m1, m5, m15, m30, h1, h4, etc.)
            limit: number of data points to return
            start_time: start time in milliseconds
            end_time: end time in milliseconds

        Returns:
            pandas DataFrame with funding rate
        """
        data = self._get(
            endpoint="funding_avg",
            params={"symbol": symbol, "interval": interval, "limit": limit,
                    "start_time": start_time, "end_time": end_time}
        )["data"]
        return self._create_dataframe(data, time_col="createTime")

    def open_interest_aggregated_ohlc(
            self,
            symbol: str,
            interval: str,
            limit: int = None,
            start_time: int = None,
            end_time: int = None
    ) -> pd.DataFrame:
        """
        Aggregated open interest in OHLC format for a symbol

        Args:
            symbol: symbol to get OI for
            interval: interval to get OI for (e.g. m1, m5, m15, m30, h1, h4, etc.)
            limit: number of data points to return
            start_time: start time in milliseconds
            end_time: end time in milliseconds

        Returns:
            pandas DataFrame with aggregated open interest in OHLC format
        """
        data = self._get(
            endpoint="open_interest_aggregated_ohlc",
            params={"symbol": symbol, "interval": interval, "limit": limit,
                    "start_time": start_time, "end_time": end_time}
        )["data"]
        return self._create_dataframe(data, time_col="t")

    def liquidation_symbol(
            self,
            symbol: str,
            interval: str,
            limit: int = None,
            start_time: int = None,
            end_time: int = None
    ) -> pd.DataFrame:
        """
        Liquidation data for a symbol

        Args:
            symbol: symbol to get liquidation data for
            interval: interval to get liquidation data for (e.g. m1, m5, m15, m30, h1, h4, etc.)
            limit: number of data points to return
            start_time: start time in milliseconds
            end_time: end time in milliseconds

        Returns:
            pandas DataFrame with liquidation data
        """
        data = self._get(
            endpoint="liquidation_symbol",
            params={"symbol": symbol, "interval": interval, "limit": limit,
                    "start_time": start_time, "end_time": end_time}
        )["data"]
        return self._create_dataframe(data, time_col="createTime")

    def long_short_symbol(
            self,
            symbol: str,
            interval: str,
            limit: int = None,
            start_time: int = None,
            end_time: int = None
    ) -> pd.DataFrame:
        """
        Long/short ratio for a symbol

        Args:
            symbol: symbol to get long/short ratio for
            interval: interval to get long/short ratio for (e.g. m1, m5, m15, m30, h1, h4, etc.)
            limit: number of data points to return
            start_time: start time in milliseconds
            end_time: end time in milliseconds

        Returns:
            pandas DataFrame with long/short ratio
        """
        data = self._get(
            endpoint="long_short_symbol",
            params={"symbol": symbol, "interval": interval, "limit": limit,
                    "start_time": start_time, "end_time": end_time}
        )["data"]
        return self._create_dataframe(data, time_col="t")
