from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from stats.models import User
from .models import UserResult

def themes_by_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    parts = UserResult.objects.filter(user=user).values('participation').distinct().order_by('participation')
    parts = [str(i['participation']) for i in parts]
    result = []
    for part in parts:
        part_res = UserResult.objects.filter(user=user).filter(participation=part).order_by('solved')
        result.append([str(part_res[0].participation), []])
        for theme_res in part_res[::-1]:
            result[-1][1].append([theme_res.theme.name, theme_res.solved])
    template = loader.get_template('by_user.html')
    return template.render({'result': result}, request)
