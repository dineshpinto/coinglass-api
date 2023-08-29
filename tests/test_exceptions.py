import os
from unittest import TestCase

from coinglass_api import CoinglassAPI, CoinglassRequestException, NoDataReturnedException, CoinglassParameterWarning


class TestExceptions(TestCase):
    def setUp(self) -> None:
        self.cg = CoinglassAPI(coinglass_secret=os.getenv("COINGLASS_SECRET"))

    def tearDown(self) -> None:
        self.cg._session.close()

    def test_coinglass_request_exception(self) -> None:
        with self.assertRaises(CoinglassRequestException):
            self.cg.open_interest_history(symbol="BTC", time_type="m1", currency="USD")
            self.cg.funding_usd_history(symbol="BTC", time_type="m1")
            self.cg.funding_coin_history(symbol="BTC", time_type="m1")

    def test_no_data_returned_exception(self) -> None:
        with self.assertRaises(NoDataReturnedException):
            self.cg.futures_market(symbol="ZEC")

    def test_warning_message(self) -> None:
        with self.assertWarns(CoinglassParameterWarning):
            with self.assertRaises(NoDataReturnedException):
                self.cg.futures_market(symbol="NotASymbol")

    def test_exchanges(self) -> None:
        exchanges = self.cg.get_exchanges()
        self.assertIn("Deribit", exchanges)
        self.assertIn("OKX", exchanges)
        self.assertIn("CME", exchanges)

        self.cg.add_exchange("TestExchange")
        exchanges = self.cg.get_exchanges()
        self.assertIn("TestExchange", exchanges)

    def test_symbols(self) -> None:
        symbols = self.cg.get_symbols()
        self.assertIn("ETH", symbols)
        self.assertIn("BTC", symbols)

        self.cg.add_symbol("TestSymbol")
        symbols = self.cg.get_symbols()
        self.assertIn("TestSymbol", symbols)

    def test_time_types(self) -> None:
        time_types = self.cg.get_time_types()
        self.assertIn("h1", time_types)
        self.assertIn("m1", time_types)

        self.cg.add_time_type("m100")
        time_types = self.cg.get_time_types()
        self.assertIn("m100", time_types)
