import json

from api import _Api

class Api(_Api):
    def __init__(self):
        super().__init__("Cryptonator")

    def _update_rate(self, xrate):
        rate = self._get_rate_cryptonator(xrate.from_currency, xrate.to_currency)
        return rate

    def _get_rate_cryptonator(self, from_currency, to_currency):
        aliases_map = {1000: 'btc', 900: "uah", 643:"rub"}
        if from_currency not in aliases_map:
            raise ValueError

        if to_currency not in aliases_map:
            raise ValueError
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
            "Upgrade-Insecure-Requests": "1", "DNT": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}

        url_end = f'{aliases_map[from_currency]}-{aliases_map[to_currency]}'
        print(url_end)
        url = f'https://api.cryptonator.com/api/ticker/{url_end}'
        response = self._send_request(url=url, method='get', headers=headers)
        response_json = json.loads(response.text)
        self.log.debug('Cryptonator response: %s' % response_json)
        rate = self._find_rate(response_json)
        print(rate)
        return rate

    def _find_rate(self, response_data):
        if 'ticker' not in response_data:
            raise ValueError
        if 'price' not in response_data['ticker']:
            raise ValueError
        return float(response_data['ticker']['price'])

