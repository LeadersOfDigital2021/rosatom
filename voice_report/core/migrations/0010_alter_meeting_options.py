# Generated by Django 3.2.6 on 2021-08-21 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20210821_1824'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meeting',
            options={'verbose_name': 'Совещание', 'verbose_name_plural': 'Совещания'},
        ),
    ]