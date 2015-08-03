from django.db import models

import recurrence as recur
from recurrence import managers, choices


class BaseRecurrence(models.Model):
    dtstart = models.DateTimeField(null=True, blank=True)
    dtend = models.DateTimeField(null=True, blank=True)

    objects = managers.RecurrenceManager()

    class Meta:
        abstract = True

    def to_recurrence_object(self):
        return self.__class__.objects.to_recurrence_object(self)


class Recurrence(BaseRecurrence):
    pass


class BaseRule(models.Model):
    mode = models.BooleanField(default=True, choices=choices.MODE_CHOICES)
    freq = models.PositiveIntegerField(choices=choices.FREQUENCY_CHOICES)
    interval = models.PositiveIntegerField(default=1)
    wkst = models.PositiveIntegerField(
        default=recur.Rule.firstweekday, null=True, blank=True)
    count = models.PositiveIntegerField(null=True, blank=True)
    until = models.DateTimeField(null=True, blank=True)

    objects = managers.RuleManager()

    class Meta:
        abstract = True

    def to_rule_object(self):
        return self.__class__.objects.to_rule_object(self)


class Rule(BaseRule):
    recurrence = models.ForeignKey(Recurrence, related_name='rules')


class BaseDate(models.Model):
    mode = models.BooleanField(default=True, choices=choices.MODE_CHOICES)
    dt = models.DateTimeField()

    class Meta:
        abstract = True


class Date(BaseDate):
    recurrence = models.ForeignKey(Recurrence, related_name='dates')


class BaseParam(models.Model):
    param = models.CharField(max_length=16)
    value = models.IntegerField()
    index = models.IntegerField(default=0)

    class Meta:
        abstract = True


class Param(BaseParam):
    rule = models.ForeignKey(Rule, related_name='params')
