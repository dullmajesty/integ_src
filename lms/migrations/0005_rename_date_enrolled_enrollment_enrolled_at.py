# Generated by Django 5.1.6 on 2025-03-20 03:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0004_enrollment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enrollment',
            old_name='date_enrolled',
            new_name='enrolled_at',
        ),
    ]
