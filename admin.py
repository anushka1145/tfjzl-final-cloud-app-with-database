from django.contrib import admin
from .models import Question, Choice, Lesson # and other required imports

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

# Ensure you register all required classes (7 total imports/classes)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Lesson, LessonAdmin)