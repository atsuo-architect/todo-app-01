from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(
            user=self.request.user
        )

    def list(self, request, *args, **kwargs):
        cache_key = f"todos_user_{request.user.id}"

        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        cache.set(cache_key, serializer.data, 60)

        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        cache.delete(f"todos_user_{self.request.user.id}")

    def perform_update(self, serializer):
        serializer.save()
        cache.delete(f"todos_user_{self.request.user.id}")

    def perform_destroy(self, instance):
        user_id = instance.user_id

        instance.delete()

        cache.delete(f"todos_user_{user_id}")