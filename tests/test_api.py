import os
from unittest import TestCase

from coinglass_api import CoinglassAPI


class TestAPI(TestCase):
    def setUp(self) -> None:
        self.cg = CoinglassAPI(coinglass_secret=os.getenv("COINGLASS_SECRET"))

    def tearDown(self) -> None:
        self.cg._session.close()

    def test_funding(self):
        fr_btc_dydx = self.cg.funding(ex="dYdX", pair="ETH-USD", interval="h8")
        self.assertEqual(fr_btc_dydx.shape[0], 500)
        self.assertTrue("fundingRate" in fr_btc_dydx.columns)

    def test_funding_ohlc(self):
        fr_ohlc_eth_binance = self.cg.funding_ohlc(ex="Binance", pair="ETHUSDT", interval="h4")
        self.assertEqual(fr_ohlc_eth_binance.shape[0], 500)
        self.assertTrue("o" in fr_ohlc_eth_binance.columns)
        self.assertTrue("h" in fr_ohlc_eth_binance.columns)
        self.assertTrue("l" in fr_ohlc_eth_binance.columns)
        self.assertTrue("c" in fr_ohlc_eth_binance.columns)

    def test_funding_average(self):
        fr_avg_eth = self.cg.funding_average(symbol="ETH", interval="h4")
        self.assertEqual(fr_avg_eth.shape[0], 500)
        self.assertIn("fundingRate", fr_avg_eth.columns)

    def test_open_interest_ohlc(self):
        oi_ohlc_eth_binance = self.cg.open_interest_ohlc(ex="Binance", pair="ETHUSDT", interval="h4")
        self.assertEqual(oi_ohlc_eth_binance.shape[0], 500)
        self.assertIn("o", oi_ohlc_eth_binance.columns)
        self.assertIn("h", oi_ohlc_eth_binance.columns)
        self.assertIn("l", oi_ohlc_eth_binance.columns)
        self.assertIn("c", oi_ohlc_eth_binance.columns)

    def test_open_interest_aggregated_ohlc(self):
        oi_ohlc_eth_binance = self.cg.open_interest_aggregated_ohlc(symbol="ETH", interval="h4")
        self.assertEqual(oi_ohlc_eth_binance.shape[0], 500)
        self.assertIn("o", oi_ohlc_eth_binance.columns)
        self.assertIn("h", oi_ohlc_eth_binance.columns)
        self.assertIn("l", oi_ohlc_eth_binance.columns)
        self.assertIn("c", oi_ohlc_eth_binance.columns)

    def test_liquidation_symbol(self):
        liq_eth = self.cg.liquidation_symbol(symbol="ETH", interval="h4")
        self.assertEqual(liq_eth.shape[0], 500)
        self.assertIn("volUsd", liq_eth.columns)
        self.assertIn("buyVolUsd", liq_eth.columns)
        self.assertIn("sellVolUsd", liq_eth.columns)

    def test_liquidation_pair(self):
        liq_eth = self.cg.liquidation_pair(ex="Binance", pair="ETHUSDT", interval="h4")
        self.assertEqual(liq_eth.shape[0], 500)
        self.assertIn("volUsd", liq_eth.columns)
        self.assertIn("buyVolUsd", liq_eth.columns)
        self.assertIn("sellVolUsd", liq_eth.columns)

    def test_long_short_accounts(self):
        lsa_eth = self.cg.long_short_accounts(ex="Binance", pair="ETHUSDT", interval="h4")
        self.assertEqual(lsa_eth.shape[0], 500)
        self.assertIn("longRatio", lsa_eth.columns)
        self.assertIn("shortRatio", lsa_eth.columns)
        self.assertIn("longShortRatio", lsa_eth.columns)

    def test_long_short_symbol(self):
        lsa_eth = self.cg.long_short_symbol(symbol="ETH", interval="h4")
        self.assertEqual(lsa_eth.shape[0], 500)
        self.assertIn("v", lsa_eth.columns)

    def test_top_long_short_account_ratio(self):
        lsa_eth = self.cg.top_long_short_account_ratio(ex="Binance", pair="ETHUSDT", interval="h4")
        self.assertEqual(lsa_eth.shape[0], 500)
        self.assertIn("longRatio", lsa_eth.columns)
        self.assertIn("shortRatio", lsa_eth.columns)
        self.assertIn("longShortRatio", lsa_eth.columns)

    def test_top_long_short_position_ratio(self):
        lsa_eth = self.cg.top_long_short_position_ratio(ex="Binance", pair="ETHUSDT", interval="h4")
        self.assertEqual(lsa_eth.shape[0], 500)
        self.assertIn("longRatio", lsa_eth.columns)
        self.assertIn("shortRatio", lsa_eth.columns)
        self.assertIn("longShortRatio", lsa_eth.columns)

    def test_bitcoin_bubble_index(self):
        bbi = self.cg.bitcoin_bubble_index()
        self.assertIn("index", bbi.columns)

    def test_ahr999(self):
        ahr999 = self.cg.ahr999()
        self.assertIn("ahr999", ahr999.columns)

    def test_tow_year_ma_multiplier(self):
        tymm = self.cg.tow_year_ma_multiplier()
        self.assertIn("mA730Mu5", tymm.columns)
        self.assertIn("mA730", tymm.columns)

    def test_tow_hundred_week_moving_avg_heatmap(self):
        thwmah = self.cg.tow_hundred_week_moving_avg_heatmap()
        self.assertIn("mA1440", thwmah.columns)

    def test_puell_multiple(self):
        pm = self.cg.puell_multiple()
        self.assertIn("puellMultiple", pm.columns)

    def test_stock_flow(self):
        sf = self.cg.stock_flow()
        self.assertIn("stockFlow365dAverage", sf.columns)
        self.assertIn("nextHalving", sf.columns)

    def test_pi(self):
        pi = self.cg.pi()
        self.assertIn("ma350Mu2", pi.columns)
        self.assertIn("ma110", pi.columns)

    def test_golden_ratio_multiplier(self):
        grm = self.cg.golden_ratio_multiplier()
        self.assertIn("3LowBullHigh", grm.columns)
        self.assertIn("x8", grm.columns)
        self.assertIn("x21", grm.columns)

    def test_bitcoin_profitable_days(self):
        bpd = self.cg.bitcoin_profitable_days()
        self.assertIn("side", bpd.columns)

    def test_log_log_regression(self):
        llr = self.cg.log_log_regression()
        self.assertIn("Fib9098Dev", llr.columns)
        self.assertIn("Oscillator", llr.columns)
        self.assertIn("HighDev", llr.columns)

    def test_grayscale_market_history(self):
        gmh = self.cg.grayscale_market_history()
        self.assertIn("markerPriceList", gmh.columns)
        self.assertIn("premiumRateList", gmh.columns)
