from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from binance.helpers import round_step_size
from trade import CalculateAmount

from config import BINANCE_FUTURE_API_KEY, BINANCE_FUTURE_API_SECRET

#connect client
request_client = RequestClient(api_key=BINANCE_FUTURE_API_KEY, secret_key=BINANCE_FUTURE_API_SECRET)

#check User account
#result = request_client.get_account_information()

# print(result.totalWalletBalance)
# print(result.totalUnrealizedProfit)
# print(result.totalMarginBalance)

# asset = result.__dict__["assets"][0]
# print(dir(asset))

# print("\n")
# result = request_client.get_open_interest(symbol="BTCUSDT")
# print(result)
# print("\n")

#gather asset data from exchange
# print("\n")
# result = request_client.get_exchange_information()
# PrintMix.print_data(result.symbols)
# print("\n")

#find base asset info
# for i in result.symbols:
#     print(i.baseAsset)



#find actual BTC Asset info and print from json format !
#function get
#calculate stepsize
#price precision

# SYMBOL = "BTCUSDT"
# AMOUNT_USDT = 100

# result = request_client.get_mark_price(symbol=SYMBOL)
# current_price = float(result.markPrice)

# result = request_client.get_exchange_information()

# for i in result.symbols:
#     if i.symbol == SYMBOL:
#         print(i.__dict__)
#         print("STEP_SIZE : "+ i.filters[1]["stepSize"])
#         STEP_SIZE = float(i.filters[1]["stepSize"])

#         print("pricePrecision : "+ str(i.pricePrecision) )
#         buy_amount = AMOUNT_USDT/current_price
        
#         print(buy_amount)
#         print(round_step_size(buy_amount, STEP_SIZE) )


###### Market Order Only ! #####################################################################

#Receive Signal from Tradingview
ORDER = "OPEN"
SIDE = "LONG"
AMOUNT_USDT = 49
LEVERAGE = 30
SYMBOL = "BTCBUSD"

#CALCULATE POSITION SIZE from BALANCE
#1. Get mark price (current_price)
result = request_client.get_mark_price(symbol="BTCBUSD")
print("======= Mark Price =======")
PrintBasic.print_obj(result)
#printonly mark price
#print(result.markPrice)
print("==========================")
#round up decimal point
quantity = CalculateAmount(AMOUNT_USDT= AMOUNT_USDT, SYMBOL=SYMBOL, LEVERAGE=LEVERAGE)


#2.Leverage auto adjusted
result = request_client.change_initial_leverage(symbol=SYMBOL, leverage=LEVERAGE)

# OPEN LONG
# resultOrder = request_client.post_order(symbol      = SYMBOL,
#                                         side        =  OrderSide.BUY,
#                                         ordertype   =  OrderType.MARKET,
#                                         quantity    =  quantity,
#                                         )

#CLOSE LONG (TP or SL)
#3. Before TP get position info before closing position

def get_position_amount_by_symbol(symbol):

    result = request_client.get_position_v2()
    for i in result:
        data = i.__dict__
        if data["symbol"] == symbol:
            print("total unit",data["positionAmt"])
            print("unrealized_profit",data["unrealizedProfit"])

            return str(abs(float(data["positionAmt"])))


# TPSLOrder = request_client.post_order(symbol    = SYMBOL,
#                                       side      =  OrderSide.SELL,
#                                       ordertype = OrderType.MARKET,
#                                       quantity  = get_position_amount_by_symbol(SYMBOL),
#                                       reduceOnly= True #Make sure the order should be in one direction no both
#                                       )

#OPEN SHORT
# resultOrder = request_client.post_order(symbol    = SYMBOL,
#                                       side        =  OrderSide.SELL,
#                                       ordertype   = OrderType.MARKET,
#                                       quantity    = quantity
#                                       )

#CLOSE SHORT
# TPSLOrder = request_client.post_order(symbol    = SYMBOL,
#                                       side      =  OrderSide.SELL,
#                                       ordertype = OrderType.MARKET,
#                                       quantity  = get_position_amount_by_symbol(SYMBOL),
#                                       reduceOnly= True #Make sure the order should be in one direction no both
#                                       )
