from unittest import TestCase
import os

from coinglass_api import CoinglassAPI

cg = CoinglassAPI(coinglass_secret=os.getenv("COINGLASS_SECRET"))


class TestAPI(TestCase):
    def test_funding(self):
        fr_btc_dydx = cg.funding(ex="dYdX", pair="ETH-USD", interval="h8")
        self.assertEqual(fr_btc_dydx.shape[0], 500)
        self.assertTrue("fundingRate" in fr_btc_dydx.columns)

    def test_funding_ohlc(self):
        fr_ohlc_eth_binance = cg.funding_ohlc(ex="Binance", pair="ETHUSDT", interval="h4")
        self.assertEqual(fr_ohlc_eth_binance.shape[0], 500)
        self.assertTrue("o" in fr_ohlc_eth_binance.columns)
        self.assertTrue("h" in fr_ohlc_eth_binance.columns)
        self.assertTrue("l" in fr_ohlc_eth_binance.columns)
        self.assertTrue("c" in fr_ohlc_eth_binance.columns)

    def test_funding_average(self):
        fr_avg_eth = cg.funding_average(symbol="ETH", interval="h4")
        self.assertEqual(fr_avg_eth.shape[0], 500)
        self.assertIn("fundingRate", fr_avg_eth.columns)

    def test_open_interest_ohlc(self):
        oi_ohlc_eth_binance = cg.open_interest_ohlc(ex="Binance", pair="ETHUSDT", interval="h4")
        self.assertEqual(oi_ohlc_eth_binance.shape[0], 500)
        self.assertIn("o", oi_ohlc_eth_binance.columns)
        self.assertIn("h", oi_ohlc_eth_binance.columns)
        self.assertIn("l", oi_ohlc_eth_binance.columns)
        self.assertIn("c", oi_ohlc_eth_binance.columns)

    def test_open_interest_aggregated_ohlc(self):
        oi_ohlc_eth_binance = cg.open_interest_aggregated_ohlc(symbol="ETH", interval="h4")
        self.assertEqual(oi_ohlc_eth_binance.shape[0], 500)
        self.assertIn("o", oi_ohlc_eth_binance.columns)
        self.assertIn("h", oi_ohlc_eth_binance.columns)
        self.assertIn("l", oi_ohlc_eth_binance.columns)
        self.assertIn("c", oi_ohlc_eth_binance.columns)

    def test_liquidation_symbol(self):
        liq_eth = cg.liquidation_symbol(symbol="ETH", interval="h4")
        self.assertEqual(liq_eth.shape[0], 500)
        self.assertIn("volUsd", liq_eth.columns)
        self.assertIn("buyVolUsd", liq_eth.columns)
        self.assertIn("sellVolUsd", liq_eth.columns)

    def test_liquidation_pair(self):
        liq_eth = cg.liquidation_pair(ex="Binance", pair="ETHUSDT", interval="h4")
        self.assertEqual(liq_eth.shape[0], 500)
        self.assertIn("volUsd", liq_eth.columns)
        self.assertIn("buyVolUsd", liq_eth.columns)
        self.assertIn("sellVolUsd", liq_eth.columns)

    def test_long_short_accounts(self):
        lsa_eth = cg.long_short_accounts(ex="Binance", pair="ETHUSDT", interval="h4")
        self.assertEqual(lsa_eth.shape[0], 500)
        self.assertIn("longRatio", lsa_eth.columns)
        self.assertIn("shortRatio", lsa_eth.columns)
        self.assertIn("longShortRatio", lsa_eth.columns)

    def test_long_short_symbol(self):
        lsa_eth = cg.long_short_symbol(symbol="ETH", interval="h4")
        self.assertEqual(lsa_eth.shape[0], 500)
        self.assertIn("v", lsa_eth.columns)
