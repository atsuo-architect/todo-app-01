import pytest
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APIClient

from .models import Todo


@pytest.mark.django_db
class TestTodoAPI:

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

    @pytest.fixture
    def authenticated_client(self, api_client, user):
        api_client.force_authenticate(user=user)
        return api_client

    def test_unauthenticated(self, api_client):
        response = api_client.get("/api/todos/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_todo(self, authenticated_client, user):
        response = authenticated_client.post(
            "/api/todos/",
            {"title": "テスト用タスク"},
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Todo.objects.count() == 1

        todo = Todo.objects.first()

        assert todo.title == "テスト用タスク"
        assert todo.user == user

    def test_user_can_only_see_own_todos(
        self,
        authenticated_client,
        user,
    ):
        other_user = User.objects.create_user(
            username="other",
            password="password",
        )

        Todo.objects.create(
            title="自分のTodo",
            user=user,
        )

        Todo.objects.create(
            title="他人のTodo",
            user=other_user,
        )

        response = authenticated_client.get("/api/todos/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["title"] == "自分のTodo"

    def test_update_todo(self, authenticated_client, user):
        todo = Todo.objects.create(
            title="変更前",
            user=user,
        )

        response = authenticated_client.patch(
            f"/api/todos/{todo.id}/",
            {"completed": True},
        )

        assert response.status_code == status.HTTP_200_OK

        todo.refresh_from_db()

        assert todo.completed is True

    def test_delete_todo(self, authenticated_client, user):
        todo = Todo.objects.create(
            title="削除するTodo",
            user=user,
        )

        response = authenticated_client.delete(
            f"/api/todos/{todo.id}/",
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Todo.objects.filter(id=todo.id).exists() is False

    def test_todo_list_uses_cache(
        self,
        authenticated_client,
        user,
    ):
        Todo.objects.create(
            title="Redisテスト",
            user=user,
        )

        cache.clear()

        response = authenticated_client.get("/api/todos/")

        assert response.status_code == status.HTTP_200_OK

        cache_key = f"todos_user_{user.id}"

        assert cache.get(cache_key) is not None