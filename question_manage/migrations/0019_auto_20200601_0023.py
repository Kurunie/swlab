# Generated by Django 2.2.12 on 2020-05-31 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question_manage', '0018_auto_20200601_0008'),
    ]

    operations = [
        migrations.CreateModel(
            name='F_Discussion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField(max_length=50, verbose_name='概要')),
                ('detail', models.TextField(max_length=500, verbose_name='详细内容')),
                ('solved', models.BooleanField(default='False')),
                ('replied', models.BooleanField(default='False')),
            ],
            options={
                'verbose_name': '填空/简答题讨论',
                'verbose_name_plural': '填空/简答题讨论',
                'db_table': 'f_discussion',
            },
        ),
        migrations.AlterModelOptions(
            name='discussion',
            options={'verbose_name': '单选题讨论', 'verbose_name_plural': '单选题讨论'},
        ),
        migrations.AlterModelOptions(
            name='fillin',
            options={'verbose_name': '填空或简答题库', 'verbose_name_plural': '填空或简答题库'},
        ),
        migrations.AlterModelOptions(
            name='reply',
            options={'verbose_name': '单选题讨论回复', 'verbose_name_plural': '单选题讨论回复'},
        ),
        migrations.CreateModel(
            name='F_Reply',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(max_length=500)),
                ('did', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question_manage.F_Discussion')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question_manage.UserEx')),
            ],
            options={
                'verbose_name': '填空/简答题讨论回复',
                'verbose_name_plural': '填空/简答题讨论回复',
                'db_table': 'f_reply',
            },
        ),
        migrations.AddField(
            model_name='f_discussion',
            name='qid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='question_manage.Fillin'),
        ),
        migrations.AddField(
            model_name='f_discussion',
            name='uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question_manage.UserEx'),
        ),
    ]
