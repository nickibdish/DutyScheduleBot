# db/engine.py

from sqlalchemy import create_engine

# Создаём engine для подключения к базе SQLite.
# 'sqlite:///schedule.db' означает, что файл schedule.db будет находиться в той же папке, откуда запущено приложение.
engine = create_engine('sqlite:///schedule.db', echo=True)
