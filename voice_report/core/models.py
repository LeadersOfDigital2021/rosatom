from django.db import models
from django.contrib.auth.models import AbstractUser, Group, BaseUserManager
import datetime


# Раздел описание моделей с пользователями
class Group(Group):
    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Не указана электронная почта пользователя')

        user = self.model(
            email=email,
        )

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.model(
            email=email
        )
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        print(user)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """ Модель пользователей (сотрудников) """
    username = None
    email = models.EmailField(
        unique=True,
    )
    phonenumber = models.CharField(
        max_length=10,
        verbose_name="Номер телефона",
        null=True,
        blank=True,
    )
    middle_name = models.CharField(
        verbose_name="Отчество",
        max_length=190,
        null=True,
        blank=True,
    )
    place = models.CharField(
        verbose_name="Должность",
        max_length=190,
        null=True,
        blank=True,
    )
    groups = models.ManyToManyField(
        Group,
        related_name='user',
        null=True,
        blank=True,
    )
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        """ Вывод фамилии и инициалов """
        short_name = self.email
        if self.last_name != "":
            short_name = f"{self.last_name} {self.first_name[0]}. {self.middle_name[0]}."
        return short_name

    class Meta:
        ordering = ['email']
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


# Раздел описания основных сущностей
class Project(models.Model):
    """ Проекты с которыми связаны совещания """
    name = models.CharField(
        verbose_name='Назвние проекта',
        max_length=100,
    )

    description = models.TextField(
        verbose_name='Описание проекта',
        max_length=2000,
    )


class PartitionTranscript(models.Model):
    """ Фрагменты стенограммы с временными метками привязанными к аудио """
    meeting = models.ForeignKey(
        "Meeting",
        verbose_name='Совещание',
        on_delete=models.CASCADE,
        related_name='partitions'
    )
    text = models.TextField(
        verbose_name='Текст',
        blank=True,
        null=True,
    )
    start_time = models.FloatField(
        verbose_name='Начало отрывка'
    )
    end_time = models.FloatField(
        verbose_name='Конец отрывка'
    )

    def get_start_time(self):
        return str(datetime.timedelta(seconds=int(self.start_time)))

    def get_end_time(self):
        return str(datetime.timedelta(seconds=int(self.end_time)))

    def get_timestamp(self):
        return int(self.start_time)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Фрагмент стенограммы'
        verbose_name_plural = 'Фрагменты стенограмм'


class Meeting(models.Model):
    """ Совещание """
    STATUS_TYPE = (
        (0, 'Получение аудио'),
        (1, 'Получение текста'),
        (2, 'Подготовлено'),
        (3, 'На согласовании'),
        (4, 'Запланировано'),
    )
    status = models.IntegerField(
        verbose_name='Статус',
        default=0,
        choices=STATUS_TYPE,
    )
    num_protocol = models.CharField(
        verbose_name='Номер протокола',
        max_length=10,
    )
    theme = models.CharField(
        verbose_name='Тема',
        max_length=1000,
    )
    date = models.DateField(
        verbose_name='Дата',
    )
    agenda = models.CharField(
        verbose_name='Повестка',
        max_length=1000,
    )
    video_file = models.FileField(
        verbose_name='Видеозапись',
        upload_to='video/',
        null=True,
        blank=True,
    )
    audio_file = models.FileField(
        verbose_name='Аудиозапись',
        upload_to='audio/',
        blank=True,
        null=True,
    )
    """ для вывода на страницу также используется МР3 для уменьшения размера файла """
    audio_file_mp3 = models.FileField(
        verbose_name='Аудиозапись в MP3',
        upload_to='audio/',
        blank=True,
        null=True,
    )
    transcript = models.TextField(
        verbose_name='Стенограмма',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'Совещание'
        verbose_name_plural = 'Совещания'


class Solution(models.Model):
    """ Решение по совещанию """
    meeting = models.ForeignKey(
        Meeting,
        verbose_name='Совещание',
        on_delete=models.CASCADE,
        related_name='solutions',
    )
    solution = models.TextField(
        verbose_name='Решение',
    )
    date_end = models.DateField(
        verbose_name='Срок',
    )
    responible = models.ForeignKey(
        User,
        verbose_name='Ответсвенный',
        on_delete=models.CASCADE,
        related_name='solutions',
    )

    def __str__(self):
        return f"{self.solution} - {self.meeting}"

    class Meta:
        verbose_name = 'Решение'
        verbose_name_plural = 'Решения'


class EmployeeRolesInMeeting(models.Model):
    """ Связующая сущность для связи роли сотрудника в совещании """
    ROLE_TYPE=(
        (0, 'Присутвующий'),
        (1, 'Секретарь'),
        (2, 'Председательствующий'),
    )
    employee = models.ForeignKey(
        User,
        verbose_name='Сотрудник',
        on_delete=models.CASCADE,
        related_name='roles_in_meeting',
    )
    meeting = models.ForeignKey(
        Meeting,
        verbose_name='Совещание',
        on_delete=models.CASCADE,
        related_name='roles_in_meeting',
    )
    role = models.IntegerField(
        verbose_name='Роль',
        default=0,
        choices=ROLE_TYPE,
    )
    report_send = models.BooleanField(
        verbose_name='Протокол отрпавлен',
        default=False,
    )
    report_read = models.BooleanField(
        verbose_name='Ознакомлен',
        default=False
    )
    report_url = models.URLField(
        verbose_name='Ссылка на протокол',
        blank=True,
        null=True,
        max_length=200,
    )

    def __str__(self):
        return f"{self.meeting} - {self.employee} - {self.role}"

    class Meta:
        verbose_name = 'Роль сотрудника на совещании'
        verbose_name_plural = 'Роли сотрудников на совещании'
