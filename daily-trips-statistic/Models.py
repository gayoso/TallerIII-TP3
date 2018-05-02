from google.appengine.ext import ndb

# [START taxi]
class Taxi(ndb.Model):
	"""A main model for representing a taxi driver."""
	driver_name = ndb.StringProperty(indexed=True);
# [END taxi]
	
# [START trip]
class Trip(ndb.Model):
	"""A main model for representing a taxi trip."""
	pickup_datetime = ndb.DateTimeProperty(indexed=True)
	pickup_location = ndb.GeoPtProperty(indexed=False)
	dropoff_datetime = ndb.DateTimeProperty(indexed=True)
	dropoff_location = ndb.GeoPtProperty(indexed=False)
	distance = ndb.FloatProperty(indexed=False)
# [END trip]

# [START statistic]
class DailyStatistic(ndb.Model):
	"""A main model for representing a daily trips statistic."""
	date = ndb.DateProperty(indexed=True)
	trips = ndb.IntegerProperty(indexed=False)
# [END statistic]