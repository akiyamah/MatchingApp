# Generated by Django 4.2 on 2023-04-17 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_user_annual_income_user_occupation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('未登録', '未登録'), ('M', '男性'), ('F', '女性'), ('O', 'その他')], max_length=10, null=True, verbose_name='gender'),
        ),
    ]
