# Generated by Django 2.2.12 on 2020-06-01 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question_manage', '0022_auto_20200601_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='f_tanswer',
            name='score',
            field=models.IntegerField(default=0, verbose_name='得分'),
        ),
        migrations.AddField(
            model_name='tanswer',
            name='score',
            field=models.IntegerField(default=0, verbose_name='得分'),
        ),
    ]
