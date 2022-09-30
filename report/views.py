from django.shortcuts import render, redirect

from banka_idea.models import User
from report.forms import ReportForm


def report_view(request, pk):
    reported_user = User.objects.get(id=pk)
    user = request.user
    form = ReportForm()
    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.reported_user = reported_user
            obj.save()
            return redirect('user-profile')
        else:
            print(form.errors)
    context = {
        'reported_user': reported_user,
        'form': form,
    }
    return render(request, "reports/report_form.html", context)
