from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from org_admin.models import Program, ProgramAnnouncement
from accounts.models import LECUser


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


def view_admin_requests(request):
    return render(request, "org_admin/view_admin_requests.html", {"users": LECUser.objects.all()})


def accept_admin_request(request, user_rq):
    user_rq.account_type = LECUser.AccountTypes.ORG_ADMIN
    user_rq.save()
    return render(request, "org_admin/view_admin_requests.html", {"users": LECUser.objects.all()})


def decline_admin_request(request, user_rq):
    user_rq.account_type = LECUser.AccountTypes.GUARDIAN
    user_rq.save()
    return render(request, "org_admin/view_admin_requests.html", {"users": LECUser.objects.all()})
