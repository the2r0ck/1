import datetime
import pymysql
import telebot
from config import TOKEN, user, password, db_name, host


try:
	connection = pymysql.connect(
			host = host,
			user = user,
			database = db_name,
			password = password
		)
	print("Successfuly connected...")

except Exception as e:
	print("Connection refused...")
	print(e)

cursor = connection.cursor()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler()
def start(message):
	nnickname = ''
	pphone_number = ''
	if message.text == '/start':
		print(isregistrated())
		if isregistrated():
			bot.send_message(message.from_user.id, "Hello my old friend!!")
		else:
			bot.send_message(message.from_user.id, "Let`s register you.\nPrint /help for more information.")
			bot.send_message(message.from_user.id, "Enter your nickname:")
			bot.register_next_step_handler(message, get_nickname)
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

def isregistrated():
	cursor.execute("SELECT telegram_id FROM user")
	tg_id = cursor.fetchall()
	for e in tg_id:
		if e == (1037555181,):
			return True
	return False


def get_nickname(message):
	global nnickname
	nnickname = message.text;
	bot.send_message(message.from_user.id, "Enter your phone number:")
	bot.register_next_step_handler(message, get_phone_number)

def get_phone_number(message):
	global pphone_number
	pphone_number = message.text
	bot.send_message(message.from_user.id, "You are registrated!")
	print(registration(message, nnickname, pphone_number))

def registration(message, nnickname, pphone_number):
	try:
		cursor.execute("SELECT * FROM user")
		user_id = len(cursor.fetchall()) + 1
		execute = "INSERT user (id, nickname, telegram_id, phone_number, activation, created_date, changed_date) VALUES ("+ str(user_id) + ", '" + nnickname + "', " + str(message.from_user.id) + ", '" + pphone_number + "', " + str(True) + ", '" + str(datetime.datetime.now())[:-7] + "', '" + str(datetime.datetime.now())[:-7] +"')"
		cursor.execute(execute)
		connection.commit()
	except Exception as e:
		print(e)

bot.polling(none_stop = True)