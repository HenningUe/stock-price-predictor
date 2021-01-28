
from datetime import datetime

from iexfinance.stocks import get_historical_intraday


def fetch_stock_data(symbol, date):
    # https://iexcloud.io/docs/api/

    # Name Pedschka Jadenhnos
    # uekoetter@gmail.com
    # datatransfer%>>f

    # account nr
    # 6366e88f7e386bbf650f11b563f1158a

    # secret token
    # sk_dd8b2fa992f944aa9343c1858c02ae35

    # pushishable
    # pk_90ab76bf8da546989bb1516e15e7084a

    token = "sk_dd8b2fa992f944aa9343c1858c02ae35"
    # token = "pk_90ab76bf8da546989bb1516e15e7084a"

    # from iexfinance.refdata import get_symbols
    # smys = get_symbols(output_format='pandas', token=token)
    # print(smys)

    # New York Stock Exchange (NYS)
    # NASDAQ (NAS)*
    # NYSE Arca (PSE)
    # Cboe BZX US Equities Exchange (BATS)
    # NYSE American (ASE)

    start = end = datetime.fromordinal(date.toordinal())
    val = get_historical_intraday(symbol, start=start, end=end, token=token, output_format='json')
    return val

    # Data Weighting
    # Adjusted + Unadjusted
    # 10 per symbol per time interval returned (Excluding 1d)
    # Example: If you query for AAPL 5 day, it will return 5 days of prices for AAPL for a total of 50.
    # Adjusted close only
    # 2 per symbol per time interval returned (Excluding 1d)
    # use chartCloseOnly param
    # NOTE: For minute-bar historical prices when a specific date is used in the range parameter, the weight
    #       is 50 messages
    # Example: If you query for AAPL minute-bar for 20190610, it will return 390 minutes of data at a cost of
    #          50 messages.
