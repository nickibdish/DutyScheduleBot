# Используем официальный образ Python (например, Python 3.9 на slim-версии)
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей в рабочую директорию
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Если бот работает через polling, можно не указывать EXPOSE, 
# но если понадобится порт (например, для вебхука) — добавьте EXPOSE <порт>
# EXPOSE 8080

# Задаем команду запуска приложения
CMD ["python", "main.py"]