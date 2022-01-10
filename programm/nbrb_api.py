import json
from programm.api import _Api

class Api(_Api):
    def __init__(self):
        super().__init__("NBRB_API")

    def _update_rate(self, xrate):
        rate = self._get_rate_nbrb(xrate.from_currency)
        return rate

    def _get_rate_nbrb(self, from_currency):
        response = self._send_request(url='https://www.nbrb.by/api/exrates/rates?periodicity=0', method='get')
        response_json = json.loads(response.text)
        self.log.debug('Api_CBR response: %s' % response_json)
        rate = self._get_rate(response_json, from_currency)
        print(rate)
        return rate

    def _get_rate(self, response_data, from_currency):
        nbrb_aliases_map = {840: "USD", 975: "BYN"}
        if from_currency not in nbrb_aliases_map:
            raise ValueError(f"Invalid from_currency: {from_currency}")
        if from_currency not in nbrb_aliases_map:
            raise ValueError(f"Invalid currency: {from_currency} not found")
        currency_alias = nbrb_aliases_map[from_currency]
        for e in response_data:
            if e["Cur_Abbreviation"] == currency_alias:
                return float(e["Cur_OfficialRate"])

        raise ValueError(f"Invalid Privat response: {currency_alias} not found")

