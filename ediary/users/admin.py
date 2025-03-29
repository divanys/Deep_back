from django.contrib import admin
from .models import User, Guardian, Student, DisciplinePrepod, TutorPrepod

# Регистрируем модели в админке
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email',)
    list_filter = ('is_active', 'is_staff')

class GuardianAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'date_input', 'date_output')
    search_fields = ('first_name', 'last_name', 'phone_number')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_birthday', 'is_learning', 'group')
    search_fields = ('first_name', 'last_name', 'group__name')
    list_filter = ('is_learning',)

class DisciplinePrepodAdmin(admin.ModelAdmin):
    list_display = ('user', 'actions')
    search_fields = ('user__email',)

class TutorPrepodAdmin(admin.ModelAdmin):
    list_display = ('user', 'actions')
    search_fields = ('user__email',)

# Регистрируем администраторов моделей
admin.site.register(User, UserAdmin)
admin.site.register(Guardian, GuardianAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(DisciplinePrepod, DisciplinePrepodAdmin)
admin.site.register(TutorPrepod, TutorPrepodAdmin)
