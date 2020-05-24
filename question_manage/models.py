from django.db import models
from django.contrib.auth.models import User
from .listfield import ListField

# Create your models here.
DEPT=(
    ('计算机与通信学院','计算机与通信学院'),
    ('电气与自动化学院','电气与自动化学院'),
    ('外国语学院','外国语学院'),
    ('理学院','理学院'),
)
ITYPE=(
    ('老师','老师'),
    ('学生','学生'),
)

class UserEx(models.Model):
    # 与user一对一
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 添加属性
    id=models.CharField('学号',max_length=20,primary_key=True)
    name=models.CharField('姓名',max_length=20)
    dept=models.CharField('学院',max_length=20,choices=DEPT,default=None)
    major=models.CharField('专业',max_length=20,default=None)
    type=models.CharField('身份', max_length=20, choices=ITYPE,default=None)

    class Meta:
        db_table='exuser'
        verbose_name='用户'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.id;

class Question(models.Model):

    ANSWER = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )

    id = models.AutoField(primary_key=True)
    category = models.CharField('标签', max_length=20)
    title = models.TextField('题目')
    optionA = models.CharField('A选项', max_length=30)
    optionB = models.CharField('B选项', max_length=30)
    optionC = models.CharField('C选项', max_length=30)
    optionD = models.CharField('D选项', max_length=30)
    answer = models.CharField('答案', max_length=10, choices=ANSWER)
    score = models.IntegerField('分数', default=1)

    class Meta:
        db_table = 'question'
        verbose_name = '单项选择题库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<%s:%s>' % (self.category, self.title);

class Paper(models.Model):
    #题号qid 和题库为多对多的关系
    id=models.AutoField(primary_key=True)
    qid=models.ManyToManyField(Question)#多对多
    tid=models.ForeignKey(UserEx,on_delete=models.CASCADE)#添加外键
    title=models.CharField('标题',max_length=20,default='')
    major=models.CharField('考卷适用专业',max_length=20)
    examtime=models.DateTimeField()

    class Meta:
        db_table='paper'
        verbose_name='试卷'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.major;

class Grade(models.Model):
    id=models.AutoField(primary_key=True)
    sid=models.ForeignKey(UserEx,on_delete=models.CASCADE,default='')#添加外键
    pid=models.ForeignKey(Paper, on_delete=models.CASCADE)
    grade=models.IntegerField()
    rewind=models.TextField(default="")

    def __str__(self):
        return '<%s:%s>'%(self.sid,self.grade);

    class Meta:
        db_table='grade'
        verbose_name='成绩'
        verbose_name_plural=verbose_name

class TAnswer(models.Model):
    gid=models.ForeignKey(Grade, on_delete=models.CASCADE)
    qid=models.ForeignKey(Question, on_delete=models.CASCADE,default='')
    ans=models.CharField('选项',max_length=5)

    class Meta:
        db_table = 'answer'
        verbose_name = '试卷选项'
        verbose_name_plural = verbose_name

class Discussion(models.Model):
    id = models.AutoField(primary_key=True)
    qid = models.ForeignKey(Question, on_delete=models.CASCADE,default='')
    uid = models.ForeignKey(UserEx, on_delete=models.CASCADE)
    title = models.TextField('概要',max_length=50)
    detail = models.TextField('详细内容',max_length=500)
    solved = models.BooleanField(default='False')

    class Meta:
        db_table = 'discussion'
        verbose_name = '讨论'
        verbose_name_plural = verbose_name

class Reply(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    uid = models.ForeignKey(UserEx, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)

    class Meta:
        db_table = 'reply'
        verbose_name = '回复'
        verbose_name_plural = verbose_name

class AutoPaper(models.Model):
    #题号qid 和题库为多对多的关系
    id=models.AutoField(primary_key=True)
    qid=models.ManyToManyField(Question)#多对多
    sid=models.ForeignKey(UserEx,on_delete=models.CASCADE)#添加外键
    tag=models.CharField('标签',max_length=20)
    title = models.CharField('标题', max_length=20, default='')
    generate_time=models.DateField(auto_now_add=True)
    scores=models.IntegerField('总分')
    sum=models.IntegerField('题数')

    class Meta:
        db_table='autopaper'
        verbose_name='自动生成试卷'
        verbose_name_plural=verbose_name

class AutoGrade(models.Model):
    id=models.AutoField(primary_key=True)
    pid=models.ForeignKey(AutoPaper, on_delete=models.CASCADE)
    sid = models.ForeignKey(UserEx, on_delete=models.CASCADE, default='')  # 添加外键
    grade=models.IntegerField()

    def __str__(self):
        return '<%s:%s>'%(self.sid,self.grade);

    class Meta:
        db_table='autograde'
        verbose_name='模拟成绩'
        verbose_name_plural=verbose_name

class AutoTAnswer(models.Model):
    gid=models.ForeignKey(AutoGrade, on_delete=models.CASCADE)
    qid=models.ForeignKey(Question, on_delete=models.CASCADE,default='')
    ans=models.CharField('选项',max_length=5)

    class Meta:
        db_table = 'autoanswer'
        verbose_name = '模拟试卷选项'
        verbose_name_plural = verbose_name