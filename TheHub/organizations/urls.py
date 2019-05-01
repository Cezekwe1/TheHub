from django.urls import path
from . import views
urlpatterns = [
    path('',views.orgs, name='all-orgs' ),
]