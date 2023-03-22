from django.contrib import admin

from .models import *

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'source','header', 'news_date')
    list_display_links = ('source','header')
    search_fields = ('source', 'header')



admin.site.register(NewsNews, NewsAdmin)
