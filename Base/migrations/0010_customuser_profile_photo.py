# Generated by Django 5.1.4 on 2025-01-13 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0009_customuser_librarymanagerprofile_studentprofile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos/'),
        ),
    ]
