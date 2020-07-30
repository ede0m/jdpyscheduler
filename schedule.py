from cabin_season import *

# main call script

year = 2020
weeks_per_block = 3
families = ['moede', 'olson', 'warren', 'dave', 'blackmon', 'lucci']

print('\nJuniper Dunes Scheduler v 1.0\n--------------------------------')
print('\n'+str(year) + ' weeks per prime season block:', weeks_per_block)
print(str(year) + ' number of families participating:', len(families))
print('\n--------------------------------')

cabin_season = cabin_season(year, weeks_per_block, len(families))
n_prime_blocks = sum(1 for b in cabin_season.season_blocks if b.block_type == season_block_type.prime)

print('\nseason goes from ', cabin_season.opening_week_start_date, ' to ', cabin_season.closing_week_start_date)
print('\n'+str(year) + ' number of prime season weeks:', n_prime_blocks * weeks_per_block)
print(str((n_prime_blocks * weeks_per_block) / len(families))+ ' prime weeks per family\n')

for b in cabin_season.season_blocks:
	print(b.start_date, b.end_date, b.block_type)

print('\n')

