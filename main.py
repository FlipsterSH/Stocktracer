import yfinance as yf #py -m pip install yfinance
from datetime import date


def update1():
    ticker_dict = {"AAPL": [], "GOOG": [], "MSFT": [], "^NDX": [], "SPY": [], "TSLA": [], "^VIX": []} #dictionary holding the tickers, and lists with closing prices

    for tck in ticker_dict: #this forloop fills up the ticker_dict with closing price data
        data = yf.download(tck, period="2y")
        ticker_dict[tck] = data['Close']

    ticker_json = {"AAPL": {"price": 0, "ma50": 0, "ma100": 0, "ma150": 0, "ma200": 0, "ath": 0, "change": 0},  #the json dictionary sent using ajax looks like this 
        "GOOG": {"price": 0, "ma50": 0, "ma100": 0, "ma150": 0, "ma200": 0, "ath": 0, "change": 0}, 
        "MSFT": {"price": 0, "ma50": 0, "ma100": 0, "ma150": 0, "ma200": 0, "ath": 0, "change": 0}, 
        "^NDX": {"price": 0, "ma50": 0, "ma100": 0, "ma150": 0, "ma200": 0, "ath": 0, "change": 0}, 
        "SPY": {"price": 0, "ma50": 0, "ma100": 0, "ma150": 0, "ma200": 0, "ath": 0, "change": 0}, 
        "TSLA": {"price": 0, "ma50": 0, "ma100": 0, "ma150": 0, "ma200": 0, "ath": 0, "change": 0},
        "^VIX": {"price": 0, "ma50": 0, "ma100": 0, "ma150": 0, "ma200": 0, "ath": 0, "change": 0}}

    avg = []
    for tck in ticker_json: #this forloop uses ticker_dict and functions below to fill up ticker_json with data
        for element in tck:
            ticker_json[tck]["price"] = round(ticker_dict[tck][-1], 3) 
            ticker_json[tck]["ma50"] = ma50(ticker_dict[tck])
            ticker_json[tck]["ma100"] = ma100(ticker_dict[tck])
            ticker_json[tck]["ma150"] = ma150(ticker_dict[tck])
            ticker_json[tck]["ma200"] = ma200(ticker_dict[tck])
            ticker_json[tck]["ath"] = ath(ticker_dict[tck])
            ticker_json[tck]["change"] = percent_numb(ticker_dict[tck][-2], ticker_dict[tck][-1])
        if tck == "^VIX":
            pass
        else:
            avg.append(ticker_json[tck]["change"])

    ticker_json["AVG"] = round(average(avg), 3) #calculates the average percent change of all the tickers
    ticker_json["MSG"] = message_creator(ticker_dict) #adds all messages to ticker_json
    ticker_json["graph"] = get_graph("SPY")
    
    return ticker_json


def message_creator(dict): #takes in dict containig ticker as key and a list of pricedata as value for the key, returns a list of multiple messages 
    messages = [] #list of messages displayed using v-for in vue
    for tck in dict:
        if tck == "^VIX": #må fjernes hvis stocks blir lagt til i lista etter VIX
            break
        movingaverages = {"ma50": ma50(dict[tck]), "ma100": ma100(dict[tck]), "ma200": ma200(dict[tck])}
        for ma in movingaverages:
            if movingaverages[ma] >= dict[tck][-1]:
                try:
                    prosent = (1 - (dict[tck][-1] / movingaverages[ma])) * -100
                    if  round(prosent) <= 3 and round(prosent) >= -3:
                        messages.append(f"{tck} er nå {round(prosent, 2)}% unna {ma}") #message appended if the price of the stock is within 3% from the movingaverage
                except:
                    pass
            else:
                try:
                    prosent = ((dict[tck][-1] / movingaverages[ma]) - 1) * 100
                    if round(prosent) <= 3 and round(prosent) >= -3:
                        messages.append(f"{tck} er nå {round(prosent, 2)}% unna {ma}")
                except:
                    pass

    messages.append("---")

    for tck in dict:
        if tck == "^VIX":
            break
        else:
            alltime = ath(dict[tck])
            now = dict[tck][-1]
            if alltime >= now:
                prosent = ((alltime / now) - 1) * 100
                messages.append(f"{tck} er {round(prosent, 2)}% unna ath")

    messages.append("---")
    status = market_status()
    for msg in status:
        messages.append(msg)

    messages.append("---")
    month_comparison = similar_months("SPY", 63) #63 --> 3months
    for msg in month_comparison:
        messages.append(msg)

    return messages #returns the list of messages
                

def get_graph(graph_id): #takes inn a ticker_symbol and returns a list with all the closing prices of this ticker last 2years
    prices = yf.download(graph_id, period="2y")["Close"]

    data = {"pricelist": [], "daylist": []}
    for price in prices:
        data["pricelist"].append(float(price))

    for day in range(1, len(data["pricelist"]) + 1, 1):
        data["daylist"].append(day)

    return data


def my_index(): #takes in nothing
    price_list = {"AAPL": [], "GOOG": [], "MSFT": [], "^NDX": [], "SPY": [], "TSLA": []} #dictionary holding the tickers, and lists with closing prices

    for tck in price_list: #this forloop fills up the ticker_dict with closing price data
        data = yf.download(tck, period="5y")["Close"]
        price_list[tck] = data['Close']

    index_value = 1000
    data = {"index": [], "daylist": []}

    for i in range(0, len(price_list["AAPL"]) - 1, 1):
        prosent_list = []
        for tck in price_list:
            prosent = percent_mult(price_list[tck][i], price_list[tck][i + 1])
            prosent_list.append(prosent)

        index_value *= average(prosent_list)
        data["index"].append(index_value)
        data["daylist"].append(i)

    return data #returns dictionary containing one list of index values and one list of days, formatted the same way as get_grapth() function


def market_status(): #takes inn a ticker_symbol and returns a list with all the closing prices of this ticker last 2years
    messages = []
    tickers = {"^NDX": [], "^VIX": [], "SPY": []}
    for tck in tickers:
        data = yf.download(tck, period="6mo")#2mo
        prices = data['Close']
        for price in prices:
            tickers[tck].append(price)

    ndx_status = compare_month(tickers["^NDX"])
    spy_status = compare_month(tickers["SPY"])
    vix_status = compare_month(tickers["^VIX"])

    statuses = {"NDX": ndx_status, "SPY": spy_status, "VIX": vix_status}

    for tck in statuses:
        if statuses[tck] == 1:
            messages.append(f"{tck} er opp siste 3mnd")
        else:
            messages.append(f"{tck} er ned siste 3mnd")

    if ndx_status + spy_status + vix_status >= 2:
        messages.append("Market is stable")
    else:
        messages.append("Market not stable")

    return messages


#21 dager er avg trading days
def similar_months(ticker_id, period): #how long the periods to compare are
    data = yf.download(ticker_id, period="30y")["Close"]

    monthlist = [] #when full, becomes a matrix where each row represents a period of closing price data
    month = []# month represents the period
    for i in range(len(data) - 1, 0, -1): #appends a list of prices in a small list size of a month to the monthlist
        if len(month) == period:
            monthlist.append(month)
            month = []

        month.append(float(data[i]))


    monthmovelist = [] #contains months in type list of monthmove
    monthmove = [] #list with data for a month, contains "G" or "R" means it is green or red candle
    for mnt in monthlist: #sets up monthmove list
        for i in range(0, len(mnt) - 1, 1):
            if mnt[i] > mnt[i + 1]:
                monthmove.append("G")
            else:
                monthmove.append("R")

        monthmovelist.append(monthmove)
        monthmove = []


    matchlist = []
    thismonth = monthmovelist[0]
    othermonths = monthmovelist[1:]
    for mnt in othermonths:
        match = 0 #keeps track of how many matches the months have with eachother, max score of 20
        for j in range(0, len(thismonth), 1):
            if thismonth[j] == mnt[j]:
                match += 1
        matchlist.append(match)


    highestmatchindexes = []
    highest = 0
    for i in range(0, len(matchlist), 1):
        if matchlist[i] == highest:
            highestmatchindexes.append(i)

        if matchlist[i] > highest:
            highest = matchlist[i]
            highestmatchindexes = [i]

    messages = [f"These dates have a {percent_match(period, highest)}% match with today:"]
    for numb in highestmatchindexes:
        messages.append(f"{get_date(period, numb)}")

    return messages


#----------Compound functions above----------

#----------Single functions below---------- 


def get_date(period, amount): #(how long a period is, and how many periods)
    months = period / 21
    amount_months = months * amount
    years = amount_months // 12
    amount_months -= years * 12

    today = date.today() #YYYY-MM-DD
    this_day = int(today.strftime("%d"))
    this_month = int(today.strftime("%m"))
    this_year = int(today.strftime("%Y"))

    if this_month > amount_months:
        this_month -= amount_months #kan bli null, må finne ut hva det skal bety
    else:
        amount_months -= this_month
        years += 1
        this_month = 11 - amount_months
        amount_months = this_month

    this_year -= int(years)

    return(f"{int(this_day)}.{int(this_month)}.{int(this_year)}") #returns a string of the end date


def percent_match(max, score):
    return round((score / max) * 100, 1)


def compare_month(liste): #return 1 is positive, return 0 is negative
    if len(liste) % 2 != 0:
        liste = liste[1:]
    middle = int(len(liste) / 2)
    avg_last = average(liste[0:middle]) #average of last month
    avg_now = average(liste[middle:]) #average of this month
    if avg_now >= avg_last:
        return 1 #returns 1 if this month is on average higher or equal to last, else return zero
    return 0


def ma50(liste): #takes in a list of data, same for all ma_functions
    counter = 0
    sum = 0

    for i in range(-1, -51, -1):
        sum += liste[i]
        counter += 1
    MA = round(sum / counter, 4)
    return float(MA) #returns the MA value of given datasett, same for all ma_functions functions


def ma100(liste):
    counter = 0
    sum = 0

    for i in range(-1, -101, -1):
        sum += liste[i]
        counter += 1
    MA = round(sum / counter, 4)
    return float(MA)


def ma150(liste):
    counter = 0
    sum = 0

    for i in range(-1, -151, -1):
        sum += liste[i]
        counter += 1
    MA = round(sum / counter, 4)
    return float(MA)


def ma200(liste):
    counter = 0
    sum = 0

    for i in range(-1, -201, -1):
        sum += liste[i]
        counter += 1
    MA = round(sum / counter, 4)
    return float(MA)


def ath(liste): #takes in a list of data
    ATH = 0

    for tall in liste:
        if float(tall) > float(ATH):
            ATH = float(tall)

    return round(float(ATH), 3) #Returns the highest datapoint ever recorded in the datasett


def percent_numb(last, now): #last is the price yesterday, now is the price today(most recent price)
    prosent = 0
    if last <= now:
        prosent = ((now / last) - 1) * 100

    if last > now:
        prosent = (1 - (now / last)) * -100

    return round(prosent, 3) #returns the percentage difference number


def percent_mult(last, now): #(percent_multiple) last is the price yesterday, now is the price today(most recent price)
    prosent = 0
    if last <= now:
        prosent = (now / last)

    if last > now:
        prosent = (now / last)

    return prosent #returns the percent multiplier


def average(liste): #tar inn en liste og returnerer gjennomsnittet av verdiene
    total = 0
    counter = 0
    for tall in liste:
        total += tall
        counter += 1

    return total / counter



if __name__ == "__main__":
    test = percent_numb(31415926.5, 31556926)
    print(test)
