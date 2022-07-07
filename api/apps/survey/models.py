from django.db import models
from django.db.models import QuerySet, F
import uuid


# reorganized some things especially nested section under survey
class Survey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    creator = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # new field since api-v2
    starts_at = models.DateTimeField(blank=True, null=True)  # TODO: default: now
    expires_at = models.DateTimeField(blank=True, null=True)
    paused = models.BooleanField(default=False)
    anonymous = models.BooleanField(default=False)
    greeting = models.TextField(blank=True, null=True)
    farewell = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'surveys'
        ordering = ['-created_at']


class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'sections'


class Item(models.Model):
    # TODO: test if that works
    class ItemType(models.IntegerChoices):
        LIST = (1, 'list')
        GRID_SINGLE = (2, 'gridSingle')
        GRID_MULTIPLE = (3, 'gridMultiple')
        SCALE5 = (4, 'scale5')
        SCALE10 = (5, 'scale10')
        SCALE_NPS = (6, 'scaleNPS')
        OPEN_SHORT = (7, 'openShort')
        OPEN_LONG = (8, 'openLong')
        OPEN_NUMERIC = (9, 'openNumeric')
        CLOSED_SINGLE = (10, 'closedSingle')
        CLOSED_MULTIPLE = (11, 'closedMultiple')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    type = models.IntegerField(choices=ItemType.choices)
    required = models.BooleanField(default=False)

    class Meta:
        db_table = 'items'


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.IntegerField(default=1)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='questions')
    value = models.TextField()

    class Meta:
        db_table = 'questions'


# announced new field 'order' in api-v2
class Option(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.IntegerField(default=1)  # new field since api-v2
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='options')
    content = models.TextField()  # changed that to non-null since api-v2

    class Meta:
        db_table = 'options'


class Precondition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING, related_name='preconditions')
    next_item = models.ForeignKey(Item, on_delete=models.DO_NOTHING, related_name='preconditions_next')
    expected_option = models.ForeignKey(Option, on_delete=models.DO_NOTHING)
    value = models.TextField()

    class Meta:
        db_table = 'preconditions'
