from django.http import HttpResponse
from django.http import JsonResponse
from .models import Student
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def auth(request):
    if request.method == 'POST':
        try:
            # Проверяем, что тело запроса непустое
            if not request.body:
                return JsonResponse({'error': 'Пустое тело запроса'}, status=400)
            
            # Загружаем JSON
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({'error': 'Не указаны email или пароль'}, status=400)

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)

                # Определяем роль пользователя
                if hasattr(user.disciplineprepod, 'disciplineprepod'):
                    role = 'discipline_prepod'
                if hasattr(user.tutorprepod, 'tutorprepod'):
                    role = 'tutor_prepod'
                elif hasattr(user, 'student'):
                    role = 'student'
                elif hasattr(user, 'guardian'):
                    role = 'guardian'
                else:
                    role = 'admin'

                return JsonResponse({'message': 'Успешный вход', 'role': role})
            else:
                print(email, password)
                return JsonResponse({'error': 'Неверный email или пароль'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Некорректный JSON'}, status=400)

    return JsonResponse({'error': 'Метод не разрешён'}, status=405)


def index(request):
    return HttpResponse("Hello METANIT.COM")


def student_list(request):
    students = Student.objects.all().values('id', 'first_name', 'last_name')
    if not students.exists():
        return JsonResponse({'error': 'No students found'}, status=404)
    return JsonResponse(list(students), safe=False)