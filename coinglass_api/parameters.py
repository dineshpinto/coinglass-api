import warnings

from .exceptions import CoinglassParameterWarning


class CoinglassParameterValidation:
    def __init__(self):
        self.exchanges: list[str] = [
            'Binance', 'OKX', 'dYdX', 'Bitget', 'Bybit', 'BingX', 'Bitmex', 'Bitfinex', 'Deribit', 'CoinEx', 'Kraken',
            'Huobi'
        ]

        self.time_types: list[str] = [
            'h1', 'h2', 'h4', 'h6', 'h8', 'h12', 'h24', 'm1', 'm3', 'm5', 'm15', 'm30', '1d', '7d'
        ]

    def add_exchange(self, exchange: str):
        self.exchanges.append(exchange)

    def add_time_type(self, time_type: str):
        self.time_types.append(time_type)

    def get_exchanges(self):
        """ Returns list of exchanges """
        return self.exchanges

    def get_time_types(self):
        """ Returns list of time types """
        return self.time_types

    def _validate_exchange(self, exchange: str):
        if exchange not in self.exchanges:
            warnings.warn(
                f"Exchange '{exchange}' not in predefined exchange list: {self.exchanges}",
                CoinglassParameterWarning
            )

    def _validate_time_type(self, time_type: str):
        if time_type not in self.time_types:
            warnings.warn(
                f"Time type '{time_type}' not in predefined time type list: {self.time_types}",
                CoinglassParameterWarning
            )

    def validate_params(self, params: dict):
        if "ex" in params.keys():
            self._validate_exchange(params["ex"])
        elif "ex_name" in params.keys():
            self._validate_exchange(params["ex_name"])
        if "time_type" in params.keys():
            self._validate_time_type(params["time_type"])
        elif "interval" in params.keys():
            self._validate_time_type(params["interval"])
