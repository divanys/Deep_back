import pandas as pd
import re
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from grades.models import Discipline
from users.models import DisciplinePrepod
from schedules.models import Group, LoadDPGSG

class Command(BaseCommand):
    help = 'Parse XLSX file and populate the database'

    def handle(self, *args, **options):
        # Замените путь на актуальный
        df = pd.read_excel('1 семестр21-22.xlsx', sheet_name='1 семестр21-22', header=5)

        # Удалить пустые строки
        df = df.dropna(subset=['Дисциплина', 'Группа', 'Преподаватель'])

        # Обработка данных
        for _, row in df.iterrows():
            try:
                # --- Обработка Дисциплины ---
                discipline_name = row['Дисциплина'].strip()
                discipline, created = Discipline.objects.get_or_create(
                    name=discipline_name,
                    defaults={
                        'count_of_hours': int(row['Нагрузка, час.']),  # Используйте актуальную колонку
                        'course_number': [],  # Заполните при необходимости
                        'semestr_number': [], # Заполните при необходимости
                    }
                )

                # --- Обработка Группы ---
                group_name = row['Группа'].strip()
                group, _ = Group.objects.get_or_create(
                    name=group_name,
                    defaults={
                        'specialization': 'Специализация',  # Заполните при необходимости
                        'journal': None,  # Заполните при наличии журнала
                        'tutor_prepod': None,  # Заполните при наличии куратора
                    }
                )

                # --- Обработка Преподавателя ---
                prepod_fullname = re.sub(r'^[^А-Яа-я]*', '', row['Преподаватель'].strip())
                prepod_names = prepod_fullname.split()
                last_name = prepod_names[0]
                first_name = prepod_names[1] if len(prepod_names) > 1 else ''
                middle_name = prepod_names[2] if len(prepod_names) > 2 else ''

                prepod, _ = DisciplinePrepod.objects.get_or_create(
                    last_name=last_name,
                    first_name=first_name,
                    middle_name=middle_name,
                )

                # --- Создание связи LoadDPGSG ---
                LoadDPGSG.objects.create(
                    discipline=discipline,
                    discipline_prepod=prepod,
                    group=group,
                    sub_group=None,  # Подгруппа не указана в Excel
                    fack_count_number=int(row['факт']),  # Используйте актуальную колонку
                )

            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка в строке {row}: {e}'))

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))