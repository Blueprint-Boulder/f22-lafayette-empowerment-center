from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from guardian.forms import ProgramRegistrationForm
from guardian.models import ProgramRegistration, Student, SurveyResponse, SurveyFieldResponse
from org_admin.models import Program, ProgramAnnouncement, Survey, SurveyField


def programs(request):
    return render(request, "guardian/view_programs.html", {'programs': Program.objects.all()})


def view_program(request, program_pk):
    return render(request, "guardian/view_program.html", {'program': Program.objects.get(pk=program_pk)})


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
    success_url = reverse_lazy("guardian:register_for_program")

    def form_valid(self, form):
        form.instance.guardian = self.request.user
        return super().form_valid(form)


class RegisterForProgram(CreateView):
    model = ProgramRegistration
    form_class = ProgramRegistrationForm
    template_name = "guardian/register_for_program.html"
    success_url = reverse_lazy("guardian:programs")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.save()
        form.instance.students.set(self.request.POST.getlist("students"))
        return super().form_valid(form)


def take_survey(request, survey_pk):
    survey = Survey.objects.get(pk=survey_pk)
    return render(request, "guardian/take_survey.html", {'survey': survey})


def save_survey_response(request, survey_pk):
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

    return redirect("guardian:home")
