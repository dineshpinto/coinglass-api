import pandas as pd
import requests


class CoinglassAPI:
    """ Unofficial Python client for Coinglass API """

    def __init__(self, coinglass_secret: str):
        """
        Args:
            coinglass_secret: key from Coinglass, get one at https://www.coinglass.com/pricing
        """
        self.__coinglass_secret = coinglass_secret
        self._base_url = "https://open-api.coinglass.com/public/v2/"
        self._session = requests.Session()

    def _get(self, endpoint: str, params: dict = None) -> dict:
        headers = {
            "accept": "application/json",
            "coinglassSecret": self.__coinglass_secret
        }
        url = self._base_url + endpoint
        return self._session.request('GET', url, params=params, headers=headers, timeout=30).json()

    @staticmethod
    def _create_dataframe(
            data: list[dict],
            time_col: str,
            unit: str | None = "ms",
            cast_objects_to_numeric: bool = False
    ) -> pd.DataFrame:
        """ Create pandas DataFrame from list of dicts """
        df = pd.DataFrame(data)
        if time_col == "time":
            df.rename(columns={"time": "t"}, inplace=True)
            time_col = "t"
        df["time"] = pd.to_datetime(df[time_col], unit=unit)
        df.drop(columns=[time_col], inplace=True)
        df.set_index("time", inplace=True, drop=True)

        if "t" in df.columns:
            df.drop(columns=["t"], inplace=True)

        if cast_objects_to_numeric:
            cols = df.columns[df.dtypes.eq('object')]
            df[cols] = df[cols].apply(pd.to_numeric)
        return df

    @staticmethod
    def _check_for_errors(response: dict) -> None:
        """ Check for errors in response """
        if not response["success"]:
            raise Exception(f"Code {response['code']}: {response['msg']}")

    def funding(
            self,
            ex: str,
            pair: str,
            interval: str,
            limit: int = 500,
            start_time: int = None,
            end_time: int = None
    ) -> pd.DataFrame:
        """
        Funding rate for a given pair

        Args:
            ex: exchange to get funding rate for (e.g. Binance, dYdX, etc.)
            pair: pair to get funding rate for (e.g. BTCUSDT on Binance, BTC-USD on dYdX, etc.)
            interval: interval to get funding rate for (e.g. m1, m5, m15, m30, h1, h4, etc.)
            limit: number of data points to return (default: 500)
            start_time: start time in milliseconds
            end_time: end time in milliseconds

        Returns:
            pandas DataFrame with funding rate
        """
        response = self._get(
            endpoint="indicator/funding",
            params={"ex": ex, "pair": pair, "interval": interval, "limit": limit,
                    "start_time": start_time, "end_time": end_time}
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="createTime")

    def funding_ohlc(
            self,
            ex: str,
            pair: str,
            interval: str,
            limit: int = 500,
            start_time: int = None,
            end_time: int = None
    ) -> pd.DataFrame:
        """
        Funding rate in OHLC format for an exchange pair

        Args:
            ex: exchange to get funding rate for (e.g. Binance, dYdX, etc.)
            pair: pair to get funding rate for (e.g. BTCUSDT on Binance, BTC-USD on dYdX, etc.)
            interval: interval to get funding rate for (e.g. m1, m5, m15, m30, h1, h4, etc.)
            limit: number of data points to return (default: 500)
            start_time: start time in milliseconds
            end_time: end time in milliseconds

        Returns:
            pandas DataFrame with funding rate in OHLC format for an exchange pair
        """
        response = self._get(
            endpoint="indicator/funding_ohlc",
            params={"ex": ex, "pair": pair, "interval": interval, "limit": limit,
                    "start_time": start_time, "end_time": end_time}
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="t")

    def funding_average(
            self,
            symbol: str,
            interval: str,
            limit: int = 500,
            start_time: int = None,
            end_time: int = None
    ) -> pd.DataFrame:
        """
        Average funding rate for a symbol

        Args:
            symbol: symbol to get funding rate for
            interval: interval to get funding rate for (e.g. m1, m5, m15, m30, h1, h4, etc.)
            limit: number of data points to return (default: 500)
            start_time: start time in milliseconds
            end_time: end time in milliseconds

        Returns:
            pandas DataFrame with funding rate
        """
        response = self._get(
            endpoint="indicator/funding_avg",
            params={"symbol": symbol, "interval": interval, "limit": limit,
                    "start_time": start_time, "end_time": end_time}
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="createTime")

    def open_interest_ohlc(
            self,
            ex: str,
            pair: str,
            interval: str,
            limit: int = 500,
            start_time: int = None,
            end_time: int = None
    ) -> pd.DataFrame:
        """
        Open interest in OHLC format for an exchange pair

        Args:
            ex: exchange to get OI for (e.g. Binance, dYdX, etc.)
            pair: pair to get OI for (e.g. BTCUSDT on Binance, BTC-USD on dYdX, etc.)
            interval: interval to get OI for (e.g. m1, m5, m15, m30, h1, h4, etc.)
            limit: number of data points to return (default: 500)
            start_time: start time in milliseconds
            end_time: end time in milliseconds

        Returns:
            pandas DataFrame with open interest in OHLC format for an exchange pair
        """
        response = self._get(
            endpoint="indicator/open_interest_ohlc",
            params={"ex": ex, "pair": pair, "interval": interval, "limit": limit,
                    "start_time": start_time, "end_time": end_time}
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="t")

    def open_interest_aggregated_ohlc(
            self,
            symbol: str,
            interval: str,
            limit: int = 500,
            start_time: int = None,
            end_time: int = None
    ) -> pd.DataFrame:
        """
        Aggregated open interest in OHLC format for a symbol

        Args:
            symbol: symbol to get OI for
            interval: interval to get OI for (e.g. m1, m5, m15, m30, h1, h4, etc.)
            limit: number of data points to return (default: 500)
            start_time: start time in milliseconds
            end_time: end time in milliseconds

        Returns:
            pandas DataFrame with aggregated open interest in OHLC format
        """
        response = self._get(
            endpoint="indicator/open_interest_aggregated_ohlc",
            params={"symbol": symbol, "interval": interval, "limit": limit,
                    "start_time": start_time, "end_time": end_time}
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="t")

    def liquidation_symbol(
            self,
            symbol: str,
            interval: str,
            limit: int = 500,
            start_time: int = None,
            end_time: int = None
    ) -> pd.DataFrame:
        """
        Liquidation data for a symbol

        Args:
            symbol: symbol to get liquidation data for
            interval: interval to get liquidation data for (e.g. m1, m5, m15, m30, h1, h4, etc.)
            limit: number of data points to return (default: 500)
            start_time: start time in milliseconds
            end_time: end time in milliseconds

        Returns:
            pandas DataFrame with liquidation data
        """
        response = self._get(
            endpoint="indicator/liquidation_symbol",
            params={"symbol": symbol, "interval": interval, "limit": limit,
                    "start_time": start_time, "end_time": end_time}
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="createTime")

    def liquidation_pair(
            self,
            ex: str,
            pair: str,
            interval: str,
            limit: int = 500,
            start_time: int = None,
            end_time: int = None
    ) -> pd.DataFrame:
        """
        Liquidation data for an exchange pair

        Args:
            ex: exchange to get liquidation data for (e.g. Binance, dYdX, etc.)
            pair: pair to get liquidation data for (e.g. BTCUSDT on Binance, BTC-USD on dYdX, etc.)
            interval: interval to get liquidation data for (e.g. m1, m5, m15, m30, h1, h4, etc.)
            limit: number of data points to return (default: 500)
            start_time: start time in milliseconds
            end_time: end time in milliseconds

        Returns:
            pandas DataFrame with liquidation data for an exchange pair
        """
        response = self._get(
            endpoint="indicator/liquidation_pair",
            params={"ex": ex, "pair": pair, "interval": interval, "limit": limit,
                    "start_time": start_time, "end_time": end_time}
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="t")

    def long_short_accounts(
            self,
            ex: str,
            pair: str,
            interval: str,
            limit: int = 500,
            start_time: int = None,
            end_time: int = None
    ) -> pd.DataFrame:
        """
        Long/short ratio for an exchange pair

        Args:
            ex: exchange to get liquidation data for (e.g. Binance, dYdX, etc.)
            pair: pair to get liquidation data for (e.g. BTCUSDT on Binance, BTC-USD on dYdX, etc.)
            interval: interval to get liquidation data for (e.g. m1, m5, m15, m30, h1, h4, etc.)
            limit: number of data points to return (default: 500)
            start_time: start time in milliseconds
            end_time: end time in milliseconds

        Returns:
            pandas DataFrame with long/short ratio for an exchange pair
        """
        response = self._get(
            endpoint="indicator/long_short_accounts",
            params={"ex": ex, "pair": pair, "interval": interval, "limit": limit,
                    "start_time": start_time, "end_time": end_time}
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="createTime")

    def long_short_symbol(
            self,
            symbol: str,
            interval: str,
            limit: int = 500,
            start_time: int = None,
            end_time: int = None
    ) -> pd.DataFrame:
        """
        Long/short ratio for a symbol

        Args:
            symbol: symbol to get long/short ratio for
            interval: interval to get long/short ratio for (e.g. m1, m5, m15, m30, h1, h4, etc.)
            limit: number of data points to return (default: 500)
            start_time: start time in milliseconds
            end_time: end time in milliseconds

        Returns:
            pandas DataFrame with long/short ratio
        """
        response = self._get(
            endpoint="indicator/long_short_symbol",
            params={"symbol": symbol, "interval": interval, "limit": limit,
                    "start_time": start_time, "end_time": end_time}
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="t")

    def top_long_short_account_ratio(
            self,
            ex: str,
            pair: str,
            interval: str,
            limit: int = 500,
            start_time: int = None,
            end_time: int = None
    ) -> pd.DataFrame:
        """
        Top accounts long/short ratio for an exchange pair

        Args:
            ex: exchange to get liquidation data for (e.g. Binance, dYdX, etc.)
            pair: pair to get liquidation data for (e.g. BTCUSDT on Binance, BTC-USD on dYdX, etc.)
            interval: interval to get liquidation data for (e.g. m1, m5, m15, m30, h1, h4, etc.)
            limit: number of data points to return (default: 500)
            start_time: start time in milliseconds
            end_time: end time in milliseconds

        Returns:
            pandas DataFrame with top accounts long/short ratio for an exchange pair
        """
        response = self._get(
            endpoint="indicator/top_long_short_account_ratio",
            params={"ex": ex, "pair": pair, "interval": interval, "limit": limit,
                    "start_time": start_time, "end_time": end_time}
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="createTime")

    def top_long_short_position_ratio(
            self,
            ex: str,
            pair: str,
            interval: str,
            limit: int = 500,
            start_time: int = None,
            end_time: int = None
    ) -> pd.DataFrame:
        """
        Top positions long/short ratio for an exchange pair

        Args:
            ex: exchange to get liquidation data for (e.g. Binance, dYdX, etc.)
            pair: pair to get liquidation data for (e.g. BTCUSDT on Binance, BTC-USD on dYdX, etc.)
            interval: interval to get liquidation data for (e.g. m1, m5, m15, m30, h1, h4, etc.)
            limit: number of data points to return (default: 500)
            start_time: start time in milliseconds
            end_time: end time in milliseconds

        Returns:
            pandas DataFrame with top positions long/short ratio for an exchange pair
        """
        response = self._get(
            endpoint="indicator/top_long_short_position_ratio",
            params={"ex": ex, "pair": pair, "interval": interval, "limit": limit,
                    "start_time": start_time, "end_time": end_time}
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="createTime")

    def bitcoin_bubble_index(self) -> pd.DataFrame:
        response = self._get(
            endpoint="index/bitcoin_bubble_index",
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="time", unit=None)

    def ahr999(self) -> pd.DataFrame:
        response = self._get(
            endpoint="index/ahr999",
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="date", unit=None)

    def tow_year_ma_multiplier(self) -> pd.DataFrame:
        response = self._get(
            endpoint="index/tow_year_MA_multiplier",
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="createTime")

    def tow_hundred_week_moving_avg_heatmap(self) -> pd.DataFrame:
        response = self._get(
            endpoint="index/tow_hundred_week_moving_avg_heatmap",
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="createTime")

    def puell_multiple(self) -> pd.DataFrame:
        response = self._get(
            endpoint="index/puell_multiple",
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="createTime")

    def stock_flow(self) -> pd.DataFrame:
        response = self._get(
            endpoint="index/stock_flow",
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="createTime", unit=None)

    def pi(self) -> pd.DataFrame:
        response = self._get(
            endpoint="index/pi",
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="createTime", cast_objects_to_numeric=True)

    def golden_ratio_multiplier(self) -> pd.DataFrame:
        response = self._get(
            endpoint="index/golden_ratio_multiplier",
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="createTime", cast_objects_to_numeric=True)

    def bitcoin_profitable_days(self) -> pd.DataFrame:
        response = self._get(
            endpoint="index/bitcoin_profitable_days",
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="createTime")

    def log_log_regression(self) -> pd.DataFrame:
        response = self._get(
            endpoint="index/log_log_regression",
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="createTime")

    def grayscale_market_history(self) -> pd.DataFrame:
        response = self._get(
            endpoint="index/grayscale_market_history",
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="dateList")
