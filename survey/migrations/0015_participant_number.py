# Generated by Django 5.1.7 on 2025-04-15 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0014_survey_question_number_participant_survey_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='number',
            field=models.IntegerField(default=1),
        ),
    ]
