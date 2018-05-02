
# [START imports]
import os
import urllib
from urlparse import *
from datetime import datetime
from datetime import timedelta

from google.appengine.ext import ndb
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
class CheckFacturacion(webapp2.RequestHandler):
	
	def get(self):
	
		template_values = {
            'facturacion_results': {}
        }
		
		template = JINJA_ENVIRONMENT.get_template('check-facturacion-index.html')
		self.response.write(template.render(template_values))
	
	def post(self):
	
		driver_id = self.request.get("driverId")
		driver_key = ndb.Key(urlsafe=driver_id)
	
		query_date = datetime.strptime(self.request.get("query_date"), "%Y-%m-%d")
		
		facturacion_query = Trip.query(ndb.AND(Trip.pickup_datetime >= query_date, Trip.pickup_datetime < query_date + timedelta(days=1)), ancestor=driver_key).order(-Trip.pickup_datetime)
		facturacion_results = facturacion_query.fetch()
		
		template_values = {
			'facturacion_results': facturacion_results
		}
		
		template = JINJA_ENVIRONMENT.get_template('check-facturacion-index.html')
		self.response.write(template.render(template_values))
		
# [END checkFacturacion]

# [START app]
app = webapp2.WSGIApplication([
	('/checkFacturacion', CheckFacturacion)
], debug=True)
# [END app]