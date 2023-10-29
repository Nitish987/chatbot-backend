from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models

# user admin portal
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'uid', 'is_active', 'is_admin', 'created_at', 'updated_at')
    list_filter = ('acc_type', 'is_active', 'is_signed', 'is_verified', 'is_admin',)
    fieldsets = (
        ('User', {'fields': ('first_name', 'last_name', 'email', 'country_code', 'phone', 'username', 'password')}),
        ('Profile', {'fields': ('gender', 'date_of_birth', 'photo')}),
        ('Account Type', {'fields': ('acc_type',)}),
        ('Account State', {'fields': ('is_signed', 'is_active', 'is_verified')}),
        ('Encryption Keys', {'fields': ('enc_key',)}),
        ('Tokens', {'fields': ('msg_token',)}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Terms and Conditions', {'fields': ('terms_conditions',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('uid', 'email', 'first_name', 'last_name', 'username', 'password1', 'password2', 'acc_type', 'is_signed', 'is_active', 'is_admin', 'terms_conditions'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(models.User, UserAdmin)


# user login state portal
class LoginStateAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')

admin.site.register(models.LoginState, LoginStateAdmin)
