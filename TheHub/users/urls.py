from . import views
from django.urls import path
from .api import LoginAPI, RegisterApi

urlpatterns = [
    path('auth/login/', LoginAPI.as_view()),
    path('auth/logout/', views.end_session),
    path('auth/signup/', RegisterApi.as_view()),

]