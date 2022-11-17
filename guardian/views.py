from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from guardian.models import Student, SurveyResponse, SurveyFieldResponse
from org_admin.models import Program, ProgramAnnouncement, Survey, SurveyField
from django.utils import timezone


def programs(request):
    return render(request, "guardian/view_programs.html", {'programs': Program.objects.all(), 'now': timezone.now()})


def view_program(request, program_pk):
    return render(request, "guardian/view_program.html", {'program': Program.objects.get(pk=program_pk), 'now': timezone.now()})


def view_announcement(request, announcement_pk):
    announcement = ProgramAnnouncement.objects.get(pk=announcement_pk)
    announcement.read_by.add(request.user)
    announcement.save()
    return render(request, "guardian/view_announcement.html",
                  {'announcement': ProgramAnnouncement.objects.get(pk=announcement_pk)})


def children(request):
    return render(request, "guardian/view_children.html", {'children': Student.objects.filter(guardian=request.user)})


class AddChild(CreateView):
    model = Student
    fields = ["name", "pronouns", "allergies", "additional_info"]
    template_name = "guardian/add_child.html"
    success_url = reverse_lazy("guardian:children")

    def form_valid(self, form):
        form.instance.guardian = self.request.user
        # this is here because it has side effects (i.e. saving the model) that must happen before returning
        default_redirect = super().form_valid(form)
        if "redirect_to" in self.kwargs:
            return redirect(self.kwargs["redirect_to"])
        else:
            return default_redirect


def register_for_program(request, program_pk):
    program = Program.objects.get(pk=program_pk)

    if request.method == "GET":
        return render(request, "guardian/register_for_program.html", {'program': program})

    elif request.method == "POST":
        program.students.set(request.POST.getlist("students"))
        program.save()
        return redirect("guardian:programs")


def take_survey(request, survey_pk):
    survey = Survey.objects.get(pk=survey_pk)

    if request.method == "GET":
        return render(request, "guardian/take_survey.html", {'survey': survey})

    elif request.method == "POST":
        survey_response = SurveyResponse()
        survey_response.survey = Survey.objects.get(pk=survey_pk)
        survey_response.respondent = request.user

        field_responses = []
        for key in request.POST:
            if key.startswith("field"):
                _, field_pk = key.split("_")
                field_responses.append(SurveyFieldResponse(text=request.POST[key], full_response=survey_response,
                                                           field=SurveyField.objects.get(pk=field_pk)))
        survey_response.save()
        for field_response in field_responses:
            field_response.save()
        survey_response.save()

        return redirect("guardian:view_program", survey.program.pk)
