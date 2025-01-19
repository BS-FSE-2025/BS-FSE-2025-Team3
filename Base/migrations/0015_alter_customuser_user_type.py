# Generated by Django 5.1.5 on 2025-01-16 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0014_alter_studentprofile_bio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('student', 'Student'), ('library_manager', 'Library Manager')], default='student', max_length=50),
        ),
    ]
