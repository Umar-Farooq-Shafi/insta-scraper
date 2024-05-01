# Django
from django.http import HttpResponseRedirect
from .models import *
import logging
from decouple import config

from strategy import RunForeverWithBreaks


from django.contrib import messages

def scrap(request):
    with AutoLikeBot(configure_chrome_driver(),
                     post_filter=MyCustomFilter(ignore_tags=config.IGNORE_TAGS),
                     running_strategy=RunForeverWithBreaks(200)) as bot:
        bot.like_from_explore()

    messages.success(request, "Timetable extraction successful.")
    return HttpResponseRedirect('/main/')
