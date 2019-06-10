from . import views
from django.urls import path
from .api import LoginAPI

urlpatterns = [
    path('auth/login/', LoginAPI.as_view()),
    path('auth/logout/', views.end_session),
    path('auth/signup/', views.signup),

]