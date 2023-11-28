from django.db import models
from admin_management.models import University, Faculty
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    description = models.TextField()
    created_date = models.DateField()
    is_active = models.BooleanField(default=False)
    course_layout = models.TextField(null = True, blank = True)
    certificate = models.TextField(null = True, blank = True)


    def __str__(self):
        return self.course_name


class CourseContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    week_no = models.IntegerField(null = False, blank = False)
    Title = models.TextField(null = False, blank = False)
    video = models.FileField(null = True, blank = True)
    youtubelink = models.CharField(null = True, blank = True,max_length=300)
    content = models.TextField(null = True, blank = True)
    pdf = models.FileField(null = True, blank = True)


    def __str__(self):
        return self.course.course_name



class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.TextField(null = False, blank = False)
    answer = models.TextField(null = False, blank = False)
    option1 = models.TextField(null = False, blank = False)
    option2 = models.TextField(null = False, blank = False)
    option3 = models.TextField(null = True, blank = True)
    option4 = models.TextField(null = True, blank = True)

    # quiz = models.CharField(null = True, blank = True)


class Enrollment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    is_completed = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now=True)
    certificate_generated = models.BooleanField(default=False)
    certificate_path = models.FileField(default="")