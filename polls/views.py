from django.http import HttpResponse
from django.shortcuts import render

# This import is no longer needed when render is imported
# from django.template import loader

from .models import Question

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
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s"
    return HttpResponse(response % question_id)

def vote(request, question_id):
    response = "Youre voting on question %s"
    return HttpResponse(response % question_id)