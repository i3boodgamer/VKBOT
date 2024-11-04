# Укажите базовый образ
FROM python:3.10

# Установите рабочую директорию
WORKDIR /app

# Скопируйте requirements.txt в контейнер
COPY requirements.txt .

# Установите зависимости
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt


# Скопируйте весь код приложения
COPY . .

# Укажите, какой файл следует запустить (по желанию)
CMD ["python", "bot.py"]