from django import forms
from .models import Lesson, ProgressStudent

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['homework', 'comment_for_lessons']
        widgets = {
            'homework': forms.Textarea(attrs={'rows': 3}),
            'comment_for_lessons': forms.Textarea(attrs={'rows': 3}),
        }

class ProgressStudentForm(forms.ModelForm):
    class Meta:
        model = ProgressStudent
        fields = ['attendance', 'mark', 'offset_mark']
        widgets = {
            'attendance': forms.Select(choices=ProgressStudent.ATTENDANCE_CHOICES),
            'mark': forms.Select(choices=ProgressStudent.MARK_CHOICES),
            'offset_mark': forms.Select(choices=ProgressStudent.OFFSET_MARK_CHOICES),
        }

ProgressStudentFormSet = forms.inlineformset_factory(
    Lesson,
    ProgressStudent,
    form=ProgressStudentForm,
    extra=0,
    can_delete=False
)