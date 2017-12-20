import requests
import json


url = 'https://bitaps.com/api/use/redeemcode/list'
parameters = {'redeemcode': 'BTCvRawDGR2NkKoiWB76FWytVCFfVrKiGmuSuqfHp9LQKSbN9Yz4s',
              "fee_level": "low",
              "payment_list": [{'amount': '7000', 'address': '18SUbhoaQqU3F2bvAgfLcUFxK1K7DZV6EJ'}, {'amount': '7000', 'address': '1AbkvC8vR9FtAubW1izEdbmewE5oQQctKk'}]}
response = requests.post(url, data=json.dumps(parameters))
print(response.text)
