# FBRQ Mailing Service

Сервис для управления и отправки рассылок с интеграцией с внешними API.

## О проекте

FBRQ Mailing Service - это веб-приложение на Django, которое предоставляет функционал для создания, управления и
отправки рассылок. Сервис использует Celery для асинхронной обработки задач и Redis в качестве брокера сообщений.

## Технический стек

- **Бэкенд**: Django 5.0.1
- **База данных**: PostgreSQL 16.1
- **Брокер сообщений**: Redis 7.2.4
- **Асинхронные задачи**: Celery 5.3.6
- **API**: Django REST Framework 3.14.0
- **Документация API**: drf-spectacular
- **Веб-сервер**: Gunicorn + Uvicorn
- **Очередь задач**: Redis
- **Контейнеризация**: Docker + Docker Compose

## Функциональность

- Создание и управление рассылками
- Асинхронная отправка сообщений
- Интеграция с внешними API (настраивается через переменные окружения)
- Административная панель Django для управления данными
- REST API для интеграции с другими сервисами
- Планировщик задач Celery Beat

## Установка и запуск

### Требования

- Docker 20.10.0+
- Docker Compose 1.29.0+

### Настройка окружения

1. Создайте файл `.env` в корневой директории проекта на основе примера:

```bash
# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# External API
OUTER_SERVER_URL=your-api-url
JWT_TOKEN=your-jwt-token
```

### Запуск в среде разработки

1. Запустите сервисы:

```bash
docker-compose -f docker-compose.dev.yml up --build
```

2. При первом запуске примените миграции:

```bash
docker-compose -f docker-compose.dev.yml exec app python manage.py migrate
```

3. Создайте суперпользователя (опционально):

```bash
docker-compose -f docker-compose.dev.yml exec app python manage.py createsuperuser
```

Сервис будет доступен по адресу: http://localhost:8000

## Структура проекта

```
fbrq/
├── app/                           # Основное приложение
│   ├── config/                    # Настройки Django
│   ├── mailing/                   # Приложение рассылок
│   │   ├── migrations/            # Миграции базы данных
│   │   ├── admin.py               # Админ-панель
│   │   ├── apps.py                # Конфигурация приложения
│   │   ├── forms.py               # Формы Django
│   │   ├── generate_mailing.py    # Генерация тестовых рассылок
│   │   ├── models.py              # Модели данных
│   │   ├── serializers.py         # Сериализаторы DRF
│   │   ├── tasks.py               # Асинхронные задачи Celery
│   │   ├── tests.py               # Тесты
│   │   ├── urls.py                # URL-маршруты приложения
│   │   └── views.py               # Представления
│   ├── manage.py                  # Управление Django
│   └── requirements.txt           # Зависимости Python
├── nginx/                         # Конфигурация Nginx
├── docker-compose.dev.yml          # Конфигурация Docker Compose для разработки
└── docker-compose.prod.yml         # Конфигурация Docker Compose для продакшена
```

## API

API документация доступна по адресу `/api/schema/swagger-ui/` после запуска сервиса.

## Разработка

### Запуск тестов

```bash
docker-compose -f docker-compose.dev.yml exec app python manage.py test
```

### Создание миграций

```bash
docker-compose -f docker-compose.dev.yml exec app python manage.py makemigrations
```
