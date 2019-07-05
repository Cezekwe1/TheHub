from django.urls import path
from . import views
urlpatterns = [
    path('create',views.make_org, name='make-org' ),
]