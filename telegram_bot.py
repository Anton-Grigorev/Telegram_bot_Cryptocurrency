# Создание Телеграмбота для получения цены нужного количества криптовалюты
import telebot
from config import cryptocurrency, TOKEN
from extensions import APIException, CryptoConverter

#Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])            # Начальное обращение к боту и помощь
def start_help(message):
    instruction = (f"Для работы бота вводим через пробел:\n"
            f"<имя валюты, цену которой надо узнать>"
            f"<имя валюты, в которой надо узнать цену первой валюты>"
            f"<количество первой валюты>\n"
            f"Пример: биткоин рубль 1\n"
            f"Отображение списка криптовалют: /values")
    bot.reply_to(message, instruction)


@bot.message_handler(commands=['values'])                   # Перечисление возможных криптовалют
def show_cryptocurrency(message):
    text = 'Доступные криптовалюты/валюты:'
    for key in cryptocurrency.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert_work(message):
    try:
        user_message = message.text.lower().split(" ")  # Создаем список из запроса пользователя, внося нижний регистр

        # Проверяем на ошибки:
        # ошибка соответствия количества параметров, введеных пользователем
        if len(user_message) != 3:
            raise APIException(f'Неверное количество параметров\n'
                               f'Инструкция:  /help')

        qoute, base, amount = user_message  # Присваиваем переменные элементам списка для дальнейшего использования

        total = CryptoConverter.get_price(qoute, base, amount)      # Получаем после проверки ответ API из extensions.py

    except APIException as e:               # Показ ошибки пользователя в чат
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')

    except Exception as e:                  # Показ ошибки системы в чат
        bot.reply_to(message, f'Ошибка в обработке:\n{e}')

    else:
        # Если все проходит без ошибок, то
        # создаем удобочитаемый текст-ответ и расчет заданного количества валюты
        text = f'Цена {amount} {qoute} в {base} = {total * float(amount)}'

        # Ответ бота в чат
        bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling(none_stop=True)             # Запуск