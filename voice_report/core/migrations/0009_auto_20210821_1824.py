# Generated by Django 3.2.6 on 2021-08-21 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_transcript_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='project',
        ),
        migrations.AddField(
            model_name='meeting',
            name='status',
            field=models.IntegerField(choices=[(0, 'Проверка'), (1, 'Готово'), (2, 'На согласовании')], default=0),
        ),
        migrations.AddField(
            model_name='meeting',
            name='theme',
            field=models.CharField(default='', max_length=1000, verbose_name='Тема'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transcript',
            name='status',
            field=models.IntegerField(choices=[(0, 'Получение аудио'), (1, 'Получение текста'), (2, 'Готово')], default=0),
        ),
    ]
