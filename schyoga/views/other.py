# Create your views here.

from django.template import loader, Context, RequestContext
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, render
from schyoga.bizobj.state import State

from schyoga.models import Instructor

import collections
import datetime

import facebook
from schyoga.models.event import Event
from schyoga.models.studio import Studio


def page404(request):
    response = render(request, "404.html")
    response.status_code = 404
    return response
    #return render(request, '404.html')


def index(request):
    return render_to_response('index.html', {}, RequestContext(request))


def states(request, state_url_name):

    state = State.createFromUrlName(state_url_name)
    if state is None:
        raise Http404

    return render_to_response('state.html', {'state': state}, RequestContext(request))


def siteMap(request):
    return render_to_response('site-map.html', {}, RequestContext(request))


def shoutOuts(request):
    return render_to_response('shout-outs.html', {}, RequestContext(request))

#TODO: V.2. Create separate page for each event, which would have microtags embeded
#TODO: V.2. Get schyoga.com email address and post it on the 500 error page in prod


 #def friends(request):
     #django_facebook.middleware.FacebookMiddleware.get_fb_user()
     # if request.facebook:
 #       friends = request.facebook.graph.get_connections('me', 'friends')


#<img src="{% static "my_app/myexample.jpg" %}" alt="My image"/>