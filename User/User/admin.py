from django.contrib import admin

from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib.sessions.models import Session

from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_admin',
    )
    list_filter = (
        'is_admin',
        'is_active'
    )
    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password'
            )
        }),
        ('Personal info', {
            'fields': (
                'first_name',
                'last_name',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_admin',
                'is_active'
            )
        }),
        ('Dates', {
            'fields': (
                'registration_date',
                'last_login',
                'activation_date',
            )
        }),
    )

    readonly_fields = (
        'registration_date',
        'last_login',
        'activation_date',
    )

    add_fieldsets = (
        (None, {
            'classes': (
                'wide',
            ),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2'
            ),
        }),
    )
    search_fields = (
        'email',
        'last_name',
        'first_name',
    )
    ordering = (
        'email',
    )
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

admin.site.register(Session)