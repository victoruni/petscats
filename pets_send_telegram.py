# 
# 
# 
# 



import telebot
from telebot import types
from datetime import datetime, timedelta
from pathlib import Path

keyboard1 = [["","Камера 1","Камера 2","Камера 3","Камера 4","Не надо"],["","cam1","cam2","cam3","cam4","no"]]
bot = telebot.TeleBot('1785097804:AAHA_1l25xLvnNRsp-F48V0mSdVU7wIl10c');

@bot.message_handler(content_types=['text', 'document', 'audio'])
def get_text_messages(message):
	chatId=message.chat.id
	print(chatId)
	key_1=[0,0,0,0,0,0]
	ftime=datetime.now()
	print(ftime.day,"  ",ftime.hour)
	day=ftime.strftime("%d-%m-%Y")
	if message.text == "/help":
		bot.send_message(message.from_user.id, "Привет, здесь ты можешь посмотреть что делали мои котики за день 9-00 - 18-00. Набери /video")
	elif message.text == "/video":
		msg="здесь ты можешь посмотреть что делали мои котики за день 9-00 - 18-00 "+day
		bot.send_message(message.from_user.id, msg)
		keyboard = types.InlineKeyboardMarkup(); # клавиатура
		for i in range(1,6):
			#кнопка
			key_1[i] = types.InlineKeyboardButton(text=keyboard1[0][i], callback_data=keyboard1[1][i]);  
			#добавляем кнопку в клавиатуру
			keyboard.add(key_1[i]);   
		bot.send_message(message.from_user.id, "Выбери камеру", reply_markup=keyboard)   
	else:
		bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	ftime=datetime.now()
	day=ftime.strftime("%d-%m-%Y")

	if call.data.find("cam") < 0:
		bot.send_message(call.message.chat.id, 'No');		
	else:
		if ftime.hour >= 18:
			bot.send_message(call.message.chat.id, 'Видео с камеры '+call.data.replace("cam","")+'. Wait ....');
			videofile = Path(call.data+'-'+day+'.mp4')
			if videofile.is_file():
				video = open(call.data+'-'+day+'.mp4', 'rb')
				bot.send_video(call.message.chat.id, video)
				bot.send_message(call.message.chat.id, "Загружено")
			else:
				bot.send_message(call.message.chat.id, 'Видео отсутствует !!!');	
		else:
			bot.send_message(call.message.chat.id, 'Просмотр видео текущего дня только после 18:00, Просмотр за предыдущий день');
			ftime=datetime.now()- timedelta(days=1)
			dayold=ftime.strftime("%d-%m-%Y")
			videofile = Path(call.data+'-'+dayold+'.mp4')
			if videofile.is_file():
				video = open(call.data+'-'+dayold+'.mp4', 'rb')
				bot.send_video(call.message.chat.id, video)
				bot.send_message(call.message.chat.id, "Загружено")
			else:
				bot.send_message(call.message.chat.id, 'Видео отсутствует !!!');	
			

		
	#if call.data == "cam1": 
	#	bot.send_message(call.message.chat.id, 'Видео с камеры 1. Wait ....');
	#	video = open('cam1-'+day+'.mp4', 'rb')
	#	bot.send_video(call.message.chat.id, video)
	#	bot.send_message(call.message.chat.id, "Загружено")
	#elif call.data == "cam2":
	#	bot.send_message(call.message.chat.id, 'Видео с камеры 2. Wait ....');
	#	video = open('cam2-'+day+'.mp4', 'rb')
	#	bot.send_video(call.message.chat.id, video)
	#	bot.send_message(call.message.chat.id, "Загружено")
	#elif call.data == "cam3":
	#	bot.send_message(call.message.chat.id, 'Видео с камеры 3. Wait ....');
	#	video = open('cam3-'+day+'.mp4', 'rb')
	#	bot.send_video(call.message.chat.id, video)
	#	bot.send_message(call.message.chat.id, "Загружено")
	#elif call.data == "cam4":
	#	bot.send_message(call.message.chat.id, 'Видео с камеры 4. Wait ....');
	#	video = open('cam4-'+day+'.mp4', 'rb')
	#	bot.send_video(call.message.chat.id, video)
	#	bot.send_message(call.message.chat.id, "Загружено")
	#elif call.data == "no":
	#	bot.send_message(call.message.chat.id, 'No');


bot.polling(none_stop=True, interval=0)
