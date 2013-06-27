# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from main import bot
from main.models import AutoReply


def goobo_control_panel(request):
    """
        Show the control panel page of GooBo
    """
    return render_to_response("main/goobo_control_panel.html",
                              {
                              },
                              context_instance=RequestContext(request))

goobo = bot.GooBo()


def goobo_take_over(request):
    """
        start/stop count down for auto-reply
    """
    is_active = request.GET.get("is_active", "0")
    # enable the default auto-reply
    default_auto_reply = AutoReply.objects.get(id=1)
    default_auto_reply.is_active = int(is_active)
    default_auto_reply.save()
    return HttpResponse(is_active)


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
