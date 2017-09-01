from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    name = models.TextField()
    email = models.TextField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=10)
    color = models.CharField(max_length=7)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class OperationalPlan(models.Model):
    year = models.TextField()
    description = models.TextField()

    def __unicode__(self):
        return self.year

    def __str__(self):
        return self.year


class OperationalArea(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class SubArea(models.Model):
    name = models.TextField()
    operational_area = models.ForeignKey(OperationalArea, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class LongTermGoal(models.Model):
    goaltext = models.TextField()
    description = models.TextField(default="", blank=True)
    sub_area = models.ForeignKey(SubArea, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.goaltext

    def __str__(self):
        return self.goaltext

    def first_year(self):
        return OperationalPlan.objects.filter(goal__in=self.goal_set).first()


class Goal(models.Model):
    year = models.ForeignKey(OperationalPlan, on_delete=models.CASCADE)
    long_term_goal = models.ForeignKey(LongTermGoal, on_delete=models.CASCADE)
    goal = models.TextField()
    description = models.TextField(default="", blank=True)
    status = models.ForeignKey(Status, null=True, on_delete=models.SET_NULL)
    responsible_groups = models.ManyToManyField(Group)

    def __unicode__(self):
        return self.goal

    def __str__(self):
        return self.goal


class Comment(models.Model):
    # Comment should belong to one of the following two goaltypes
    goal = models.ForeignKey(Goal, null=True, blank=True)
    long_term_goal = models.ForeignKey(LongTermGoal, null=True, blank=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    suggested_status = models.ForeignKey(Status, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.content

    def __str__(self):
        return self.content
