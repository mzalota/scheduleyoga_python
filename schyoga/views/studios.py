import logging
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

from django.template.response import TemplateResponse, SimpleTemplateResponse
from schyoga.bizobj.page import Page
from schyoga.bizobj.state import State
from schyoga.models import Studio

from schyoga.bizobj.schedule import Schedule

from django.views.generic.base import View

import datetime
import facebook

# Get an instance of a logger
logger = logging.getLogger(__name__)
#     logger.error('Found '+studios.count()+' instances of Studio objects for studio_url: '+studio_url_name)


#TODO: Show badge on Schedule Tab to show how many events we have there
#TODO: Show badge on Facebook Feed Tab to show how many posts we have there
#TODO: Get schyoga.com email address and post it on the 500 error page in prod

def list(request, state_url_name):
    state = State.createFromUrlName(state_url_name)
    if state is None:
        raise Http404

    studios = Studio.objects.all().filter(state_name_url=state_url_name).order_by('name')

    return render_to_response('studio/list.html',
                              {'studios': studios,
                               'state': state, },
                              context_instance=RequestContext(request))


def schedule_one_day(request, state_url_name, studio_url_name, year, month, day):
    """Handles view for old studio urls that end with date

     Handles urls such as this http://scheduleyoga.com/new-york/studios/bikram-yoga-grand-central/2013-10-08.html
    Notice the /2013-10-08.html at the end. The site no longer supports "these date urls" so they are redirected to Studio schedule page

    """

    newURL = reverse('studio-schedule', kwargs={'state_url_name': state_url_name, 'studio_url_name': studio_url_name})

    response = HttpResponse(content="", status=301)
    response["Location"] = newURL
    return response


class StudioViews(View):
    pagename = ''

    #template_name='studio/profile.html'
    def get(self, request, state_url_name, studio_url_name):

        curPage = Page.createFromEnum(self.pagename)
        if not curPage:
            assert "Invalid parameter to instantiate Page object"

        studio = get_object_or_404(Studio, nameForURL=studio_url_name)

        state = State.createFromUrlName(state_url_name)
        if not state:
            newURL = curPage.urlForStudioPage(studio)
            response = HttpResponse(content="", status=301)
            response["Location"] = newURL
            return response


        if self.pagename == Page.ENUM_STUDIO_PROFILE:
            return self.profile(request, studio, state, curPage)
        if self.pagename == Page.ENUM_STUDIO_SCHEDULE:
            return self.schedule(request, studio, state, curPage)
        if self.pagename == Page.ENUM_STUDIO_FACEBOOKFEED:
            return self.facebookFeed(request, studio, state, curPage)


    def profile(self, request, studio, state, curPage):
        return render_to_response('studio/profile.html',
                                  {'studio': studio,
                                   'state': state,
                                   'curPage': curPage},
                                  RequestContext(request))


    def schedule(self, request, studio, state, curPage):
        #TODO: filter events from DB by date, so that dates on the calendar correspond with what was pulled from DB

        #TODO: check if we need to pass State variable to every view. Extract it into a custom superclass based on View


        startDateStr = datetime.datetime.now().strftime('%Y-%m-%d')
        events = studio.event_set.all().order_by('start_time').filter(start_time__gt=startDateStr)

        sched = Schedule(events)
        #sched = Schedule(events, datetime.datetime(2013, 8, 6), 14)

        return render_to_response('studio/schedule.html',
                                  {'studio': studio,
                                   'state': state,
                                   'curPage': curPage,
                                   'calendar': sched,},
                                  RequestContext(request))



    def facebookFeed(self, request, studio, state, curPage):
        #https://www.facebook.com/JeanneEllenHeaton
        #https://graph.facebook.com/JeanneEllenHeaton/feed?access_token=CAAAAAITEghMBAIeRlyE803IvUcjjQ43WPkM44b36XLAnCVZBFjJEF76ZBBXaiDS7kBfSY4fqrEphDiXVZBl9ot9WFGZBCKpP7U9CcMMZCMIhmZBb0BBF5D7NLWY3a9XAj02EZCaOeksYFpm2bP4rWWthGN2X6MhWuCmokuZAnZAHSa8LYx21FmomqrvoJgtUmO0HhOkTGpqFU0DZA8wy9eKpGwDpxIvim1DhSGbYpK0LSABwZDZD
        #https://graph.facebook.com/me/feed?access_token=CAACZAZApvSluYBAPdgdAF0A2ZCPCnZBOYHHcPmte2ZCuzqkrDZAGLCM1xRQ9eanr8IQBJP09eGFQBHLFN641g1BeJZCj4HZA9xnq3D5i4d0q9OPNXbSjZAiZAaoGVnE54zGAIROMuTSOotXuaFPjK4uZBMXBCZCqy954MGZB7mX91i6bzolsIQG2wzTMdpJeSSKfODwUBTsSJYUV6aypVDyGVLEOedNAYNVUzTHQMCCQLqZCu7QQZDZD

        #Get token from here: https://developers.facebook.com/tools/explorer

        token = 'CAACEdEose0cBAMuCitukuwEJ9ymzsww0R4FmudJifbWIf4EnjGFmwm2HVUZBTCv3a4Da2id8dFC4WHLvgRWzDEwadZBTYWNUqW5QANGwdPYpClR6kcmrXZAqB2toBjf927HxWphZAR1rBgLziZBagTkEn7barRIZBufvSG3HgIM5FaqHZCsas5KAFEamZCx5ZCZBY5vHdUSBTQfRhJ9s3CbwPNkHMtOal43801QOKTru2ZC1wZDZD'
        graph = facebook.GraphAPI(token)

        fbUserId = studio.fbPageID  #'balancedyoga' #instructor.fb_userid

        #profile = graph.get_object("me")
        #friends = graph.get_connections("me", "friends")
        #friend_list = [friend['name'] for friend in friends['data']]

        if fbUserId:
            fbFeed = graph.get_connections(fbUserId, "feed")
            feeds = fbFeed['data']
        else:
            feeds = None

        return render_to_response('studio/facebook-feed.html',
                                  {'studio': studio,
                                   'state': state,
                                   'curPage': curPage,
                                   'feeds': feeds, },
                                  RequestContext(request))
