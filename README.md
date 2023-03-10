# Coinglass API
[![PyPi version](https://img.shields.io/pypi/v/coinglass-api)](https://pypi.python.org/pypi/coinglass-api/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100//)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110//)

## Unofficial Python client for Coinglass API

Wrapper around the [Coinglass API](https://coinglass.com/pricing) to fetch data about the crypto markets.
All data is output in pandas DataFrames (single or multi-index) and all time series data uses a DateTimeIndex.

**Note**: This is work in progress. Currently only supports the `indicator` API endpoint.

![Example Plot](https://github.com/dineshpinto/coinglass-api/blob/main/examples/example_plot.jpg?raw=true)

## Installation

```bash
pip install coinglass-api
```

### or with poetry 

```bash
poetry add coinglass-api
```

## Usage


```python
from coinglass_api import CoinglassAPI

cg = CoinglassAPI(api_key="abcd1234")

# Funding rate of ETH on dYdX
fr_btc_dydx = cg.funding(ex="dYdX", pair="ETH-USD", interval="h8")

# Get average funding for BTC
fr_avg_btc = cg.funding_average(symbol="BTC", interval="h4")

# Get funding OHLC for ETHUSDT on Binance
fr_ohlc_eth_binance = cg.funding_ohlc(ex="Binance", pair="ETHUSDT", interval="h4")

# Get aggregated OI OHLC data for BTC
oi_agg_eth = cg.open_interest_aggregated_ohlc(symbol="ETH", interval="h4")

# Get OHLC liquidations data for ETHUSDT on dYdX
liq_ohlc_eth_dydx = cg.liquidation_pair(ex="dYdX", pair="ETH-USD", interval="h4")

# Get liquidation data for BTC
liq_btc = cg.liquidation_symbol(symbol="BTC", interval="h4")

# Get long/short ratios for BTC
lsr_btc = cg.long_short_symbol(symbol="BTC", interval="h4")
```

## Examples

```
>>> cg.funding(ex="dYdX", pair="ETH-USD", interval="h8").head()
```

| <br/>time           | exchangeName<br/> | symbol<br/> | quoteCurrency<br/> | fundingRate<br/> |
|:--------------------|:------------------|:------------|:-------------------|:-----------------|
| 2022-08-22 08:00:00 | dYdX              | ETH         | USD                | -0.001151        |
| 2022-08-22 16:00:00 | dYdX              | ETH         | USD                | 0.001678         |
| 2022-08-23 00:00:00 | dYdX              | ETH         | USD                | 0.003743         |
| 2022-08-23 08:00:00 | dYdX              | ETH         | USD                | 0.003561         |
| 2022-08-23 16:00:00 | dYdX              | ETH         | USD                | 0.000658         |

```
>>> cg.funding(ex="dYdX", pair="ETH-USD", interval="h8").info()
```

```
<class 'pandas.core.frame.DataFrame'>
DatetimeIndex: 500 entries, 2022-08-22 08:00:00 to 2023-02-04 16:00:00
Data columns (total 4 columns):
 #   Column         Non-Null Count  Dtype  
---  ------         --------------  -----  
 0   exchangeName   500 non-null    object 
 1   symbol         500 non-null    object 
 2   quoteCurrency  500 non-null    object 
 3   fundingRate    500 non-null    float64
dtypes: float64(1), object(3)
memory usage: 19.5+ KB
```

```
>>> cg.funding(ex="dYdX", pair="ETH-USD", interval="h8").plot(y="fundingRate")
```
![funding_rate](https://github.com/dineshpinto/coinglass-api/blob/main/examples/funding_rate.jpg?raw=true)

## Disclaimer

This project is for educational purposes only. You should not construe any such information or other material as legal,
tax, investment, financial, or other advice. Nothing contained here constitutes a solicitation, recommendation,
endorsement, or offer by me or any third party service provider to buy or sell any securities or other financial
instruments in this or in any other jurisdiction in which such solicitation or offer would be unlawful under the
securities laws of such jurisdiction.

Under no circumstances will I be held responsible or liable in any way for any claims, damages, losses, expenses, costs,
or liabilities whatsoever, including, without limitation, any direct or indirect damages for loss of profits.