# Generated by Django 2.1 on 2018-12-17 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20181215_0919'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adminloginattempts',
            old_name='lastUnblockedLogin',
            new_name='lastTime',
        ),
    ]
