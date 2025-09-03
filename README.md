# 

## 🚀 Стек технологий
- 🐍 **Backend**: Django, Django REST Framework
- 🤖 **Bots**: pyTelegramBotAPI
- 🗄️ **Database**: PostgreSQL
- ⚡ **Cache & State Management**: Redis
- 🐳 **Containerization**: Docker, Docker Compose
- 🎭 **Package Management**: Poetry



### 2️⃣ Настройка `.env`
Создайте `.env` файл в корне проекта и добавьте переменные окружения:

```ini
# 🔧 Режим работы приложения
DEVELOPMENT_MODE=PRODUCTION  # или DEVELOPMENT для разработки

# 🔐 Настройки Django
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=*
CSRF_TRUSTED_ORIGINS=http://localhost

# 🗄️ Настройки базы данных PostgreSQL
POSTGRES_DB=db_name
POSTGRES_USER=db_user
POSTGRES_PASSWORD=MySuperSecretPassword
POSTGRES_HOST=db
POSTGRES_PORT=5432

# ⚡ Настройки Redis
REDIS_HOST=redis
REDIS_PORT=6379
```

### 3️⃣ Установка зависимостей с Poetry
```sh
poetry install
```

### 4️⃣ Запуск в Docker
```sh
docker-compose up -d --build
```

### 5️⃣ Создание суперпользователя Django
```sh
docker-compose exec backend python manage.py createsuperuser
```

### 6️⃣ Установка вебхука для бота
```sh
docker-compose exec backend python manage.py set_webhook
```

### 7️⃣ Запуск бота в режиме разработки
```sh
docker-compose exec backend python manage.py start_bot
```

---

## ⚙️ Основные команды
| Команда                                                        | Описание                       |
|----------------------------------------------------------------|--------------------------------|
| `poetry install`                                               | Установить зависимости         |
| `docker-compose up -d --build`                                 | Запустить проект в контейнерах |
| `docker-compose exec backend python manage.py createsuperuser` | Создать администратора Django  |
| `docker-compose exec backend python manage.py set_webhook`     | Установить вебхук для бота     |
| `docker-compose exec backend python manage.py start_bot`       | Запустить бота вручную         |

---

## 📂 Монтируемые папки
В `docker-compose.yml` используются монтируемые папки:
- `mounts/src/logs/` — логи работы backend-а
- `mounts/src/static/` — статические файлы Django
- `mounts/src/media/` — загруженные пользователями файлы
- `mounts/db/pg_data/` — данные PostgreSQL
- `mounts/db/backups/` — резервные копии базы данных
- `mounts/db/logs/` — логи работы PostgreSQL
- `mounts/redis/data/` — данные Redis
- `mounts/redis/conf/` — конфигурационные файлы Redis

---

## 🔗 Доступы
- **Django Admin Panel**: [`http://localhost:8000/admin/`](http://localhost:8000/admin/)
---

## 📜 Лицензия
Этот проект распространяется по лицензии MIT. Подробнее см. в файле [`LICENSE`](LICENSE).

© 2025 Рустам Мухтаров

