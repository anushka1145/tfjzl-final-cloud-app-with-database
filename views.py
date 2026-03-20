from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice, Submission, Course, Enrollment

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    # Ensure enrollment exists for the user
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    
    if request.method == 'POST':
        # Create a new submission object
        submission = Submission(enrollment=enrollment)
        submission.save()
        
        # Get all question IDs from the post data to associate choices
        for key, value in request.POST.items():
            if key.startswith('question_'):
                choice_id = int(value)
                choice = get_object_or_404(Choice, pk=choice_id)
                submission.choices.add(choice)
        
        submission.save()
        return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))

def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # 1. Implementation of the logic required by is_get_score()
    total_score = 0
    possible_score = 0
    
    # Get all questions related to this course
    questions = Question.objects.filter(lesson__course=course)
    
    # Get IDs of choices the user actually selected
    selected_ids = [choice.id for choice in submission.choices.all()]
    
    for question in questions:
        possible_score += question.grade
        # Check if the selected choice for this question is correct
        selected_choice = submission.choices.filter(question=question).first()
        if selected_choice and selected_choice.is_correct:
            total_score += question.grade

    # 2. Calculate the grade percentage
    grade = (total_score / possible_score * 100) if possible_score > 0 else 0
    
    # 3. Pass all required values to the context
    context['course'] = course
    context['submission'] = submission
    context['total_score'] = total_score
    context['possible_score'] = possible_score
    context['selected_ids'] = selected_ids  # Required for highlighting in template
    context['grade'] = grade                # Required for 'Congratulations' logic
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
