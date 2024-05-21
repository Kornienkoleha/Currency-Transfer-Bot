import telebot
from Config import TOKEN, keys
from Extensions import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

# Обрабатываются все сообщения, содержащие команды '/start' или '/help'.
@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Привет! Я бот, который переводит валюты.\n\
Для перевода введите команду в формате:\n\
<имя валюты> <в какую валюту хотите перевести> <количество первой валюты>\n\
Например: Доллар Рубль 100\n\
Увидеть список всех доступных валют: /values"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты для перевода:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException("Слишком много параметров.")

        quote, base, amount = values
        total_base = CurrencyConverter.convert(quote, base, amount)

    except ConvertionException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду.\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()

