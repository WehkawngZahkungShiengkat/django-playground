# Generated by Django 5.1.6 on 2025-04-03 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_post_html_file_post_html_file_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='html_file_name',
        ),
    ]
