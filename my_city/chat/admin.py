from django.contrib import admin

from chat.models import Message, Chat, GroupChat

admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(GroupChat)