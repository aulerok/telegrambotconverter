import telebot
import time
from extensions import ConvertionException, CriptoConverter
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['info'])
def handle_info(message):
    bot.send_message(message.chat.id, f"Это телеграм бот для конфертации валют.\n"
                                      f"Пришлите мне сообщение\n"
                                      f"'Название валюты которую надо перевести' 'валюту в которую переводим' "
                                      f"'количество'\n"
                                      f"Например  'доллар рубль 100'\n"
                                      f"доступные валюты можно увидеть по команде /value\n"
                                      f"чтобы еще раз увидеть это сообщение введите /info ")


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, f"Привет {message.chat.username} дружочек чем могу помогу\n"
                                      "Всегда можно увидеть инструкцию вызвав команду /info\n"
                                      f"введите команду /value для просмотра доступных валют")

    time.sleep(2)
    bot.send_message(message.chat.id, f"Это телеграм бот для конфертации валют.\n"
                                      f"Пришлите мне сообщение\n"
                                      f"'Название валюты которую надо перевести' 'валюту в которую переводим' "
                                      f"'количество'\n"
                                      f"Например  'доллар рубль 100'\n"
                                      f"доступные валюты можно увидеть по команде /value\n"
                                      f"чтобы еще раз увидеть это сообщение введите /info ")


@bot.message_handler(commands=['value'])
def value(message: telebot.types.Message):
    text = 'Доступные валюты на данный момент:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ConvertionException("Слишком много параметров")

        quote, base, amount, = values
        total_base = CriptoConverter.get_price(quote.lower(), base.lower(), amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя \n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду \n{e}")
    else:
        text = f"Цена {amount} {quote} в {base} = {total_base}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
