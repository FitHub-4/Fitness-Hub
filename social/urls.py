from django.urls import path

from . import views

urlpatterns = [
    path('', views.social_hub, name='social-hub'),
    path('search/', views.search_users, name='social-search'),
    path('send/', views.send_connection, name='social-send'),
    path('respond/', views.respond_connection, name='social-respond'),
    path('remove/', views.remove_connection, name='social-remove'),
    path('chat/<str:username>/', views.chat, name='chat'),
    path('api/send/', views.api_send_message, name='api-send-message'),
    path('api/messages/<str:username>/', views.api_get_messages, name='api-get-messages'),
]
