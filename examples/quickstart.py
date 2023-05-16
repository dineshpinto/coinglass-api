import os

from coinglass_api import CoinglassAPI

if __name__ == "__main__":
    cg = CoinglassAPI(coinglass_secret=os.getenv("COINGLASS_SECRET"))
    eth_funding_dydx = cg.funding(ex="dYdX", pair="ETH-USD", interval="h8")
    print(eth_funding_dydx.info())
    print(eth_funding_dydx.head())
    eth_funding_dydx.plot(y="fundingRate")
