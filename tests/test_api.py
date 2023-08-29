import os
from unittest import TestCase

from coinglass_api import CoinglassAPI


class TestAPI(TestCase):
    def setUp(self) -> None:
        self.cg = CoinglassAPI(coinglass_secret=os.getenv("COINGLASS_SECRET"))

    def tearDown(self) -> None:
        self.cg._session.close()

    def test_perpetual_market(self) -> None:
        btc_perp = self.cg.perpetual_market(symbol="BTC")
        self.assertIn("openInterest", btc_perp.columns)
        self.assertIn("fundingRate", btc_perp.columns)
        self.assertIn("totalVolUsd", btc_perp.columns)

    def test_futures_markets(self) -> None:
        btc_futs = self.cg.futures_market(symbol="BTC")
        self.assertIn("longRate", btc_futs.columns)
        self.assertIn("shortRate", btc_futs.columns)
        self.assertIn("openInterestAmount", btc_futs.columns)

    def test_open_interest(self) -> None:
        btc_oi = self.cg.open_interest(symbol="BTC")
        self.assertIn("openInterest", btc_oi.columns)
        self.assertIn("openInterestAmountByStableCoinMargin", btc_oi.columns)
        self.assertIn("h4OIChangePercent", btc_oi.columns)

    def test_option(self):
        btc_option = self.cg.option(symbol="BTC")
        self.assertIn("openInterest", btc_option.columns)
        self.assertIn("rate", btc_option.columns)
        self.assertIn("h24Change", btc_option.columns)

    def test_option_history(self):
        btc_option = self.cg.option_history(symbol="BTC", currency="USD")
        self.assertIn(('dataMap', 'Deribit'), btc_option.columns)
        self.assertIn(('dataMap', 'CME'), btc_option.columns)
        self.assertIn(('dataMap', 'OKX'), btc_option.columns)

    def test_option_vol_history(self) -> None:
        btc_option = self.cg.option_vol_history(symbol="BTC", currency="USD")
        self.assertIn(('dataMap', 'Deribit'), btc_option.columns)
        self.assertIn(('dataMap', 'CME'), btc_option.columns)
        self.assertIn(('dataMap', 'OKX'), btc_option.columns)

    def test_top_liquidations(self) -> None:
        btc_liquidations = self.cg.top_liquidations(time_type="h1")
        self.assertIn("number", btc_liquidations.columns)
        self.assertIn("amount", btc_liquidations.columns)
        self.assertIn("longVolUsd", btc_liquidations.columns)
        self.assertIn("shortVolUsd", btc_liquidations.columns)

    def test_liquidation_info(self) -> None:
        btc_liquidations_info = self.cg.liquidation_info(symbol="BTC", time_type="h1")
        self.assertIn("h1TotalVolUsd", btc_liquidations_info)
        self.assertIn("h1Amount", btc_liquidations_info)
        self.assertIn("h24TotalVolUsd", btc_liquidations_info)
        self.assertIn("h24TotalVolUsd", btc_liquidations_info)

    def test_exchange_liquidations(self) -> None:
        btc_liquidations = self.cg.exchange_liquidations(symbol="BTC", time_type="h1")
        self.assertIn("shortRate", btc_liquidations.columns)
        self.assertIn("longRate", btc_liquidations.columns)
        self.assertIn("exchangeName", btc_liquidations.columns)

    def test_liquidations_history(self) -> None:
        btc_liquidations = self.cg.liquidations_history(symbol="BTC", time_type="h1")
        self.assertIn(('list', 'Binance', 'exchangeName'), btc_liquidations.index)
        self.assertIn(('list', 'OKX', 'sellQty'), btc_liquidations.index)

    def test_exchange_long_short_ratio(self) -> None:
        btc_long_short_ratio = self.cg.exchange_long_short_ratio(symbol="BTC", time_type="h1")
        self.assertIn(('list', 'Binance', 'exchangeName'), btc_long_short_ratio.index)
        self.assertIn(('list', 'Kraken', 'shortVolUsd'), btc_long_short_ratio.index)

    def test_long_short_ratio_history(self) -> None:
        btc_long_short_ratio = self.cg.long_short_ratio_history(symbol="BTC", time_type="h1")
        self.assertIn("sellQty", btc_long_short_ratio.columns)
        self.assertIn("longRateList", btc_long_short_ratio.columns)

    def test_futures_coins_markets(self) -> None:
        futures_coins = self.cg.futures_coins_markets()
        self.assertIn("exchangeName", futures_coins.columns)
        self.assertIn("avgFundingRate", futures_coins.columns)
        self.assertIn("avgFundingRateByVol", futures_coins.columns)

    def test_futures_coins_price_change(self) -> None:
        futures_coins = self.cg.futures_coins_price_change()
        self.assertIn("m5PriceChangePercent", futures_coins.columns)
        self.assertIn("m15PriceChangePercent", futures_coins.columns)
        self.assertIn("h1PriceChangePercent", futures_coins.columns)

    def test_futures_basis_chart(self) -> None:
        futures_basis = self.cg.futures_basis_chart(symbol="BTC")
        self.assertIn(('PERPETUAL', 'name'), futures_basis.index)
        self.assertIn(('QUARTER', 'name'), futures_basis.index)

    def test_futures_vol(self) -> None:
        futures_vol = self.cg.futures_vol(symbol="BTC", time_type="h1")
        self.assertIn(('dataMap', 'Binance'), futures_vol.columns)
        self.assertIn(('dataMap', 'Deribit'), futures_vol.columns)
