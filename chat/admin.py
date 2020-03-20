from django.contrib import admin

from chat.forms import UserChangeForm, UserCreationForm
from chat.models import Users
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(Users)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('phone', 'first_name', 'last_name')
    list_filter = ('phone',)
    fieldsets = (
        ('Auth', {'fields': ('phone', 'email', 'password', 'is_staff', 'is_superuser', 'is_active',)}),
        ('About', {'fields': ('first_name', 'last_name', 'role', 'bio', 'avatar')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Access', {'fields': ('last_login',)})
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2')}
         ),
    )
    search_fields = ('phone',)
    ordering = ('phone',)
    filter_horizontal = ()

    def get_form(self, request, obj=None, **kwargs):
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        return form
