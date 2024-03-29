# Generated by Django 2.2.6 on 2019-10-07 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(help_text='密码长度为8到16位字符串, 需包含大小写字母和数字', max_length=16, verbose_name='password'),
        ),

        migrations.RunSQL("UPDATE sqlite_sequence SET seq=1000 WHERE name='main_user'")
    ]
