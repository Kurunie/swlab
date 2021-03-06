
from django.shortcuts import render,redirect, render_to_response
from question_manage import models as q_models
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from .function import *
from itertools import chain

import xlwt
from io import BytesIO


# Create your views here.


def index(request):
    t1 = Question.objects.values("category").distinct()
    t2 = Fillin.objects.values("category").distinct()
    taglist = t1.union(t2)
    sq = Question.objects.all()
    fq = Fillin.objects.filter(type='f')
    saq = Fillin.objects.filter(type='sa')
    return render_to_response("index.html", {'sq': sq, 'fq': fq, 'saq': saq, 'tlist': taglist})

def singleq(request, type, id):
    t1 = Question.objects.values("category").distinct()
    t2 = Fillin.objects.values("category").distinct()
    taglist = t1.union(t2)
    if type == 's':
        q = Question.objects.get(id=id)
        s_dlist = Discussion.objects.filter(qid=q, solved=True)
        un_dlist = Discussion.objects.filter(qid=q, solved=False)
        return render_to_response("singleq.html", {'q': q, 'tlist': taglist, 's_dlist': s_dlist, 'un_dlist': un_dlist, 'type':'s'})
    else:
        q = Fillin.objects.get(id=id)
        s_dlist = F_Discussion.objects.filter(qid=q, solved=True)
        un_dlist = F_Discussion.objects.filter(qid=q, solved=False)
        return render_to_response("fillq.html", {'q': q, 'tlist': taglist, 's_dlist': s_dlist, 'un_dlist': un_dlist, 'type':'f'})

def discussion(request, type, id, did):
    t1 = Question.objects.values("category").distinct()
    t2 = Fillin.objects.values("category").distinct()
    taglist = t1.union(t2)
    if type == 's':
        q = Question.objects.get(id=id)
        d = Discussion.objects.get(id=did)
        rlist = Reply.objects.filter(did=d)
    else:
        q = Fillin.objects.get(id=id)
        d = F_Discussion.objects.get(id=did)
        rlist = F_Reply.objects.filter(did=d)
    user = request.user
    is_auth = '0'
    if user.is_authenticated:
        if user.username == d.uid.user.username:
            is_auth = '1'
    return render(request, "discussion.html", {'q': q, 'tlist': taglist, 'd': d, 'rlist': rlist, 'is_auth': is_auth, 'type': type})

def change_s(request):
    if request.is_ajax():
        status = request.POST.get('status')
        type = request.POST.get('type')
        data = {}
        did = request.POST.get('did')
        user = request.user
        # return HttpResponse(status)
        if user.is_authenticated:
            if type == 's':
                d = Discussion.objects.get(id=did)
            else:
                d = F_Discussion.objects.get(id=did)
            if status == '1':
                d.solved = 1
            else:
                d.solved = 0
            d.save()
            data['status'] = 'success'
            data['data'] = {'solved': status}
        return JsonResponse(data)

@login_required
def my_dis(request, type, id):
    t1 = Question.objects.values("category").distinct()
    t2 = Fillin.objects.values("category").distinct()
    taglist = t1.union(t2)
    user = request.user
    if user.is_authenticated:
        exu = UserEx.objects.get(user=user)
        if type == 's':
            q = Question.objects.get(id=id)
            s_dlist = Discussion.objects.filter(qid=q, uid=exu, solved=True)
            un_dlist = Discussion.objects.filter(qid=q, uid=exu, solved=False)
        else:
            q = Fillin.objects.get(id=id)
            s_dlist = F_Discussion.objects.filter(qid=q, uid=exu, solved=True)
            un_dlist = F_Discussion.objects.filter(qid=q, uid=exu, solved=False)
        return render(request, "my_dis.html", {'q': q, 'tlist': taglist, 's_dlist': s_dlist, 'un_dlist': un_dlist, 'user':exu, 'type':type})

def add_dis(request):
    if request.is_ajax():
        title = request.POST.get('title')
        type = request.POST.get('type')
        detail = request.POST.get('detail')
        data = {}
        qid = request.POST.get('qid')
        user = request.user
        if user.is_authenticated:
            exu = UserEx.objects.get(user=user)
            if type == 's':
                q = Question.objects.get(id=qid)
                Discussion.objects.create(qid=q, uid=exu, title=title, detail=detail)
            else:
                q = Fillin.objects.get(id=qid)
                F_Discussion.objects.create(qid=q, uid=exu, title=title, detail=detail)
            data['status'] = 'success'
            data['message'] = '发布成功'
            data['data'] = {'title': title, 'detail': detail}
        else:
            data['status'] = 'fail'
            data['message'] = '未登录，请登录后再发布'
            data['data'] = {'title': title, 'detail': detail}
        return JsonResponse(data)

def add_rep(request):
    if request.is_ajax():
        content = request.POST.get('content')
        data = {}
        did = request.POST.get('did')
        user = request.user
        if user.is_authenticated:
            exu = UserEx.objects.get(user=user)
            type = request.POST.get('type')
            if type == 's':
                d = Discussion.objects.get(id=did)
                Reply.objects.create(did=d, uid=exu, content=content)
            else:
                d = F_Discussion.objects.get(id=did)
                F_Reply.objects.create(did=d, uid=exu, content=content)
            if exu.type == '老师':
                d.replied = True
                d.save()
            data['status'] = 'success'
            data['message'] = '回复成功'
            data['data'] = {'content': content}
        else:
            data['status'] = 'fail'
            data['message'] = '未登录，请登录后重试'
            data['data'] = {'content': content}
        return JsonResponse(data)

def search(request):
    t1 = Question.objects.values("category").distinct()
    t2 = Fillin.objects.values("category").distinct()
    taglist = t1.union(t2)
    q = request.GET.get('ss')
    t = request.GET.get('sc')
    error_msg = ''
    if t == 'ALL':
        if not q:
            qlist = Question.objects.all()
            fqlist = Fillin.objects.all()
        else:
            qlist = Question.objects.filter(title__icontains=q)
            fqlist = Fillin.objects.filter(title__icontains=q)
    else:
        if not q:
            qlist = Question.objects.filter(category=t)
            fqlist = Fillin.objects.filter(category=t)
        else:
            qlist = Question.objects.filter(title__icontains=q, category=t)
            fqlist = Question.objects.filter(title__icontains=q, category=t)
    return render(request, 'result.html', {'error_msg': error_msg,
                                                 'qlist': qlist, 'tlist': taglist ,'fqlist': fqlist})

def mylogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return userpage(request)
    else:
        return HttpResponse("登录失败")


def mylogout(request):
    logout(request)
    return index(request)


@login_required
def userpage(request):
    t1 = Question.objects.values("category").distinct()
    t2 = Fillin.objects.values("category").distinct()
    taglist = t1.union(t2)
    user = UserEx.objects.get(user=request.user)
    plist = Paper.objects.all()
    aplist = AutoPaper.objects.filter(sid=user)
    aglist = AutoGrade.objects.filter(sid=user)
    if user.type == "老师":
        glist = Grade.objects.all()
    else:
        glist = Grade.objects.filter(sid=user)
    return render(request,'user.html', {'tlist': taglist, 'user':user, 'plist':plist, 'glist':glist, 'aplist':aplist, 'aglist':aglist})

def exam(request, sid, pid):
    paper = Paper.objects.get(id=pid)
    student = UserEx.objects.get(id=sid)
    return render(request, 'exam.html', {'student': student, 'paper': paper})

def a_exam(request, sid, pid):
    paper = AutoPaper.objects.get(id=pid)
    student = UserEx.objects.get(id=sid)
    return render(request, 'a_exam.html', {'student': student, 'paper': paper})

def lookAnswer(request, id):
    g = Grade.objects.get(id=id)
    s = g.sid
    alist = g.tanswer_set.all()
    falist = g.f_tanswer_set.all()
    return render(request, 'answer_base.html', {'student': s, 'alist':alist, 'grade':g, 'falist':falist})

def a_lookAnswer(request, id):
    g = AutoGrade.objects.get(id=id)
    s = g.sid
    alist = g.autotanswer_set.all()
    falist = g.f_autotanswer_set.all()
    return render(request, 'a_answer_base.html', {'student': s, 'alist':alist, 'grade':g, 'falist':falist})

def sub_rewind(request):
    r = request.POST['rewind']
    gid = request.POST['gid']
    g = Grade.objects.get(id=gid)
    g.rewind = r
    falist = F_TAnswer.objects.filter(gid=g)
    alist = TAnswer.objects.filter(gid=g)
    for a in alist:
        r = request.POST['sr'+str(a.id)]
        a.rewind = r
        a.save()
    for fa in falist:
        if fa.qid.type == 'f':
            r = request.POST.get('fr'+str(fa.id))
            s = request.POST.get('fs'+str(fa.id))
        else:
            r = request.POST.get('sar' + str(fa.id))
            s = request.POST.get('sas' + str(fa.id))
        g.grade = g.grade + int(s)
        fa.rewind = r
        fa.score = s
        fa.save()
    g.is_checked = True
    g.save()
    return userpage(request)

def rewind(request, id):
    g = Grade.objects.get(id=id)
    s = g.sid
    alist = g.tanswer_set.all()
    falist = g.f_tanswer_set.all()
    return render(request, 'rewind.html', {'student': s, 'alist': alist, 'grade':g, 'falist':falist})

def calGrade(request):
    grade = 0
    if request.method=='POST':
        sid = request.POST['sid']
        pid = request.POST['pid']
        s = UserEx.objects.get(id=sid)
        paper = Paper.objects.get(id=pid)
        g = Grade.objects.create(sid=s, pid=paper, grade=grade)
        qlist = paper.sqid.all()
        for q in qlist:
            ans = request.POST['s'+str(q.id)]
            t = TAnswer.objects.create(gid=g, qid=q, ans=ans)
            if ans == q.answer:
                grade += q.score
                t.score = q.score
                t.save()
        g.grade = grade
        g.save()
        fql = paper.fqid.filter(type='f')
        for fq in fql:
            ans = request.POST['f'+str(fq.id)]
            F_TAnswer.objects.create(gid=g, qid=fq, ans=ans)
        saql = paper.fqid.filter(type='sa')
        for saq in saql:
            ans = request.POST['sa'+str(saq.id)]
            F_TAnswer.objects.create(gid=g, qid=saq, ans=ans)
    return userpage(request)

def a_calGrade(request):
    grade = 0
    if request.method=='POST':
        sid = request.POST['sid']
        pid = request.POST['pid']
        s = UserEx.objects.get(id=sid)
        paper = AutoPaper.objects.get(id=pid)
        g = AutoGrade.objects.create(sid=s, pid=paper, grade=grade)
        qlist = paper.sqid.all()
        for q in qlist:
            ans = request.POST['s'+str(q.id)]
            AutoTAnswer.objects.create(gid=g, qid=q, ans=ans)
            if ans == q.answer:
                grade += q.score
        g.grade = grade
        g.save()
        fql = paper.fqid.filter(type='f')
        for fq in fql:
            ans = request.POST['f' + str(fq.id)]
            F_AutoTAnswer.objects.create(gid=g, qid=fq, ans=ans)
        saql = paper.fqid.filter(type='sa')
        for saq in saql:
            ans = request.POST['sa' + str(saq.id)]
            F_AutoTAnswer.objects.create(gid=g, qid=saq, ans=ans)
    return userpage(request)


def add_auto_paper(request):
    data = {}
    data['status'] = 'fail'
    if request.method == 'POST':
        user = request.user
        # print(user.username)
        exu = UserEx.objects.get(user=user)
        title = request.POST['title']
        # scores = request.POST['scores']
        scores = 0
        sum = request.POST['sum']
        sc = request.POST.getlist('sc')
        # print(sc, sum, title)
        if sc == '' or sum == '' or title == '':
            data['status'] = 'fail'
            data['message'] = '有数据为空，请检查'
        elif not sum.isdigit() or int(sum) <= 0:
            data['status'] = 'fail'
            data['message'] = '题目数量不正确，请检查'
        else:
            sc = list(set(sc))
            # print (sc)
            flag, qlist, fqlist = get_auto_exam(sc, int(sum))
            if not flag:
                data['status'] = 'fail'
                data['message'] = '题库题目数量不足'
            else:
                ap = AutoPaper.objects.create(title=title, scores=scores, sum=sum, sid=exu)
                ap.sqid.add(*qlist)
                ap.fqid.add(*fqlist)
                data['status'] = 'success'
                data['message'] = '添加成功'
    return JsonResponse(data)

def del_apaper(request, id):
    p = AutoPaper.objects.get(id=id)
    p.delete()
    return userpage(request)

def del_agrade(request, id):
    g = AutoGrade.objects.get(id=id)
    g.delete()
    return userpage(request)

# 导出excel数据
def export_excel(request):
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=score.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('order-sheet')

    # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
    style_heading = xlwt.easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour 0x19;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """)

    # 写入文件标题
    sheet.write(0,0,'考生姓名',style_heading)
    sheet.write(0,1,'考生学号',style_heading)
    sheet.write(0,2,'考试标题',style_heading)
    sheet.write(0,3,'成绩',style_heading)
    sheet.write(0, 4, '评语', style_heading)

    # 写入数据
    data_row = 1
    # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
    for i in Grade.objects.all():
        # 格式化datetime
        sheet.write(data_row,0,i.sid.name)
        sheet.write(data_row,1,i.sid.id)
        sheet.write(data_row,2,i.pid.title)
        sheet.write(data_row,3,i.grade)
        sheet.write(data_row,4,i.rewind)
        data_row = data_row + 1

    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response
