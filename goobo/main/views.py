# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from main import bot


def goobo_control_panel(request):
    """
        Show the control panel page of GooBo
    """
    return render_to_response("main/goobo_control_panel.html",
                              {
                              },
                              context_instance=RequestContext(request))


def goobo_start(request):
    """
        start GooBo!!!
    """
    bot.start_goobo()
    return HttpResponse("abcde")
