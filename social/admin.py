from django.contrib import admin

from .models import Connection, Message


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'connection_type', 'status', 'created_at')
    list_filter = ('connection_type', 'status')
    search_fields = ('from_user__username', 'to_user__username')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'timestamp', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('sender__username', 'recipient__username', 'content')
