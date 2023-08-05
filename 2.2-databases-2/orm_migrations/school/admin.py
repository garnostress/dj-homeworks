from django.contrib import admin

from .models import Student, Teacher, TeacherStudent


class TeacherStudentInline(admin.StackedInline):
    model = TeacherStudent


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [TeacherStudentInline]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass
