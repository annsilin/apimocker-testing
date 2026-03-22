# Apimocker API Test Framework

Автоматизированный фреймворк для тестирования REST API [apimocker.com](https://apimocker.com)

---

## Содержание

- [Структура проекта](#структура-проекта)
- [Теcтируемое API](#тестируемое-api)
- [Тест-кейсы](#тест-кейсы)
- [Локальная установка](#установка)
- [Запуск тестов локально](#запуск)
- [Docker + Jenkins](#jenkins--docker)

---

## Структура проекта

```
apimocker-testing/
├── config/
│   └── config.py              # BASE_URL, таймауты, заголовки
├── api/
│   ├── base_client.py         # BaseClient — requests + логирование + Allure
│   ├── users_client.py        # /users CRUD
│   ├── posts_client.py        # /posts CRUD + search + likes
│   ├── todos_client.py        # /todos CRUD
│   ├── comments_client.py     # /comments (read-only)
│   └── health_client.py       # /health
├── tests/
│   ├── test_users.py
│   ├── test_posts.py
│   ├── test_todos.py
│   ├── test_comments.py
│   └── test_health.py
├── utils/
│   └── helpers.py             # NONEXISTENT_ID, extract_id, get_first_item, unique_email
├── conftest.py                # session-фикстуры для всех клиентов
├── pytest.ini
├── requirements.txt
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions → Allure Report → GitHub Pages
└── docker-setup/
    ├── docker-compose.yml     # Jenkins + Allure
    ├── Jenkinsfile            # pipeline с расписанием
    ├── jenkins/
    │   ├── Dockerfile
    │   └── docker-entrypoint.sh
    └── tests/
        ├── Dockerfile
        └── entrypoint.sh
```

---

## Тестируемое API

**Base URL:** `https://apimocker.com`


| Ресурс       | Эндпоинты                                             | Особенности                               |
|--------------|-------------------------------------------------------|-------------------------------------------|
| `/users`     | GET, POST, PUT, DELETE                               | POST требует уникальный email (иначе 409) |
| `/posts`     | GET, POST, PUT, DELETE, GET /search, GET/POST /likes | PATCH не поддерживается (→ 400)           |
| `/todos`     | GET, POST, PUT, DELETE                               | PATCH не поддерживается (→ 400)           |
| `/comments`  | GET только                                           | Запись не поддерживается (→ 400/204)      |
| `/health`    | GET                                                  | Проверка доступности API                  |

**Формат ID:** целые числа (`/users/1`, `/posts/11`).

---

## Тест-кейсы

Всего **38 тестов**, сгруппированных по ресурсам и HTTP-методам:

| Файл                  | Классы                                                                   | Тестов |
|-----------------------|--------------------------------------------------------------------------|--------|
| `test_health.py`      | `TestHealth`                                                             | 1      |
| `test_users.py`       | `TestUsersGet`, `TestUsersPost`, `TestUsersPut`, `TestUsersPatch`, `TestUsersDelete` | 8 |
| `test_posts.py`       | `TestPostsGet`, `TestPostsPost`, `TestPostsPut`, `TestPostsPatch`, `TestPostsDelete` | 9 |
| `test_todos.py`       | `TestTodosGet`, `TestTodosPost`, `TestTodosPut`, `TestTodosPatch`, `TestTodosDelete` | 8 |
| `test_comments.py`    | `TestCommentsGet`, `TestCommentsWrite`                                   | 6      |

Стратегия по каждому ресурсу:

- **GET all** — прямой вызов, проверка 200
- **GET with limit** — параметр `?limit=N`, проверка 200
- **GET by id** — `get_first_item()` из списка → реальный id
- **GET nonexistent** — `NONEXISTENT_ID = 999999`, ожидается 404
- **POST** — уникальный payload (timestamp в email/username), ожидается 201
- **PUT** — `get_first_item()` из списка (seed data), ожидается 200
- **DELETE** — создаём через POST → `extract_id()` → удаляем
- **Неподдерживаемые методы** — документируют реальное поведение API (400/404)

---

## Установка

```bash
# 1. Клонировать репозиторий
git clone https://github.com/<your-username>/apimocker-tests.git
cd apimocker-tests

# 2. Виртуальное окружение
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# 3. Зависимости
pip install -r requirements.txt
```

---

## Запуск

```bash
# Все тесты
pytest

# С Allure-отчётом
pytest --alluredir=allure-results
allure serve allure-results

# Конкретный файл
pytest tests/test_users.py

# Конкретный тест
pytest -k test_create_user_returns_201

# С подробным выводом
pytest -v --tb=long
```

---

### Jenkins + Docker

[docker-setup/README.md](docker-setup/README.md)

