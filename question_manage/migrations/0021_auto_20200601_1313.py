# Generated by Django 2.2.12 on 2020-06-01 05:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question_manage', '0020_auto_20200601_1153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tanswer',
            options={'verbose_name': '答卷单选题', 'verbose_name_plural': '答卷单选题'},
        ),
        migrations.RenameField(
            model_name='autopaper',
            old_name='qid',
            new_name='sqid',
        ),
        migrations.AddField(
            model_name='autopaper',
            name='fqid',
            field=models.ManyToManyField(to='question_manage.Fillin'),
        ),
        migrations.AddField(
            model_name='grade',
            name='is_checked',
            field=models.BooleanField(default='False'),
        ),
        migrations.CreateModel(
            name='F_TAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ans', models.TextField(verbose_name='选项')),
                ('gid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question_manage.Grade')),
                ('qid', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='question_manage.Fillin')),
            ],
            options={
                'db_table': 'f_answer',
                'verbose_name_plural': '答卷填空题',
                'verbose_name': '答卷填空题',
            },
        ),
    ]
