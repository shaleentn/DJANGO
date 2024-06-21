
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Student, Lecturer, Resource

class StudentSignUpForm(UserCreationForm):
    reg_no = forms.CharField(max_length=10)
    name = forms.CharField(max_length=100)
    department = forms.CharField(max_length=100)
    course = forms.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ('username', 'reg_no', 'name', 'department', 'course', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
            Student.objects.create(user=user, reg_no=self.cleaned_data['reg_no'], name=self.cleaned_data['name'], department=self.cleaned_data['department'], course=self.cleaned_data['course'])
        return user

class LecturerSignUpForm(UserCreationForm):
    staff_id = forms.CharField(max_length=10)
    name = forms.CharField(max_length=100)
    department = forms.CharField(max_length=100)
    course = forms.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ('username', 'staff_id', 'name', 'department', 'course', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_lecturer = True
        if commit:
            user.save()
            Lecturer.objects.create(user=user, staff_id=self.cleaned_data['staff_id'], name=self.cleaned_data['name'], department=self.cleaned_data['department'], course=self.cleaned_data['course'])
        return user

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ('title', 'description', 'file')