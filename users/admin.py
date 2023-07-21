from django.contrib.gis import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .forms import UserCreationForm, UserChangeForm


class UserAdmin(admin.OSMGeoAdmin):
    """
    User admin interface
    """
    model = get_user_model()
    add_form = UserCreationForm
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','groups', 'user_permissions')}),
        (_('More fields'), {'fields': ('address', 'phone', 'location')})
    )
    add_fieldsets = (
        (
            None,
            {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
            }
        )
    )


    def remove_fields(superset, subset):
        # return superset fields which do not present in subset if subset is not empty
        if len(subset) > 0:
            return [element for element in superset if element not in subset]
        return []

    def get_readonly_fields(self, request, obj=None):
        is_superuser = request.user.is_superuser
        # If user is not a super user return fields based on object ownership
        if not is_superuser:
            if not obj:     # If there is no user object no fild are marked as read only
                return []
            elif obj.pk == request.pk:      # If the object belongs to requested user no fields are marked as read only
                 return []
            else:       # If the object does not belogns to requested user few fieds marked as read only
                return [
                    'email',
                    'first_name',
                    'last_name',
                    'address',
                    'phone',
                    'location'
                ]
        # If user is super user, no fields are marked as read only fields
        return []

    def get_form(self, request, obj=None, **kwargs):
        form = self.form
        is_superuser = request.user.is_superuser

        disabled_fields = []
        all_fields = [field.name for field in self.model._meta.fields]

        if not is_superuser:
            fields_to_remove = []
            if not obj:     # Makes all fields are available for new records
                disabled_fields = self.remove_fields(all_fields, fields_to_remove)
            elif obj and obj.pk == request.user.pk:     # Prevents user from changing own permissions
                disabled_fields = [
                    'is_superuser', 
                    'is_staff', 
                    'user_permissions', 
                    'groups', 
                    'is_active'
                ]
            else:       # Limits read only fields and disables remaining fields
                readonly_fields = self.get_readonly_fields(request, obj=None)
                disabled_fields = self.remove_fields(all_fields, readonly_fields)

        for field in disabled_fields:
            if field in form.base_fields:
                form.base_fields[field].disabled = True
        
        return form

# Register the default User model with a custom ModelAdmin
admin.site.register(get_user_model(), UserAdmin)
