# Generated by Django 2.2.12 on 2020-05-10 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question_manage', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userex',
            old_name='o_user',
            new_name='user',
        ),
    ]