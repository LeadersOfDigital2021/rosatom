# Generated by Django 3.2.6 on 2021-08-21 06:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_user_phonenumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('have_signature', models.BooleanField(default=False, verbose_name='Имеет право подписи')),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('agenda', models.CharField(max_length=1000, verbose_name='Повестка')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Назвние проекта')),
                ('description', models.TextField(max_length=2000, verbose_name='Описание проекта')),
            ],
        ),
        migrations.CreateModel(
            name='Transcript',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_file', models.FileField(upload_to='video/')),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution', models.TextField(verbose_name='Решение')),
                ('date_end', models.DateField(verbose_name='Срок')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='core.meeting', verbose_name='Совещание')),
                ('responible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to=settings.AUTH_USER_MODEL, verbose_name='Ответсвенный')),
            ],
        ),
        migrations.AddField(
            model_name='meeting',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetings', to='core.project', verbose_name='Проект'),
        ),
        migrations.CreateModel(
            name='EmployeeRolesInMeeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles_in_meeting', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles_in_meeting', to='core.meeting', verbose_name='Совещание')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles_in_meeting', to='core.employeerole', verbose_name='Роль')),
            ],
        ),
    ]
