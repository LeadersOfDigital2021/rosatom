from django.db import models
from django.contrib.auth.models import AbstractUser, Group, BaseUserManager

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

    def __str__(self):
        return self.email

    objects = UserManager()

    def get_short_name(self):
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


class EmployeeRole(models.Model):
    """ Роль сотрудника на совещании """
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    have_signature = models.BooleanField(
        verbose_name='Имеет право подписи',
        default=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Роль сотрудника'
        verbose_name_plural = 'Роли сотрудников'


class Transcript(models.Model):

    STATUS_TYPE = (
        (0, 'Получение аудио'),
        (1, 'Получение текста'),
        (2, 'Готово'),
    )
    video_file = models.FileField(
        verbose_name='Видеозапись',
        upload_to='video/'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    audio_file = models.FileField(
        verbose_name='Аудиозапись',
        upload_to='audio/',
        blank=True,
        null=True,
    )
    text = models.TextField(
        verbose_name='Текст',
        blank=True,
        null=True,
    )
    status = models.IntegerField(
        default=0,
        choices=STATUS_TYPE,
    )

    def __str__(self):
        return self.name


class Meeting(models.Model):
    """ Совещание """
    STATUS_TYPE = (
        (0, 'Проверка'),
        (1, 'Готово'),
        (2, 'На согласовании'),
    )
    status = models.IntegerField(
        default=0,
        choices=STATUS_TYPE,
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


class EmployeeRolesInMeeting(models.Model):
    """ Связующая сущность для связи роли сотрудника в совещании """
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
    role = models.ForeignKey(
        EmployeeRole,
        verbose_name='Роль',
        on_delete=models.CASCADE,
        related_name='roles_in_meeting',
    )

    def __str__(self):
        return f"{self.meeting} - {self.role} - {self.employee}"

    class Meta:
        verbose_name = 'Роль сотрудника на совещании'
        verbose_name_plural = 'Роли сотрудников на совещании'
