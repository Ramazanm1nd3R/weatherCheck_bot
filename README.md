# WeatherBot

WeatherBot - это Telegram бот на Python, предоставляющий погодные уведомления. Бот использует API OpenWeatherMap для получения данных о погоде и `telebot` для взаимодействия с Telegram API.

## Функциональность

Бот позволяет пользователям:
- Подписаться на ежедневные уведомления о погоде.
- Получить текущий прогноз погоды по запросу.
- Отписаться от уведомлений.

## Технологии

- Python 3.8+
- PostgreSQL
- Telebot
- Requests
- APScheduler (для планирования задач)

## Настройка проекта

1. Клонируйте репозиторий:
git clone https://github.com/Ramazanm1nd3R/weatherCheck_bot.git

markdown
Copy code
2. Установите зависимости:
pip install -r requirements.txt

markdown
Copy code
3. Создайте файл `.env` в корневой директории проекта и добавьте необходимые переменные окружения:
TELEGRAM_BOT_TOKEN=your_telegram_bot_token OPENWEATHER_API_KEY=your_openweather_api_key DB_NAME=your_database_name DB_USER=your_database_user DB_PASSWORD=your_database_password DB_HOST=your_database_host

markdown
Copy code
4. Запустите бота:
python bot.py

shell
Copy code

## Вклад в проект

Вклады в проект приветствуются. Перед тем как отправить Pull Request, убедитесь, что ваш код соответствует стандартам проекта и протестирован.

## Лицензия

Укажите здесь информацию о лицензии вашего проекта.
Этот README.md предоставляет базовую информацию о том, как начать работу с ботом, и о том, какие технологии используются в проекте. Вы можете расширить этот документ, добавив более подробную информацию о конфигурации, использовании и разработке.