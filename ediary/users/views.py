from django.http import HttpResponse
from django.http import JsonResponse
from .models import Student


def index(request):
    return HttpResponse("Hello METANIT.COM")

def student_list(request):
    students = Student.objects.all().values('id', 'first_name', 'last_name')
    if not students.exists():
        return JsonResponse({'error': 'No students found'}, status=404)
    return JsonResponse(list(students), safe=False)