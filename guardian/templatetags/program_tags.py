from django.template import Library

from accounts.models import LECUser
from guardian.models import SurveyResponse, Student
from org_admin.models import Program, Survey

register = Library()


@register.filter
def has_unread_announcements_in(user: LECUser, program: Program):
    for announcement in program.announcements.all():
        if user not in announcement.read_by.all():
            return True
    return False


@register.filter
def has_children_in(user: LECUser, program: Program):
    # don't know of a way to do this with a single query
    for student in program.students.all():
        if student in user.children.all():
            return True
    return False


@register.filter
def children_in(user: LECUser, program: Program):
    return set(student for student in program.students.all() if student in user.children.all())

@register.filter
def has_taken_survey(user: LECUser, survey: Survey):
    return SurveyResponse.objects.filter(respondent=user, survey=survey).exists()
