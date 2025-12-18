# Bitrix_tg_bot
=======
# Bitrix24 API Expert Bot

Интеллектуальный чат-бот в Telegram для помощи разработчикам по документации Bitrix24 API. Построен на базе Yandex GPT и поддерживает актуализацию знаний через Selenium-парсинг.

## Основные возможности
- **Техническая консультация:** Ответы на вопросы по методам REST API Bitrix24.
- **RAG-логика:** Формирование ответов на основе официальной документации.
- **Selenium Parsing:** Возможность автоматического сбора данных с сайта apidocs.bitrix24.ru.
- **История диалогов:** Сохранение всех запросов и ответов в PostgreSQL через SQLAlchemy.

## Технологический стек
- **Python 3.12**
- **Yandex GPT API** (LLM)
- **python-telegram-bot** (Interface)
- **SQLAlchemy + PostgreSQL** (Database)
- **Selenium + WebDriver Manager** (Parsing)
- **python-dotenv** (Security)

## Требования к .env файлу
Для работы проекта необходимо создать файл `.env` в корневой папке и заполнить следующие поля:

| Ключ | Описание | Пример |
| :--- | :--- | :--- |
| `TG_BOT_TOKEN` | Токен вашего бота от BotFather | `855925:AAE...` |
| `YANDEX_API_KEY` | API-ключ Yandex Cloud | `AQVN...` |
| `YANDEX_FOLDER_ID` | ID каталога в Yandex Cloud | `b1g...` |
| `POSTGRES_USER` | Имя пользователя БД | `octagon` |
| `POSTGRES_PASSWORD` | Пароль от БД | `12345` |
| `POSTGRES_HOST` | Хост базы данных | `localhost` |
| `POSTGRES_PORT` | Порт базы данных | `5432` |
| `POSTGRES_DB` | Название базы данных | `tg_bitrix_bot` |

## Установка и запуск

1. **Клонируйте репозиторий:**
   ```bash
   git clone [https://github.com/ваш-логин/tg_bitrix_bot.git](https://github.com/ваш-логин/tg_bitrix_bot.git)
   cd tg_bitrix_bot

