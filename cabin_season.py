
import calendar
from season_block import *


"""

represents one season a Juniper dunes.

"""

class cabin_season:

	season_calander = calendar.Calendar(firstweekday=calendar.SUNDAY)
	change_segment = datetime.timedelta(weeks=1)

	def __init__(self, year, n_families):

		self.year = year
		open_close_weeks = self.__get_open_close_weeks(n_families)
		self.opening_week_start_date = open_close_weeks[0]
		self.closing_week_start_date = open_close_weeks[1]
		self.n_weeks = (self.closing_week_start_date - self.opening_week_start_date).days / 7
		self.season_blocks = self.__create_season_blocks()


	def __create_season_blocks(self):

		season_blocks = []

		if self.opening_week_start_date is not None and self.closing_week_start_date is not None:

			curr_date = self.opening_week_start_date
			curr_date_block_type = season_block_type.opening
			this_block_type = season_block_type.opening

			# iterate whole year
			while curr_date < self.closing_week_start_date:
				start_block_date = curr_date
				while curr_date_block_type is this_block_type:
					curr_date += cabin_season.change_segment
					curr_date_block_type = self.__get_season_block_type(curr_date)
				end_block_date = curr_date
				
				#block_type = self.__set_season_block_type(start_block_date, end_block_date)
				season_blocks.append(season_block(start_block_date, end_block_date, this_block_type))
				this_block_type = curr_date_block_type

		else:
			raise ValueError("cabin season ", self.year, " is missing opening/closing weeks")

		return season_blocks


	def __get_open_close_weeks(self, n_families):
		
		print('\nstarting dynamic scheduling ...\n')

		# earliest start is second week of april
		april_calander = cabin_season.season_calander.monthdatescalendar(self.year, 4)
		earliest_open_date = april_calander[2][0]
		open_date = earliest_open_date	

		# latest possible closing week is third week of oct 
		oct_calander = cabin_season.season_calander.monthdatescalendar(self.year, 10)
		latest_close_date = oct_calander[2][0]
		close_date = latest_close_date

		max_available_weeks = (close_date - open_date).days / 7
		# start stripping from head of season
		strip_from = open_date
		while max_available_weeks % n_families != 0:

			print('max_available_weeks:', max_available_weeks, 'for', n_families, 'families.', open_date, ' - ', close_date)

			if strip_from is close_date:
				close_date = close_date - cabin_season.change_segment
				print('stripping tail of schedule. new close:', close_date)
				strip_from = open_date # alternate stripper to front of season
			else:
				open_date = open_date + cabin_season.change_segment
				print('stripping head of schedule. new open:', open_date)
				strip_from = close_date # alternate stripper to tail of season

			max_available_weeks = ((close_date + cabin_season.change_segment) - open_date).days / 7

		return (open_date, close_date)


	def __get_season_block_type(self, week_start_date):

		# opening season is first 3 weeks of season
		if self.opening_week_start_date <= week_start_date <= self.opening_week_start_date + (cabin_season.change_segment * 2):
			return season_block_type.opening
		# closing season is last three weeks of season
		elif self.closing_week_start_date - (cabin_season.change_segment * 2) <= week_start_date <= self.closing_week_start_date:
			return season_block_type.closing
		else:
			curr_date = week_start_date
			delta_day = datetime.timedelta(days=1)
			while curr_date < (week_start_date + cabin_season.change_segment):
				# prime time is any week that has days in july or august
				if curr_date.month == 7 or curr_date.month == 8:
					return season_block_type.prime
				curr_date += delta_day

			# early is not prime and before july
			if week_start_date.month < 7:
				return season_block_type.early
			# late is not prime and after august
			else:
				return season_block_type.late



"""
	def __set_season_block_type(self, start_block_date, end_block_date):

		# opening = 1 	# defined by "contains opening week"
		# prime = 2		# defined by "contains at least 2 weeks in july, starts within the second half of June, or ends before the second half of august"
		# marginal = 3 	# defined by "anything that is not already assigned a type"
		# closing = 4	# defined by "contains closing week"

		if start_block_date <= self.opening_week_start_date <= end_block_date:
			return season_block_type.opening
		elif start_block_date <= self.closing_week_start_date <= end_block_date:
			return season_block_type.closing
		else:
			delta_day = datetime.timedelta(days=1)
			# find prime time
			curr_date = start_block_date
			n_july_days = 0
			while curr_date < end_block_date:
				if curr_date.month == 7:
					n_july_days += 1
				curr_date += delta_day

			# contains at least 2 weeks in july
			if n_july_days >= 14: 
				return season_block_type.prime
			# starts within the second half of June or ends in july
			elif start_block_date.month == 6 and (start_block_date.day > 15 or end_block_date.month == 7): 
				return season_block_type.prime
			# ends before the second half of august or starts in july
			elif end_block_date.month == 8 and (end_block_date.day <= 16 or start_block_date.month == 7): 
				return season_block_type.prime
			else:
				return season_block_type.marginal

"""




