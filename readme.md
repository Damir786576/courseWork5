# Habit Tracker
## Описание проекта
- Django REST API для управления привычками с JWT-аутентификацией, Telegram-уведомлениями через Celery и API-документацией (Swagger/ReDoc).

### Локальный запуск
#### Требования
- Docker и Docker Compose
- Python 3.10
- Git
### Шаги
- Установите Docker Desktop 
- Проверьте, что Docker работает:
```docker --version```
- Склонируйте репозиторий:
```git clone https://github.com/your-username/habit-tracker.git```,
```cd habit-tracker```
- Создайте файл .env:
```SECRET_KEY=your-secret-key DEBUG=True POSTGRES_DB=habit_tracker_db POSTGRES_USER=habit_user POSTGRES_PASSWORD=habit_password POSTGRES_HOST=db POSTGRES_PORT=5432 REDIS_URL=redis://:default_redis_pass@redis:6379/0 TELEGRAM_TOKEN=your-telegram-bot-token```

- Запустите проект:
``` docker-compose up -d ```
- Убедитесь, что всё работает:
``` docker-compose ps ```
#### API: http://localhost:8000/api/ 
- Примените миграции:
``` docker-compose run backend python manage.py migrate ```
- Остановите проект, если нужно:
``` docker-compose down ```
## Запуск на сервере
### Требования
- Сервер с Ubuntu 24.04
- Docker и Docker Compose
- SSH-доступ
### Настройка сервера
-  Подключитесь:
``` ssh user@your-server-ip ```
- Установите зависимости:
```sudo apt update ```,
```sudo apt install -y docker.io docker-compose```,
```sudo systemctl start docker```,
```sudo systemctl enable docker```,

- Настройте SSH:
```ssh-keygen -t rsa -b 4096```
```ssh-copy-id user@your-server-ip```
### Настройка CI/CD
- В GitHub добавьте секреты (Settings → Secrets and variables → Actions → Repository secrets):
- SSH_USER: имя пользователя (например, Ubuntu)
- SSH_KEY: приватный SSH-ключ
- SERVER_IP: IP сервера (например, 158.160.87.62)
- DEPLOY_DIR: путь (например, /home/ubuntu/habit-tracker)
- TELEGRAM_TOKEN: токен Telegram-бота
- Файл .github/workflows/ci.yml запускает тесты и деплоит проект.

### Адрес сервера
- API доступно на:
http://158.160.87.62:8000/api/

### Тесты
```docker-compose run backend python manage.py test```

### API-документация
- Swagger: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/