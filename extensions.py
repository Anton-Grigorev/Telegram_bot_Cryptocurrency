import requests
import json
from config import cryptocurrency

# Создаем собственный класс ошибок
class APIException(Exception):
    pass

# Создаем собственный класс с методом получения ответа по get-запросу к
# API сервиса Cryptocompare и проверка на ошибки пользователя
class CryptoConverter:
    @staticmethod
    def get_price(qoute: str, base: str, amount: str):

        # Проверяем на ошибки:
        # Сверяем на одинаковость валют
        if qoute == base:
            raise APIException(f'Одинаковые валюты - "{base}"\n'
                               f'Инструкция:  /help')

        # Проверка на правильность написания названия криптовалюты (ключа cryptocurrency из config.py)
        try:
            qoute_ticker = cryptocurrency[qoute]
        except KeyError:
            raise APIException(f'Неверное написание криптовалюты - "{qoute}"\n'
                               f'Отображение списка криптовалют: /values')

        try:
            base_ticker = cryptocurrency[base]
        except KeyError:
            raise APIException(f'Неверное написание криптовалюты - "{base}"\n'
                               f'Отображение списка криптовалют: /values')

        # Проверка написания количества - amount на соответствие его вещественному числу
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неверное написание количества - "{amount}"\n'
                               f'Инструкция:  /help')

        # Отправляем запрос по API сервиса Cryptocompare с вводом необходимых пользователю криптовалют +
        # проверка на правильность указания криптовалют в запросе
        respone = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={qoute_ticker}&tsyms={base_ticker}')

        # Конвертируем полученный ответ
        result = json.loads(respone.content)

        # Если возврат get-запроса - будет ошибкой
        if 'error' in result:
            raise APIException(result['error'])
        else:
            result = json.loads(respone.content)[cryptocurrency[base]] # Конвертируем полученный ответ в нужный нам

        # Возврат результата
        return result