# Generated by Django 5.1.7 on 2025-03-26 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0011_question_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='kind',
            field=models.CharField(choices=[('UNSPECIFIED', 'Unspecified'), ('NUMERIC', 'Numeric Rating'), ('SINGLE_CHOICE', 'Single Choice'), ('MULTIPLE_CHOICE', 'Multiple Choice'), ('OPEN_ENDED', 'Open-ended')], default='UNSPECIFIED', max_length=50),
        ),
    ]
