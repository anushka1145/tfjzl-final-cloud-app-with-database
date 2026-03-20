from django.contrib import admin
# TASK 2: Importing all 7 required classes
from .models import (
    Course, 
    Lesson, 
    Question, 
    Choice, 
    Instructor, 
    Learner, 
    Submission
)

# 1. ChoiceInline: Allows adding choices directly inside a Question
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

# 2. QuestionInline: Allows adding questions directly inside a Lesson
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2

# 3. QuestionAdmin: Uses the ChoiceInline
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

# 4. LessonAdmin: Uses the QuestionInline
class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

# Registering the models to the Admin site
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Submission)
