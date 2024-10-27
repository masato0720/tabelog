from django.contrib import admin

from .models import CustomUser

#admin.site.register(CustomUser)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name','email',]
    search_fields = ['email']
    ordering = ['id']
    list_per_page = 20

admin.site.register(CustomUser,CustomUserAdmin)
    