# Generated by Django 4.0.6 on 2022-11-16 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0011_enrollment_created_time_enrollment_is_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='certificate_path',
            field=models.FileField(default='', upload_to=''),
        ),
    ]
