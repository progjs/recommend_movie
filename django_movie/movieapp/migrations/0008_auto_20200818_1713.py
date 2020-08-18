# Generated by Django 3.1 on 2020-08-18 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieapp', '0007_auto_20200818_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='password2',
            field=models.CharField(default='password', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='birth',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='favorite_genre',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='sex',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
