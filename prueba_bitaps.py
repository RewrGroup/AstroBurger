import requests
import json
import binascii

url = 'https://bitaps.com/api/use/redeemcode/list'
parameters = {'redeemcode': 'BTCuoC8AGRbHjEss347c4KoQrdzqyJwDSdAxbjAoC4tyAbxTAhBuq',
              "payment_list": [
                {'amount': '3000', 'address': '39cjjxHTu7344mXExKb5SoDzbAoDWBpCj9'},  # Tal parece no importa cual key
                {'address': '1NtWuDrj5MSB1dioLKYX7oAy4S9XnDrWj7', 'amount': '40000'},  # vaya primero
                {'address': '1EctJ88N6xsVhiSQLYHTqd9amkW57SPwpx', 'amount': '50000'}]}
response = requests.post(url, data=json.dumps(parameters))
print(response.text)