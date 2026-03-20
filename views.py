from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice, Submission, Course, Enrollment

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    # Get the user's enrollment for this course
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    
    if request.method == 'POST':
        # Create a new submission instance
        submission = Submission(enrollment=enrollment)
        submission.save()
        
        # Loop through all questions in the course
        questions = Question.objects.filter(lesson__course=course)
        for question in questions:
            # Get the selected choice ID from the radio button input
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                selected_choice = get_object_or_404(Choice, pk=selected_choice_id)
                submission.choices.add(selected_choice)
        
        submission.save()
        # Redirect to the results page passing the submission ID
        return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))

def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Calculate score logic
    total_questions = Question.objects.filter(lesson__course=course).count()
    correct_answers = submission.choices.filter(is_correct=True).count()
    
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    context['course'] = course
    context['submission'] = submission
    context['score'] = round(score, 2)
    
    # Task 7 requirement: Pass a success flag for the 'Congratulations' message
    context['passed'] = score >= 70  # Assuming 70% is the pass mark from your criteria
    
    return render(request, 'onlinecourse/exam_result.html', context)