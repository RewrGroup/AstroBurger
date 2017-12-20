import requests
import json


# Esto para chequear cuanto tenemos

url = 'https://bitaps.com/api/get/redeemcode/info'
parameters = {'redeemcode': 'BTCvRawDGR2NkKoiWB76FWytVCFfVrKiGmuSuqfHp9LQKSbN9Yz4s'}
response = requests.post(url, data=json.dumps(parameters))
print(response.text)

