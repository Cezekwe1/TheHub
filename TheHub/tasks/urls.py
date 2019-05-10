from django.urls import path
from . import views
urlpatterns = [
    path('',views.get_tasks, name='all-tasks' ),
    path('<int:task_id>/',views.get_task, name='one-task' )
]