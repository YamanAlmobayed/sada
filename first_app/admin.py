from django.contrib import admin
from first_app import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

    
class CustomizedUserAdmin(UserAdmin):
    readonly_fields = ['get_account_type']
    fieldsets = (
        (None, {'fields': ('username', 'password', 'get_account_type')}),
    )
    
    @admin.display(description='Account_type')
    def get_account_type(self, obj):
        account = models.Account.objects.get(user=obj)
        return account.account_type
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        models.Account.objects.create(user = obj)
    
admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)


admin.site.register(models.ChildPersonalInfo)
admin.site.register(models.PortageQuestion)
admin.site.register(models.WechslerQuestion)
admin.site.register(models.LddrsQuestion)
#admin.site.register(models.RavnQuestion)
admin.site.register(models.PortageBlock)
admin.site.register(models.PortageTest)
admin.site.register(models.WechslerScaledScore)
admin.site.register(models.WechslerChild)



