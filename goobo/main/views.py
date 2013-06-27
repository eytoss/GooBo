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

goobo = bot.GooBo()


def goobo_start(request):
    """
        start GooBo!!!
    """
    goobo.start_goobo()
    return HttpResponse("abcde")


def goobo_restart(request):
    """
        restart GooBo!!!
    """
    goobo.quit_goobo("#goobo")
    goobo.start_goobo()
    return HttpResponse("abcde")


def goobo_quit(request):
    """
        quit GooBo!!!
    """
    goobo.quit_goobo("#goobo")
    return HttpResponse("abcde")


def goobo_say(request):
    """
        call say() directly from web page
    """
    reply_to = request.GET.get("reply_to", "#goobo")
    message = request.GET.get("message", "")
    goobo.say(reply_to, message)
    return HttpResponse("abcde")
