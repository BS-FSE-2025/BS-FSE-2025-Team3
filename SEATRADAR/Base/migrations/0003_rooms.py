# Generated by Django 5.1.4 on 2024-12-20 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0002_librarymanager'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # ('name_room',models.CharField(max_length=200)),
                ('Closed', models.TextField(max_length=30)),
                ('people', models.IntegerField()),
            ],
        ),
    ]
