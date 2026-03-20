from django.urls import path
from . import views

urlpatterns = [
    # ... existing paths
    path('course/<int:course_id>/submission/', views.submit, name='submit'),
    path('course/<int:course_id>/submission/<int:submission_id>/result/', 
         views.show_exam_result, name='show_exam_result'),
]