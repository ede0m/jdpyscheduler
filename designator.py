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
		self.family_weeks_claimed = dict((f, 0) for f in families)


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
				n_fams_to_double = len(b.weeks) % len(self.family_weeks_claimed.keys())
				fam_idx = 0
				for idx, w in enumerate(b.weeks):
					self.__assign_family_to_week(w, self.family_pick_orders[block_type]['order'][fam_idx])
					if idx % 2 is 1 and fam_idx < n_fams_to_double:
						# back to back week for this fam_idx
						fam_idx += 1
					elif fam_idx >= n_fams_to_double:
						fam_idx += 1
				self.family_pick_orders[block_type]['order'] = self.__rotate_pick_order(self.family_pick_orders[block_type]['order'])
						
			# have to cycle across seasons
			elif weeks_per_fam_in_block < 1:
				fam_idx = self.family_pick_orders[block_type]['current_index']
				for w in b.weeks:
					self.__assign_family_to_week(w, self.family_pick_orders[block_type]['order'][fam_idx])
					fam_idx += 1
					self.family_pick_orders[block_type]['current_index'] = fam_idx

					if fam_idx >= len(self.family_pick_orders[block_type]['order']):
						self.__rotate_pick_order(self.family_pick_orders[block_type]['order'])
						self.family_pick_orders[block_type]['current_index'] = 0

			# each fam gets 1 week
			else:
				for idx, w in enumerate(b.weeks):
					self.__assign_family_to_week(w, self.family_pick_orders[block_type]['order'][idx])
				# rotate after everyone goes
				self.family_pick_orders[block_type]['order'] = self.__rotate_pick_order(self.family_pick_orders[block_type]['order'])

			season.extend(b.weeks)

		return season

		

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


	def __assign_family_to_week(self, cabin_week, family):
		# can't assign if you pass the max family weeks per year
#		if self.family_weeks_claimed[family] < self.max_family_weeks_per_year and cabin_week.family_assigned is None:
		cabin_week.assign_family(family)
		self.family_weeks_claimed[family] += 1
			#return True
		#return False



