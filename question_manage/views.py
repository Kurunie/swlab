
from django.shortcuts import render,redirect, render_to_response
from question_manage import models as q_models
from django.http import HttpResponse
from django.contrib.auth import logout
from .models import Question
# Create your views here.


def index(request):
    taglist = Question.objects.values("category").distinct()
    ques = Question.objects.all()
    return render_to_response("index.html", {'qlist': ques, 'tlist': taglist})

def singleq(request, id):
    taglist = Question.objects.values("category").distinct()
    q = Question.objects.get(id=id)
    return render_to_response("singleq.html", {'q': q, 'tlist': taglist})

def search(request):
    taglist = Question.objects.values("category").distinct()
    q = request.GET.get('ss')
    t = request.GET.get('sc')
    error_msg = ''
    if t == 'ALL':
        if not q:
            qlist = Question.objects.all()
        else:
            qlist = Question.objects.filter(title__icontains=q)
    else:
        if not q:
            qlist = Question.objects.filter(category=t)
        else:
            qlist = Question.objects.filter(title__icontains=q, category=t)
    return render(request, 'result.html', {'error_msg': error_msg,
                                                 'qlist': qlist, 'tlist': taglist})
