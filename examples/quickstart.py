from coinglass_api import CoinglassAPI
import os

if __name__ == "__main__":
    api_key = os.getenv("COINGLASS_API_KEY")
    cg = CoinglassAPI(api_key=api_key)
    df = cg.average_funding(symbol="BTC", interval="h4")
    print(df)
