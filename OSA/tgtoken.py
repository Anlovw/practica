
bot_token = ('6110324452:AAFLAQsjgQ3NqvxsJO83QLpCz1A0QZwJFrQ');
my_id = 669525450



import telebot
def send_message_to_tg_user(user_id: int, text: str):
    bot = telebot.TeleBot(bot_token)
    bot.send_message(user_id, text)

    #send_message(669525450, 'Hell')

