from django.contrib import admin

# Register your models here.
from core.models import Repository, Developer, Language, Module, ModuleVersion

admin.site.register(Repository)
admin.site.register(Developer)
admin.site.register(Language)
admin.site.register(Module)
admin.site.register(ModuleVersion)