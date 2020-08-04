from cabin_season import *
from operator import itemgetter

class designator:

	season_block_ranks = {
		season_block_type.opening : 1,
		season_block_type.early : 2,
		season_block_type.prime : 3,
		season_block_type.late : 2,
		season_block_type.closing : 1
	}

	def __init__(self, families):

		self.family_pick_orders = self.__create_initial_pick_order(families)
		self.family_weeks_claimed = dict((f, 0.0) for f in families)
		self.family_points = dict((f, 0.0) for f in families)


	def assign_season(self, cabin_season):
		
		# clear family claimed weeks
		self.family_weeks_claimed = dict((f, 0) for f in self.family_weeks_claimed.keys())
		self.max_family_weeks_per_year = cabin_season.n_weeks / len(self.family_weeks_claimed.keys())

		season = []
		for b in cabin_season.season_blocks:
			block_type = b.season_block_type
			weeks_per_fam_in_block = len(b.weeks) / len(self.family_weeks_claimed.keys())

			# everyone can fit and more
			if weeks_per_fam_in_block > 1:
				# assign some back to back weeks
				n_fams_to_double = len(b.weeks) % len(self.family_weeks_claimed.keys())

				# assign weeks later in the block first if 'early' in season
				if block_type is season_block_type.early:
					b.weeks = b.weeks[::-1]

				for idx, w in enumerate(b.weeks):
					fam_pick_idx = self.family_pick_orders[block_type]['current_index']
					self.__assign_family_to_week(w, fam_pick_idx)
					if (idx % 2 is 0 and fam_pick_idx < n_fams_to_double):
						# hold the pick at this family
						self.family_pick_orders[block_type]['current_index'] = fam_pick_idx
						
			# family gets less than or exactly 1 week. rotate across calander years
			else:
				for w in b.weeks:
					self.__assign_family_to_week(w, self.family_pick_orders[block_type]['current_index'])

			season.extend(b.weeks)

		return sorted(season, key=lambda x: x.start_date)

		

	def __create_initial_pick_order(self, families):
		families = sorted(families)
		family_pick_orders = {}
		for b in season_block_type:
			family_pick_orders[b] = {
				"current_index" : 0,
				"order" : list(self.__rotate_pick_order(families))
			}
		return family_pick_orders

	def __rotate_pick_order(self, order):
		rotated = order
		rotated.append(rotated.pop(0))
		return rotated


	def __assign_family_to_week(self, cabin_week, fam_pick_idx):
		block_type = cabin_week.season_block_type
		
		# get a family that still needs weeks for this year
		family = self.family_pick_orders[block_type]['order'][fam_pick_idx]
		while self.family_weeks_claimed[family] >= self.max_family_weeks_per_year:
			fam_pick_idx += 1
			# rotate after everyone goes
			if fam_pick_idx >= len(self.family_pick_orders[block_type]['order']):
				self.family_pick_orders[block_type]['order'] = self.__rotate_pick_order(self.family_pick_orders[block_type]['order'])
				fam_pick_idx = 0
			family = self.family_pick_orders[block_type]['order'][fam_pick_idx]

		cabin_week.assign_family(family)
		self.family_points[family] += round(cabin_week.point_value, 2)
		self.family_weeks_claimed[family] += 1
		self.family_pick_orders[block_type]['current_index'] = fam_pick_idx + 1

		# rotate after everyone goes
		if self.family_pick_orders[block_type]['current_index'] >= len(self.family_pick_orders[block_type]['order']):
			self.family_pick_orders[block_type]['order'] = self.__rotate_pick_order(self.family_pick_orders[block_type]['order'])
			self.family_pick_orders[block_type]['current_index'] = 0



