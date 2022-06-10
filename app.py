from flask import Flask , request
from trade import OPEN_LONG, OPEN_SHORT, TPSL_LONG, TPSL_SHORT

app = Flask(__name__)

@app.route("/") # add path url
def hello_world():
    return "Hello, World!"

@app.route("/webhook")
def webhook():
    return "This is url for webhook!"

@app.route("/signals",methods=['POST'])
def signals():
    print("Someone Post Signals to me !")
    signal = request.data.decode("utf-8")
    import json
    signal = json.loads(signal) # เปลี่ยนจาก json ให้เป็น dictionary

    trade_side = signal["ACTION"]
    amount_coin = float(signal["AMOUNT_COIN"])
    leverage = int(signal["LEV"])
    symbol = signal["SYMBOL"]
    password = signal["PASSWORD"]
    if password != "123456789":
        print("Wrong Password")
        return "403"

    print("Signal Activated.....")
    print(trade_side)
    print(amount_coin)
    print(leverage)
    print(symbol)
    print("Sending Signal to Binance.....")

    message = f"🤖🤖🤖🤖🤖🤖🤖\n🤖Signal Received..... \n🤖Side {trade_side} {symbol}\n🤖Amount {amount_coin} \n🤖LEVERAGE {leverage}\n🤖🤖🤖🤖🤖🤖🤖"
    # Line notify Process
    from line_notify import LineNotify
    Access_Token = "ZAvBLcngbfpmowKEZTfxzN6XoQMSkdqKESGqqDxNPbm" # generate line notify
    notify = LineNotify(Access_Token)
    notify.send(message) # ส่งไปที่ห้องแชท

#======================================SPOT ORDER=========================================#
    from trade import buy , sell
    if trade_side == "OPEN LONG" and leverage == 0: # if leverage = 0 => trade spot
        buy(symbol=symbol,amount_coin=amount_coin) # ซื้อแบบ market
    
    elif trade_side == "TPSL LONG" and leverage == 0: # if leverage = 0 => trade spot
        sell(symbol=symbol,amount_coin=amount_coin) # ขายแบบ takeprofit stoploss

#=====================================FUTURE=============================================#
    #Receive USD Future Order : dollar for each trade
    AMOUNT_USDT = 1000  #USER SETTING
    

    #Open Long
    if trade_side == "OPEN LONG" and leverage > 0:
        OPEN_LONG(symbol=symbol, amount_usdt=AMOUNT_USDT , leverage=leverage)

    #TPSL Long
    elif trade_side == "TPSL LONG" and leverage > 0:
        TPSL_LONG(symbol=symbol)
    
    #Open Short
    elif trade_side == "OPEN SHORT" and leverage > 0:
        OPEN_SHORT(symbol=symbol, amount_usdt=AMOUNT_USDT, leverage=leverage)
        
    #TPSL Short
    elif trade_side == "TPSL SHORT" and leverage > 0:   
        TPSL_SHORT(symbol=symbol)

    return "200"

#========================================================================================#
if __name__=="__main__":
    app.run() # สั่งให้ app run !