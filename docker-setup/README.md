# Docker Infrastructure — Apimocker API Tests

## Порты

| Сервис  | URL                   | Описание                          |
|---------|-----------------------|-----------------------------------|
| Jenkins | http://localhost:8080 | CI/CD, расписание, ручной запуск  |
| Allure  | http://localhost:5050 | Отчёты|

---

## Быстрый старт

```cmd
cd apimocker-tests
docker compose -f docker-setup/docker-compose.yml up -d
```

Проверить статус:
```cmd
docker compose -f docker-setup/docker-compose.yml ps
```

---

## Запуск тестов

### Через Jenkins

- **Build with Parameters** → опционально `PYTEST_ARGS` → **Build**
- **По расписанию**: автоматически каждый будний день в 09:00

### Напрямую через Docker

```cmd
# Собрать образ (один раз или после изменений)
docker build -t apimocker-tests -f docker-setup/tests/Dockerfile .

# Запустить все тесты
docker run --rm ^
    -v %CD%:/app ^
    -v apimocker_allure_results:/app/allure-results ^
    apimocker-tests /app/tests --alluredir=/app/allure-results -v

# Запустить конкретный файл
docker run --rm ^
    -v %CD%:/app ^
    -v apimocker_allure_results:/app/allure-results ^
    apimocker-tests /app/tests/test_users.py -v
```

---

## Просмотр отчётов Allure

Открыть: http://localhost:5050/allure-docker-service/projects/default/reports/latest/index.html

Allure автоматически подхватывает новые результаты каждые 10 секунд.

---

## Остановка

```cmd
docker compose -f docker-setup/docker-compose.yml down

# Остановить и удалить все данные
docker compose -f docker-setup/docker-compose.yml down -v
```
