# Generated by Django 3.2.6 on 2021-08-21 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210821_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcript',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='Название'),
            preserve_default=False,
        ),
    ]
