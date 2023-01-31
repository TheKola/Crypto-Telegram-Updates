# Crypto Screener 
This repository contains the source code for a real-time cryptocurrency screener that sends updates to Telegram. The program connects to the Binance exchange and fetches the prices of all the cryptocurrencies listed on the platform. The data is then stored in a pandas data frame, and the program calculates the percentage change of each cryptocurrency every 5 minutes. The updates are sent to a Telegram channel in real-time.

The screener requires API keys from both Binance and Telegram to function properly. To obtain your Binance API keys, visit https://www.binance.com/en/my/settings/api-management. To create a Telegram bot, you can use the BotFather by searching @BotFather on Telegram and following the instructions provided. More information on creating a Telegram bot can be found at https://core.telegram.org/bots.

The code consists of three main files:

"bin_keys.py", which includes the Binance API keys
"telegram_keys.py", which includes the Telegram token key and chat ID
"modules.py", which includes all the modules used in the program.
Please make sure to replace the placeholder values in "bin_keys.py" and "telegram_keys.py" with your own API keys.

It is important to note that this project requires a good understanding of Python and its libraries, specifically Pandas, to run and modify the code. If you encounter any issues or have questions, feel free to reach out to the repository's maintainer for assistance.
