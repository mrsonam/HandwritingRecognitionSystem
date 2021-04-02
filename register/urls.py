from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
app_name = "register"

urlpatterns = [          
    path('', views.index, name="index"),

    path('register/',views.register, name="register"),
    path('registration_form_submission/', views.registration_form_submission, name='registration_form_submission'),

    path('login/',views.login, name="login"),
    path('login_form_submission/', views.login_form_submission, name='login_form_submission'),

    path('logout/',views.logout, name="logout"),

    path('welcome/', views.welcome, name="welcome"),
    path('settings/', views.settings, name="settings"),
    path('change_PP/', views.change_PP, name="change_PP"),
    
    path('add_student/', views.add_student, name="add_student"),
    path('student_form_submission/', views.student_form_submission, name='student_form_submission'),

    path('student_info/', views.student_info, name="student_info"),

    path('change_password/', views.change_password, name="change_password"),
    path('change_password_sent/', views.change_password_sent, name="change_password_sent"),

    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password_sent/', views.reset_password_sent, name='reset_password_sent'),

    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_conditions/', views.terms_conditions, name='terms_conditions'),

]