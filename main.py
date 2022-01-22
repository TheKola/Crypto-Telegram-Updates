from modules import *

client = Client(bin_keys.p_key,bin_keys.s_key)

#Returns a list of information about each of the symbols available in the exchange
symbol_info = client.get_exchange_info()['symbols']

#Maps the symbols againsts the columns names
symbol_check = pd.DataFrame(columns=['symbol' ,'quoteAsset' ,'baseAsset','status'])

for dic in symbol_info:
    new_row = pd.Series({'symbol':dic['symbol'],'quoteAsset':dic['quoteAsset'],'baseAsset':dic['baseAsset'],'status':dic['status']})
    symbol_check = symbol_check.append(new_row , ignore_index=True)
symbol_check.set_index("symbol",inplace=True)

def quoteAsset_to_usdt_converter(symbol_check):
    
    #creating a list of all the quoteAsset
    quote_asset_list = list(symbol_check["quoteAsset"].unique())
    
    #Tries to get the quote assest price in terms of all other quote asset
    prices = client.get_all_tickers()#gets the current prices of all the symbols as dictionary
    prices_dict = dict(zip([i["symbol"] for i in prices],[i['price'] for i in prices]))
    conv_price_dict = {}
    
    for mainQuoteAsset in quote_asset_list:
        for quoteAsset in quote_asset_list:
            if quoteAsset + mainQuoteAsset in prices_dict.keys():
                 conv_price_dict[quoteAsset+mainQuoteAsset] = prices_dict[quoteAsset + mainQuoteAsset]

    final_conv = {}
    final_conv["USDT"] = 1
    for quoteAsset in [i for i in quote_asset_list if i != "USDT"]:
        temp_quoteAsset = quoteAsset
        i=0
        while i < len(list(conv_price_dict.items())):
            symbol,price = list(conv_price_dict.items())[i]
            if (temp_quoteAsset + "USDT") in conv_price_dict.keys():
                final_conv[quoteAsset] = final_conv.setdefault(quoteAsset,1) * float(conv_price_dict[temp_quoteAsset +"USDT"])
                break
            elif ("USDT" + temp_quoteAsset) in conv_price_dict.keys():
                final_conv[quoteAsset] = final_conv.setdefault(quoteAsset,1) / float(conv_price_dict["USDT" + temp_quoteAsset])
                break

            elif temp_quoteAsset == symbol[len(temp_quoteAsset):]:
                final_conv[quoteAsset] = final_conv.setdefault(quoteAsset,1) /float(price)
                temp_quoteAsset = symbol[:len(temp_quoteAsset)]
                i = 0
            elif temp_quoteAsset == symbol[:len(temp_quoteAsset)]:
                final_conv[quoteAsset] = final_conv.setdefault(quoteAsset,1) * float(price)
                temp_quoteAsset = symbol[len(temp_quoteAsset):]
                i = 0
            else:
                i += 1
    return final_conv

def volume_filter(symbol_check):
    filtered_top = []
    
    #Extracting the volume for symbols based on the top percentage changes 
    volume_threshold = 3000 #USDT/5mins
    
    #We take first 40 symbols from the sorted percentage change column
    for symbol in top.index[:40]:
        candles = client.get_klines(symbol=symbol, interval='5m' , limit = 1)
        volume_tracker[symbol] = candles[0][7]

    for key in volume_tracker.keys():
        quoteAsset = symbol_check.loc[key]["quoteAsset"]
        new_volume = float(volume_tracker[key]) * final_conv[quoteAsset]
        if new_volume > volume_threshold:
            filtered_top.append(key)
    return filtered_top

def telegram_bot_sendtext(bot_message):
    bot_token = telegram_keys.token_key
    bot_chatID = telegram_keys.chatID_key

    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    print(send_text)
    response = requests.get(send_text)
    return response.json()

#Getting the prices and volume for all the symbols continuously till interruption (click on 'i' key twice)
time_count = 0
volume_tracker = {}
final_top = {}
final_top_buffer = {}
final_conv = quoteAsset_to_usdt_converter(symbol_check)


while True:
    time.sleep(1)
    #Below function gets all the current prices of the symbols and stors in the variable price as a dictionary
    prices = client.get_all_tickers()
    
    #new_column_name takes in the current time and we initialize all the values in that column as NAN
    new_column_name = datetime.now()
    symbol_check[new_column_name] = np.nan
    
    #Adding prices to dataframe with timestamp as column name
    for price_dict in prices:
        symbol_check.loc[price_dict["symbol"],new_column_name] = float(price_dict["price"]) 
        
    #Finding price difference once the last column exceeds the specified time gap i.e 5 minutes with certain tolerance
    #The following if condition makes sure that 5 minutes have passed so that a 
    #minimum 5minute old column exists in the dataframe
    last_column = -1 
    first_column_with_prices = 3 #this is the starting column number with prices
    if (symbol_check.columns[last_column] - symbol_check.columns[first_column_with_prices]) > timedelta(minutes=5):
        now = symbol_check.columns[last_column]
        #setting the tolerance
        upper_limit = now - timedelta(minutes=4,seconds=57)
        lower_limit = now - timedelta(minutes=5,seconds=3)
        
        #Finding 5 min old column which is in between the upper and lower limit
        five_min_old_colname = [i for i in symbol_check.columns[first_column_with_prices:] if lower_limit < i < upper_limit]
        if five_min_old_colname == []:
            continue
        else:
            five_min_old_colname = five_min_old_colname[0]
        
        five_min_ago = symbol_check[five_min_old_colname]
        percentage_change_five_min = (((symbol_check.iloc[:,last_column] - five_min_ago)/five_min_ago)*100)
        
        #Sorts the symbols based on percentage change (Higher to lower )
        top = abs(percentage_change_five_min).sort_values( axis=0 , ascending=False )
        
        #This runs only if new coins are added which are not present in volume_tracker
        if [i for i in top.index[:40] if i not in volume_tracker.keys()] != []:
            #Extracting the volume for symbols based on the top percentage changes 
            filtered_top = volume_filter(symbol_check)
        
        for symbol in filtered_top:
            symbol_percentage_change = percentage_change_five_min[symbol]
            greater_than_threshold = 1.47329
            greater_than_percent = 3.0
            #If symbol has not been added  
            if ((symbol not in final_top_buffer.keys()) or (abs(symbol_percentage_change) > (greater_than_threshold * abs(final_top_buffer[symbol])))) and (abs(symbol_percentage_change) > greater_than_percent):
                bot_message = "{} , {}%".format(symbol,round(symbol_percentage_change,3))#stores the symbol and % change
                telegram_bot_sendtext(bot_message)
            final_top[symbol] = symbol_percentage_change

        #Below code runs once every 3600 secs 
        #It deletes the symbol is not present in the top 40 symbols list during the time this code runs
        #then that symbol is removed from final_top list
        if (time.time() - time_count) > 60*60:
            final_top_keys = list(final_top.keys())   
            for key in final_top_keys:
                if key not in top.index[:40]:
                    del final_top[key]
            time_count = time.time()
            
        #Save a copy of the current final_top so that it can be checked in the next 
        #iteration so as to not send duplicate signals
        final_top_buffer = final_top
        #Dropping the  first column everytime it takes the price difference
        symbol_check.drop(columns=symbol_check.columns[first_column_with_prices]) 