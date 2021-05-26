from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255, null=False, blank=False)
    education_level = models.CharField(max_length=255, null=False, blank=False)
    role = models.CharField(max_length=255, null=False, blank=False)
    join_date = models.DateField()
    evaluation_manager = models.ForeignKey('EvaluationManager', on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.get_full_name()} || {self.job_title} @ {self.join_date}'


class EvaluationManager(models.Model):
    year = models.CharField(max_length=10)
    quarter = models.CharField(max_length=10)
    evaluated_by = models.ForeignKey('Employee', on_delete=models.CASCADE)
    evaluation_360 = models.ForeignKey('Evaluation360', on_delete=models.CASCADE)

    def __str__(self):
        return f'Quarter-{self.quarter} of {self.year} from {self.evaluated_by.user.get_full_name()}'


class Evaluation360(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)


class Question(models.Model):
    stage = models.CharField(max_length=255, null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    category = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    def __str__(self):
        return f'{self.stage}|{self.category}={self.text}'


class Answer(models.Model):
    stage = models.CharField(max_length=255, null=False, blank=False)
    text = models.CharField(max_length=255, null=False, blank=False)
    weight = models.IntegerField(default=0)


class SelfAssignment(models.Model):
    pass


class Team(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    members = models.ManyToManyField(User, through='TeamMember')

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'team')
