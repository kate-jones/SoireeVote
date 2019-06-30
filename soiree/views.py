from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
#from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


'''
def index(request):
    return HttpResponse("Bienvenue a l'Index de Votes!")

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('soiree/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
'''

'''
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:100]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'soiree/index.html', context)


def detail(request, question_id):
    #try:
        #question = Question.objects.get(pk=question_id)
    #except Question.DoesNotExist:
        #raise Http404("Numero incorrecte")
    #return render(request, 'soiree/detail.html', {'question': question})
    #return HttpResponse("You're looking at question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'soiree/detail.html', {'question': question})


#def results(request, question_id):
    #response = "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'soiree/results.html', {'question': question})


#def vote(request, question_id):
    #return HttpResponse("You're voting on question %s." % question_id)
'''


class IndexView(generic.ListView):
    template_name = 'soiree/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return all published questions (not including those set to be published in the future)."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:400]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'soiree/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that are'nt published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'soiree/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'soiree/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('soiree:results', args=(question.id,)))