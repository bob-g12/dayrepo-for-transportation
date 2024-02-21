# Generated by Django 4.2.2 on 2024-02-21 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0003_alter_snippet_end_mileage_alter_snippet_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='break_spot',
            field=models.CharField(max_length=20, verbose_name='休憩地点'),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='end_point',
            field=models.CharField(max_length=20, verbose_name='最終到着地点'),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='日報ID'),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='start_point',
            field=models.CharField(max_length=20, verbose_name='出発地点'),
        ),
    ]
