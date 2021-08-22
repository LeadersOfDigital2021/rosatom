# Generated by Django 3.2.6 on 2021-08-21 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20210822_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='num_protocol',
            field=models.CharField(default=1, max_length=10, verbose_name='Номер протокола'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.IntegerField(choices=[(0, 'Получение аудио'), (1, 'Получение текста'), (2, 'Готово'), (3, 'На согласовании')], default=0, verbose_name='Статус'),
        ),
    ]