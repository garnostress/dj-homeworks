from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from students.models import Course, Student


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        course = self.initial_data['name']
        objects = Student.objects.filter(course__name=course)
        method = self.context['request'].method

        if objects.count() > settings.MAX_STUDENTS_PER_COURSE and method in ['POST', 'PUT', 'PATCH']:
            raise ValidationError

        return data
