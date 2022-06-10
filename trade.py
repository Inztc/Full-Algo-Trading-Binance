#from config import BINANCE_API_KEY , BINANCE_API_SECRET

#from binance.client import Client
#from binance.helpers import round_step_size

from config import BINANCE_FUTURE_API_KEY, BINANCE_FUTURE_API_SECRET
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from binance.helpers import round_step_size
from binance.client import Client


#Spot API
#client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

#Future API
future_client = RequestClient(api_key=BINANCE_FUTURE_API_KEY, secret_key=BINANCE_FUTURE_API_SECRET)


# myaccount_info = client.get_account()
# print(myaccount_info)

# balance = client.get_asset_balance(asset="USDT")
# print(balance["free"])

# if float(balance["free"]) < 15:
#     print("คุณมีจำนวนเงินไม่พอ")

# else:
#     print("จำนวนเงินมากพอสำหรับการซื้อขาย")

def CalculateAmount(AMOUNT_USDT, SYMBOL, LEVERAGE):
   

    result = future_client.get_mark_price(symbol=SYMBOL)
    current_price = float(result.markPrice)

    result = future_client.get_exchange_information()

    for i in result.symbols:
        if i.symbol == SYMBOL:
            print(i.__dict__)
            print("STEP SIZE : "+ i.filters[1]["stepSize"])
            STEP_SIZE = float(i.filters[1]["stepSize"])

            print("pricePrecision : "+ str(i.pricePrecision) )
            buy_amount = AMOUNT_USDT/current_price
            
            print(buy_amount)
            print(round_step_size(buy_amount, STEP_SIZE))

            return round_step_size(buy_amount, STEP_SIZE) 




# เปิด BUY AT MARKET Order !
def buy(symbol,amount_coin):
    # ราคาเหรียญตอนนี้ = client.get_avg_price(symbol="BTCUSDT")
    # ราคาเหรียญตอนนี้ = float(ราคาเหรียญตอนนี้["price"])
    # จำนวนที่ต้องการซื้อ = 20/ราคาเหรียญตอนนี้
    buy_amount = amount_coin
    symbol_info = client.get_symbol_info(symbol)
    stepSize = float(symbol_info["filters"][2]["stepSize"])
    buy_amount = round_step_size(buy_amount, stepSize)
    # print(จำนวนที่ต้องการซื้อ)

    order = client.order_market_buy(
        symbol=symbol,
        quantity=buy_amount)


 #==================================================
# sell At market
def sell(symbol,amount_coin):
    # balance = float(client.get_asset_balance(asset="BTC")["free"])
    # print(balance)
    sell_amount = amount_coin
    symbol_info = client.get_symbol_info(symbol)
    stepSize = float(symbol_info["filters"][2]["stepSize"])
    
    
    # จำนวนที่ต้องการขาย = round_step_size(จำนวนที่ต้องการขาย,stepSize) - stepSize # 0.00046 - 0.00001 => 0.00045
    """
    แก้ไข Function คำนวณจำนวนที่ต้องการขาย โดยลบออกด้วย stepsize ก่อน
    """
    sell_amount = round_step_size(sell_amount - stepSize ,stepSize) # 0.00046 - 0.00001 => 0.00045
    
    
    # print(จำนวนที่ต้องการขาย)
    order = client.order_market_sell(
        symbol=symbol,
        quantity=sell_amount)



 #===========================FUTURE ORDER=======================#

def get_position_amount_by_symbol(symbol):

    result = future_client.get_position_v2()
    for i in result:
        data = i.__dict__
        if data["symbol"] == symbol:
            print("total unit",data["positionAmt"])
            print("unrealized_profit",data["unrealizedProfit"])

            return str(abs(float(data["positionAmt"])))

def TPSL_LONG(symbol):
    TPSLOrder = future_client.post_order(symbol    = symbol,
                                      side          =  OrderSide.SELL,
                                      ordertype     = OrderType.MARKET,
                                      quantity      = get_position_amount_by_symbol(symbol),
                                      reduceOnly    = True #Make sure the order should be in one direction no both
                                      )

def TPSL_SHORT(symbol):
    TPSLOrder = future_client.post_order(symbol    = symbol,
                                      side      =  OrderSide.BUY,
                                      ordertype = OrderType.MARKET,
                                      quantity  = get_position_amount_by_symbol(symbol),
                                      reduceOnly= True #Make sure the order should be in one direction no both
                                      )


def OPEN_LONG(symbol, amount_usdt, leverage):
    
    #Calculate quantity
    quantity = CalculateAmount(AMOUNT_USDT = amount_usdt, SYMBOL = symbol, LEVERAGE = leverage)

    

    try:
    #if short position appears, close Short before Open Long Position
        TPSL_SHORT(symbol)

    except Exception as e:
        print(e)

#Leverage auto adjusted
    result = future_client.change_initial_leverage(symbol = symbol, leverage = leverage)

# OPEN LONG
    resultOrder = future_client.post_order(symbol      = symbol,
                                        side        =  OrderSide.BUY,
                                        ordertype   =  OrderType.MARKET,
                                        quantity    =  quantity
                                        )

    return


    

def OPEN_SHORT(symbol, amount_usdt, leverage):
     #Calculate quantity
    quantity = CalculateAmount(AMOUNT_USDT=amount_usdt, SYMBOL=symbol, LEVERAGE=leverage)

   


    try:
    #if long position appears, close long before Open Short Position
        TPSL_LONG(symbol)

    except Exception as e:
        print(e)

#Leverage auto adjusted
    result = future_client.change_initial_leverage(symbol=symbol, leverage=leverage)

#OPEN SHORT
    resultOrder = future_client.post_order(symbol      = symbol,
                                        side        =  OrderSide.SELL,
                                        ordertype   =  OrderType.MARKET,
                                        quantity    =  quantity
                                        )
    




#===========================FUTURE ORDER=======================#

if __name__ == "__main__":
     amount = 0.0004
     sym = "BTCUSDT"
    # # buy(symbol=sym,amount_coin=amount)
    # # sell(symbol=sym,amount_coin=amount)

    # result = CalculateAmount(1000, "BTCUSDT")
    # print(result)

    ############Test Prototype############################
    
    #Long
    #OPEN_LONG(symbol="DOGEUSDT", amount_usdt=5, leverage=50)

    #Exit long
    #TPSL_LONG(symbol="DOGEUSDT")

    #Short
    #OPEN_SHORT(symbol="DOGEUSDT", amount_usdt=5 , leverage=50)
    
    #Exit Short
    #TPSL_SHORT(symbol="DOGEUSDT)