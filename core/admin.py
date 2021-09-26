from .models import User, LoginAttempt



from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Permission
# from django.contrib.auth.models import User 

admin.site.site_header = "Sumit Hero"
admin.site.site_title = "Sumit Hero Admin Portal"
admin.site.index_title = "Welcome to The Sumit Hero"

# User Creating Form
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# User Update Form
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=("Password"),
        help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))
    class Meta:
        model = User
        fields = "__all__"
    
    def clean_password(self):
        return self.initial['password']


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'full_name', 'id', 'email',  'is_staff', 'is_superuser', 'last_login',)
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    ordering = ['-id']
    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('User Credentials', {'fields': ('username', 'screen_lock_img', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups')}), # 'user_permissions', 'groups'
    )
    # Creation Fields
    add_fieldsets = (
        ('User Credentials', {'classes': ('wide',), 'fields': ('username', 'password1', 'password2',)}),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name' )
    ordering = ('-date_joined',)
    filter_horizontal = ()

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


# admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Permission)



# Register your models here.
admin.site.register(LoginAttempt)