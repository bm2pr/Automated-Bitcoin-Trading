import json, hmac, hashlib, time, requests, base64, sys
from requests.auth import AuthBase
 
# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
 
    def __call__(self, request):
        timestamp = str(time.time())
        #message = timestamp + request.method + request.path_url + (request.body or '')
        message = timestamp + request.method
        message = message + request.path_url
        weirdOrThing = (request.body or b'').decode('utf-8')
        message = message + weirdOrThing
 
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, bytes(message, 'utf-8'), hashlib.sha256)
        byteObject = signature.digest()
        #signature_b64 = byteObject.encode('base64').rstrip('\n')
        
        signature_b64 = base64.b64encode(byteObject).decode("utf-8")
        signature_b64.rstrip("\n")
        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request
 
class Account:
    def __init__(self, account_file_location):
        with open(account_file_location) as json_file:
            account = json.load(json_file)
            API_KEY = account['API_KEY']
            API_SECRET = account['API_SECRET']
            API_PASS = account['API_PASS']
            self.api_url = 'https://api.pro.coinbase.com/'
            self.auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)
 
    def retrieve_account(self):
        r = requests.get(self.api_url + 'accounts', auth=self.auth)
        return r.json()
    
 
    
    # 4 = BTC, 20 = USD
    def sell(self):
        account_json = self.retrieve_account()
        
        current_BTC = account_json[4]['available']
        order = {
                'product_id':'BTC-USD',
                'side' : 'sell',
                'type' : 'market',
                'size' : float(current_BTC),
                 }
        r = requests.post(self.api_url + 'orders', json=order, auth=self.auth)
        json_formatted_str = json.dumps(r.json(), indent=2)
        print(json_formatted_str)  
        
    def buy(self):
        
        account_json = self.retrieve_account()
        print(account_json[21]['balance'])
        order = {
        'funds': float(account_json[21]['balance']),
        'side': 'buy',
        'type': 'market',
        'product_id': 'BTC-USD',
        }
        r = requests.post(self.api_url + 'orders', json=order, auth=self.auth)
        json_formatted_str = json.dumps(r.json(), indent=2)
 
        print(json_formatted_str)
 
 
 
 
 
 
 
'''
 
my_account = Account(sys.argv[1])
output_file = open('Account.txt', 'w')
output_file.write(json.dumps(my_account.retrieve_account(), indent=2))
'''