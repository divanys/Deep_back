from django.db import models
from django.contrib.postgres.fields import ArrayField

# 1. Журнал
class Journal(models.Model):
    date_birthday = models.DateField(auto_now_add=True)
    date_die = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Journal {self.id}'


# 2. Дисциплина
class Discipline(models.Model):
    name = models.CharField(max_length=140, unique=True)
    count_of_hours = models.IntegerField()
    course_number = ArrayField(models.IntegerField(), blank=True, default=list)  # Для хранения массива чисел
    semestr_number = ArrayField(models.IntegerField(), blank=True, default=list)

    def __str__(self):
        return self.name


# 3. Страница журнала
class JournalPage(models.Model):
    name = models.CharField(max_length=140)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


# 4. Тема
class Theme(models.Model):
    name = models.CharField(max_length=140)
    count_of_hours = models.IntegerField()
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# 5. Содержание темы
class ContentTheme(models.Model):
    name = models.TextField()
    count_of_hours = models.IntegerField()
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# 6. Уроки
class Lesson(models.Model):
    date_done = models.DateField()
    date_fill = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)
    homework = models.TextField(null=True, blank=True)
    comment_for_lessons = models.TextField(null=True, blank=True)
    load_dpgsg = models.ForeignKey('schedules.LoadDPGSG', on_delete=models.CASCADE)
    journal_page = models.ForeignKey(JournalPage, on_delete=models.CASCADE)

    def __str__(self):
        return f'Lesson {self.id}'


# 7. Успеваемость студента
class ProgressStudent(models.Model):
    MARK_CHOICES = [(i, str(i)) for i in range(2, 6)]
    OFFSET_MARK_CHOICES = [('зачёт', 'Зачёт'), ('не зачёт', 'Не зачёт')]
    ATTENDANCE_CHOICES = [(1, 'Присутствовал'), (2, 'Отсутствовал по УП'), (3, 'Отсутствовал')]

    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL)
    mark = models.IntegerField(choices=MARK_CHOICES, null=True, blank=True)
    offset_mark = models.CharField(max_length=10, choices=OFFSET_MARK_CHOICES, null=True, blank=True)
    attendance = models.IntegerField(choices=ATTENDANCE_CHOICES)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)
    student = models.ForeignKey('users.Student', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Progress for {self.student}'


# 8. Результаты семестра
class SemesterResult(models.Model):
    OFFSET_MARK_CHOICES = [('зачёт', 'Зачёт'), ('не зачёт', 'Не зачёт')]
    MARK_CHOICES = [(i, str(i)) for i in range(2, 6)]

    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, null=True, blank=True)
    journal_page = models.ForeignKey(JournalPage, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    number_semestr = models.IntegerField()
    offset_mark_1 = models.CharField(max_length=10, choices=OFFSET_MARK_CHOICES, null=True, blank=True)
    offset_mark_2 = models.CharField(max_length=10, choices=OFFSET_MARK_CHOICES, null=True, blank=True)
    mark_1 = models.IntegerField(choices=MARK_CHOICES, null=True, blank=True)
    mark_2 = models.IntegerField(choices=MARK_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'Result for {self.student}'
