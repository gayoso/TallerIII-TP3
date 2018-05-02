
# [START imports]
import os
import urllib
from urlparse import *
from datetime import datetime
from Configuration import *

from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.api import datastore
from google.appengine.api import taskqueue
from Models import *

import webapp2
import logging

# [START endTrip]
class DailyTripSummary(webapp2.RequestHandler):
	
	def get(self):
		
		q = taskqueue.Queue(Configuration.DailyTripsTaskQueue)
		tasks = q.lease_tasks_by_tag(Configuration.TasksLeaseDurationSeconds, Configuration.AmountOfTasksPerLease)
		logging.info(tasks)
		
		numTrips = len(tasks)
		if numTrips <= 0:
			return
		
		tag = tasks[0].tag
		statistic_key = ndb.Key('DailyStatistic', tag)
		statistic = memcache.get(tag)
		if statistic is None:
			statistic = statistic_key.get()
			if statistic is None:
				statistic = DailyStatistic(key=statistic_key, date=datetime.strptime(tag, "%Y-%m-%d"), trips=0)
			memcache.add(tag, statistic)
		statistic.trips += numTrips
		statistic.put()
		
		q.delete_tasks(tasks)

# [START app]
app = webapp2.WSGIApplication([
	('/tasks/daily-trip-summary', DailyTripSummary)
], debug=True)
# [END app]