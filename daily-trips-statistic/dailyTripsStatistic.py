
# [START imports]
import os
import urllib
from urlparse import *
from datetime import datetime
from datetime import timedelta

from google.appengine.ext import ndb
from google.appengine.api import memcache
from Models import *

import jinja2
import webapp2
from webapp2_extras import json

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
# [END imports]

# [START checkFacturacion]
class DailyTripsStatistic(webapp2.RequestHandler):
	
	def get(self):
	
		template_values = {
            'date': datetime.today().strftime('%Y-%m-%d')
        }
		
		template = JINJA_ENVIRONMENT.get_template('daily-trips-statistic-index.html')
		self.response.write(template.render(template_values))
	
	def post(self):
	
		date = self.request.get("date")
		statistic_key = ndb.Key('DailyStatistic', date)
		
		statistic = memcache.get(statistic_key.urlsafe())
		if statistic is None:
			statistic = statistic_key.get()
			if statistic is None:
				num_trips = 0
			else:
				memcache.add(statistic_key.urlsafe(), statistic)
				num_trips = statistic.trips
		else:
			num_trips = statistic.trips
		
		showTrips = True
		template_values = {
			'date': date,
			'number_of_trips': num_trips,
			'showTrips': showTrips
		}
		
		template = JINJA_ENVIRONMENT.get_template('daily-trips-statistic-index.html')
		self.response.write(template.render(template_values))
		
# [END checkFacturacion]

# [START app]
app = webapp2.WSGIApplication([
	('/dailyTripsStatistic', DailyTripsStatistic)
], debug=True)
# [END app]