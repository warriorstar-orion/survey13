# Generated by Django 5.1.7 on 2025-03-24 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_remove_participant_cohort_cohort_participant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cohort',
            name='participant',
        ),
        migrations.AddField(
            model_name='cohort',
            name='participants',
            field=models.ManyToManyField(to='survey.participant'),
        ),
    ]
