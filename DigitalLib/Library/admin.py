from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from .models import Lecturer, Student, Resource, CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_lecturer', 'is_student')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_lecturer', 'is_student')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_lecturer', 'is_student')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_lecturer', 'is_student')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

# Admin for Lecturer
@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'staff_id', 'department', 'course')
    list_filter = ('department', 'course')

# Admin for Student
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'reg_no', 'department', 'course')
    list_filter = ('department', 'course')

# Admin for Resource
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_by', 'uploaded_at')
