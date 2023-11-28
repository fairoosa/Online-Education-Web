from django.contrib import admin
from .models import CourseContent, Course, Quiz, Enrollment

admin.site.register(CourseContent)
admin.site.register(Course)
admin.site.register(Quiz)
admin.site.register(Enrollment)
