import requests
import json
import time
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


def Session():
    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


class Api_GXP:
    def __init__(self):
        self.url = "http://api.sctg.xyz"

        # Здесь надо указать ваш APIKEY с https://t.me/Xevil_check_bot
        # Сервис так же поддерживает передачу дополнительных параметров в apikey
        # |offfast - отключит быстрое решение recaptcha (некоторые сайты не принимают токены полученые таким способом)
        # |onlyxevil - запрещает сервису решать recaptcha через любые другие сервисы, кроме Xevil, другие сервисы обычно дороже Xevil, так же некоторые сайты не принимают токен не с Xevil
        # Пример приминения этих параметров:
        # APIKEY|onlyxevil
        # APIKEY|offfast
        # Так же можно одновременно:
        # APIKEY|onlyxevil|offfast
        self.key = "APIKEY"
        self.max_wait = 300
        self.sleep = 5

    def in_api(self, data):
        session = Session()
        params = {"key": (None, self.key)}
        for key in data:
            params[key] = (None, data[key])
        return session.post(self.url + '/in.php', files=params, verify=False, timeout=15)

    def res_api(self, api_id):
        session = Session()
        params = {"key": self.key, "id": api_id}
        return session.get(self.url + '/res.php', params=params, verify=False, timeout=15)

    def get_balance(self):
        session = Session()
        params = {"key": self.key, "action": "getbalance"}
        return session.get(self.url + '/res.php', params=params, verify=False, timeout=15).text

    def run(self, data):

        get_in = self.in_api(data)
        if get_in:
            if "|" in get_in.text:
                api_id = get_in.text.split("|")[1]
            else:
                return get_in.text
        else:
            return "ERROR_CAPTCHA_UNSOLVABLE"
        for i in range(self.max_wait // self.sleep):
            time.sleep(self.sleep)
            get_res = self.res_api(api_id)
            if get_res:
                answer = get_res.text
                if 'CAPCHA_NOT_READY' in answer:
                    continue
                elif "|" in answer:
                    return answer.split("|")[1]
                else:
                    return answer


api = Api_GXP()

# То как выглядят все эти виды капчи, вы можете посмотреть здесь: https://sctg.readme.io/reference/startuseservice

# Check Balance
# Вернет баланс в рублях
balance = api.get_balance()
print("Balance key: ", balance)
# 55.176
# reCaptcha
# Получает токен рекапчи
# Для нахождения параметров и callback функции советую использовать этот код, его надо вводить в консоль браузера: https://gist.github.com/2captcha/2ee70fa1130e756e1693a5d4be4d8c70
# После чего при вводе этих строк вы увидите список всех reCaptcha на странице, их параметры и callback функции, если есть
# let res = findRecaptchaClients()
# console.log(res)
# Для вызова callback можно попытатся использовать этот код: https://community.bablosoft.com/topic/23356/%D0%BA%D0%B0%D0%BA-%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D0%BD%D0%B8%D1%82%D1%8C-%D1%82%D0%BE%D0%BA%D0%B5%D0%BD-%D1%80%D0%B5%D0%BA%D0%B0%D0%BF%D1%87%D0%B8
#
# Обязательные параметры
# "sitekey": str - Значение параметра sitekey, которое вы нашли в коде сайта, обычно оно не меняется, и его достаточно найти один раз
# "pageurl": str - Полный URL страницы, на которой вы решаете reCAPTCHA V2 (На некоторых сайтах рекапча находится во iframe в таком случае надо давать url этого iframe)
#
# Можно так же передать другие параметры reCaptcha для решения:
# "invisible": 1 - сообщает Xevil что на сайте невидимая рекапча (капча которая появляется только после нажатия на какуюто кнопку, и сразу в открытом виде)
# "data-s": str - Значение параметра data-s найденное на странице. Актуально для поиска в Google и других сервисов Google
# "cookies": str - Ваши cookies которые будут использованы Xevil для решения капчи. Формат: КЛЮЧ:Значение, разделитель - точка с запятой, например: KEY1:Value1;KEY2:Value2;
# "userAgent": str - Подставляем Xevil ваш userAgent
# "proxy": str - Формат: логин:пароль@123.123.123.123:3128
# "proxytype": str - Тип вашего прокси-сервера: HTTP, HTTPS, SOCKS4, SOCKS5
# "version": "v3" - указывает на то, что это reCAPTCHA V3
# "enterprise": 1 -  указывает на то, что это reCAPTCHA Enterpise
data = {"method": "userrecaptcha", "pageurl": "https://2captcha.com/demo/recaptcha-v2",
        "sitekey": "6LfD3PIbAAAAAJs_eEHvoOl75_83eXSqpPSRFJ_u"}
reCaptcha = api.run(data)
print('reCaptcha: ', reCaptcha[:20])
# 03AFcWeA5WYnymLllnbn