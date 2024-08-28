from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# the above is to make password only in read only mode.
from .models import Account

# Register your models here.
# the main use of below function is to make sure that the password is in read only foramt not in edit format
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email','first_name', 'last_name')
    #it means when we click on value in the field it will show that all details of that particluar user
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    # The below are some important things that are needed to add to make sure the password is in read only mode and
    #  as it is custom user model, the below are some of the things we need to add.
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
#Account means model name 
