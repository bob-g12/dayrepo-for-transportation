# Generated by Django 4.2.2 on 2024-02-14 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='アカウントID')),
                ('last_name', models.CharField(max_length=25, verbose_name='姓')),
                ('first_name', models.CharField(max_length=25, verbose_name='名')),
                ('password', models.SlugField(max_length=20, verbose_name='パスワード')),
                ('is_administrator', models.BooleanField(default=False, verbose_name='管理権限')),
                ('is_approval', models.BooleanField(default=False, verbose_name='承認')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
            options={
                'verbose_name': 'アカウント',
                'db_table': 'accounts',
            },
        ),
    ]