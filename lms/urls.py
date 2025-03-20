from django.urls import path
from .views import *
from . import views



app_name = 'lms'

urlpatterns = [
    path('', views.home, name="home"),
    path('user_registration', user_registration, name="user_registration"),
    path('login', login, name="login"),
    path('logout', logout, name="logout"),
    path('trainer_registration', trainer_registration, name="trainer_registration"),
    path('trainer_choice', trainer_choice, name='trainer_choice'),
    path('login_trainer', login_trainer, name='login_trainer'),
    path('learn_as_trainer', learn_as_trainer, name="learn_as_trainer"),
    path('logout_trainer', views.logout_trainer, name='logout_trainer'),
    path('create_course', create_course, name="create_course"),
    path('view_courses', view_courses, name="view_courses"),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('trainer_dashboard', trainer_dashboard, name='trainer_dashboard'),
    path('edit_course/<int:course_id>/', edit_course, name='edit_course'),


    
]
