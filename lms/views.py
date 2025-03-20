from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import TrainerRegistration
from .models import Course, Enrollment
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404


def home(request):
    return render(request, 'lms/home.html')

def user_registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get("last_name")
        user_name  = request.POST.get("user_name")
        email      = request.POST.get("email")
        mobile     = request.POST.get("mobile")
        password1  = request.POST.get("password1")
        password2  = request.POST.get("password2")

        if password1 == password2:
            if User.objects.filter(username=user_name).exists():
                messages.info(request, 'Username Taken')
                return redirect('lms:user_registration')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('lms:user_registration')
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=user_name,
                    email=email,
                    password=password1
                )
                user.save()
                print('User Created')
                return redirect('lms:login')
        else:
            messages.info(request, "Passwords do not match.")
            return redirect('lms:user_registration')
    else:
        return render(request, 'lms/user_registration.html')
    
def view_courses(request):
    courses = Course.objects.all()
    enrolled_courses = Enrollment.objects.filter(user=request.user).values_list('course_id', flat=True)
    return render(request, 'lms/view_courses.html', {
        'courses': courses,
        'enrolled_courses': enrolled_courses
    })

def enroll_in_course(request, course_id):
    course = Course.objects.get(id=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('lms:view_courses')

def user_dashboard(request):
    enrolled_courses = Enrollment.objects.filter(user=request.user)
    enrolled_course_ids = enrolled_courses.values_list('course_id', flat=True)
    available_courses = Course.objects.exclude(id__in=enrolled_course_ids)

    context = {
        'enrollments': enrolled_courses,
        'available_courses': available_courses
    }
    return render(request, 'lms/user_dashboard.html', context)

def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        Enrollment.objects.create(user=request.user, course=course)

    return redirect('lms:user_dashboard')


def login(request):
    if request.method == 'POST':
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")

        user = auth.authenticate(username=user_name, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('lms:user_dashboard')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('lms:login')
    else:
        return render(request, 'lms/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


def trainer_choice(request):
    return render(request, 'lms/trainer_choice.html')


def trainer_registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get("last_name")
        user_name = request.POST.get("user_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            if User.objects.filter(username=user_name).exists():
                messages.info(request, 'Username Taken')
                return redirect('lms:trainer_registration')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('lms:trainer_registration')
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=user_name,
                    email=email,
                    password=password1
                )
                user.is_staff = True  
                user.save()

                trainer_exists = TrainerRegistration.objects.filter(user=user).exists()
                if not trainer_exists:
                    TrainerRegistration.objects.create(user=user, status=False)
                    return redirect('lms:learn_as_trainer')
        else:
            messages.info(request, "Passwords do not match.")
            return redirect('lms:trainer_registration')
    else:
        return render(request, 'lms/trainer_registration.html')
    
    
@login_required(login_url='lms:login_trainer')
def learn_as_trainer(request):
    return render(request, 'lms/learn_as_trainer.html')

def login_trainer(request):
    if request.method == 'POST':
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")

        user = auth.authenticate(username=user_name, password=password)

        if user is not None:
            try:
                trainer_profile = TrainerRegistration.objects.get(user=user)

                if trainer_profile.status:  
                    auth.login(request, user)
                    return redirect('lms:trainer_dashboard')  # Dashboard after login
                else:
                    messages.warning(request, "Your account is not verified by the admin yet.")
                    return redirect('lms:login_trainer')

            except TrainerRegistration.DoesNotExist:
                messages.error(request, "Trainer profile does not exist.")
                return redirect('lms:login_trainer')

        else:
            messages.error(request, 'Invalid trainer credentials.')
            return redirect('lms:login_trainer')

    return render(request, 'lms/login_trainer.html')


@login_required
def trainer_dashboard(request):
    trainer = get_object_or_404(TrainerRegistration, user=request.user)

    # Handle Course Creation
    if request.method == 'POST' and 'create_course' in request.POST:
        course_name = request.POST.get('course_name')
        course_description = request.POST.get('course_description')
        course_duration = request.POST.get('course_duration')

        Course.objects.create(
            trainer=request.user,
            course_name=course_name,
            course_description=course_description,
            course_duration=course_duration
        )
        return redirect('lms:trainer_dashboard')

    # Handle Course Edit
    editing_course = None
    if 'edit' in request.GET:
        course_id = request.GET.get('edit')
        editing_course = get_object_or_404(Course, id=course_id, trainer=request.user)

    # Handle Course Update
    if request.method == 'POST' and 'update_course' in request.POST:
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, id=course_id, trainer=request.user)

        course.course_name = request.POST.get('course_name')
        course.course_description = request.POST.get('course_description')
        course.course_duration = request.POST.get('course_duration')
        course.save()
        return redirect('lms:trainer_dashboard')

    courses = Course.objects.filter(trainer=request.user)
    return render(request, 'lms/trainer_dashboard.html', {
        'trainer': trainer,
        'courses': courses,
        'editing_course': editing_course,
    })


def edit_course(request, course_id):
    course = Course.objects.get(id=course_id, trainer=request.user)

    if request.method == 'POST':
        course.course_name = request.POST.get('course_name')
        course.course_description = request.POST.get('course_description')
        course.course_duration = request.POST.get('course_duration')
        course.save()
        return redirect('lms:trainer_dashboard')

    return render(request, 'lms/edit_course.html', {'course': course})



from .models import Course, TrainerRegistration
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def create_course(request):
    trainer = TrainerRegistration.objects.get(user=request.user)

    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course_description = request.POST.get('course_description')
        course_duration = request.POST.get('course_duration')

        Course.objects.create(
            trainer=request.user,
            course_name=course_name,
            course_description=course_description,
            course_duration=course_duration
        )

    # Fetch updated course list whether GET or after POST
    courses = Course.objects.filter(trainer=request.user)

    return render(request, 'lms/trainer_dashboard.html', {
        'trainer': trainer,
        'courses': courses
    })
    
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, trainer=request.user)

    if request.method == 'POST':
        course.course_name = request.POST.get('course_name')
        course.course_description = request.POST.get('course_description')
        course.course_duration = request.POST.get('course_duration')
        course.save()
        return redirect('lms:trainer_dashboard')

    return render(request, 'lms/edit_course.html', {'course': course})

    
def logout_trainer(request):
    logout(request)  
    return redirect('lms:login_trainer') 
    



    