

# https://forum.alpaca.markets/
# Name Fun
# uekoetter@gmail.com
# datagigly!>>:-)

# https://app.alpaca.markets/signup
# Name Fun
# uekoetter@gmail.com
# datagigly!>>:-)ng

import alpaca_trade_api as tradeapi

api = tradeapi.REST('<key_id>', '<secret_key>', base_url='https://paper-api.alpaca.markets')  # or use ENV Vars shown below
account = api.get_account()
api.list_positions()
