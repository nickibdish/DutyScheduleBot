# db/session.py

from sqlalchemy.orm import sessionmaker
from .engine import engine

# Создаем фабрику сессий, привязанную к нашему engine.
Session = sessionmaker(bind=engine)
