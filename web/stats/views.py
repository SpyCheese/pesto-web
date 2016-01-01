from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from themes.themes_by_user import themes_by_user
from doreshka.doreshka_by_user import doreshka_by_user_str
from .forms import AdminThemesForm
from django import forms
import tool_stat_themes_count
from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    return HttpResponse("Sample text")

def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'profile.html', {'user': user,
                                            'themes': themes_by_user(user_id),
                                            'doreshka': doreshka_by_user_str(user_id)})

def users(request):
    users = User.objects.order_by('last_name', 'first_name')
    return render(request, 'users.html', {'users': users})

def home(request):
    return render(request, 'home.html')

@staff_member_required
def admin_themes(request):
    seasons = []
    for season in Season.objects.all():
        parallels = []
        for parallel in Parallel.objects.all():
            contests = list(Contest.objects.filter(season=season, parallel=parallel))
            if len(contests) == 0:
                continue
            parallels.append((parallel.name, contests))
        if len(parallels) == 0:
            continue
        seasons.append((season.name, parallels))
    seasons.reverse()

    top_str = ""
    if request.method == 'POST':
        form = AdminThemesForm(request.POST)
        for field_name in form.data:
            if not field_name.startswith('theme_'):
                continue
            value = form.data[field_name]
            if value == 'Prev':
                continue
            else:
                value = get_object_or_404(Theme, pk=int(value))
            contest = get_object_or_404(Contest, pk=int(field_name[len('theme_'):]))
            contest.theme = value
            contest.save()
        top_str = 'Данные о темах обновлены'
        tool_stat_themes_count.main("db.sqlite3")
        return render(request, 'admin_themes.html', {'top_str': top_str})

    form = AdminThemesForm()
    return render(request, 'admin_themes.html', {'top_str': top_str,
                                                 'seasons': seasons,
                                                 'form': form,
                                                 'themes': Theme.objects.all()})
