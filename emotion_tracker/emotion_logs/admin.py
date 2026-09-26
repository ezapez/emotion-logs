from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.unregister(User)


@admin.register(User)
class EmotionUserAdmin(UserAdmin):
	list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'last_login', 'date_joined')
	list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups', 'date_joined')
	search_fields = ('username', 'email', 'first_name', 'last_name')
	date_hierarchy = 'date_joined'
	ordering = ('-date_joined',)
	list_per_page = 30


admin.site.site_header = 'EmotionLogs administration'
admin.site.site_title = 'EmotionLogs admin'
admin.site.index_title = 'Manage user accounts'


