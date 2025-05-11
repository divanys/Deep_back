from django.db import models

# 1. Группа
class Group(models.Model):
    name = models.CharField(max_length=10, unique=True)
    specialization = models.CharField(max_length=40)
    journal = models.ForeignKey('grades.Journal', on_delete=models.CASCADE, null=True, blank=True)
    tutor_prepod = models.ForeignKey('users.TutorPrepod', on_delete=models.SET_NULL, null=True, blank=True)  

    def __str__(self):
        return self.name

# 2. Подгруппа
class SubGroup(models.Model):
    group = models.ForeignKey('schedules.Group', on_delete=models.CASCADE)
    discipline = models.ForeignKey('grades.Discipline', on_delete=models.SET_NULL, null=True, blank=True)
    number_sub_group = models.IntegerField()

    def __str__(self):
        return f'{self.group.name} - Подгруппа {self.number}'


# 3. Нагрузка
class LoadDPGSG(models.Model):
    discipline = models.ForeignKey('grades.Discipline', on_delete=models.SET_NULL, null=True)
    discipline_prepod = models.ForeignKey('users.DisciplinePrepod', on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sub_group = models.ForeignKey(SubGroup, on_delete=models.CASCADE, null=True, blank=True)
    fack_count_number = models.IntegerField(default=0)
    is_teaching = models.BooleanField(default=True)
    date_input_to_group = models.DateField(auto_now_add=True)
