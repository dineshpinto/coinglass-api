import os
from unittest import TestCase

from coinglass_api import CoinglassAPI


class TestIndicatorEndpoint(TestCase):
    def setUp(self) -> None:
        self.cg = CoinglassAPI(coinglass_secret=os.getenv("COINGLASS_SECRET"))

    def tearDown(self) -> None:
        self.cg._session.close()

    def test_funding_rate(self) -> None:
        btc_fr = self.cg.funding_rate()
        self.assertIn(('uMarginList', 'Binance', 'rate'), btc_fr.index)
        self.assertIn(("BTC", 0), btc_fr.columns)

    def test_funding(self) -> None:
        fr_btc_dydx = self.cg.funding(ex="dYdX", pair="ETH-USD", interval="h8")
        self.assertEqual(fr_btc_dydx.shape[0], 500)
        self.assertTrue("fundingRate" in fr_btc_dydx.columns)

    def test_funding_ohlc(self) -> None:
        fr_ohlc_eth_binance = self.cg.funding_ohlc(
            ex="Binance", pair="ETHUSDT", interval="h4"
        )
        self.assertEqual(fr_ohlc_eth_binance.shape[0], 500)
        self.assertTrue("o" in fr_ohlc_eth_binance.columns)
        self.assertTrue("h" in fr_ohlc_eth_binance.columns)
        self.assertTrue("l" in fr_ohlc_eth_binance.columns)
        self.assertTrue("c" in fr_ohlc_eth_binance.columns)

    def test_funding_average(self) -> None:
        fr_avg_eth = self.cg.funding_average(symbol="ETH", interval="h4")
        self.assertEqual(fr_avg_eth.shape[0], 500)
        self.assertIn("fundingRate", fr_avg_eth.columns)

    def test_open_interest_ohlc(self) -> None:
        oi_ohlc_eth_binance = self.cg.open_interest_ohlc(
            ex="Binance", pair="ETHUSDT", interval="h4"
        )
        self.assertEqual(oi_ohlc_eth_binance.shape[0], 500)
        self.assertIn("o", oi_ohlc_eth_binance.columns)
        self.assertIn("h", oi_ohlc_eth_binance.columns)
        self.assertIn("l", oi_ohlc_eth_binance.columns)
        self.assertIn("c", oi_ohlc_eth_binance.columns)

    def test_open_interest_aggregated_ohlc(self) -> None:
        oi_ohlc_eth_binance = self.cg.open_interest_aggregated_ohlc(
            symbol="ETH", interval="h4"
        )
        self.assertEqual(oi_ohlc_eth_binance.shape[0], 500)
        self.assertIn("o", oi_ohlc_eth_binance.columns)
        self.assertIn("h", oi_ohlc_eth_binance.columns)
        self.assertIn("l", oi_ohlc_eth_binance.columns)
        self.assertIn("c", oi_ohlc_eth_binance.columns)

    def test_liquidation_symbol(self) -> None:
        liq_eth = self.cg.liquidation_symbol(symbol="ETH", interval="h4")
        self.assertEqual(liq_eth.shape[0], 500)
        self.assertIn("volUsd", liq_eth.columns)
        self.assertIn("buyVolUsd", liq_eth.columns)
        self.assertIn("sellVolUsd", liq_eth.columns)

    def test_liquidation_pair(self) -> None:
        liq_eth = self.cg.liquidation_pair(ex="Binance", pair="ETHUSDT", interval="h4")
        self.assertEqual(liq_eth.shape[0], 500)
        self.assertIn("volUsd", liq_eth.columns)
        self.assertIn("buyVolUsd", liq_eth.columns)
        self.assertIn("sellVolUsd", liq_eth.columns)

    def test_long_short_accounts(self) -> None:
        lsa_eth = self.cg.long_short_accounts(
            ex="Binance", pair="ETHUSDT", interval="h4"
        )
        self.assertEqual(lsa_eth.shape[0], 500)
        self.assertIn("longRatio", lsa_eth.columns)
        self.assertIn("shortRatio", lsa_eth.columns)
        self.assertIn("longShortRatio", lsa_eth.columns)

    def test_long_short_symbol(self) -> None:
        lsa_eth = self.cg.long_short_symbol(symbol="ETH", interval="h4")
        self.assertEqual(lsa_eth.shape[0], 500)
        self.assertIn("v", lsa_eth.columns)

    def test_top_long_short_account_ratio(self) -> None:
        lsa_eth = self.cg.top_long_short_account_ratio(
            ex="Binance", pair="ETHUSDT", interval="h4"
        )
        self.assertEqual(lsa_eth.shape[0], 500)
        self.assertIn("longRatio", lsa_eth.columns)
        self.assertIn("shortRatio", lsa_eth.columns)
        self.assertIn("longShortRatio", lsa_eth.columns)

    def test_top_long_short_position_ratio(self) -> None:
        lsa_eth = self.cg.top_long_short_position_ratio(
            ex="Binance", pair="ETHUSDT", interval="h4"
        )
        self.assertEqual(lsa_eth.shape[0], 500)
        self.assertIn("longRatio", lsa_eth.columns)
        self.assertIn("shortRatio", lsa_eth.columns)
        self.assertIn("longShortRatio", lsa_eth.columns)
