from django.db import models
from django.contrib.auth.models import User

# 🧑‍🏫 Trainer Profile
class TrainerRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    status = models.BooleanField(default=False)  # Admin approval
    role = models.CharField(default='trainer', max_length=20)

    def __str__(self):
        return f"{self.user.username} (Trainer)"


# 🧑‍🎓 Learner Profile
class LearnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    role = models.CharField(default='learner', max_length=20)

    def __str__(self):
        return f"{self.user.username} (Learner)"


# 📚 Course linked to Trainer
class Course(models.Model):
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)  # Make sure only trainers create courses
    course_name = models.CharField(max_length=100)
    course_description = models.TextField()
    course_duration = models.CharField(max_length=50)

    def __str__(self):
        return self.course_name


# 🎓 Enrollment links Learner to Course
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.course_name}"
