from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Contest)
admin.site.register(Theme)
admin.site.register(Problem)
admin.site.register(Season)
admin.site.register(Parallel)
admin.site.register(User)
admin.site.register(Participation)
admin.site.register(Language)