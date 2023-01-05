import uuid
from django.db import models, signals


class SoftDelete(models.Model):
    is_deleted = models.BooleanField(default=False)

    def is_Deleted(self):
        self.is_deleted = True
        self.save()

    def Restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True


class AbstractTodo(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        abstract = True


class Todo(AbstractTodo, SoftDelete):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    task_name = models.CharField(max_length=100)
    completed = models.BooleanField(default=False, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.task_name
