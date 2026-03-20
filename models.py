from django.db import models
from django.conf import settings

class Question(models.Model):
    # Link to a Lesson or Course model if already defined
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField(default=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

class Submission(models.Model):
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)