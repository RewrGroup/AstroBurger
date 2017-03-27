import requests
import json

url = 'https://bitaps.com/api/use/redeemcode/list'
parameters = {'redeemcode': 'BTCvRawDGR2NkKoiWB76FWytVCFfVrKiGmuSuqfHp9LQKSbN9Yz4s',
              "payment_list": [
                {'address': '1Bdmd7mqMNJzD4ydoQKfKm9q26WzmtHJB5', 'amount': '330000'},
                {'address': '19d43xNp6ZMfjgwkoQsMzn3aLSPhMC33hy', 'amount': "200000"}]}
response = requests.post(url, data=json.dumps(parameters))
print(response.text)


"""
# Esto para chequear cuanto tenemos

url = 'https://bitaps.com/api/get/redeemcode/info'
parameters = {'redeemcode': 'BTCvRawDGR2NkKoiWB76FWytVCFfVrKiGmuSuqfHp9LQKSbN9Yz4s'}
response = requests.post(url, data=json.dumps(parameters))
print(response.text)
"""