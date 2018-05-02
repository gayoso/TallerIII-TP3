
# [START imports]
import os
import urllib
from urlparse import *
from datetime import datetime
from datetime import timedelta

from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb
from google.appengine.api import memcache
from Models import *
from Configuration import *

import jinja2
import webapp2
from webapp2_extras import json
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
# [END imports]

# [START adminQuery]
class AdminQuery(webapp2.RequestHandler):

	def get(self):
	
		template_values = {
            'results': {},
			'query_date_from': "2018-04-01",
			'query_date_to': datetime.today().strftime('%Y-%m-%d'),
			'driverId': "",
			'prev_cursor': "",
			'next_cursor': "",
			'TRIPS_PER_PAGE': Configuration.AdminQueryDefaultTripsPerPage
        }
		
		template = JINJA_ENVIRONMENT.get_template('admin-query-index.html')
		self.response.write(template.render(template_values))
	
	def post(self):
	
		TRIPS_PER_PAGE = int(self.request.get("TRIPS_PER_PAGE"))
		
		# IF prev BUTTON WAS PRESSED
		is_prev = self.request.get("prev", "") != ""
		
		# DRIVER QUERY		
		driverId = self.request.get("driverId", "")
		
		# DATE FROM QUERY
		query_date_from = datetime.strptime(self.request.get("query_date_from"), "%Y-%m-%d")
		
		# DATE TO QUERY
		query_date_to = datetime.strptime(self.request.get("query_date_to"), "%Y-%m-%d")
		
		# CURSOR
		prev_cursor_before = self.request.get('prev_cursor',default_value="")
		next_cursor_before = self.request.get('next_cursor',default_value="")
		
		# if a driver_id was input, use it to filter
		if driverId == "":
			query = Trip.query(ndb.AND(Trip.pickup_datetime >= query_date_from, Trip.pickup_datetime < query_date_to + timedelta(days=1)))
		else:
			driver_key = ndb.Key(urlsafe=driverId).get() # usar memcache
			query = Trip.query(ndb.AND(Trip.pickup_datetime >= query_date_from, Trip.pickup_datetime < query_date_to + timedelta(days=1)), ancestor=driver_key)
		
		# --------- PAGE MANAGEMENT		
		query_forward = query.order(Trip.pickup_datetime)
		query_reverse = query.order(-Trip.pickup_datetime)
		
		if is_prev:
			qry = query_reverse
			cursor = ndb.Cursor(urlsafe=prev_cursor_before).reversed() if prev_cursor_before != "" else None
		else:
			qry = query_forward
			cursor = ndb.Cursor(urlsafe=next_cursor_before) if next_cursor_before != "" else None
			
		# trips in page
		query_results, cursor, more = qry.fetch_page(TRIPS_PER_PAGE, start_cursor=cursor)
		# get driver info for each trip
		results = []
		drivers = {}
		for result in query_results:
			taxiKey = result.key.parent()
			if taxiKey.urlsafe() not in drivers:
				taxi = memcache.get(taxiKey.urlsafe())
				if taxi is None:
					taxi = taxiKey.get()
					if taxi is None:
						logging.error("Received trip exists for taxiKey: %s, but taxi doesn't exist", trip_id)
						taxi = { "driver_name": "MISSING" }
					else:
						memcache.add(taxiKey.urlsafe(), taxi)
				drivers[taxiKey.urlsafe()] = taxi.driver_name
			total_result = { "driver": drivers[taxiKey.urlsafe()], "trip": result }
			results.append(total_result)
		
		if is_prev:
			prev_cursor_url = cursor.reversed().urlsafe() if more else ""
			next_cursor_url = prev_cursor_before
		else:
			prev_cursor_url = next_cursor_before
			next_cursor_url = cursor.urlsafe() if more else ""
		# ---------
			
		template_values = {
			'results': results,
			'query_date_from': query_date_from,
			'query_date_to': query_date_to,
			'driverId': driverId,
			'prev_cursor': prev_cursor_url,
			'next_cursor': next_cursor_url,
			'TRIPS_PER_PAGE': TRIPS_PER_PAGE
		}
		
		template = JINJA_ENVIRONMENT.get_template('admin-query-index.html')
		self.response.write(template.render(template_values))
		
# [END adminQuery]

# [START app]
app = webapp2.WSGIApplication([
	('/adminQuery', AdminQuery)
], debug=True)
# [END app]