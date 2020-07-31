
"""

represents a week a juniper dunes.
traditionally, start dates should always be sundays. 

"""


class cabin_week:

	def __init__(self, start_date, season_block_type):
		self.start_date = start_date
		self.season_block_type = season_block_type
		self.family_assigned = None

	def assign_family(self, family_name):
		self.family_assigned = family_name