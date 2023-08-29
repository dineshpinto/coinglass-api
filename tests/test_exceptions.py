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
