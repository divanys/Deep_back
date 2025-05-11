from django.http import HttpResponse
from django.http import JsonResponse
from .models import Student, TutorPrepod, DisciplinePrepod
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@require_http_methods(["POST", "OPTIONS", "GET"])
@csrf_exempt
def auth(request):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response["Access-Control-Allow-Headers"] = "content-type"
        return response
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({'error': 'Email and password required'}, status=400)

            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                
                # Определяем роль пользователя
                role = 'unknown'  
                if hasattr(user, 'student'):
                    role = 'student'
                elif hasattr(user, 'tutorprepod'):  # Добавляем проверку на куратора
                    role = 'curator'
                elif hasattr(user, 'disciplineprepod'):
                     role = 'teacher'
                elif user.is_superuser:
                    role = 'admin'
                
                print(f"User {user.email} auth check:")
                print(f"Student: {hasattr(user, 'student')}")
                print(f"TutorPrepod: {hasattr(user, 'tutorprepod')}")
                print(f"DisciplinePrepod: {hasattr(user, 'disciplineprepod')}")
               
                return JsonResponse({
                    'token': token.key,
                    'role': role,
                    'email': user.email,
                })
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def student_info(request):
    response_data = {}
    status_code = 200

    try:
        user = request.user
        student = Student.objects.select_related("group").get(user=user)
        response_data = {
            "first_name": student.first_name,
            "last_name": student.last_name,
            "middle_name": student.middle_name,
            "group": student.group.name if student.group else None
        }
    except Student.DoesNotExist:
        response_data = {"error": "Student data not found"}
        status_code = 404

    response = JsonResponse(response_data, status=status_code)
    response["Access-Control-Allow-Origin"] = "http://localhost:5173"
    return response


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def curator_info(request):
    response_data = {}
    status_code = 200

    try:
        user = request.user
        tutor = TutorPrepod.objects.select_related("user").get(user=user)
        response_data = {
            "first_name": tutor.first_name,
            "last_name": tutor.last_name,
            "middle_name": tutor.middle_name,
            "date_input": tutor.date_input,
            "date_output": tutor.date_output
        }
    except TutorPrepod.DoesNotExist:
        response_data = {"error": "Curator data not found"}
        status_code = 404

    response = JsonResponse(response_data, status=status_code)
    response["Access-Control-Allow-Origin"] = "http://localhost:5173"
    return response


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def teacher_info(request):
    response_data = {}
    status_code = 200

    try:
        user = request.user
        discipline_prepod = DisciplinePrepod.objects.select_related("user").get(user=user)
        response_data = {
            "first_name": discipline_prepod.first_name,
            "last_name": discipline_prepod.last_name,
            "middle_name": discipline_prepod.middle_name,
            "date_input": discipline_prepod.date_input,
            "date_output": discipline_prepod.date_output
        }
    except DisciplinePrepod.DoesNotExist:
        response_data = {"error": "Discipline teacher data not found"}
        status_code = 404

    response = JsonResponse(response_data, status=status_code)
    response["Access-Control-Allow-Origin"] = "http://localhost:5173"
    return response



def index(request):
    return HttpResponse("Hello METANIT.COM")


def student_list(request):
    students = Student.objects.all().values('id', 'first_name', 'last_name')
    if not students.exists():
        return JsonResponse({'error': 'No students found'}, status=404)
    return JsonResponse(list(students), safe=False)


