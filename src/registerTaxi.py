
# [START imports]
import os
import urllib
from urlparse import *
from datetime import datetime

from google.appengine.ext import ndb
from Models import *

#import jinja2
import webapp2
from webapp2_extras import json

# [START registerTaxi]
class RegisterTaxi(webapp2.RequestHandler):
	
	def get(self):
		
		driver_name = self.request.get("driverName")
		
		taxi = Taxi(driver_name=driver_name)
			
		taxi_key = taxi.put()
		taxi_key_urlsafe = taxi_key.urlsafe()
		
		self.response.content_type = 'application/json'
		response_json = {
			'success': 'OK',
			'taxiKey': taxi_key_urlsafe
		}
		self.response.write(json.encode(response_json))

# [START app]
app = webapp2.WSGIApplication([
	('/registerTaxi', RegisterTaxi)
], debug=True)
# [END app]