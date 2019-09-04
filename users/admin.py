from django.contrib import admin

from users.models import User, UserGroup


# Register your models here.

class userExtAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'username', 'email', 'phone', 'role', 'date_expired', 'is_active', 'date_joined')


class userGroupExtAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_created')


admin.site.register(User, userExtAdmin)
admin.site.register(UserGroup, userGroupExtAdmin)
