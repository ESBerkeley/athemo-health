# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    #title = request.GET['title']
    #msg = request.GET['msg']
    return render_to_response('home.html',context_instance=RequestContext(request))