from django.urls import path, include
from rest_framework.routers import DefaultRouter

from App.views import TodoApiViewSet

router_master = DefaultRouter()
router_master.register('todo', TodoApiViewSet, basename="todo")

urlpatterns = [
    path('', include(router_master.urls)),
]