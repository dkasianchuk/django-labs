from django.contrib import admin
from .models import CustomUser, ConnectedUsers


admin.site.register(CustomUser)
admin.site.register(ConnectedUsers)
