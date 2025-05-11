from django.contrib import admin
from .models import Journal, Discipline, JournalPage, Theme, ContentTheme, Lesson, ProgressStudent, SemesterResult

class JournalAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_birthday', 'date_die')
    search_fields = ('id',)

class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('name', 'count_of_hours')
    search_fields = ('name',)

class JournalPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'journal', 'discipline')
    search_fields = ('name',)

class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'count_of_hours', 'discipline')
    search_fields = ('name', 'discipline__name')

class ContentThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'count_of_hours', 'theme')
    search_fields = ('name', 'theme__name')

class LessonAdmin(admin.ModelAdmin):
    list_display = ('date_done', 'load_dpgsg', 'journal_page')
    search_fields = ('journal_page__name',)

class ProgressStudentAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'mark', 'attendance')
    search_fields = ('student__first_name', 'student__last_name', 'lesson__date_done')

class SemesterResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'discipline', 'number_semestr', 'mark_1', 'mark_2')
    search_fields = ('student__first_name', 'discipline__name')

# Регистрация моделей в админке
admin.site.register(Journal, JournalAdmin)
admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(JournalPage, JournalPageAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(ContentTheme, ContentThemeAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(ProgressStudent, ProgressStudentAdmin)
admin.site.register(SemesterResult, SemesterResultAdmin)
