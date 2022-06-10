import requests
import json

url = 'http://127.0.0.1:5000/signals'
heroku_url = "https://eth-4h-atr-sm.herokuapp.com/signals" # webhook
ข้อมูลตัวอย่าง = {
            'ACTION': 'OPEN LONG',
            'AMOUNT_COIN' : '1000.00',
            'LEV' : '40',
            'SYMBOL' : 'ETHUSDT',
            'PASSWORD' : "123456789"
            }

ข้อมูลตัวอย่าง = json.dumps(ข้อมูลตัวอย่าง)

#x = requests.post(url, data = ข้อมูลตัวอย่าง)
x = requests.post(heroku_url, data = ข้อมูลตัวอย่าง)

print(x.text)