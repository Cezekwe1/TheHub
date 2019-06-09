from . import views
from django.urls import path

urlpatterns = [
    path('auth/login/', views.login),
    path('auth/logout/', views.end_session),
    path('auth/signup/', views.signup),

]