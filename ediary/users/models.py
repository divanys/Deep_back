from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.db import IntegrityError


class UserManager(BaseUserManager):    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
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


# 1. Предметник
class DisciplinePrepod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # заменили на User
    actions = models.TextField(null=True, blank=True)


# 2. Куратор
class TutorPrepod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # заменили на User
    actions = models.TextField(null=True, blank=True)


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
