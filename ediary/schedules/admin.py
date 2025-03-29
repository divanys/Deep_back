from django.contrib import admin
from .models import Group, SubGroup, LoadDPGSG

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'tutor_prepod')
    search_fields = ('name', 'specialization')

class SubGroupAdmin(admin.ModelAdmin):
    list_display = ('group', 'discipline', 'number_sub_group')
    search_fields = ('group__name', 'discipline__name')

class LoadDPGSGAdmin(admin.ModelAdmin):
    list_display = ('discipline', 'discipline_prepod', 'group', 'sub_group', 'fack_count_number', 'is_teaching', 'date_input_to_group')
    search_fields = ('discipline__name', 'discipline_prepod__user__email', 'group__name')

# Регистрация моделей в админке
admin.site.register(Group, GroupAdmin)
admin.site.register(SubGroup, SubGroupAdmin)
admin.site.register(LoadDPGSG, LoadDPGSGAdmin)
