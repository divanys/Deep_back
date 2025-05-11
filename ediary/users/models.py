from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.db import IntegrityError


from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


# 1. Для предметника
class DisciplinePrepod(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name='disciplineprepod'  # Добавляем related_name
    )
    first_name = models.CharField(max_length=40, null=True)
    middle_name = models.CharField(max_length=40, null=True)
    last_name = models.CharField(max_length=40, null=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True)
    date_input = models.DateField(auto_now_add=True, null=True)
    date_output = models.DateField(blank=True, null=True)
    actions = models.TextField(null=True, blank=True)
    # Добавим связь с дисциплиной, если нужно
    # discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, null=True)

# 2. Для куратора
class TutorPrepod(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=40, null=True)
    middle_name = models.CharField(max_length=40, null=True)
    last_name = models.CharField(max_length=40, null=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True)
    date_input = models.DateField(auto_now_add=True, null=True)
    date_output = models.DateField(blank=True, null=True)
    actions = models.TextField(null=True, blank=True)
    # Дополнительные связи при необходимости
    # group = models.ForeignKey(StudentGroup, on_delete=models.SET_NULL, null=True)

# 3. Родитель
class Guardian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True)
    date_input = models.DateField(auto_now_add=True, null=True)
    date_output = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# 4. Студент
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    date_birthday = models.DateField()
    is_learning = models.BooleanField(default=True)
    is_headman = models.BooleanField(default=False)
    guardian = models.ForeignKey('users.Guardian', on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey('schedules.Group', on_delete=models.CASCADE, null=True, blank=True)
    date_input = models.DateField(null=True, blank=True)
    date_output = models.DateField(null=True, blank=True)

    sub_groups = models.ManyToManyField('schedules.SubGroup', related_name='students')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
