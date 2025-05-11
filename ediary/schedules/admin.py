from django.contrib import admin
from .models import Group, SubGroup, LoadDPGSG
import pandas as pd
from django.contrib import admin
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from .models import Group, SubGroup, LoadDPGSG
from users.models import DisciplinePrepod
from grades.models import Discipline
from .forms import ExcelUploadForm
from django.urls import path

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'tutor_prepod')
    search_fields = ('name', 'specialization')

class SubGroupAdmin(admin.ModelAdmin):
    list_display = ('group', 'discipline', 'number_sub_group')
    search_fields = ('group__name', 'discipline__name')


# Функция импорта данных из Excel
def import_load_from_excel(file):
    # Чтение данных из Excel
    df = pd.read_excel(file, sheet_name=0, skiprows=2)  # Пропускаем первые две строки заголовков

    # Процесс записи в базу данных
    for index, row in df.iterrows():
        try:
            # Считываем значения из строк
            discipline_name = row['Дисциплина']
            group_name = row['Группа']
            teacher_name = row['Преподаватель']
            load_hours = row['Нагрузка, час.']

            # Получаем дисциплину из модели Discipline (по имени)
            discipline = Discipline.objects.get(name=discipline_name)
            
            # Получаем группу из модели Group (по имени)
            group = Group.objects.get(name=group_name)

            # Получаем преподавателя из модели DisciplinePrepod (по имени преподавателя)
            teacher = DisciplinePrepod.objects.get(user__email=teacher_name)

            # Создаём запись нагрузки (LoadDPGSG)
            LoadDPGSG.objects.create(
                discipline=discipline,
                discipline_prepod=teacher,
                group=group,
                fack_count_number=load_hours,
                is_teaching=True,  # Если преподавание ведется, можно добавить логику, чтобы изменить это значение
            )

        except ObjectDoesNotExist as e:
            print(f"Ошибка при добавлении данных: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")


# Кастомное представление для обработки загрузки файла
def load_excel_view(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Получаем файл из формы
            file = request.FILES['excel_file']
            
            # Вызываем функцию для импорта данных
            import_load_from_excel(file)
            return HttpResponse("Данные успешно загружены.")
    else:
        form = ExcelUploadForm()

    return render(request, 'admin/load_excel.html', {'form': form})


# Настройка админки
class LoadDPGSGAdmin(admin.ModelAdmin):
    change_list_template = "admin/load_excel.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('load-excel/', load_excel_view, name='load_excel'),
        ]
        return custom_urls + urls



# Регистрация моделей в админке
admin.site.register(Group, GroupAdmin)
admin.site.register(SubGroup, SubGroupAdmin)
admin.site.register(LoadDPGSG, LoadDPGSGAdmin)
