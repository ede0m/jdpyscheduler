from designator import *

# main call script

def schedule_year(year):

	print('\n--------------------------------')

	season = cabin_season(year, len(families))
	
	"""
	for b in season.season_blocks:
		for w in b.weeks:
			print(w.start_date, w.season_block_type)
	"""


	print('\n--------------------------------\n\nseason goes from ', season.opening_week_start_date, ' to ', season.closing_week_start_date, 
		' | ', (season.closing_week_start_date + cabin_season.change_segment - season.opening_week_start_date).days / 7, 'weeks\n')
	
	assigned_season = d.assign_season(season)
	for w in assigned_season:
		print("{:<10s}\t | \t{:<10s} | \t{:<10s}".format(w.start_date.strftime("%m-%d-%Y"), w.family_assigned, w.season_block_type.name))


	print('\n')



families = ['moede', 'olson', 'warren', 'dave', 'blackmon', 'lucci']
d = designator(families)

print('\nJuniper Dunes Scheduler v 1.0\n--------------------------------')
print('number of families participating:', len(families))

year = 2020
while year < 2032:
	schedule_year(year)
	year += 1



