from . import views
from django.urls import path
from .api import LoginAPI, RegisterApi

urlpatterns = [
    path('auth/login/', LoginAPI.as_view()),
    path('auth/logout/', views.end_session),
    path('auth/signup/', RegisterApi.as_view()),
    path('search/<str:query_str>',views.search),
    path('<int:user_id>', views.get_person),
    path('invite/<str:invite_type>',views.send_invite),
    path('remove/<str:removal_type>',views.remove_person),
    path('upgrade',views.make_admin),
    path('change/org',views.change_current_org),
    path('invite/accept/<str:type>',views.answer_invite),
    path('notifications',views.get_notifications),
    path('notifications/remove',views.remove_invites)
]