# Generated by Django 2.1 on 2018-09-30 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_galleryimage_created_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='published_date',
        ),
    ]
