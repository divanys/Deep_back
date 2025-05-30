from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from schedules.models import LoadDPGSG
from users.models import Student
from .models import Lesson, ProgressStudent
from .forms import LessonForm, ProgressStudentFormSet

@login_required
def lesson_management(request, load_id):
    load = get_object_or_404(LoadDPGSG, id=load_id)
    
    # Проверка прав доступа преподавателя
    if not hasattr(request.user, 'disciplineprepod') or request.user.disciplineprepod != load.discipline_prepod:
        return redirect('access_denied')
    
    # Получаем или создаем урок
    lesson, created = Lesson.objects.get_or_create(
        load_dpgsg=load,
        date_done=timezone.now().date(),
        defaults={
            'journal_page': load.group.journal.journalpage_set.first(),
        }
    )
    
    # Получаем студентов
    students = Student.objects.filter(group=load.group)
    if load.sub_group:
        students = students.filter(sub_groups=load.sub_group)
    
    # Создаем прогресс студентов если урок новый
    if created:
        for student in students:
            ProgressStudent.objects.create(
                lesson=lesson,
                student=student,
                attendance=1  # По умолчанию "Присутствовал"
            )
    
    if request.method == 'POST':
        lesson_form = LessonForm(request.POST, instance=lesson)
        formset = ProgressStudentFormSet(request.POST, instance=lesson)
        
        if lesson_form.is_valid() and formset.is_valid():
            lesson = lesson_form.save()
            formset.save()
            return redirect('lesson_success')
    else:
        lesson_form = LessonForm(instance=lesson)
        formset = ProgressStudentFormSet(instance=lesson)
    
    context = {
        'lesson_form': lesson_form,
        'formset': formset,
        'students': students,
        'load': load,
    }
    return render(request, 'grades/lesson_management.html', context)