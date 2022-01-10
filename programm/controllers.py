import json

import bs4
import requests
from flask import render_template


class GetRates:
    def get(self):
        resp = requests.get('https://timeweb.com/ru/community/articles/luchshie-servisy-dlya-skrapinga-dannyh')

        html  = bs4.BeautifulSoup(resp, features="html.parser")

        title = html.find('div', class_="cm-article__info d-if ai-c fl-n-ch cm-h5 mb-12")

        data = {'title': title.text}
        context = json.dumps(data)
        print(data)

        return render_template('templates/rate.html', co)