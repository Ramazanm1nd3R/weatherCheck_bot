import telebot
from telebot import types
import psycopg2
import logging
import os
import requests
import pytz
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_KEY = os.getenv('OPENWEATHER_API_KEY')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Подключение к базе данных
def create_connection():
    return psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

# Проверка и обновление пользователя в базе данных
def update_user_subscription(user_id, is_active):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
            if cursor.fetchone():
                cursor.execute('UPDATE users SET is_active = %s WHERE user_id = %s', (is_active, user_id))
            else:
                cursor.execute('INSERT INTO users (user_id, is_active) VALUES (%s, %s)', (user_id, is_active))
            conn.commit()

# Функция для получения погоды
def fetch_weather():
    url = f"http://api.openweathermap.org/data/2.5/forecast?q=Almaty&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        today = datetime.now().strftime('%Y-%m-%d')
        forecasts = [item for item in data['list'] if item['dt_txt'].startswith(today)]
        weather_info = "Погода на сегодня:\n"
        for forecast in forecasts:
            time = forecast['dt_txt'].split(' ')[1][:5]
            temp = forecast['main']['temp']
            description = forecast['weather'][0]['description']
            weather_info += f"{time} - Температура: {temp}°C, {description}\n"
        return weather_info
    else:
        return "Не удалось получить данные о погоде."

# Функция для отправки погоды только активным пользователям
def send_weather():
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT user_id FROM users WHERE is_active = TRUE')
            users = cursor.fetchall()
            weather_info = fetch_weather()
            for user in users:
                bot.send_message(user[0], weather_info)

# Настройка расписания для выполнения задачи отправки погоды в 8 утра по Алматы
almaty_tz = pytz.timezone('Asia/Almaty')
schedule.every().day.at("08:00").do(send_weather)  

# Запуск расписания
def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Команда start и обработка кнопок подписки и отписки
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Подписаться на рассылку', 'Отписаться', 'Получить погоду')
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Подписаться на рассылку', 'Отписаться', 'Получить погоду'])
def handle_subscription(message):
    if message.text == 'Подписаться на рассылку':
        update_user_subscription(message.chat.id, True)
        bot.send_message(message.chat.id, "Вы успешно подписались на рассылку!")
    elif message.text == 'Отписаться':
        update_user_subscription(message.chat.id, False)
        bot.send_message(message.chat.id, "Вы успешно отписались от рассылки.")
    elif message.text == 'Получить погоду':
        weather_info = fetch_weather()
        bot.send_message(message.chat.id, weather_info)

if __name__ == '__main__':
    import threading
    t = threading.Thread(target=schedule_checker)
    t.start()
    bot.polling(non_stop=True)
