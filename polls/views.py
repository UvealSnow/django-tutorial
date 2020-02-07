from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# This import is no longer needed when render is imported
# from django.template import loader

from .models import Question, Choice

# Create your views here.

class IndexView(generic.ListView):
    # This would be useful if we hadn't changed the names of our templates
    # By default ListView points to <app_name>/<model_name>_list.html
    # template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # Returns the last five published questions where pub_date lte than now()
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    # This would be useful if we hadn't changed the names of our templates
    # By default ListView points to <app_name>/<model_name>_detail.html
    # template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

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

""" 
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
"""