# Crypto Screener 
This repository contains the source code for a real-time cryptocurrency screener that sends updates to Telegram. The program connects to the Binance exchange and fetches the prices of all the cryptocurrencies listed on the platform. The data is then stored in a pandas data frame, and the program calculates the percentage change of each cryptocurrency every 5 minutes. The updates are sent to a Telegram channel in real time.

The screener requires API keys from both Binance and Telegram to function properly. To obtain your Binance API keys, visit https://www.binance.com/en/my/settings/api-management. To create a Telegram bot, you can use BotFather by searching @BotFather on Telegram and following the instructions provided. More information on creating a Telegram bot can be found at https://core.telegram.org/bots.

The code consists of three main files:

"bin_keys.py", which includes the Binance API keys
"telegram_keys.py", which includes the Telegram token key and chat ID
"modules.py", which includes all the modules used in the program.
Please make sure to replace the placeholder values in "bin_keys.py" and "telegram_keys.py" with your API keys.

## Prerequisites
Before using this script, you need the following:
- Python 3.6 or higher
- `pip` for installing dependencies
- A Telegram bot token (obtainable through BotFather on Telegram)
- A Telegram channel ID where updates will be sent

## Installation
To get started with Crypto Telegram Updates, follow these steps:

Clone the repository:
```shell
git clone https://github.com/TheKola/Crypto-Telegram-Updates.git
cd Crypto-Telegram-Updates
```

Install the required dependencies:
```shell
pip install -r requirements.txt
```

## Configuration
1. Configure the script by editing the `telegram_keys.py` file with the generated `token_key` and `chatID_key`
2. Follow the same procedure to configure the `bin_keys.py` file with the obtained `p_key` and `s_key`

## Running the Script
Execute the script to start sending updates to your Telegram channel:
```shell
python main.py
```
