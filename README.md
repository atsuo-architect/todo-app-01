# Todo API

Django REST Frameworkで構築したTodo管理APIです。

JWT認証、ユーザーごとのデータ分離、Redisによるキャッシュ、
PostgreSQL、Docker、pytest、GitHub Actions、Renderへのデプロイまで実装しています。

## Features

- JWT認証
- Todo CRUD
- ユーザーごとのTodoデータ分離
- Redisキャッシュ
- キャッシュ無効化
- PostgreSQL
- Docker / Docker Compose
- pytest
- GitHub ActionsによるCI
- Renderへのデプロイ
- Postman CollectionによるAPI動作確認

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Docker
- pytest
- GitHub Actions
- Render
- Postman

## API

### Authentication

POST /api/token/
POST /api/token/refresh/

### Todo

GET    /api/todos/
POST   /api/todos/
GET    /api/todos/{id}/
PATCH  /api/todos/{id}/
DELETE /api/todos/{id}/

## API Testing

Postman Collectionを `postman/` に用意しています。

JWT認証からTodoのCRUDまで動作確認できます。

## Deployment

Renderにデプロイしています。

## Testing

    docker compose exec web pytest

## Local Development

    docker compose up -d

API:

    http://localhost:8000/