# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def goobo_control_panel(request):
    """
        Show the control panel page of GooBo
    """
    return render_to_response("main/goobo_control_panel.html",
                              {
                               },
                              context_instance=RequestContext(request))


