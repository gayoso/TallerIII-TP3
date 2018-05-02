
# [START imports]
import os
import urllib
from urlparse import *

import jinja2
import webapp2
from webapp2_extras import json

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
# [END imports]

# [START main]
class MainPage(webapp2.RequestHandler):
	
	def get(self):
		
		template = JINJA_ENVIRONMENT.get_template('default-index.html')
		self.response.write(template.render())
		
# [END main]

# [START app]
app = webapp2.WSGIApplication([
	('/', MainPage)
], debug=True)
# [END app]