from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Choise, Question
from django.urls import reverse

# システム上にある最新５件の質問項目をカンマで区切り、日付順に表示するビュー
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list
    }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choise = question.choise_set.get(pk=request.POST['choise'])
    except(KeyError, Choise.DoesNotExist):
        return render(request, 'polls/detail.html',{
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choise.votes += 1
        selected_choise.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
    return HttpResponse("You're voting on question %s." % question_id) 