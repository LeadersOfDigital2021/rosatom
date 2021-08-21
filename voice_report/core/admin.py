from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Group, Transcript, Meeting, EmployeeRole, EmployeeRolesInMeeting
from django.contrib.auth.models import Group as default_group

admin.site.unregister(default_group)


class cUserAdmin(UserAdmin):
    fieldsets = (('Основная информация', {'fields': ('email', 'password')}),
                 ('Персональные данные', {'fields': ('last_name', 'first_name', 'middle_name', 'phonenumber', 'place')}),
                 ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                 ('Важные данные', {'fields': ('last_login', 'date_joined')}))
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}),)
    list_display = ('email', 'last_name', 'first_name', 'middle_name', 'is_staff')
    ordering = ['email']


admin.site.register(User, cUserAdmin)
admin.site.register(Group)
admin.site.register(Transcript)
admin.site.register(Meeting)
admin.site.register(EmployeeRole)
admin.site.register(EmployeeRolesInMeeting)
