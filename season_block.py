
import datetime
from cabin_week import *

"""

A season block represents a window of weeks within a cabin 
season that assumes some inheriant rank. 

i.e. traditional cabin seasons have been blocked into "prime-time", "middle-season", "marginal-start" and "marginal-end"

for this implementation we will build our blocks into 8 week segments. 

"""

class season_block:

	def __init__(self, start_date, end_date, block_type):
		self.start_date = start_date
		self.end_date = end_date
		self.block_type = block_type
		self.weeks = self.__segment_block_weeks(start_date, end_date)

	def __segment_block_weeks(self, start_date, end_date):
		
		weeks = []

		# start cabin weeks on sundays
		if start_date.weekday() is not 6:
			print("error: weeks must start on sundays")

		# end date is exclusive (so it is the start date of the next season block)
		delta = datetime.timedelta(weeks=1)
		curr = start_date
		while curr < end_date:
			weeks.append(cabin_week(curr))
			curr += delta









