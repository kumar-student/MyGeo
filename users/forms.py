from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, \
    UserChangeForm as BaseUserChangeForm

from django.contrib.auth import get_user_model


class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = get_user_model()
        fields = (
            'email', 
            'first_name', 
            'last_name', 
            'address', 
            'phone', 
            'location',
            'is_staff', 
            'is_superuser', 
            'groups',
            'user_permissions',
            'is_active'
        )


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = get_user_model()
        fields = (
            'email', 
            'first_name', 
            'last_name', 
            'address', 
            'phone', 
            'location',
            'is_staff', 
            'is_superuser', 
            'groups',
            'user_permissions',
            'is_active'
        )
