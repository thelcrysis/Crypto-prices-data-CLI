import requests,json,datetime
class Crypto:
    '''
    Class representing CryptoCurrency 
    '''
    currency_exchange_api_url = "https://free.currconv.com/api/v7/convert"
    usd_quote_exchange_rate = None
    api_key = None
    def __init__(self,base,quote,usd_quote_exchange_rate=None):

        self._base = base
        self._quote = quote
        if usd_quote_exchange_rate != None:
            Crypto.usd_quote_exchange_rate = usd_quote_exchange_rate
            
        #properties
        self.base_quote_exchange_history = []
        self.last_rate = None
        self.value_change = None
        self.percentage_change = None
        
        self.update()
    
    def get_base(self):
        return self._base.upper()
    
    def get_quote(self):
        return self._quote.upper()
    
    def get_base_quote_pair(self):
        return self._base.upper() + self._quote.upper()
     
    def fetch_base_usd_exchange(self):
        '''
            Get base to usd exchange rate
        '''
        while True:
            try:
                response = requests.get('https://www.bitstamp.net/api/v2/ticker/'+self._base.lower()+'usd/')
                base_usd_exchange_rate = float(json.loads(response.text)['last']) 
                break
            except:
                continue
        return base_usd_exchange_rate
    
    def fetch_usd_quote_exchange(self):
        '''
            Get usd/quote echange rate
        '''
        if Crypto.usd_quote_exchange_rate == None:
                currency_exchange_ratio = {'q':'USD_'+self._quote.upper(),'apiKey':Crypto.api_key}
                response = requests.get(
                    Crypto.currency_exchange_api_url,
                    params=currency_exchange_ratio
                )
                Crypto.usd_quote_exchange_rate = float(json.loads(response.text)['results']['USD_'+self._quote.upper()]['val'] )
    
    def fetch_base_quote_exchange(self):
        '''
            Get base/quote currency pair exhange rate
        '''
        self.load_api_key()
        base_usd_exchange_rate = self.fetch_base_usd_exchange()
        self.fetch_usd_quote_exchange()
        self.base_quote_exchange_rate = base_usd_exchange_rate * Crypto.usd_quote_exchange_rate
        
    def refresh_properties(self):
        '''
            Update all class properties.
        '''
        self.base_quote_exchange_history.append({'time':datetime.datetime.now().isoformat(),'rate':self.base_quote_exchange_rate})
        if len(self.base_quote_exchange_history) > 1:
            self.last_rate = self.base_quote_exchange_history[-2]['rate']
        if self.last_rate != None:
            self.value_change = self.base_quote_exchange_rate - self.last_rate
            self.percentage_change = self.value_change / self.last_rate
            
    def load_api_key(self):
        '''
            Load apiKey from headers.json
        '''
        if Crypto.api_key == None:
            with open('headers.json','r') as f:
                key = json.loads(f.read())
                Crypto.api_key = key['key']
    def update(self):
        '''
            Get new base/quote and refresh all cryptocurrency object properties.
        '''
        self.fetch_base_quote_exchange()
        self.refresh_properties()
