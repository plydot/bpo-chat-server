from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, identify_hasher
from django.utils.translation import gettext, gettext_lazy as _

from chat.models import Users


class UserCreationForm(forms.ModelForm):
    # A form for creating new users. Includes all the required
    # fields, plus a repeated password.
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ('phone',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user


class ReadOnlyPasswordHashWidget(forms.Widget):
    template_name = 'auth/widgets/read_only_password_hash.html'
    read_only = True

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        summary = []
        if not value or value.startswith(UNUSABLE_PASSWORD_PREFIX):
            summary.append({'label': gettext("No password set.")})
        else:
            try:
                hasher = identify_hasher(value)
            except ValueError:
                summary.append({'label': gettext("*********************************")})
            else:
                for key, value_ in hasher.safe_summary(value).items():
                    summary.append({'label': gettext(key), 'value': value_})
        context['summary'] = summary
        return context


class CustomReadOnlyPasswordHashField(ReadOnlyPasswordHashField):
    widget = ReadOnlyPasswordHashWidget


class UserChangeForm(forms.ModelForm):
    # A form for updating users. Includes all the fields on
    # the user, but replaces the password field with admin's
    # password hash display field.

    password = CustomReadOnlyPasswordHashField(label=("Password"),
                                               help_text=("Raw passwords are not stored, so there is no way to see "
                                                          "this user's password, but you can change the password "
                                                          "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = Users
        fields = ('phone', 'password', 'is_active', 'is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]