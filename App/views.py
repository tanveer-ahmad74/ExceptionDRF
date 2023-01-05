from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from App.serializers import TodoSerializer
from App.models import Todo
from rest_framework.permissions import AllowAny, IsAuthenticated


class TodoApiViewSet(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]





