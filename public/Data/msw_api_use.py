import requests
import datetime
import ast
import re

key = 'bHR9ihtoB8bA57704gzfcQ9h0yr9rXi1'
dni = [0, 1, 7]
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
times = ['12 a.m.', '3 a.m.', '6 a.m.', '9 a.m.', '12 p.m.', '3 p.m.', '6 p.m.', '9 p.m.']
fo = open('msw_spot_id_dict.txt', 'r')
d = ast.literal_eval(fo.read())
fo.close()

def get_best_time(spot_name):
	name_pattn = re.compile('.*'+make_name_pattern(spot_name)+'.*')
	spot_id = -1
	the_spot = spot_name
	try:
		spot_id = d[spot_name]
	except KeyError as e:	
		for spot in d.keys():
			if name_pattn.match(spot):
				spot_name = spot
				spot_id = d[spot]
	if spot_id == -1:
		raise Exception
	print(spot_id)
	r = requests.get('http://magicseaweed.com/api/'+key+'/forecast/?spot_id='+str(spot_id)+'&units=us')
	j = r.json()
	max_rating = -1
	best_time = -1
	for i in range(0,40):
		rating = j[i]['solidRating'] + .5*j[i]['fadedRating']
		if rating > max_rating and i%8 not in dni:
			best_time = i
			max_rating = rating
	conds = {}
	conds['MaxHeight'] = j[best_time]['swell']['absMaxBreakingHeight']
	conds['Period'] = j[best_time]['swell']['components']['combined']['period']
	conds['WindSpeed'] = j[best_time]['wind']['speed']
	conds['WindDirection'] = j[best_time]['wind']['compassDirection']
	print(best_time)
	print('You should paddle out at ' + spot_name + ' on ' + get_date(best_time) + \
		  ' when the rating will be a ' + str(max_rating*2) + \
		  ' and the waves will be ' + \
		  str(j[best_time]['swell']['absMaxBreakingHeight']) + ' feet.')
	return conds

def make_name_pattern(spot_name):
	final = ''
	for char in spot_name.lower():
		final += '['+char+char.upper()+']'
	return final


def get_date(time):
	today_index = datetime.datetime.now().weekday()
	day = days[((time/8)+today_index)%7]
	hour = times[time%8]
	return day + ' at ' + hour
