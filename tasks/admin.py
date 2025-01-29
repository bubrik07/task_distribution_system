from django.contrib import admin
from .models import Task, TaskStatus, TaskPriority, Executor

admin.site.register(TaskStatus)
admin.site.register(TaskPriority)
admin.site.register(Task)
admin.site.register(Executor)
