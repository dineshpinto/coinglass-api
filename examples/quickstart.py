import os

from coinglass_api import CoinglassAPI

if __name__ == "__main__":
    api_key = os.getenv("COINGLASS_API_KEY")
    cg = CoinglassAPI(api_key=api_key)
    df = cg.funding_average(symbol="BTC", interval="h4")
    print(df)
