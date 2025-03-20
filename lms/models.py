from django.db import models
from django.contrib.auth.models import User

class TrainerRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    status = models.BooleanField(default=False) 
    def __str__(self):
        return self.user.first_name

class Course(models.Model):
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    course_description = models.TextField()
    course_duration = models.CharField(max_length=50)

    def __str__(self):
        return self.course_name

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.course_name}"