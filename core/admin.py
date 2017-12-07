from django.contrib import admin

# Register your models here.
from core.models import Repository, Developer, Language

admin.site.register(Repository)
admin.site.register(Developer)
admin.site.register(Language)
