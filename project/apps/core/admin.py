from django.contrib import admin
from .models import Disambiguation, WikiPage, Search

admin.site.register(Disambiguation)
admin.site.register(WikiPage)
admin.site.register(Search)
