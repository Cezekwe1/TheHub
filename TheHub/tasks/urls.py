from django.urls import path
from . import views
from .api import TaskViewSet
urlpatterns = [
    path('',views.get_tasks, name='all-tasks' ),
    path('create/',views.make_task, name='create-task' ),
    path('<int:task_id>/',views.get_task, name='one-task' ),
    path('update/<int:task_id>/',views.update_task, name='update-one-task' ),
    path('delete/<int:task_id>/',views.delete_task, name='delete-one-task' ),
]