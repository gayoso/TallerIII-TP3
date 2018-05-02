
# [START imports]
import os
import urllib
from urlparse import *
from datetime import datetime

from google.appengine.ext import ndb
from Models import *

import webapp2
from webapp2_extras import json

# [START startTrip]
class StartTrip(webapp2.RequestHandler):
	
	def get(self):
		
		driver_id = self.request.get("driverId")
		driver_key = ndb.Key(urlsafe=driver_id)
		new_id = ndb.Model.allocate_ids(size=1, parent=driver_key)[0]
		trip_key = ndb.Key('Trip', new_id, parent=driver_key)
		
		pickup_datetime = self.request.get("datetime")
		pickup_latitude = self.request.get("latitude")
		pickup_longitude = self.request.get("longitude")
		
		trip = Trip(key=trip_key, 
			pickup_datetime=datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S"),
			pickup_location=ndb.GeoPt(pickup_latitude, pickup_longitude))
			
		trip.put();
		self.response.content_type = 'application/json'
		response_json = {
			'success': 'OK',
			'tripKey': trip_key.urlsafe()
		}
		self.response.write(json.encode(response_json))

# [START app]
app = webapp2.WSGIApplication([
	('/startTrip', StartTrip)
], debug=True)
# [END app]