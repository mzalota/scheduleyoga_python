
from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response

from schyoga.models import Instructor
from schyoga.models import Studio
from schyoga.models import Event


import collections
import datetime

import facebook

class Schedule():
    def __init__(self, events, startDate, numDays = 14):
        self.events = events
        self.__startDate = startDate
        self.__numDays = numDays

        self.__orgEvents = self.__initOrganizedEvents(events)

        self.calendarTimesStr = self.__initStartTimes(events)

        self.calendarDates, self.calendarDatesStr = self.__initCalendarDates(startDate, numDays)

    def __initCalendarDates(self, startDate, numDays):
        calendarDates = []
        calendarDatesStr = []
        for i in range(numDays):
            curDate = startDate + datetime.timedelta(days=i)
            calendarDates.append(curDate)
            calendarDatesStr.append(curDate.strftime('%x'))

        return calendarDates, calendarDatesStr

    def __initStartTimes(self, events):
        startTimesStr = []
        distinctDates = []
        for event in self.events:
            startTimeStr = event.start_time.strftime('%H:%M')
            if not startTimeStr in startTimesStr:
                startTimesStr.append(startTimeStr)

        startTimesStr.sort()
        return startTimesStr


    def __initOrganizedEvents(self, events):
        """
        returns  dictionary - key is event start_time and value is array of events that start at that time.

        :return: collections.OrderedDict
        """
        startTimes = collections.OrderedDict()
        for event in events:
            startTimeStr = event.start_time.strftime('%H:%M')
            dayOfWeek = event.start_time.strftime('%x')
            if not startTimeStr in startTimes:
                startTimes[startTimeStr] = collections.OrderedDict() # dict() #first time that a key is inserted to the dictionary initalize value to be a list

            if not dayOfWeek in startTimes[startTimeStr]:
                startTimes[startTimeStr][dayOfWeek] = list() #first time that a key is inserted to the dictionary initalize value to be a list

            startTimes[startTimeStr][dayOfWeek].append(event)

        return startTimes


    def getEventsByDateAndTime(self, eventDate, eventTimeStr):
        eventDate = eventDate.strftime('%x')

        if not eventTimeStr in self.__orgEvents:
            return None;

        if not eventDate in self.__orgEvents[eventTimeStr]:
            return None

        return self.__orgEvents[eventTimeStr][eventDate]

def instructorSchedule(request, instructor_url_name):
    instructors = Instructor.objects.filter(name_url=instructor_url_name)
    instructor = instructors[0]
    eventsTmp = instructor.event_set.all().order_by('start_time')

    sched = Schedule(eventsTmp, datetime.datetime(2013, 8, 6), 14)

    return render_to_response('instructor-schedule.html',
                                {'instructor': instructor,
                                 'calendar': sched, },
                              RequestContext(request))


def instructorFacebookFeed(request, instructor_url_name):
    #https://www.facebook.com/JeanneEllenHeaton
    #https://graph.facebook.com/JeanneEllenHeaton/feed?access_token=CAAAAAITEghMBAIeRlyE803IvUcjjQ43WPkM44b36XLAnCVZBFjJEF76ZBBXaiDS7kBfSY4fqrEphDiXVZBl9ot9WFGZBCKpP7U9CcMMZCMIhmZBb0BBF5D7NLWY3a9XAj02EZCaOeksYFpm2bP4rWWthGN2X6MhWuCmokuZAnZAHSa8LYx21FmomqrvoJgtUmO0HhOkTGpqFU0DZA8wy9eKpGwDpxIvim1DhSGbYpK0LSABwZDZD
    #https://graph.facebook.com/me/feed?access_token=CAACZAZApvSluYBAPdgdAF0A2ZCPCnZBOYHHcPmte2ZCuzqkrDZAGLCM1xRQ9eanr8IQBJP09eGFQBHLFN641g1BeJZCj4HZA9xnq3D5i4d0q9OPNXbSjZAiZAaoGVnE54zGAIROMuTSOotXuaFPjK4uZBMXBCZCqy954MGZB7mX91i6bzolsIQG2wzTMdpJeSSKfODwUBTsSJYUV6aypVDyGVLEOedNAYNVUzTHQMCCQLqZCu7QQZDZD

    #Get token from here: https://developers.facebook.com/tools/explorer

    token = 'CAACEdEose0cBAFN6ojoBZBPq9vXv9iOJ5WPWHSLQ8jQb4ZC5waEzyYfvUnoMKiTN1Uz6NlWclZCekB2zBahrN2gMZBkUNxCr6VoPOV091AlbeF0HkqmGHMtsbGoUoZAOpmO7ISbFQmDDHRbGiVYgb5QcJpeCtwV5TRebuQaqg7ccwcp0bRkpQQjZB5noudVErpbWypL0pevKYxo0Pk5cAprmLPy8bNypkU35eD2Xx6GQZDZD'
    graph = facebook.GraphAPI(token)
    instructors = Instructor.objects.filter(name_url=instructor_url_name)
    instructor = instructors[0]
    fbUserId = instructor.fb_userid

    #profile = graph.get_object("me")
    #friends = graph.get_connections("me", "friends")
    #friend_list = [friend['name'] for friend in friends['data']]

    if fbUserId is not None:
        fbFeed = graph.get_connections(fbUserId, "feed")
        feeds = fbFeed['data']
    else:
        feeds = None

    return render_to_response('instructor-facebook-feed.html',
                          { 'instructor': instructor, 'feeds': feeds, },
                            RequestContext(request))


def instructor(request, instructor_url_name):

    instructors = Instructor.objects.filter(name_url=instructor_url_name)
    instructor = instructors[0]

    return render_to_response('instructor.html',
                          { 'instructor': instructor,},
                            RequestContext(request))


def instructors(request):
    #instructors = Instructor.objects.filter(instructor_name="Jeanne Heaton")
    instructors = Instructor.objects.all()

    return render_to_response('instructors.html',
                            { 'instructors': instructors, },
                            context_instance=RequestContext(request))