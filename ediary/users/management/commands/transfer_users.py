from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from users.models import User, Prepod, Guardian, Student

class Command(BaseCommand):
    help = 'Transfer existing user data to the User model'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data transfer...'))

        # === Перенос данных для Prepod ===
        prepods = Prepod.objects.all()
        for prepod in prepods:
            if not User.objects.filter(email=prepod.email).exists():
                user = User.objects.create(
                    email=prepod.email,
                    password=make_password(prepod.password) if prepod.password else None
                )
                prepod.user = user
                prepod.save()

        self.stdout.write(self.style.SUCCESS(f'Transferred {prepods.count()} prepods'))

        # === Перенос данных для Guardian ===
        guardians = Guardian.objects.all()
        for guardian in guardians:
            if not User.objects.filter(email=guardian.email).exists():
                user = User.objects.create(
                    email=guardian.email,
                    password=make_password(guardian.password) if guardian.password else None
                )
                guardian.user = user
                guardian.save()

        self.stdout.write(self.style.SUCCESS(f'Transferred {guardians.count()} guardians'))

        # === Перенос данных для Student ===
        students = Student.objects.all()
        for student in students:
            if not User.objects.filter(email=student.email).exists():
                user = User.objects.create(
                    email=student.email,
                    password=make_password(student.password) if student.password else None
                )
                student.user = user
                student.save()

        self.stdout.write(self.style.SUCCESS(f'Transferred {students.count()} students'))

        self.stdout.write(self.style.SUCCESS('Data transfer completed successfully!'))
