from django.contrib import admin
from .models import User, Guardian, Student, DisciplinePrepod, TutorPrepod
import pandas as pd
import random
import string
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from .models import User, Guardian, Student, DisciplinePrepod, TutorPrepod
from django.contrib.auth.hashers import make_password
import os
import datetime


from .utils import parse_docx_to_student_xlsx  

# Регистрируем модели в админке
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email',)
    list_filter = ('is_active', 'is_staff')
    
class GuardianAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'date_input', 'date_output')
    search_fields = ('first_name', 'last_name', 'phone_number')

EXPORT_FILENAME = "generated_students.xlsx"

# Функции генерации логина и пароля
def generate_login():
    unique_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"student_{unique_id}"

def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Функция создания пользователя в БД с хэшированным паролем
def create_user(student):
    password = student["password"]
    user = User.objects.create(
        email=student["username"],
        is_superuser=False,
        is_active=True,
        is_staff=False,
    )
    user.set_password(password)  # Хэшируем пароль перед сохранением
    user.save()
    return user

# Функция создания студента в БД
def create_student(student, user):
    Student.objects.create(
        user=user,
        first_name=student.get("first_name"),
        middle_name=student.get("middle_name"),
        last_name=student.get("last_name"),
        date_birthday=student.get("date_birthday"),
        is_learning=student.get("is_learning"),
        is_headman=student.get("is_headman"),
        guardian=student.get("guardian"),
        date_input=student.get("date_input"),
        date_output=student.get("date_output"),
    )

# Класс импорта студентов через админку
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_birthday', 'is_learning')
    search_fields = ('first_name', 'last_name')
    list_filter = ('is_learning',)
    change_list_template = "admin/student_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-xlsx/', self.import_xlsx, name='import_xlsx'),
            path('download-xlsx/', self.download_xlsx, name='download_xlsx'),
            path('parse-docx/', self.parse_docx_view, name='parse_docx'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['import_xlsx_url'] = reverse('admin:import_xlsx')
        extra_context['download_xlsx_url'] = reverse('admin:download_xlsx')
        extra_context['parse_docx_url'] = reverse('admin:parse_docx')

        return super().changelist_view(request, extra_context=extra_context)

    def import_xlsx(self, request):
        if request.method == "POST" and request.FILES.get('xlsx_file'):
            xlsx_file = request.FILES['xlsx_file']
            df = pd.read_excel(xlsx_file, dtype=str).fillna("")
            
            students = []
            for _, row in df.iterrows():
                try:
                    date_birthday = pd.to_datetime(row["date_birthday"]).strftime("%Y-%m-%d")
                    date_input = pd.to_datetime(row["date_input"]).strftime("%Y-%m-%d")

                    is_headman_str = row.get("is_headman", "").strip().upper()
                    is_headman = is_headman_str in ["ИСТИНА", "TRUE", "1"]



                    student_data = {
                        "username": generate_login(),
                        "password": generate_password(),
                        "first_name": row["first_name"],
                        "middle_name": row.get("middle_name", ""),
                        "last_name": row["last_name"],
                        "date_birthday": date_birthday,
                        "is_learning": True,
                        "is_headman": is_headman,
                        "guardian": None,
                        "date_input": date_input,
                        "date_output": None
                    }

                    user = create_user(student_data)
                    create_student(student_data, user)
                    students.append(student_data)

                except Exception as e:
                    messages.error(request, f"Ошибка при обработке строки: {e}")
            
            self.save_to_excel(students)
            messages.success(request, f"Импортировано {len(students)} студентов. Файл с логинами и паролями доступен для скачивания.")
            return redirect("..")

        return TemplateResponse(request, "admin/upload_xlsx.html")

    def save_to_excel(self, students):
        df = pd.DataFrame(students)
        df.to_excel(EXPORT_FILENAME, index=False)

    def download_xlsx(self, request):
        if os.path.exists(EXPORT_FILENAME):
            with open(EXPORT_FILENAME, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename={EXPORT_FILENAME}'
                return response
        messages.error(request, "Файл не найден.")
        return redirect("..")

    def parse_docx_view(self, request):
        if request.method == "POST" and request.FILES.get("docx_file"):
            docx_file = request.FILES["docx_file"]
            output_filename = EXPORT_FILENAME  # или можно сделать уникальным
            parse_docx_to_student_xlsx(docx_file, output_filename)
            messages.success(request, f"Файл преобразован в Excel: {EXPORT_FILENAME}")
            return redirect("..")

        return TemplateResponse(request, "admin/parse_docx_upload.html")


# Класс импорта куратороы через админку
class TutorPrepodAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'date_input')
    search_fields = ('first_name', 'last_name', 'middle_name')
    change_list_template = "admin/tutorprepod_changelist.html"
    EXPORT_FILENAME = "generated_curators.xlsx"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-curators-xlsx/', self.import_xlsx, name='import_curators_xlsx'),
            path('download-curators-xlsx/', self.download_xlsx, name='download_curators_xlsx'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({
            'import_curators_xlsx_url': reverse('admin:import_curators_xlsx'),
            'download_curators_xlsx_url': reverse('admin:download_curators_xlsx'),
        })
        return super().changelist_view(request, extra_context=extra_context)

    def import_xlsx(self, request):
        if request.method == "POST" and request.FILES.get("xlsx_file"):
            xlsx_file = request.FILES["xlsx_file"]
            df = pd.read_excel(xlsx_file, dtype=str).fillna("")
            created = []

            for _, row in df.iterrows():
                try:
                    # Генерация учетных данных
                    login = generate_login().replace("student", "curator")
                    password = generate_password()
                    
                    # Парсинг дат
                    date_input = pd.to_datetime(row.get("date_input", datetime.date.today())).strftime("%Y-%m-%d")
                    date_output = pd.to_datetime(row["date_output"]).strftime("%Y-%m-%d") if row.get("date_output") else None

                    # Создание пользователя
                    user = User.objects.create(
                        email=login,
                        is_active=True,
                        is_staff=False,
                    )
                    user.set_password(password)
                    user.save()

                    # Создание записи куратора
                    curator = TutorPrepod.objects.create(
                        user=user,
                        first_name=row["first_name"],
                        last_name=row["last_name"],
                        middle_name=row.get("middle_name", ""),
                    )

                    created.append({
                        "username": login,
                        "password": password,
                        "first_name": curator.first_name,
                        "last_name": curator.last_name,
                        "middle_name": curator.middle_name,
                        "phone_number": curator.phone_number,
                        "date_input": date_input,
                        "date_output": date_output,
                    })

                except Exception as e:
                    messages.error(request, f"Ошибка в строке {_ + 2}: {str(e)}")
                    continue

            self.save_to_excel(created)
            messages.success(request, f"Успешно импортировано {len(created)} кураторов")
            return redirect("..")

        return TemplateResponse(request, "admin/upload_xlsx.html")

    def save_to_excel(self, data):
        df = pd.DataFrame(data)
        df.to_excel(self.EXPORT_FILENAME, index=False)

    def download_xlsx(self, request):
        if os.path.exists(self.EXPORT_FILENAME):
            with open(self.EXPORT_FILENAME, 'rb') as f:
                response = HttpResponse(
                    f.read(),
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = f'attachment; filename={self.EXPORT_FILENAME}'
                return response
        messages.error(request, "Файл для скачивания не найден")
        return redirect("..")

# Класс импорта предметника через админку
class DisciplinePrepodAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'date_input')
    search_fields = ('first_name', 'last_name', 'middle_name')
    change_list_template = "admin/disciplineprepod_changelist.html"
    EXPORT_FILENAME = "generated_discipline_prepods.xlsx"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-discipline-xlsx/', self.import_xlsx, name='import_discipline_xlsx'),
            path('download-discipline-xlsx/', self.download_xlsx, name='download_discipline_xlsx'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({
            'import_discipline_xlsx_url': reverse('admin:import_discipline_xlsx'),
            'download_discipline_xlsx_url': reverse('admin:download_discipline_xlsx'),
        })
        return super().changelist_view(request, extra_context=extra_context)

    def import_xlsx(self, request):
        if request.method == "POST" and request.FILES.get("xlsx_file"):
            xlsx_file = request.FILES["xlsx_file"]
            df = pd.read_excel(xlsx_file, dtype=str).fillna("")
            created = []

            for index, row in df.iterrows():
                try:
                    # Генерация учетных данных
                    login = f"teacher_{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}"
                    password = generate_password()
                    
                    # Парсинг данных
                    date_input = pd.to_datetime(row.get("date_input", datetime.date.today())).strftime("%Y-%m-%d")
                    date_output = pd.to_datetime(row["date_output"]).strftime("%Y-%m-%d") if row.get("date_output") else None

                    # Создание пользователя
                    user = User.objects.create(
                        email=login,
                        is_active=True,
                        is_staff=False,
                    )
                    user.set_password(password)
                    user.save()

                    # Создание записи преподавателя
                    discipline_prepod = DisciplinePrepod.objects.create(
                        user=user,
                        first_name=row["first_name"],
                        last_name=row["last_name"],
                        middle_name=row.get("middle_name", ""),
                        date_input=date_input,
                        date_output=date_output,
                    )

                    created.append({
                        "username": login,
                        "password": password,
                        "first_name": discipline_prepod.first_name,
                        "last_name": discipline_prepod.last_name,
                        "middle_name": discipline_prepod.middle_name,
                        "phone_number": discipline_prepod.phone_number,
                        "date_input": date_input,
                        "date_output": date_output,
                    })

                except Exception as e:
                    messages.error(request, f"Ошибка в строке {index + 2}: {str(e)}")
                    continue

            self.save_to_excel(created)
            messages.success(request, f"Успешно импортировано {len(created)} преподавателей")
            return redirect("..")

        return TemplateResponse(request, "admin/upload_xlsx.html")

    def save_to_excel(self, data):
        df = pd.DataFrame(data)
        df.to_excel(self.EXPORT_FILENAME, index=False)

    def download_xlsx(self, request):
        if os.path.exists(self.EXPORT_FILENAME):
            with open(self.EXPORT_FILENAME, 'rb') as f:
                response = HttpResponse(
                    f.read(),
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = f'attachment; filename={self.EXPORT_FILENAME}'
                return response
        messages.error(request, "Файл для скачивания не найден")
        return redirect("..")

   



# Регистрируем администраторов моделей
admin.site.register(User, UserAdmin)
admin.site.register(Guardian, GuardianAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(DisciplinePrepod, DisciplinePrepodAdmin)
admin.site.register(TutorPrepod, TutorPrepodAdmin)
