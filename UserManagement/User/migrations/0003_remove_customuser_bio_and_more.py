# Generated by Django 5.2 on 2025-04-28 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_alter_customuser_options_customuser_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='profile_picture',
        ),
    ]
