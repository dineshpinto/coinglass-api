import warnings

from .exceptions import CoinglassParameterWarning


class CoinglassParameterValidation:
    def __init__(self):
        self.exchanges: list[str] = [
            'Binance', 'Coinbase Pro', 'Huobi', 'Kraken', 'Bitfinex', 'Bitmex', 'Bybit', 'Bitget',  'CoinEx', 'CME', 'Deribit', 'dYdX',
            'Gate', 'Gemini',  'LedgerX', 'OKX', 'CME', 'Bit.com'
        ]

        self.symbols: list[str] = [
            '1000BONK', '1000LUNC', '1000SHIB', '1000XEC', '1INCH', 'AAVE', 'ACH', 'ADA', 'AGIX', 'AGLD', 'ALGO',
            'ALICE', 'ALPHA', 'AMB', 'ANKR', 'ANT', 'APE', 'API3', 'APT', 'AR', 'ARPA', 'ASTR', 'ATA', 'ATOM', 'AUDIO',
            'AVAX', 'AXS', 'BAKE', 'BAL', 'BAND', 'BAT', 'BCH', 'BEL', 'BICO', 'BIT', 'BLUEBIRD', 'BLZ', 'BMEX', 'BNB',
            'BNT', 'BNX', 'BSV', 'BSW', 'BTC', 'BTCDOM', 'C98', 'CEL', 'CELO', 'CELR', 'CFX', 'CHR', 'CHZ', 'COMP',
            'COTI', 'CREAM', 'CRO', 'CRV', 'CSPR', 'CTK', 'CTSI', 'CVC', 'CVX', 'DAR', 'DASH', 'DEFI', 'DENT', 'DGB',
            'DODO', 'DOGE', 'DOME', 'DORA', 'DOT', 'DUSK', 'DYDX', 'EGLD', 'ENJ', 'ENS', 'EOS', 'ETC', 'ETH', 'ETHW',
            'FET', 'FIL', 'FITFI', 'FLM', 'FLOW', 'FOOTBALL', 'FTM', 'FXS', 'GAL', 'GALA', 'GLMR', 'GMT', 'GMX', 'GODS',
            'GRT', 'GTC', 'HBAR', 'HNT', 'HOOK', 'HOT', 'HT', 'ICP', 'ICX', 'ILV', 'IMX', 'INJ', 'IOST', 'IOTA', 'IOTX',
            'JASMY', 'JST', 'KAVA', 'KDA', 'KISHU', 'KLAY', 'KNC', 'KSM', 'LDO', 'LEVER', 'LINA', 'LINK', 'LIT',
            'LOOKS', 'LPT', 'LRC', 'LTC', 'LUNA', 'LUNA2', 'LUNC', 'MAGIC', 'MANA', 'MASK', 'MATIC', 'MINA', 'MKR',
            'MTL', 'NEAR', 'NEO', 'NFT', 'NKN', 'OCEAN', 'OGN', 'OMG', 'ONE', 'ONT', 'OP', 'PAXG', 'PEOPLE', 'PERP',
            'PHB', 'QNT', 'QTUM', 'REEF', 'REN', 'RLC', 'RNDR', 'ROSE', 'RSR', 'RSS3', 'RUNE', 'RVN', 'SAND', 'SFP',
            'SHIB', 'SHIB1000', 'SKL', 'SLP', 'SNX', 'SOL', 'SPELL', 'STARL', 'STG', 'STMX', 'STORJ', 'STX', 'SUSHI',
            'SWEAT', 'SXP', 'T', 'THETA', 'TLM', 'TOMO', 'TON', 'TRB', 'TRX', 'TWT', 'UMA', 'UNFI', 'UNI', 'USDC',
            'USTC', 'VET', 'WAVES', 'WOO', 'XCH', 'XCN', 'XEM', 'XLM', 'XMR', 'XNO', 'XRP', 'XTZ', 'YFI', 'YFII', 'YGG',
            'ZEC', 'ZEN', 'ZIL', 'ZRX', 'ALL'
        ]

        self.time_types: list[str] = [
            'h1', 'h4', 'h8', 'h12', 'h24', 'm1', 'm5', 'm15', 'm30',
        ]

    def add_exchange(self, exchange: str):
        self.exchanges.append(exchange)

    def add_symbol(self, symbol: str):
        self.symbols.append(symbol)

    def add_time_type(self, time_type: str):
        self.time_types.append(time_type)

    def get_exchanges(self):
        """ Returns list of exchanges """
        return self.exchanges

    def get_symbols(self):
        """ Returns list of symbols """
        return self.symbols

    def get_time_types(self):
        """ Returns list of time types """
        return self.time_types

    def _validate_exchange(self, exchange: str):
        if exchange not in self.exchanges:
            warnings.warn(
                f"Exchange '{exchange}' not in predefined exchange list: {self.exchanges}",
                CoinglassParameterWarning
            )

    def _validate_symbol(self, symbol: str):
        if symbol not in self.symbols:
            warnings.warn(
                f"Symbol '{symbol}' not in predefined symbol list: {self.symbols}",
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
        if "symbol" in params.keys():
            self._validate_symbol(params["symbol"])
        if "time_type" in params.keys():
            self._validate_time_type(params["time_type"])
