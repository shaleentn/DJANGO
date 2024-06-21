from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('signup/student/', views.student_signup, name='student_signup'),
    path('signup/lecturer/', views.lecturer_signup, name='lecturer_signup'),
    path('upload/', views.upload_resource, name='upload_resource'),
    path('resources/', views.view_resources, name='view_resources'),
]