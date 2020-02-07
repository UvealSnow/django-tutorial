from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

# This import is no longer needed when render is imported
# from django.template import loader

from .models import Question, Choice

# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}

    # This is the first way they show to load a tamplate
    # template = loader.get_template('polls/index.html')
    # return HttpResponse(template.render(context, request))

    # This is a simpler way to manage the rendering of a template
    return render(request, "polls/index.html", context)



def detail(request, question_id):
    # This is a very verbose way of doing something very simple...
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")

    # This is the regular way to do it
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'polls/results.html', { 
        'question': question
    })

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You need to select a choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        
        # Returning an HttpResponseRedirect is required so that the user will not accidentally
        # re-submit the form if he hits the back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))