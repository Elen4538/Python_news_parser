from django import template

from news.models import *

register = template.Library()

@register.simple_tag()
def get_tjnews():
    return TjournalNews.objects.using('tj_db').all().last()

@register.simple_tag()
def get_vcnews():
    return VcNews.objects.using('vc_db').all().last()

@register.simple_tag()
def get_habrnews():
    return HabrInfo.objects.using('habr_db').all().last()

@register.simple_tag()
def sum_news():
    res = (get_tjnews().post_number + get_habrnews().user_id +
            get_vcnews().post_number)
    return res


