from django.db import models
from django.db.models import QuerySet, F
import uuid


class SurveySent(models.Model):
    id = models.CharField(max_length=64, primary_key=True, editable=False)
    survey = models.ForeignKey('survey.Survey', on_delete=models.DO_NOTHING)
    email = models.CharField(max_length=320, editable=False, blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    # TODO: think of something to change in logic

    class Meta:
        db_table = 'survey_sent'


class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    survey = models.ForeignKey('survey.Survey', on_delete=models.CASCADE)

    # TODO: think if hash should be resolved somewhere else, and here stored only user
    # hash = models.ForeignKey

    class Meta:
        db_table = 'submissions'


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey('survey.Question', on_delete=models.DO_NOTHING)
    content_numeric = models.FloatField(blank=True, null=True)  # changed that since api-v2
    content_character = models.TextField(blank=True, null=True)
    option = models.ForeignKey('survey.Option', on_delete=models.DO_NOTHING, blank=True, null=True)
    submission = models.ForeignKey(Submission, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'answers'
        