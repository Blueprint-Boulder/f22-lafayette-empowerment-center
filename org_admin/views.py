from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from org_admin.models import Program, ProgramAnnouncement, Survey, SurveyField


class AddProgram(CreateView):
    model = Program
    fields = ["name", "description"]
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
        return redirect("org_admin:view_program", program_pk)


def view_program(request, program_pk):
    return render(request, "org_admin/view_program.html",
                  {'program': Program.objects.get(pk=program_pk)})


def programs(request):
    return render(request, "org_admin/view_programs.html", {"programs": Program.objects.all()})


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
        return redirect("org_admin:view_program", program_pk)


def survey_responses(request, survey_pk):
    return render(request, "org_admin/survey_responses.html", {'survey': Survey.objects.get(pk=survey_pk)})
