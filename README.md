# GoldDecor Test

Django shop using Django Templates and PostgreSQL.

## Requirements
- Python 3.11+
- PostgreSQL 14+

## Setup (local)
1. Create and activate venv, then install deps:
   ```bash
   pip install -r requirements.txt
   ```
2. Set environment variables (example):
   ```bash
   set POSTGRES_DB=db
   set POSTGRES_USER=pg
   set POSTGRES_PASSWORD=password
   set POSTGRES_HOST=localhost
   set POSTGRES_PORT=5432
   ```
3. Run migrations and start server:
   ```bash
   python manage.py migrate
   python manage.py runserver 0.0.0.0:8000
   ```

## Features
- Categories and Products with images
- Product list with category filter, search (name+description), pagination (8/page)
- Product detail with stock, price, add-to-cart
- Session cart (add/update/remove), totals, note (not persisted)
- Auth: signup, login, logout (templates included)
- Base templates with navbar and cart item count
- Query optimizations with `select_related("category")`

## Routes
- `/` catalog list
- `/category/<slug>/` filtered list
- `/product/<id>/` detail
- `/cart/` cart page
- `/login/`, `/signup/`, `/logout/`

## Docker
Build and run (expects env vars for DB):
```bash
docker build -t golddecor .
# run using your compose or pass envs and port map
```
