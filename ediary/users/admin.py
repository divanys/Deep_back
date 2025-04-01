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
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['import_xlsx_url'] = reverse('admin:import_xlsx')
        extra_context['download_xlsx_url'] = reverse('admin:download_xlsx')
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

                    student_data = {
                        "username": generate_login(),
                        "password": generate_password(),
                        "first_name": row["first_name"],
                        "middle_name": row.get("middle_name", ""),
                        "last_name": row["last_name"],
                        "date_birthday": date_birthday,
                        "is_learning": True,
                        "is_headman": row.get("is_headman", False),
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

class DisciplinePrepodAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__email',)

class TutorPrepodAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__email',)

# Регистрируем администраторов моделей
admin.site.register(User, UserAdmin)
admin.site.register(Guardian, GuardianAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(DisciplinePrepod, DisciplinePrepodAdmin)
admin.site.register(TutorPrepod, TutorPrepodAdmin)
