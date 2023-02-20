from datetime import datetime

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from guardian.models import Student
from org_admin.models import Program, ProgramAnnouncement, Survey, SurveyField, CommunityContact
from accounts.models import Notification


class AddProgram(CreateView):
    model = Program
    fields = ["name", "description", "registration_opens", "registration_closes", "program_starts", "program_ends"]
    template_name = "org_admin/add_program.html"
    success_url = reverse_lazy("org_admin:programs")

    def form_valid(self, form):
        form.instance.is_active = True
        return super().form_valid(form)


class MakeAnnouncement(CreateView):
    model = ProgramAnnouncement
    fields = ["title", "content"]
    template_name = "org_admin/make_announcement.html"

    def form_valid(self, form):
        program_pk = int(self.kwargs["program_pk"])
        form.instance.program = Program.objects.get(pk=program_pk)
        form.instance.save()
        notif = Notification(message=form.instance.title,
                             link=reverse("guardian:view_announcement", kwargs={'announcement_pk': form.instance.pk}))
        notif.save()
        for student in form.instance.program.students.all():
            notif.recipients.add(student.guardian)
        return redirect("org_admin:view_program", program_pk)


def view_program(request, program_pk):
    return render(request, "org_admin/view_program.html",
                  {'program': Program.objects.get(pk=program_pk), 'now': datetime.now()})


def programs(request):
    return render(request, "org_admin/view_programs.html", {"programs": Program.objects.all()})

def view_child(request, child_pk):
    return render(request, "org_admin/view_child.html", {'child': Student.objects.get(pk=child_pk)})

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

        notif = Notification(message=survey.name,
                             link=reverse("guardian:take_survey", kwargs={'survey_pk': survey.pk}))
        notif.save()
        for student in survey.program.students.all():
            notif.recipients.add(student.guardian)

        return redirect("org_admin:view_program", program_pk)


def survey_responses(request, survey_pk):
    return render(request, "org_admin/survey_responses.html", {'survey': Survey.objects.get(pk=survey_pk)})


def community_contacts(request):
    return render(request, "org_admin/community_contacts.html", {'contacts': CommunityContact.objects.all()})


class AddCommunityContact(CreateView):
    model = CommunityContact
    fields = "__all__"
    success_url = reverse_lazy("org_admin:community_contacts")
    template_name = "org_admin/add_community_contact.html"


def view_students(request):
    return render(request, "org_admin/view_students.html",
                  {"students": Student.objects.all(),
                   "sort_by": request.GET["sort_by"],
                   "ascending": request.GET["ascending"] == "t"})
