from django.views.generic import ListView

from .models import Student


class StudentsListView(ListView):
    model = Student
    template_name = 'school/students_list.html'
    queryset = Student.objects.order_by('group')
