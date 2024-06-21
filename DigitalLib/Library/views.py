from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import StudentSignUpForm, LecturerSignUpForm, ResourceForm
from .models import CustomUser, Student, Lecturer, Resource
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string

def home(request):
    if request.user.is_authenticated:
        if request.user.is_lecturer:
            return redirect('upload_resource')
        elif request.user.is_student:
            return redirect('view_resources')
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            
            else:
             try:
                    User.objects.get(username=username)
                    messages.error(request, 'Invalid password. Please try again.')
             except User.DoesNotExist:
                    return redirect('signup')  # Re
        else:
            return render(request, 'Library/login.html', {'form': form, 'error': 'Invalid credentials'})
    form = AuthenticationForm()
    return render(request, 'Library/login.html', {'form': form})

def signup_view(request):
    return render(request, 'Library/signup.html')

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = StudentSignUpForm()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('Library/student_signup.html', {'form': form})
        return HttpResponse(html)
    
    return redirect('signup')

   
def lecturer_signup(request):
    if request.method == 'POST':
        form = LecturerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = LecturerSignUpForm()
     
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('Library/lecturer_signup.html', {'form': form})
        return HttpResponse(html)
    
    return redirect('signup')

@login_required
def upload_resource(request):
    if not request.user.is_lecturer:
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = Lecturer.objects.get(user=request.user)
            resource.save()
            return redirect('view_resources')
    else:
        form = ResourceForm()
    return render(request, 'Library/upload_resource.html', {'form': form})

@login_required
def view_resources(request):
    if not (request.user.is_student or request.user.is_lecturer):
        return HttpResponse('Unauthorized', status=401)

    if request.user.is_student:
        student = Student.objects.get(user=request.user)
        resources = Resource.objects.filter(uploaded_by__department=student.department)
    else:  # User is a lecturer
        lecturer = Lecturer.objects.get(user=request.user)
        resources = Resource.objects.filter(uploaded_by__department=lecturer.department)

    return render(request, 'Library/view_resources.html', {'resources': resources})