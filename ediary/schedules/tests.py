# schedules/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from schedules.models import LoadDPGSG, Group, SubGroup
from grades.models import Lesson, ProgressStudent, Journal, Discipline, JournalPage
from users.models import DisciplinePrepod

User = get_user_model()

class LessonTestCase(TestCase):
    def setUp(self):
        # Создаем пользователя и преподавателя
        self.user = User.objects.create_user(email='teacher@test.com', password='testpass123')
        self.discipline_prepod = DisciplinePrepod.objects.create(user=self.user)
        
        # Создаем журнал
        self.journal = Journal.objects.create()
        
        # Создаем группу
        self.group = Group.objects.create(
            name="TEST-101",
            journal=self.journal,
            tutor_prepod=None
        )
        
        # Создаем дисциплину
        self.discipline = Discipline.objects.create(
            name="Математика",
            count_of_hours=100
        )
        
        # Создаем нагрузку
        self.load = LoadDPGSG.objects.create(
            discipline=self.discipline,
            discipline_prepod=self.discipline_prepod,
            group=self.group
        )
        
        # Создаем страницу журнала
        self.journal_page = JournalPage.objects.create(
            name="Страница 1",
            journal=self.journal,
            discipline=self.discipline
        )

    def test_lesson_creation(self):
        self.client.login(email='teacher@test.com', password='testpass123')
        response = self.client.post(f'/lesson/{self.load.id}/', {
            'homework': 'Test homework',
            'form-0-attendance': 1,
            'form-0-mark': 5,
            'form-TOTAL_FORMS': 1,
            'form-INITIAL_FORMS': 0
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(ProgressStudent.objects.first().mark, 5)