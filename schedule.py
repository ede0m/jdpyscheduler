from designator import *

# main call script

def schedule_year(year):

	print('\n--------------------------------')

	season = cabin_season(year, weeks_per_block, len(families))

	print('\n--------------------------------\n\nseason goes from ', season.opening_week_start_date, ' to ', season.closing_week_start_date, '\n')
	assigned_season = d.assign_season(season)

	for w in assigned_season:
		print("{:<10s}\t | \t{:<10s} | \t{:<10s}".format(w.start_date.strftime("%m-%d-%Y"), w.family_assigned, w.season_block_type.name))

	print('\n')

weeks_per_block = 3
families = ['moede', 'olson', 'warren', 'dave', 'blackmon', 'lucci']
d = designator(families)

print('\nJuniper Dunes Scheduler v 1.0\n--------------------------------')
print('\nweeks per prime season block:', weeks_per_block)
print('number of families participating:', len(families))

year = 2020
while year < 2025:
	schedule_year(year)
	year += 1



