from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .models import LoadDPGSG 

def load_excel_view(request):
    if request.method == 'POST' and 'excel_file' in request.FILES:
        # Загружаем файл
        excel_file = request.FILES['excel_file']
        
        # Используем pandas для чтения данных из Excel
        try:
            df = pd.read_excel(excel_file)
            
            # Обрабатываем данные и сохраняем их в модель LoadDPGSG
            for _, row in df.iterrows():
                LoadDPGSG.objects.create(
                    discipline=row['Дисциплина'],
                    group=row['Группа'],
                    discipline_prepod=row['Преподаватель'],
                    fack_count_number=row['Нагрузка, час.'],
                )
            
            print('Файл успешно загружен и данные добавлены в таблицу!')
            return HttpResponse('Файл успешно загружен и данные добавлены в таблицу!')
        
        except Exception as e:
            print(f'Ошибка при обработке файла: {str(e)}')
            return HttpResponse(f'Ошибка при обработке файла: {str(e)}')

    return render(request, 'schedules/load_excel.html')
