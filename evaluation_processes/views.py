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
    return render(request, 'evaluation_processes/home.html')


def evaluation_dashboard(request):
    return render(request, 'evaluation_processes/evaluation_dashboard.html')


@login_required
def evaluation_360_application(request, team_member_id):
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
    return render(
        request,
        'evaluation_processes/evaluation_360_main_page.html',

    )


@login_required
def get_teammates(request):
    teams_ids = list(TeamMember.objects.filter(user=request.user).values_list('team_id', flat=True))

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
            'teammateHref': str(reverse('evaluation_360_application', args=(teammate['id'],)))
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
    return render(request, 'evaluation_processes/self_evaluation.html')


@login_required
def get_evaluation_application(request):
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
def post_evaluation_application(request):
    answer_questions = []
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        tabs = data['tabs']
        team_member_id = data['teamMemberId']

        # Check if there is a evaluation cycle.
        active_cycle = EvaluationCycle.objects.filter(is_active=True).first()
        if active_cycle:
            evaluation_360_manager = Evaluation360Manager.objects.create(
                cycle=active_cycle,
                evaluated_by=Employee.objects.get(user_id=team_member_id),
            )

            for tab in tabs:
                questions = tab['questions']
                for question in questions:
                    print('The question is : ', question)
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
