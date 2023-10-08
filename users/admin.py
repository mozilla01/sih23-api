from django.contrib import admin
from .models import User, RailwayAccount, CompanyAccount, ConsumerAccount, Rake

# Register your models here.

admin.site.register(User)
admin.site.register(RailwayAccount)
admin.site.register(CompanyAccount)
admin.site.register(ConsumerAccount)
admin.site.register(Rake)
