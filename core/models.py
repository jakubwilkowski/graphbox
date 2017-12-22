from django.db import models

# Create your models here.


class Developer(models.Model):
    login = models.TextField()
    name = models.TextField(default=None, null=True, blank=True)
    created_at = models.DateTimeField()
    location = models.TextField(default=None, null=True, blank=True)

    def __str__(self):
        return 'Developer {}({})'.format(self.name, self.login)


class Language(models.Model):
    name = models.TextField()

    def __str__(self):
        return 'Language {}'.format(self.name)


class Module(models.Model):
    name = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return '{} module {}'.format(self.language.name, self.name)


class Repository(models.Model):
    name = models.TextField()
    created_at = models.DateTimeField()
    contributors = models.ManyToManyField(Developer)
    languages = models.ManyToManyField(Language)
    modules = models.ManyToManyField(Module, through='ModuleVersion')

    def __str__(self):
        return 'Repository {}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Repositories'


class ModuleVersion(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    version = models.TextField()
