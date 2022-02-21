from django.contrib import admin
from evaluation_processes.models import *


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass


@admin.register(Evaluation360Manager)
class Evaluation360ManagerAdmin(admin.ModelAdmin):
    pass


@admin.register(Evaluation360)
class Evaluation360Admin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(SelfAssignment)
class SelfAssignmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(TeamMember)
class TeamMemberCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(QuestionChoices)
class QuestionChoicesCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(EvaluationCycle)
class EvaluationCycleCategoryAdmin(admin.ModelAdmin):
    pass


