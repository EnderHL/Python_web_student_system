from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path('',include(router.urls)),
    path('students/',views.student_list,name = 'student_list'),
]