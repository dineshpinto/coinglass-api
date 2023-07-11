import pandas as pd
import requests

from .exceptions import CoinglassAPIException, CoinglassRequestException, RateLimitExceededException


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

    def _get(self, endpoint: str, params: dict | None = None) -> dict:
        headers = {
            "accept": "application/json",
            "coinglassSecret": self.__coinglass_secret
        }
        url = self._base_url + endpoint
        return self._session.request(
            method='GET',
            url=url,
            params=params,
            headers=headers,
            timeout=30
        ).json()

    @staticmethod
    def _create_dataframe(
            data: list[dict],
            time_col: str | None = None,
            unit: str | None = "ms",
            cast_objects_to_numeric: bool = False
    ) -> pd.DataFrame:
        """
        Create pandas DataFrame from a list of dicts

        Args:
            data: list of dicts
            time_col: name of time column in dict
            unit: unit of time column, specify None to use auto-resolver (default: ms)
            cast_objects_to_numeric: cast all object columns to numeric (default: False)

        Returns:
            pandas DataFrame
        """
        df = pd.DataFrame(data)

        if time_col:
            if time_col == "time":
                # Handle edge case of time column being named "time"
                df.rename(columns={"time": "t"}, inplace=True)
                time_col = "t"

            df["time"] = pd.to_datetime(df[time_col], unit=unit)
            df.drop(columns=[time_col], inplace=True)
            df.set_index("time", inplace=True, drop=True)

            if "t" in df.columns:
                # Drop additional "t" column if it exists
                df.drop(columns=["t"], inplace=True)

        if cast_objects_to_numeric:
            cols = df.columns[df.dtypes.eq('object')]
            df[cols] = df[cols].apply(pd.to_numeric)

        return df

    @staticmethod
    def _create_multiindex_dataframe(
            data: list[dict],
            list_key: str
    ) -> pd.DataFrame:
        """
        Create MultiIndex pandas DataFrame from a list of nested dicts

        Args:
            data: list of nested dicts
            list_key: key in dict that contains list of dicts

        Returns:
            dict of pandas DataFrame
        """
        flattened_data = {}

        # Flatten nested dicts
        for symbol_data in data:
            flattened_dict = {}
            for outer_key, outer_value in symbol_data.items():
                if isinstance(outer_value, list):
                    for exchange in outer_value:
                        exchange_name = exchange["exchangeName"]
                        for inner_key, value in exchange.items():
                            flattened_dict[(outer_key, exchange_name, inner_key)] = value
                else:
                    flattened_dict[outer_key] = outer_value

            # Remove non-tuple keys
            remove_keys = []
            for key in list(flattened_dict.keys()):
                if not isinstance(key, tuple):
                    remove_keys.append(key)

            for k in remove_keys:
                flattened_dict.pop(k, None)

            df = pd.DataFrame.from_dict(flattened_dict, orient="index")
            df.index = pd.MultiIndex.from_tuples(df.index)

            flattened_data[symbol_data[list_key]] = df

        return pd.concat(flattened_data, axis=1)

    @staticmethod
    def _flatten_dictionary(data: dict) -> dict:
        flattened_dict = {}

        for outer_key, outer_value in data.items():
            if isinstance(outer_value, dict):
                for inner_key, inner_value in outer_value.items():
                    if isinstance(inner_value, list):
                        flattened_dict[(outer_key, inner_key)] = inner_value
                    else:
                        flattened_dict[inner_key] = inner_value
            else:
                flattened_dict[(outer_key, 0)] = outer_value

        return flattened_dict

    @staticmethod
    def _check_for_errors(response: dict) -> None:
        """ Check for errors in response """

        if "success" not in response.keys():
            # Handle error case
            raise CoinglassAPIException(status=response["status"], error=response["error"])

        if not response["success"]:
            # Handle unsuccessful response
            code, msg = int(response["code"]), response["msg"]
            match code:
                case 50001:
                    raise RateLimitExceededException()
                case _:
                    raise CoinglassRequestException(code=code, msg=msg)

    def perpetual_market(self, symbol: str) -> pd.DataFrame:
        response = self._get(
            endpoint="perpetual_market",
            params={"symbol": symbol}
        )
        self._check_for_errors(response)
        data = response["data"][symbol]
        return self._create_dataframe(data)

    def futures_market(self, symbol: str) -> pd.DataFrame:
        response = self._get(
            endpoint="futures_market",
            params={"symbol": symbol}
        )
        self._check_for_errors(response)
        data = response["data"][symbol]
        return self._create_dataframe(data)

    def funding_rate(self) -> pd.DataFrame:
        response = self._get(
            endpoint="funding",
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_multiindex_dataframe(data, list_key="symbol")

    def funding_usd_history(self, symbol: str, time_type: str) -> list[dict]:
        """
        Get funding history in USD for a coin

        Args:
            symbol: Coin symbol (e.g. BTC)
            time_type: Time type (e.g. m1, m5, h8)

        Returns:
            List of dicts
        """
        response = self._get(
            endpoint="funding_usd_history",
            params={"symbol": symbol, "time_type": time_type}
        )
        self._check_for_errors(response)
        data = response["data"]
        return data

    def funding_coin_history(self, symbol: str, time_type: str) -> list[dict]:
        """
        Get funding history in coin for a coin

        Args:
            symbol: Coin symbol (e.g. BTC)
            time_type: Time type (e.g. m1, m5, h8)

        Returns:
            List of dicts
        """
        response = self._get(
            endpoint="funding_coin_history",
            params={"symbol": symbol, "time_type": time_type}
        )
        self._check_for_errors(response)
        data = response["data"]
        return data

    def open_interest(self, symbol: str) -> pd.DataFrame:
        response = self._get(
            endpoint="open_interest",
            params={"symbol": symbol}
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data)

    def open_interest_history(
            self,
            symbol: str,
            time_type: str,
            currency: str
    ) -> pd.DataFrame:
        """
        Get open interest history

        Args:
            symbol: Coin symbol (e.g. BTC)
            time_type: Time type (e.g. m1, m5, h8, all)
            currency: Currency (e.g. USD or symbol)

        Returns:
            pandas DataFrame
        """
        response = self._get(
            endpoint="open_interest_history",
            params={"symbol": symbol, "time_type": time_type, "currency": currency}
        )
        self._check_for_errors(response)
        data = response["data"]

        flattened_dict = {}

        for k, v in data.items():
            if isinstance(v, dict):
                for outer_key, outer_value in v.items():
                    if isinstance(outer_value, list):
                        flattened_dict[(k, outer_key)] = outer_value
                    else:
                        flattened_dict[outer_key] = outer_value
            else:
                flattened_dict[(k, 0)] = v

        df = pd.DataFrame(flattened_dict)
        df["time"] = pd.to_datetime(df["dateList"][0], unit="ms")
        df.drop(columns=["dateList"], inplace=True)
        df.set_index("time", inplace=True, drop=True)
        return df

    def option(self, symbol: str) -> pd.DataFrame:
        response = self._get(
            endpoint="option",
            params={"symbol": symbol}
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data)

    def option_history(self, symbol: str, currency: str) -> pd.DataFrame:
        """
        Get option history

        Args:
            symbol: Coin symbol (e.g. BTC)
            currency: Currency (e.g. USD or symbol)

        Returns:
            pandas DataFrame
        """
        response = self._get(
            endpoint="option_history",
            params={"symbol": symbol, "currency": currency}
        )
        self._check_for_errors(response)
        data = response["data"]
        df = pd.DataFrame(self._flatten_dictionary(data[0]))
        df["time"] = pd.to_datetime(df["dateList"][0], unit="ms")
        df.drop(columns=["dateList"], inplace=True, level=0)
        df.set_index("time", inplace=True, drop=True)
        return df

    def option_vol_history(self, symbol: str, currency: str) -> pd.DataFrame:
        response = self._get(
            endpoint="option/vol/history",
            params={"symbol": symbol, "currency": currency}
        )
        self._check_for_errors(response)
        data = response["data"]
        df = pd.DataFrame(self._flatten_dictionary(data))
        df["time"] = pd.to_datetime(df["dateList"][0], unit="ms")
        df.drop(columns=["dateList"], inplace=True, level=0)
        df.set_index("time", inplace=True, drop=True)
        return df

    def top_liquidations(self, time_type: str) -> pd.DataFrame:
        """
        Get top liquidations

        Args:
            time_type: Time type (e.g. h1, h4, h12, h24)

        Returns:
            pandas DataFrame
        """
        response = self._get(
            endpoint="liquidation_top",
            params={"time_type": time_type}
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data)

    def liquidation_info(self, symbol: str, time_type: str) -> dict:
        response = self._get(
            endpoint="liquidation_info",
            params={"symbol": symbol, "time_type": time_type}
        )
        self._check_for_errors(response)
        data = response["data"]
        return data

    def exchange_liquidations(self, symbol: str, time_type: str) -> pd.DataFrame:
        response = self._get(
            endpoint="liquidation_ex",
            params={"symbol": symbol, "time_type": time_type}
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data)

    def liquidations_history(self, symbol: str, time_type: str) -> pd.DataFrame:
        response = self._get(
            endpoint="liquidation_history",
            params={"symbol": symbol, "time_type": time_type}
        )
        self._check_for_errors(response)
        data = response["data"]
        # TODO: Improve formatting
        return self._create_multiindex_dataframe(data, list_key="createTime")

    def exchange_long_short_ratio(self, symbol: str, time_type: str) -> pd.DataFrame:
        response = self._get(
            endpoint="long_short",
            params={"symbol": symbol, "time_type": time_type}
        )
        self._check_for_errors(response)
        data = response["data"]
        # TODO: Improve formatting
        return self._create_multiindex_dataframe(data, list_key="symbol")

    def long_short_ratio_history(self, symbol: str, time_type: str) -> pd.DataFrame:
        response = self._get(
            endpoint="long_short_history",
            params={"symbol": symbol, "time_type": time_type}
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data, time_col="dateList")

    def futures_coins_markets(self) -> pd.DataFrame:
        response = self._get(
            endpoint="futures_coins_markets",
            params={}
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data)

    def futures_coins_price_change(self) -> pd.DataFrame:
        response = self._get(
            endpoint="futures_coins_price_change",
            params={}
        )
        self._check_for_errors(response)
        data = response["data"]
        return self._create_dataframe(data)

    def futures_basis_chart(self, symbol: str) -> pd.DataFrame:
        response = self._get(
            endpoint="futures_basis_chart",
            params={"symbol": symbol}
        )
        self._check_for_errors(response)
        data = response["data"]

        flattened_data = {}

        # Flatten nested dicts
        for symbol_data in data:
            flattened_dict = {}
            for outer_key, outer_value in symbol_data.items():
                if isinstance(outer_value, dict):
                    for inner_key, value in outer_value.items():
                        flattened_dict[(outer_key, inner_key)] = value
                else:
                    flattened_dict[outer_key] = outer_value

            # Remove non-tuple keys
            remove_keys = []
            for key in list(flattened_dict.keys()):
                if not isinstance(key, tuple):
                    remove_keys.append(key)

            for k in remove_keys:
                flattened_dict.pop(k, None)

            df = pd.DataFrame.from_dict(flattened_dict, orient="index")
            df.index = pd.MultiIndex.from_tuples(df.index)

            flattened_data[symbol_data["exName"]] = df

        return pd.concat(flattened_data, axis=1)

    def futures_vol(self, symbol: str, time_type: str) -> pd.DataFrame:
        """
        Get futures volume

        Args:
            symbol: Coin symbol (e.g. BTC, ETH, LTC, etc.)
            time_type: Time type (e.g. h1, h4, h12, h24, all)

        Returns:
            pandas DataFrame
        """
        response = self._get(
            endpoint="futures_vol",
            params={"symbol": symbol, "time_type": time_type}
        )
        self._check_for_errors(response)
        data = response["data"]
        df = pd.DataFrame(self._flatten_dictionary(data))
        df["time"] = pd.to_datetime(df["dateList"][0], unit="ms")
        df.drop(columns=["dateList"], inplace=True, level=0)
        df.set_index("time", inplace=True, drop=True)
        return df

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
