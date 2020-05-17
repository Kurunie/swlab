
from django.shortcuts import render,redirect, render_to_response
from question_manage import models as q_models
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required

import xlwt
from io import BytesIO


# Create your views here.


def index(request):
    taglist = Question.objects.values("category").distinct()
    ques = Question.objects.all()
    return render_to_response("index.html", {'qlist': ques, 'tlist': taglist})

def singleq(request, id):
    taglist = Question.objects.values("category").distinct()
    q = Question.objects.get(id=id)
    s_dlist = Discussion.objects.filter(qid=q, solved=True)
    un_dlist = Discussion.objects.filter(qid=q, solved=False)
    return render_to_response("singleq.html", {'q': q, 'tlist': taglist, 's_dlist': s_dlist, 'un_dlist': un_dlist})

def discussion(request, id, did):
    taglist = Question.objects.values("category").distinct()
    q = Question.objects.get(id=id)
    d = Discussion.objects.get(id=did)
    rlist = Reply.objects.filter(did=d)
    user = request.user
    is_auth = '0'
    if user.is_authenticated:
        if user.username == d.uid.user.username:
            is_auth = '1'
    return render(request, "discussion.html", {'q': q, 'tlist': taglist, 'd': d, 'rlist': rlist, 'is_auth': is_auth})

def change_s(request):
    if request.is_ajax():
        status = request.POST.get('status')
        data = {}
        did = request.POST.get('did')
        d = Discussion.objects.get(id=did)
        user = request.user
        # return HttpResponse(status)
        if user.is_authenticated:
            if status == '1':
                d.solved = 1
            else:
                d.solved = 0
            d.save()
            data['status'] = 'success'
            data['data'] = {'solved': status}
        return JsonResponse(data)

@login_required
def my_dis(request, id):
    taglist = Question.objects.values("category").distinct()
    q = Question.objects.get(id=id)
    user = request.user
    if user.is_authenticated:
        exu = UserEx.objects.get(user=user)
        s_dlist = Discussion.objects.filter(qid=q, uid=exu, solved=True)
        un_dlist = Discussion.objects.filter(qid=q, uid=exu, solved=False)
        return render(request, "my_dis.html", {'q': q, 'tlist': taglist, 's_dlist': s_dlist, 'un_dlist': un_dlist, 'user':exu})

def add_dis(request):
    if request.is_ajax():
        title = request.POST.get('title')
        detail = request.POST.get('detail')
        data = {}
        qid = request.POST.get('qid')
        q = Question.objects.get(id=qid)
        user = request.user
        if user.is_authenticated:
            exu = UserEx.objects.get(user=user)
            Discussion.objects.create(qid=q, uid=exu, title=title, detail=detail)
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
        d = Discussion.objects.get(id=did)
        user = request.user
        if user.is_authenticated:
            exu = UserEx.objects.get(user=user)
            Reply.objects.create(did=d, uid=exu, content=content)
            data['status'] = 'success'
            data['message'] = '回复成功'
            data['data'] = {'content': content}
        else:
            data['status'] = 'fail'
            data['message'] = '未登录，请登录后重试'
            data['data'] = {'content': content}
        return JsonResponse(data)

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
    taglist = Question.objects.values("category").distinct()
    user = UserEx.objects.get(user=request.user)
    plist = Paper.objects.all()
    if user.type == "老师":
        glist = Grade.objects.all()
    else:
        glist = Grade.objects.filter(sid=user)
    return render(request,'user.html', {'tlist': taglist, 'user':user, 'plist':plist, 'glist':glist})

def exam(request, sid, pid):
    paper = Paper.objects.get(id=pid)
    student = UserEx.objects.get(id=sid)
    return render(request, 'exam.html', {'student': student, 'paper': paper})

def lookAnswer(request, id):
    g = Grade.objects.get(id=id)
    s = g.sid
    alist = g.tanswer_set.all()
    return render(request, 'answer_base.html', {'student': s, 'alist':alist, 'grade':g})

def sub_rewind(request):
    r = request.POST['rewind']
    gid = request.POST['gid']
    g = Grade.objects.get(id=gid)
    g.rewind = r
    g.save()
    return userpage(request)

def rewind(request, id):
    g = Grade.objects.get(id=id)
    s = g.sid
    alist = g.tanswer_set.all()
    return render(request, 'rewind.html', {'student': s, 'alist': alist, 'grade':g})

def calGrade(request):
    grade = 0
    if request.method=='POST':
        sid = request.POST['sid']
        pid = request.POST['pid']
        s = UserEx.objects.get(id=sid)
        paper = Paper.objects.get(id=pid)
        g = Grade.objects.create(sid=s, pid=paper, grade=grade)
        qlist = paper.qid.all()
        for q in qlist:
            ans = request.POST[str(q.id)]
            TAnswer.objects.create(gid=g, qid=q, ans=ans)
            if ans == q.answer:
                grade += q.score
        g.grade = grade
        g.save()

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
