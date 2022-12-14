from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('infoManager/', views.infoManager, name='infoManager'),
    path('addStudent/', views.addStudent, name='addStudent'),
    path('addStudent/add/', views.add, name='add'),
    path('stuAttendInfo/', views.stuAttendInfo, name='stuAttendInfo'),
    path('stuAttendInfo/modify/', views.modify, name='modify'),
]