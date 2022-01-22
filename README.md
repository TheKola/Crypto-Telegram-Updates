# Crypto_Telegram-Updates
This project focusses on creating a cryptocurrency screener which gives updates on telegram, 
which includes the name of the coins and the percentage change in the previous 5 minutes.

The Binance exchange has more than 900 cryptocurrencies. The program takes the prices of all the
cryptocurrencies listed on the Binance platform and stores this price data in a pandas data frame and calculates the

price change for every 5 minutes.

"bin_keys.py" provide the required binance api keys
Get your Binance Api keys at https://www.binance.com/en/my/settings/api-management

"telegram_keys.py" provide the required telegram token key and chat id
Create your own telegram bot using The Botfather, https://core.telegram.org/bots

"modules.py" contains all the modules used in the program
