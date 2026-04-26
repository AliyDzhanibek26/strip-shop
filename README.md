# Django Stripe Shop

Простой сервис приёма платежей через Stripe. Поддерживает товары, заказы, скидки и налоги. Реализованы Stripe Checkout Session и Payment Intent, мультивалютность (USD/EUR).

## Эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/item/<id>/` | Страница товара с кнопкой оплаты |
| GET | `/buy/<id>/` | Создать Stripe Checkout Session для товара, вернуть `{"id": session_id}` |
| GET | `/pay/<id>/` | Создать Payment Intent для товара, вернуть `client_secret` |
| GET | `/order/<id>/` | Страница заказа с итоговой суммой |
| GET | `/buy-order/<id>/` | Создать Stripe Checkout Session для заказа |
| GET | `/success/` | Страница успешной оплаты |

## Запуск через Docker (рекомендуется)

```bash
cp .env.example .env
# заполнить .env своими ключами Stripe и настройками БД

docker compose up --build
```

После старта:
- Сервис: http://localhost:8000
- Применить миграции и создать суперпользователя:

```bash
docker compose exec web python manage.py createsuperuser --settings=config.settings.production
```

Для заполнения базы тестовыми данными:

```bash
docker compose exec web python manage.py loaddata fixtures/initial_data.json --settings=config.settings.production
```

## Запуск локально

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# задать POSTGRES_HOST=localhost, заполнить ключи Stripe

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Переменные окружения

| Переменная | Описание |
|-----------|----------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` / `False` |
| `ALLOWED_HOSTS` | Список хостов через запятую |
| `POSTGRES_*` | Реквизиты PostgreSQL |
| `STRIPE_PUBLIC_KEY_USD` | Публичный ключ Stripe (USD) |
| `STRIPE_SECRET_KEY_USD` | Секретный ключ Stripe (USD) |
| `STRIPE_PUBLIC_KEY_EUR` | Публичный ключ Stripe (EUR) |
| `STRIPE_SECRET_KEY_EUR` | Секретный ключ Stripe (EUR) |

Ключи Stripe берутся из [Stripe Dashboard → Developers → API keys](https://dashboard.stripe.com/apikeys). Для тестирования используются ключи с префиксом `pk_test_` / `sk_test_`.

## Структура проекта

```
├── apps/
│   └── payments/
│       ├── models.py       # Item, Order, Discount, Tax
│       ├── views.py
│       ├── urls.py
│       ├── admin.py
│       ├── services/
│       │   └── stripe_service.py
│       └── templates/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   └── urls.py
├── templates/
│   └── base.html
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Бонусные задачи

- [x] Docker + docker-compose
- [x] Environment variables (python-decouple)
- [x] Django Admin для всех моделей
- [x] Модель `Order` с несколькими `Item`, единый платёж
- [x] Модели `Discount` и `Tax`, интеграция со Stripe (Coupon + Tax Rate)
- [x] `Item.currency`, два Stripe-keypair (USD / EUR)
- [x] Stripe Payment Intent (`/pay/<id>/`)
