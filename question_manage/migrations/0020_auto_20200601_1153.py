# Generated by Django 2.2.12 on 2020-06-01 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question_manage', '0019_auto_20200601_0023'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paper',
            old_name='qid',
            new_name='sqid',
        ),
        migrations.AddField(
            model_name='paper',
            name='fqid',
            field=models.ManyToManyField(to='question_manage.Fillin'),
        ),
    ]
