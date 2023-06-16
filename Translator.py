import logging
import requests
from pydantic import BaseModel
from models import Translation


class Translator:
    def __init__(self):
        self.text = None
        self.from_code = None
        self.to_code = None
        self.__providers = [
            self.__reverso,
        ]

    @staticmethod
    def get_codes():
        return []

    def translate(self, text, from_code='en', to_code='ru'):
        self.text = text
        self.from_code = from_code
        self.to_code = to_code
        if not (text, from_code, to_code):
            return
        for provider in self.__providers:
            x = provider()
            if type(x) == Translation:
                return x

    def __reverso(self):
        headers = {
            'authority': 'api.reverso.net',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://www.reverso.net',
            'pragma': 'no-cache',
            'referer': 'https://www.reverso.net/',
            'sec-ch-ua': '"Chromium";v="112", "YaBrowser";v="23", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.0.2285 Yowser/2.5 Safari/537.36',
            'x-reverso-origin': 'translation.web',
        }

        json_data = {
            'format': 'text',
            'from': 'zh',
            'to': 'rus',
            'input': self.text,
            'options': {
                'sentenceSplitter': True,
                'origin': 'translation.web',
                'contextResults': True,
                'languageDetection': True,
            },
        }

        response = requests.post('https://api.reverso.net/translate/v1/translation', headers=headers, json=json_data)
        if response.ok:
            data = response.json()
            from_code = str(data.get('from', ''))
            to_code = str(data.get('to', ''))
            translation = '\n'.join(data.get('translation', ''))
            return Translation(
                from_code=from_code,
                to_code=to_code,
                translation=translation
            )
        else:
            logging.error(f'{response}, {response.json()}')
