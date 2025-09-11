from django.shortcuts import render
from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer
from django.http import HttpResponse

# Create your views here.

def student_list(request):
    students = Student.objects.all()
    result = ", ".join([f"{s.name}({s.age}, {s.major})" for s in students])
    return HttpResponse(result if result else "No students found.")



