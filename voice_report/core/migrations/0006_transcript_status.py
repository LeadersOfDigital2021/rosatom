# Generated by Django 3.2.6 on 2021-08-21 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210821_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcript',
            name='status',
            field=models.IntegerField(choices=[(0, 'Получено видео'), (1, 'Получено аудио'), (2, 'Получен тектс')], default=0),
        ),
    ]
