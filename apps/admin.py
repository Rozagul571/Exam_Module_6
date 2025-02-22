from django.contrib import admin

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.models import User, Transaction

admin.site.site_header = "Product Admin"
admin.site.site_title = "Product Admin Portal"
admin.site.index_title = "Welcome to Product Researcher Portal"

@admin.register(User)
class UserAdmin(ModelAdmin):
    pass

@admin.register(Transaction)
class TransactionsAdmin(ModelAdmin):
    pass


