# Generated by Django 2.1 on 2018-09-25 14:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_galleryimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='uploaded_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
