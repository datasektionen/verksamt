from django.db import models


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


class LongTermGoal(models.Model):
    goaltext = models.TextField()
    description = models.TextField(default="", blank=True)
    operational_area = models.ForeignKey(OperationalArea, on_delete=models.CASCADE)

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

    def __unicode__(self):
        return self.goal

    def __str__(self):
        return self.goal


class Status(models.Model):
    name = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
