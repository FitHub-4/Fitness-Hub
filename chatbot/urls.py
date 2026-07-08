from django.urls import path

from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_page, name='chat'),
    path('api/', views.chat_api, name='api'),
    path('groq/', views.groq_chat_view, name='groq'),
    path('voice/', views.voice_assistant_view, name='voice'),
    path('voice-ui/', views.voice_page, name='voice_ui'),
]
