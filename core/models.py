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


class Repository(models.Model):
    name = models.TextField()
    created_at = models.DateTimeField()
    contributors = models.ManyToManyField(Developer)
    languages = models.ManyToManyField(Language)

    def __str__(self):
        return 'Repository {}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Repositories'

