from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from django.db import models

# 1. Преподаватель
class Prepod(models.Model):
    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    date_birthday = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    date_input = models.DateField(auto_now_add=True)
    date_output = models.DateField(null=True, blank=True)
    pswd = models.CharField(max_length=100)
    
    def set_password(self, raw_password):
        self.pswd = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.pswd)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# 2. Предметник
class DisciplinePrepod(models.Model):
    prepod = models.ForeignKey(Prepod, on_delete=models.CASCADE)
    actions = models.TextField(null=True, blank=True)



# 3. Куратор
class TutorPrepod(models.Model):
    prepod = models.ForeignKey(Prepod, on_delete=models.CASCADE)
    actions = models.TextField(null=True, blank=True)


# 4. Родитель
class Guardian(models.Model):
    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    pswd = models.CharField(max_length=100)
    date_input = models.DateField(auto_now_add=True, null=True)  # Заполняется автоматически при создании
    date_output = models.DateField(blank=True, null=True)  # Может быть пустым


    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def set_password(self, raw_password):
        self.pswd = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.pswd)

# 5. Студент
class Student(models.Model):
    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    date_birthday = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    is_learning = models.BooleanField(default=True)
    is_headman = models.BooleanField(default=False)
    guardian = models.ForeignKey('users.Guardian', on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey('schedules.Group', on_delete=models.CASCADE)
    password = models.CharField(max_length=128, null=True, blank=True)
    date_input = models.DateField(null=True, blank=True)
    date_output = models.DateField(null=True, blank=True)

    # Прямое указание на связь с SubGroup
    sub_groups = models.ManyToManyField('schedules.SubGroup', related_name='students')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
