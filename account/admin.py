from django.contrib import admin
from .models import Account, CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin

class AccountInLine(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Accounts'

class CustomUserAdmin(UserAdmin):  # Change this line to inherit from UserAdmin
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["username", "email", "is_staff", "is_superuser"]
    inlines = (AccountInLine, )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Account)