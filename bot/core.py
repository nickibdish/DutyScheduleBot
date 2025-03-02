import telebot
import logging
from .handlers import register_handlers  # Функция для регистрации обработчиков команд
import os

# Настройка логирования (опционально)
logging.basicConfig(level=logging.INFO)

# Ваш API-токен бота. Обычно его удобно хранить в переменной окружения или конфиге.
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Создаем объект бота TeleBot
bot = telebot.TeleBot(BOT_TOKEN)

def run_bot():
    """
    Инициализирует и запускает бота, используя TeleBot.
    """
    # Регистрируем обработчики команд и сообщений
    register_handlers(bot)
    
    # Запускаем опрос (polling). none_stop=True означает, что бот будет работать без остановок.
    bot.polling(none_stop=True)
