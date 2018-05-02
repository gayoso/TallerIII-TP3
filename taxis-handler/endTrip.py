
# [START imports]
import os
import urllib
from urlparse import *
from datetime import datetime
import logging

from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.api import datastore
from google.appengine.api import taskqueue
from Models import *
from Configuration import *

import webapp2
from webapp2_extras import json

# [START endTrip]
class EndTrip(webapp2.RequestHandler):
	
	def get(self):
		
		trip_id = self.request.get("tripId")
		trip_key = ndb.Key(urlsafe=trip_id)
		
		trip = memcache.get(trip_key.urlsafe())
		if trip is None:
			trip = trip_key.get()
			if trip is None:
				logging.error("Received endTrip request for invalid trip id: %s", trip_id)
				return
			memcache.add(trip_key.urlsafe(), trip)
		
		dropoff_datetime = self.request.get("datetime")
		dropoff_latitude = self.request.get("latitude")
		dropoff_longitude = self.request.get("longitude")
		distance = float(self.request.get("distance"))
		
		trip.dropoff_datetime = datetime.strptime(dropoff_datetime, "%Y-%m-%d %H:%M:%S")
		trip.dropoff_location = ndb.GeoPt(dropoff_latitude, dropoff_longitude)
		trip.distance = distance
		
		trip.put();
		
		# pass to pull queue for dayli trips counter
		tag = trip.pickup_datetime.strftime("%Y-%m-%d")
		q = taskqueue.Queue(Configuration.DailyTripsTaskQueue)
		tasks = []
		payload_str = '1'
		tasks.append(taskqueue.Task(payload=payload_str, method='PULL', tag=tag))
		q.add(tasks)
		
		self.response.content_type = 'application/json'
		response_json = {
			'success': 'OK'
		}
		self.response.write(json.encode(response_json))

# [START app]
app = webapp2.WSGIApplication([
	('/endTrip', EndTrip)
], debug=True)
# [END app]