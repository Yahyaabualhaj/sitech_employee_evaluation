from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Constants.
Multiple_Choice = 'Multiple_Choice'
Open_Ended_Question = 'Open_Ended_Question'

Question_Type = (
    (Multiple_Choice, _('Multiple Choice')),
    (Open_Ended_Question, _('Open Ended Question')),
)

Evaluation_360 = 'Evaluation_360'
Evaluation_Self = 'Open_Ended_Question'

Evaluation_Type = (
    (Evaluation_360, _('360 Evaluation')),
    (Evaluation_Self, _('Self Evaluation')),

)

Evaluation_360 = 'Evaluation_360'
Evaluation_Self = 'Open_Ended_Question'


# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255, null=False, blank=False)
    education_level = models.CharField(max_length=255, null=False, blank=False)
    role = models.CharField(max_length=255, null=False, blank=False)
    join_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.get_full_name()} || {self.job_title} @ {self.join_date}'


class EvaluationCycle(models.Model):
    year = models.CharField(max_length=10)
    quarter = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Quarter-{self.quarter} of {self.year} || is active? {self.is_active}'


class Evaluation360Manager(models.Model):
    cycle = models.ForeignKey('EvaluationCycle', on_delete=models.CASCADE)
    evaluated_member = models.ForeignKey(
        'Employee',
        db_column='evaluated_member',
        related_name='evaluation_processes_%(class)s_evaluated_member',
        on_delete=models.CASCADE
    )  # The employee/member who evaluated.
    evaluated_by = models.ForeignKey(
        'Employee',
        db_column='created_by',
        related_name='evaluation_processes_%(class)s_evaluated_by',
        on_delete=models.CASCADE
    )  # The Employee/member who did the evaluation (logged in user).

    def __str__(self):
        return f'Quarter-{self.cycle.quarter} of {self.cycle.year} || from: {self.evaluated_by.user.get_full_name()} | to: {self.evaluated_member.user.get_full_name()}'


class Evaluation360(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.CharField(max_length=255, null=False, blank=False)
    evaluation_360_manager = models.ForeignKey('Evaluation360Manager', on_delete=models.CASCADE)

    def __str__(self):
        return f'Q-{self.question.id} answered? {self.answer} || C: {self.evaluation_360_manager.cycle}'


class Question(models.Model):
    evaluation_type = models.CharField(
        max_length=255,
        choices=Evaluation_Type,
        null=False,
        blank=False
    )
    question_type = models.CharField(
        max_length=255,
        choices=Question_Type,
        null=False, blank=False
    )
    question_category = models.ForeignKey(
        'evaluation_processes.QuestionCategory',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    text = models.TextField(null=False, blank=False)
    disabled = models.BooleanField(default=False)
    required = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.evaluation_type}|{self.question_type} = {self.text}'


class QuestionCategory(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)

    def __str__(self):
        return f'{self.name} || {self.description}'


class QuestionChoices(models.Model):
    text = models.CharField(max_length=255, null=False, blank=False)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.text} == {self.weight}'


class Answer(models.Model):
    # evaluation_type = models.CharField(max_length=255, choices=Evaluation_Type, null=False, blank=False)
    text = models.CharField(max_length=255, null=False, blank=False)
    # weight = models.IntegerField(default=0)


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

    def __str__(self):
        return f'{self.user} || {self.team}'

    class Meta:
        unique_together = ('user', 'team')
