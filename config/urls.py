from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from todos.views import TodoViewSet


router = DefaultRouter()
router.register(r"todos", TodoViewSet, basename="todo")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
