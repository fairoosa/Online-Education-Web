# Generated by Django 4.1 on 2022-10-14 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0003_coursecontent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursecontent',
            old_name='couese',
            new_name='course',
        ),
    ]
