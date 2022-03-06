import telebot
from extensions import ConvertionException, CriptoConverter
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, f"Привет {message.chat.username} дружочек чем могу помогу\n"
                                      f"Всегда можно увидеть инструкцию вызвав команду /help\n"
                                      f"введите команду /value для просмотра доступных валют")


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
        total_base = CriptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя \n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду \n{e}")
    else:
        text = f"Цена {amount} {quote} в {base} = {total_base}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
