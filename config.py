import os


BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
LINE_NOTIFY_API = os.getenv("LINE_NOTIFY_API")
BINANCE_FUTURE_API_KEY = os.getenv("BINANCE_FUTURE_API_KEY")
BINANCE_FUTURE_API_SECRET = os.getenv("BINANCE_FUTURE_API_SECRET")


# BINANCE_FUTURE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# BINANCE_FUTURE_API_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# BINANCE_API_KEY = "xxxxxxxxxxxxxxxx"
# BINANCE_API_SECRET = "xxxxxxxxxxxxxxxx"
# LINE_NOTIFY_API = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# แก้ไขเวลา Deploy ขึ้น heroku ใช้ ENV variable เพื่อปกป้อง api key
# heroku config:set BINANCE_API_KEY=xxx
# heroku config:set BINANCE_API_SECRET=xxx
# heroku config:set LINE_NOTIFY_API=xxx
# heroku config:set BINANCE_FUTURE_API_KEY=xxx
# heroku config:set BINANCE_FUTURE_API_SECRET=xxx


# git add .
# git commit -m "add"
# git push heroku master
