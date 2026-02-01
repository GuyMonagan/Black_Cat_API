> # 📚Black_Cat_API
> ### Бэкенд библиотечной системы с Telegram-ботом, ролями и напоминаниями

Backend API для библиотечной системы, разработанный с использованием Django REST Framework. 
Проект упрощает управление книжным фондом, учётом аренды, отзывами, а также предоставляет 
интеграцию с Telegram для напоминаний о возвратах.
>Даёт бумажным книгам окошко в цифру 🐾


---

## 🚀 Возможности

- Регистрация и авторизация через JWT 
- 3 уровня ролей: админ, библиотекарь, читатель 
- Управление книгами, бронированиями и отзывами 
- Система прав доступа для каждого действия 
- Напоминания в Telegram о возврате книг 
- Отчёты: популярные книги, должники, потерянные книги 
- Админка с отображением обложек и связанной информацией 
- Документация через Swagger и Redoc 
- Покрытие тестами (pytest) 92% 
- Асинхронные задачи через Celery + Redis 
- Docker для локальной разработки и деплоя

### 🔒 Защита и ограничения
- Приватность: просмотр чужих аренд невозможен 
- Telegram: требует ручной привязки аккаунта по токену (исключает случайные совпадения)
- Отзывы: модерировать могут только библиотекари и администраторы 
- Книги: создание доступно только библиотекарям и администраторам 
- Удаление: отзывы, пользователей и книги может удалять только администратор


---

## 🧩 Стек технологий

- Django REST Framework
- PostgreSQL 
- JWT (djangorestframework-simplejwt)
- Celery + Redis 
- Docker + Docker Compose 
- Swagger / Redoc 
- pytest + coverage 
- CORS Headers
---

## ⚙️ Установка и запуск

### 1. Клонируйте репозиторий

```
git clone https://github.com/GuyMonagan/Black_Cat_API.git
cd Black_Cat_API
```

### 2. Создайте .env файл

Подставьте актуальные данные:

```
DEBUG=
SECRET_KEY=
ALLOWED_HOSTS=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

TELEGRAM_BOT_TOKEN=

CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=
CELERY_ACCEPT_CONTENT=
CELERY_TASK_SERIALIZER=

CORS_ALLOWED_ORIGINS=

```


### 3. Соберите и запустите проект

```
docker-compose up --build
```


### 4. Примените миграции и создайте суперпользователя

```
docker-compose exec web poetry run python manage.py migrate
docker-compose exec web poetry run python manage.py createsuperuser

```

### 5. Запустите Telegram-бота

Бот активируется отдельной management-командой. Убедитесь, что в .env указан корректный TELEGRAM_BOT_TOKEN.

```
docker-compose exec web python manage.py runbot

```
После запуска:

> - Бот начнёт принимать команды в Telegram
> - Доступна команда `/connect <токен>` для привязки аккаунта
> - Работает в паре с задачей напоминаний через Celery

---

## 📄 Swagger и Redoc

- Swagger: http://localhost:8000/api/docs/
- Redoc: http://localhost:8000/api/redoc/

---

## 🧪 Тестирование и линтинг

```
# Тесты
docker-compose exec web poetry run pytest

# Статический анализ
docker-compose exec web poetry run flake8 .

# Сортировка импортов
docker-compose exec web poetry run isort .

# Форматирование кода
docker-compose exec web poetry run black .

```

---

## 🔮 Планы на будущее
В дальнейшем планируется добавить в проект следующий функционал:
- 📸 Интеграция авторизации Telegram через QR-код
- 📊 Расширенное отображение отчётов для администраторов (графики, экспорт в PDF)
- 💬 Введение обсуждений книг и отзывов в виде "тредов"
- 📥 Возможность отправлять личные сообщения между пользователями
- 👀 Отдельная панель администратора для управления нарушениями/жалобами
- 📅 Отложенное бронирование книг (резервы на будущее)

---

## 👋 Пасхалка

В проекте есть скрытая страничка благодарности по адресу:
http://localhost:8000/thanks/

Не забудьте улыбнуться 😊

---

## 📬 Автор

Разработчик: GuyMonagan  
Telegram: [@GuyMonagan](https://t.me/GuyMonagan)  
Email: werevalkury@gmail.com

---