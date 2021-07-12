import sqlite3
import telebot
import config


conn = sqlite3.connect("Bot.db")


bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler()
def start(message):
	if message.text == '/start':
		bot.send_message(message.from_user.id, "I started. Print /help for more information.")
	elif message.text == '/help':
		bot.send_message(message.from_user.id, """
												Print:\n
												/start - for start\n
												/help - for getting manual\n
												/about - about info\n
												/subtitle - authors info
												""")
	elif message.text == '/about':
		bot.send_message(message.from_user.id, "About info")
	elif message.text == '/subtitle':
		bot.send_message(message.from_user.id, "Authors info")
	else:
		bot.send_message(message.from_user.id, "I don`t understand. Print /help.")

bot.polling(none_stop = True)