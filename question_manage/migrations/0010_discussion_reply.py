# Generated by Django 2.2.12 on 2020-05-17 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question_manage', '0009_grade_rewind'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField(max_length=50, verbose_name='概要')),
                ('detail', models.TextField(max_length=500, verbose_name='详细内容')),
                ('qid', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='question_manage.Question')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question_manage.UserEx')),
            ],
            options={
                'verbose_name': '讨论',
                'verbose_name_plural': '讨论',
                'db_table': 'discussion',
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(max_length=500)),
                ('did', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question_manage.Discussion')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question_manage.UserEx')),
            ],
            options={
                'verbose_name': '讨论',
                'verbose_name_plural': '讨论',
                'db_table': 'reply',
            },
        ),
    ]
