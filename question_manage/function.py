from .models import *

def get_auto_exam(tlist, sum):
    data = []
    tq = Question.objects.none()
    for t in tlist:
        temp = Question.objects.filter(category=t)
        tq = tq | temp
    return tq.order_by('?')[:int(sum)]