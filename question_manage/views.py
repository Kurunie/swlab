
from django.shortcuts import render,redirect, render_to_response
from question_manage import models as q_models
from django.http import HttpResponse
from django.contrib.auth import logout
from .models import Question
# Create your views here.


def index(request):
    ques = Question.objects.all()
    return render_to_response("index.html", {'qlist': ques})

def singleq(request, id):
    q = Question.objects.get(id=id)
    return render_to_response("singleq.html", {'q': q})