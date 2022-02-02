import telebot
from extensions import Converter, InputParser, ConversionException
from config import CODES
from SECRET import TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    bot.send_message(message.chat.id, f"Чтобы узнать цену валюты введите данные в следующем порядке через пробел:\n"
                                      f"(валюта цену которой хотите узнать) (валюта в которую хотите сконвертировать)"
                                      f"(опционально количество валюты)\n Чтобы узнать список доступных валют "
                                      f"используйте команду /values")


@bot.message_handler(commands=['values'])
def send_values(message):
    text = "доступные валюты:\n" + "\n".join(CODES.keys())
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        base, quote, base_code, quote_code, amount = InputParser.parse_conversion(message.text)
        result = Converter.get_price(base_code, quote_code, amount)
    except ConversionException as e:
        bot.reply_to(message, str(e))
    else:
        # убераем лишние .0 если количество целое
        if amount.is_integer():
            amount = int(amount)
        bot.send_message(message.chat.id, f"цена {amount} {base} в {quote}: {result}")


bot.polling(none_stop=True)
