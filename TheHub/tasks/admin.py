from django.contrib import admin
from .models import Task,TaskAssigment


admin.site.register(Task)
admin.site.register(TaskAssigment)