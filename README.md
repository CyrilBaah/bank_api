# Bank API

Django REST API with Celery, RabbitMQ, and Flower monitoring.

## Services

- **Django API**: http://localhost:8000/api/docs/
- **Flower (Celery Monitor)**: http://localhost:5555
- **RabbitMQ Management**: http://localhost:15672 (admin/Pass123)
- **Mailpit**: http://localhost:8025

## Quick Start

```bash
docker-compose up -d
```

## Environment

Copy `.env` and configure:
- Database: PostgreSQL
- Broker: RabbitMQ  
- Cache: Redis
- Email: Mailpit

## Celery Tasks

Tasks are in `user_auth/tasks.py`. Monitor via Flower interface.
