from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from evaluation_processes.models import QuestionCategory, TeamMember, QuestionChoices, Evaluation360Manager, \
    EvaluationCycle, Employee, Evaluation360
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse


def home(request):
    """
    Home page.
    """

    return render(request, 'evaluation_processes/home.html')


@login_required
def evaluation_dashboard(request):
    """
    Evaluation dashboard to display all required notifications and performance graphs for employee.
    """
    return render(request, 'evaluation_processes/evaluation_dashboard.html')


@login_required
def evaluation_360_application(request, team_member_id):
    """
    To render the vue.js page to display 360 evaluation form/application.

    Args:
        team_member_id(str): The team member who will evaluated from logged in user.
    """
    return render(
        request,
        'evaluation_processes/evaluation_360_application.html',
        {
            'user_id': request.user.id,
            'team_member_id': team_member_id
        }
    )


@login_required
def evaluation_360(request):
    """
    To render the vue.js page to display the team members that you can evaluate them.
    """
    return render(
        request,
        'evaluation_processes/evaluation_360_main_page.html',

    )


@login_required
def get_teammates(request):
    """
    Get all team members who will evaluated by logged in user  to use with (Vue.js).
    
    Returns: Json data
    """
    teams_ids = list(TeamMember.objects.filter(user=request.user).values_list('team_id', flat=True))

    # Get all team members 
    members = list(
        TeamMember.objects.filter(team_id__in=teams_ids).values_list('user__id', flat=True).exclude(user=request.user)
    )

    members_ids = list(dict.fromkeys(members))

    teammates = User.objects.filter(id__in=members_ids).values('id', 'first_name', 'last_name')
    teammates = [
        {
            'id': teammate['id'],
            'firstName': teammate['first_name'],
            'lastName': teammate['last_name'],
            'teammateHref': str(reverse('evaluation_360_application', args=(teammate['id'],))),
            'is_evaluated': Evaluation360Manager.objects.filter(
                evaluated_member__user_id=teammate['id'],
                evaluated_by__user_id=request.user.id,

            ).exists(),
        }
        for teammate in teammates
    ]

    return JsonResponse(
        {
            'success': True,
            'teammates': teammates,
        }
    )


def self_evaluation(request):
    """
    Self evaluation form page.
    """
    return render(request, 'evaluation_processes/self_evaluation.html')


@login_required
def get_evaluation_application(request):
    """
    Get all evaluation question to build the evaluation application to use with (Vue.js).
    
    Returns: Json data.
    """
    tabs = []
    if request.method == 'GET':

        question_category = QuestionCategory.objects.all()
        choices = QuestionChoices.objects.all().values('id', 'text')
        choices = [{'key': choice['id'], 'name': choice['text']} for choice in choices]

        show_active = True

        for cat in question_category:
            all_questions = cat.question_set.all().values('id', 'text', 'question_type')
            questions = []
            for q in all_questions:
                questions.append({
                    'id': q['id'],
                    'name': q['text'],
                    'text': q['text'],
                    'value': None,
                    'choices': choices,
                    'questionType': q['question_type'],
                    'disabled': False,
                    'required': True,
                })

            tabs.append({
                'name': tab_name_converter(cat.name),
                'text': cat.name,
                'description': cat.description,
                'active': 'show active' if show_active else '',
                'tabActivated': 'active' if show_active else '',
                'questions': questions,
            })
            show_active = False

    return JsonResponse(
        {
            'success': True,
            'message': 'The form is submitted successfully',
            'tabs': tabs,
            'user_id': request.user.id
        }
    )


@csrf_exempt
@login_required
def post_evaluation_application(request):
    """
    Receive (from Vue.js) the answered evaluation form and save in DB.
    
    Returns:
        team_member_id(str): The team member who will evaluated.
    """
    answer_questions = []
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        tabs = data['tabs']
        team_member_id = data['teamMemberId']

        # Check if there is a evaluation cycle.
        active_cycle = EvaluationCycle.objects.filter(is_active=True).first()
        evaluated_by = Employee.objects.filter(user=request.user).first()  # the logged in user of did the evaluation.
        evaluated_member = Employee.objects.get(pk=team_member_id)  # the member who was evaluated.

        if active_cycle:
            evaluation_360_manager, __ = Evaluation360Manager.objects.get_or_create(
                evaluated_member=evaluated_member,
                evaluated_by=evaluated_by,
                cycle=active_cycle,
            )

            # Start collect the answers tab after tab.
            for tab in tabs:
                questions = tab['questions']  # Get all questions related to specific tab.
                for question in questions:

                    if question.get('value') is not None:

                        Evaluation360.objects.create(
                            question_id=question.get('id'),
                            answer=question.get('value'),
                            evaluation_360_manager=evaluation_360_manager,
                        )
                        answer_questions.append({
                            'id': question.get('id'),
                            'value': question.get('value'),
                        })
                    else:
                        return JsonResponse(
                            {
                                'success': False,
                                'error': f"The question {question.get('name')} is not answered",
                            }
                        )

            return JsonResponse(
                {
                    'success': True,
                    'answer_questions': answer_questions
                }
            )


def tab_name_converter(text):
    split_texts = text.split(' ')
    final_name = ''
    for txt in split_texts:
        final_name += txt

    return final_name
