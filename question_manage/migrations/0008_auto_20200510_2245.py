# Generated by Django 2.2.12 on 2020-05-10 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question_manage', '0007_auto_20200510_2236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tanswer',
            name='qid',
        ),
        migrations.AddField(
            model_name='tanswer',
            name='qid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='question_manage.Question'),
        ),
    ]