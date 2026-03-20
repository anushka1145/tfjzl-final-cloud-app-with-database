from django.db import models
from django.conf import settings

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class Submission(models.Model):
    # Ensure this links to your Enrollment model
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE)
    
    # REQUIRED: ManyToManyField to Choice model
    choices = models.ManyToManyField(Choice)
    
    # REQUIRED: __str__ method for the admin interface
    def __str__(self):
        return f"Submission by {self.enrollment.user.username} for {self.enrollment.course.name}"
