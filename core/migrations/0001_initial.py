# Generated by Django 2.0 on 2017-12-07 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.TextField()),
                ('name', models.TextField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField()),
                ('location', models.TextField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('contributors', models.ManyToManyField(to='core.Developer')),
                ('languages', models.ManyToManyField(to='core.Language')),
            ],
            options={
                'verbose_name_plural': 'Repositories',
            },
        ),
    ]