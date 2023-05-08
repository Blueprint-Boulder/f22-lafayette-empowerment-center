from datetime import datetime

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView

from guardian.models import Student
from org_admin.models import Program, ProgramAnnouncement, Survey, SurveyField, CommunityContact
from accounts.models import Notification, LECUser


def is_org_admin(user: User):
    if not user.is_authenticated:
        return False
    assert isinstance(user, LECUser)
    return user.account_type == LECUser.AccountTypes.ORG_ADMIN

# like @user_passes_test(is_org_admin), but for class-based views
cbv_user_must_be_org_admin = method_decorator(user_passes_test(is_org_admin), "dispatch")


@cbv_user_must_be_org_admin
class AddProgram(CreateView):
    model = Program
    fields = ["name", "description", "registration_opens", "registration_closes", "program_starts", "program_ends"]
    template_name = "org_admin/add_program.html"
    success_url = reverse_lazy("org_admin:programs")

    def form_valid(self, form):
        form.instance.is_active = True
        return super().form_valid(form)

@cbv_user_must_be_org_admin
class EditProgram(UpdateView):
    model = Program
    fields = ["name", "description", "registration_opens", "registration_closes", "program_starts", "program_ends"]
    template_name = "org_admin/edit_program.html"
    success_url = reverse_lazy("org_admin:programs")  # TODO change to specific program URL


@cbv_user_must_be_org_admin
class MakeAnnouncement(CreateView):
    model = ProgramAnnouncement
    fields = ["title", "content"]
    template_name = "org_admin/make_announcement.html"

    def form_valid(self, form):
        program_pk = int(self.kwargs["program_pk"])
        print(program_pk)
        form.instance.program = Program.objects.get(pk=program_pk)
        form.instance.save()
        notif = Notification(message=f"New announcement for {form.instance.program.name}: {form.instance.title}",
                             link=reverse("guardian:view_announcement", kwargs={'announcement_pk': form.instance.pk}))
        notif.save()
        for student in form.instance.program.students.all():
            notif.recipients.add(student.guardian)
        return redirect("org_admin:view_program", program_pk)

@user_passes_test(is_org_admin)
def view_program(request, program_pk):
    program = Program.objects.get(pk=program_pk)
    return render(request, "org_admin/view_program.html",
              {"programs": Program.objects.all(), "program": program,
               "now": datetime.now(),
               "sort_by": request.GET.get("roster-sort-by", default="name") or "name",
               "ascending": request.GET.get("roster-asc", default="ascending") == "ascending",
               "search": request.GET.get("roster-search", default=""),
               "students": program.students.filter(name__contains=request.GET.get("roster-search", default=""))})

@user_passes_test(is_org_admin)
def programs(request):
    return render(request, "org_admin/view_programs.html", {"programs": Program.objects.all()})

@user_passes_test(is_org_admin)
def view_child(request, child_pk):
    return render(request, "org_admin/view_child.html", {'child': Student.objects.get(pk=child_pk)})

@user_passes_test(is_org_admin)
def create_survey(request, program_pk):
    if request.method == "GET":
        return render(request, "org_admin/create_survey.html", {'program': Program.objects.get(pk=program_pk)})

    elif request.method == "POST":
        survey = Survey(program=Program.objects.get(pk=program_pk))
        survey.name = request.POST['survey_title']
        labels = []
        for key in request.POST:
            if key.startswith("field"):
                labels.append(SurveyField(label=request.POST[key], survey=survey))
        survey.is_active = True
        survey.save()
        for label in labels:
            label.save()

        notif = Notification(message=f"You have a new survey to take for {survey.program.name}: \"{survey.name}\"",
                             link=reverse("guardian:take_survey", kwargs={'survey_pk': survey.pk}))
        notif.save()
        for student in survey.program.students.all():
            notif.recipients.add(student.guardian)

        return redirect("org_admin:view_program", program_pk)

@user_passes_test(is_org_admin)
def survey_responses(request, survey_pk):
    return render(request, "org_admin/survey_responses.html", {'survey': Survey.objects.get(pk=survey_pk), "programs": Program.objects.all()})

@user_passes_test(is_org_admin)
def community_contacts(request):
    return render(request, "org_admin/community_contacts.html", {'contacts': CommunityContact.objects.all()})

class AddCommunityContact(CreateView):
    model = CommunityContact
    fields = "__all__"
    success_url = reverse_lazy("org_admin:community_contacts")
    template_name = "org_admin/add_community_contact.html"

@user_passes_test(is_org_admin)
def view_students(request):
    return render(request, "org_admin/view_students.html",
                  {"sort_by": request.GET.get("roster-sort-by", default="name") or "name",
                   "ascending": request.GET.get("roster-asc", default="ascending") == "ascending",
                   "search": request.GET.get("roster-search", default=""),
                   "students": Student.objects.filter(name__contains=request.GET.get("roster-search", default=""))})
