# Generated by Django 3.2.6 on 2021-08-20 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phonenumber',
            field=models.CharField(default=89991234567, max_length=10, verbose_name='Номер телефона'),
            preserve_default=False,
        ),
    ]
