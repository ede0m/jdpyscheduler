from cabin_season import *
from operator import itemgetter

class designator:

	season_block_ranks = {
		season_block_type.opening : 1,
		season_block_type.closing : 1,
		season_block_type.marginal : 2,
		season_block_type.prime : 3
	}

	def __init__(self, families):
		# points tracked across years to see who has the priority "pick"
		self.familiy_points = dict((f, 0) for f in families)

	def assign_season(self, cabin_season):
		
		prime_weeks = []
		other_weeks = []
		# flatten and sort weeks
		for b in cabin_season.season_blocks:
			point_val = designator.season_block_ranks[b.season_block_type]
			for w in b.weeks:
				if w.season_block_type == season_block_type.prime:
					prime_weeks.append(w)
				else:
					other_weeks.append((w, point_val))

		prime_weeks = self.__assign_prime_weeks(prime_weeks)
		other_weeks = self.__assign_other_weeks(other_weeks)
		joined = prime_weeks + other_weeks
		return sorted(joined, key=lambda cabin_week: cabin_week.start_date)


	def __assign_other_weeks(self, other_weeks):
		# sort by rank desc "greedy", sorted by date asc within rank value
		other_weeks = sorted(other_weeks,key=itemgetter(1), reverse=True) 
		other_weeks = [w[0] for w in other_weeks]
		for w in other_weeks:
			min_fam = min(self.familiy_points, key=self.familiy_points.get)
			self.__assign_family_to_week(w, min_fam)
		return other_weeks


	def __assign_prime_weeks(self, prime_weeks):

		assigned_prime_weeks = []
		# all families should get at least one prime week every year. Assign back to back in prime when we can
		n_back_to_back = (len(prime_weeks) - (len(prime_weeks) % len(self.familiy_points.keys())))/2
		back_to_back_assigned = 0
		prime_assigned = 0

		while prime_assigned < len(prime_weeks):
			min_fam = min(self.familiy_points, key=self.familiy_points.get)
			self.__assign_family_to_week(prime_weeks[prime_assigned], min_fam)
			assigned_prime_weeks.append(prime_weeks[prime_assigned])
			prime_assigned += 1
			if back_to_back_assigned < n_back_to_back:
				self.__assign_family_to_week(prime_weeks[prime_assigned], min_fam)
				assigned_prime_weeks.append(prime_weeks[prime_assigned])
				prime_assigned += 1
				back_to_back_assigned += 1

		return assigned_prime_weeks


	def __assign_family_to_week(self, cabin_week, family):
		cabin_week.assign_family(family)
		self.familiy_points[family] += designator.season_block_ranks[cabin_week.season_block_type]

