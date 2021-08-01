import pymysql
import telebot
from telebot import types
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


############################# REGISTRATION ##############################
def isregistrated(chat):
	cursor.execute("SELECT telegram_id FROM user")
	tg_id = cursor.fetchall()
	for e in tg_id:
		if e == (chat.id,):
			return True
	return False


def registration(chat):
	try:
		cursor.execute("SELECT * FROM user")
		user_id = len(cursor.fetchall()) + 1
		execute = "INSERT user (id, nickname, telegram_id, activation, created_date) VALUES ("+ str(user_id) + ", '" + chat.username + "', " + str(chat.id) + ", " + str(True) + ", '" + str(datetime.datetime.now())[:-7] +"')"
		cursor.execute(execute)
		connection.commit()
	except Exception as e:
		print(e)


##############################  PROFILE  ###################################
def user_info(chat):
	message = "Your info:\n"
	
	cursor.execute("SELECT id FROM user WHERE telegram_id = " + str(chat.id))
	users_id = cursor.fetchone()
	message += "id: " + str(users_id[0]) + "\n"


	cursor.execute("SELECT nickname FROM user WHERE telegram_id = " + str(chat.id))
	nickname = cursor.fetchone()
	message += "nickname: " + str(nickname[0]) + "\n"


	cursor.execute("SELECT telegram_id FROM user WHERE telegram_id = " + str(chat.id))
	telegram_id = cursor.fetchone()
	message += "telegram id: " + str(telegram_id[0]) + "\n"

	cursor.execute("SELECT phone_number FROM user WHERE telegram_id = " + str(chat.id))
	phone_number = cursor.fetchone()
	message += "phone number: " + str(phone_number[0]) + "\n"

	cursor.execute("SELECT type_of_user FROM user WHERE telegram_id = " + str(chat.id))
	type_of_user = cursor.fetchone()
	message += "type of user: " + str(type_of_user[0]) + "\n"

	cursor.execute("SELECT activation FROM user WHERE telegram_id = " + str(chat.id))
	activation = cursor.fetchone()
	message += "activation: " + str(activation[0]) + "\n"

	cursor.execute("SELECT created_date FROM user WHERE telegram_id = " + str(chat.id))
	created_date = cursor.fetchone()
	message += "created date: " + str(created_date[0]) + "\n"

	cursor.execute("SELECT changed_date FROM user WHERE telegram_id = " + str(chat.id))
	changed_date = cursor.fetchone()
	message += "changed date: " + str(changed_date[0])
	

	return message


########################  EDIT  ###############################
#nickname
def change_nickname(message):
	bot.send_message(message.chat.id, "Enter data:")
	bot.register_next_step_handler(message, get_nickname)

	
def get_nickname(message):
	new_nickname = message.text
	cursor.execute("UPDATE user SET nickname = '" + str(new_nickname) + "' WHERE telegram_id = " + str(message.chat.id))
	connection.commit()
	bot.send_message(message.chat.id, "Success!")


#phone number
def change_phone_number(message):
	bot.send_message(message.chat.id, "Enter data:")
	bot.register_next_step_handler(message, get_phone_number)

	
def get_phone_number(message):
	new_phone_number = message.text
	cursor.execute("UPDATE user SET phone_number = '" + str(new_phone_number) + "' WHERE telegram_id = " + str(message.chat.id))
	connection.commit()
	bot.send_message(message.chat.id, "Success!")



















































@bot.message_handler(commands = ['start'])
def start(message):
	#Menu
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("profile")
	markup.add(item1)


	#Registration
	print(isregistrated(message.chat))
	if isregistrated(message.chat):
		bot.send_message(message.from_user.id, "Hello my old friend!!", reply_markup=markup)
	else:
		registration(message.chat)
		bot.send_message(message.from_user.id, "Let`s register you.\nPrint /help for more information.", reply_markup=markup)
	

@bot.message_handler(content_types = ['text'])
def bot_message(message):
	if message.text == 'profile':

		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		
		item1 = types.KeyboardButton("edit")
		menu_back = types.KeyboardButton("back to menu")

		markup.add(item1, menu_back)

		bot.send_message(message.chat.id, user_info(message.chat), reply_markup=markup)



	elif message.text == 'back to menu':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		
		item1 = types.KeyboardButton("profile")
		
		markup.add(item1)

		bot.send_message(message.chat.id, "Menu", reply_markup=markup)


	elif message.text == 'edit':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		
		item1 = types.KeyboardButton("nickname")
		item2 = types.KeyboardButton("phone number")
		edit_back = types.KeyboardButton("back to profile")

		markup.add(item1, item2, edit_back)

		bot.send_message(message.chat.id, "Choose editing element", reply_markup=markup)



	elif message.text == 'nickname':
		try:
			change_nickname(message)
		except Exception as e:
			print(e)

	elif message.text == 'phone number':
		try:
			change_phone_number(message)
		except Exception as e:
			print(e)



	elif message.text == 'back to profile':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		
		item1 = types.KeyboardButton("edit")
		edit_back = types.KeyboardButton("back to menu")

		markup.add(item1, edit_back)

		bot.send_message(message.chat.id, user_info(message.chat), reply_markup=markup)


bot.polling(none_stop = True)


















