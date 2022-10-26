from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from org_admin.models import Program, ProgramAnnouncement, Survey, SurveyField


class AddProgram(CreateView):
    model = Program
    fields = "__all__"
    template_name = "org_admin/add_program.html"
    success_url = reverse_lazy("org_admin:programs")


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
    return render(request, "org_admin/create_survey.html", {'program': Program.objects.get(pk=program_pk)})


def save_survey(request, program_pk):
    survey = Survey(program=Program.objects.get(pk=program_pk))
    survey.name = request.POST['survey-title']
    labels = []
    for key in request.POST:
        val: str = request.POST[key]
        if key.startswith("field"):
            labels.append(SurveyField(label=val, survey=survey))
    survey.is_active = True
    survey.save()
    for label in labels:
        label.save()
    return redirect("org_admin:home")
