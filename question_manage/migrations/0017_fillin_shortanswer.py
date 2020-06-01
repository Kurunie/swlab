# Generated by Django 2.2.12 on 2020-05-31 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question_manage', '0016_question_solution'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fillin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=20, verbose_name='标签')),
                ('title', models.TextField(verbose_name='题目')),
                ('answer', models.TextField(max_length=10, verbose_name='答案')),
                ('score', models.IntegerField(default=1, verbose_name='分数')),
                ('solution', models.TextField(default='无', verbose_name='解析')),
            ],
            options={
                'verbose_name_plural': '填空题库',
                'db_table': 'fillin',
                'verbose_name': '填空题库',
            },
        ),
        migrations.CreateModel(
            name='Shortanswer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=20, verbose_name='标签')),
                ('title', models.TextField(verbose_name='题目')),
                ('answer', models.TextField(max_length=10, verbose_name='答案')),
                ('score', models.IntegerField(default=1, verbose_name='分数')),
                ('solution', models.TextField(default='无', verbose_name='解析')),
            ],
            options={
                'verbose_name_plural': '简答题库',
                'db_table': 'Shortanswer',
                'verbose_name': '简答题库',
            },
        ),
    ]
