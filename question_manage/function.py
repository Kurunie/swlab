from .models import *
import random

def get_auto_exam(tlist, sum):
    data = []
    q1 = Question.objects.none()
    q2 = Fillin.objects.none()
    for t in tlist:
        temp = Question.objects.filter(category=t)
        q1 = q1 | temp
        temp = Fillin.objects.filter(category=t)
        q2 = q2 | temp
    s1 = q1.count()
    s2 = q2.count()
    if s1+s2<sum:
        return False,[],[];
    else:
        l = s1-sum
        r = s1+sum
        if l < 0:
            l = 0
        if r > s1+s2:
            r = s1+s2
        mid = (l+s1)//2
        while mid+sum > r:
            mid-=1
        while mid+sum <= s1:
            mid+=1
        # 区间(mid, mid+sum]
        ts1 = s1-mid
        ts2 = sum-ts1
        return True, q1.order_by('?')[:int(ts1)], q2.order_by('?')[:int(ts2)]