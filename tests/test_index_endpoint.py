import os
from unittest import TestCase

from coinglass_api import CoinglassAPI


class TestIndexEndpoint(TestCase):
    def setUp(self) -> None:
        self.cg = CoinglassAPI(coinglass_secret=os.getenv("COINGLASS_SECRET"))

    def tearDown(self) -> None:
        self.cg._session.close()

    def test_bitcoin_bubble_index(self) -> None:
        bbi = self.cg.bitcoin_bubble_index()
        self.assertIn("index", bbi.columns)

    def test_ahr999(self) -> None:
        ahr999 = self.cg.ahr999()
        self.assertIn("ahr999", ahr999.columns)

    def test_tow_year_ma_multiplier(self) -> None:
        tymm = self.cg.tow_year_ma_multiplier()
        self.assertIn("mA730Mu5", tymm.columns)
        self.assertIn("mA730", tymm.columns)

    def test_tow_hundred_week_moving_avg_heatmap(self) -> None:
        thwmah = self.cg.tow_hundred_week_moving_avg_heatmap()
        self.assertIn("mA1440", thwmah.columns)

    def test_puell_multiple(self) -> None:
        pm = self.cg.puell_multiple()
        self.assertIn("puellMultiple", pm.columns)

    def test_stock_flow(self) -> None:
        sf = self.cg.stock_flow()
        self.assertIn("stockFlow365dAverage", sf.columns)
        self.assertIn("nextHalving", sf.columns)

    def test_pi(self) -> None:
        pi = self.cg.pi()
        self.assertIn("ma350Mu2", pi.columns)
        self.assertIn("ma110", pi.columns)

    def test_golden_ratio_multiplier(self) -> None:
        grm = self.cg.golden_ratio_multiplier()
        self.assertIn("3LowBullHigh", grm.columns)
        self.assertIn("x8", grm.columns)
        self.assertIn("x21", grm.columns)

    def test_bitcoin_profitable_days(self) -> None:
        bpd = self.cg.bitcoin_profitable_days()
        self.assertIn("side", bpd.columns)

    def test_log_log_regression(self) -> None:
        llr = self.cg.log_log_regression()
        self.assertIn("Fib9098Dev", llr.columns)
        self.assertIn("Oscillator", llr.columns)
        self.assertIn("HighDev", llr.columns)

    def test_grayscale_market_history(self) -> None:
        gmh = self.cg.grayscale_market_history()
        self.assertIn("markerPriceList", gmh.columns)
        self.assertIn("premiumRateList", gmh.columns)
