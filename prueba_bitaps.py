import requests
import json
import binascii

url = 'https://bitaps.com/api/use/redeemcode/list'
parameters = {'redeemcode': 'BTCvRawDGR2NkKoiWB76FWytVCFfVrKiGmuSuqfHp9LQKSbN9Yz4s',
              "payment_list": [
                {'amount': '10000', 'address': '1BK5kxMDRwxCNuP6XhmdtkH7hjh5TBhjad'},   # Tal parece no importa cual key
                {'address': '1Bdmd7mqMNJzD4ydoQKfKm9q26WzmtHJB5', 'amount': '330000'},
                {'address': '19d43xNp6ZMfjgwkoQsMzn3aLSPhMC33hy', 'amount': "200000"}]}  # Vaya primero
response = requests.post(url, data=json.dumps(parameters))
print(response.text)
