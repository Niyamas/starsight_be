# Generated by Django 4.1.1 on 2022-09-09 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navigations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='links',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='navigation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]