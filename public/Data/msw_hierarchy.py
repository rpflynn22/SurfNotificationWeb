from bs4 import BeautifulSoup
import re
import requests
import ast

def make_data():
	data = requests.get("http://magicseaweed.com/site-map.php/").text
	soup = BeautifulSoup(data)
	wide_cats = soup('optgroup')
	wide_cats = wide_cats[0:12]
	wide_cats_str_lst = []
	for el in wide_cats:
		if el.has_attr('label'):
			wide_cats_str_lst.append(el['label'])
	subcats = {}
	for el in wide_cats: #el is like North America
		inner_soup = BeautifulSoup(str(el))
		inner_dict = {}
		inner_lst = inner_soup.find_all('option')
		sort_me_dict = {}
		for el0 in inner_lst: #el0 is like Southern Cali
			inner_dict1 = {}
			temp_req = requests.get('http://magicseaweed.com' + str(el0['value']))
			temp_data = temp_req.text
			temp_soup = BeautifulSoup(temp_data)
			inner_cats = temp_soup('optgroup')
			inner_cats = inner_cats[25:]
			for el1 in inner_cats: #el1 is like Orange County
				final_soup = BeautifulSoup(str(el1))
				final_lst = []
				for it in final_soup('option'): #it is like Huntington pier
					try:
						final_lst.append(str(it.get_text()))
					except UnicodeEncodeError as e1:
						pass
				if not el1['label'] in wide_cats_str_lst:
					try:
						inner_dict1[str(el1['label'])] = str(final_lst)
					except UnicodeEncodeError as e2:
						pass
			try:				
				inner_dict[str(el0.get_text())] = inner_dict1
			except UnicodeEncodeError as e3:
				pass
		try:
			subcats[str(el['label'])] = inner_dict
		except UnicodeEncodeError as e4:
			pass
			#print('key: ' + el['label'])
			#raise e4
	return subcats

def write_format():
	fo = open('msw_data.html', 'r+')
	info = open('msw_dict.txt', 'r')
	data_dict = eval(info.read())
	info.close()
	start_adding = False
	beginning = []
	rest = []
	lines = fo.readlines()
	for li in lines:
		if li.strip().lower() == '<!-- insert here -->':
			start_adding = True
		elif start_adding:
			rest += [li,]
		elif not start_adding:
			beginning += [li,]
	fo.close()
	fo = open('msw_data.html', 'wb')
	for li in beginning:
		fo.write(li)
	fo.write('<select id="BigSelect">\n')
	secondary_lines = []
	fo.write('\t<option value="null">Select Region</option>\n')
	for big_region in data_dict.keys():
		fo.write('\t<optgroup label="' + str(big_region) + '">\n')
		temp_lst = data_dict[big_region].keys()
		temp_lst = sorted(temp_lst, key=str.lower)
		for area_name in temp_lst:
			value = ''
			for char in str(area_name):
				if re.compile('[a-zA-Z0-9]').match(char):
					value += char
				elif re.compile(' ').match(char):
					value += '-'
			secondary_lines.append('<select class="spots" id="' + value + '">\n')
			secondary_lines.append('<option value="null">Select Spot</option>\n')
			for sub_region in data_dict[big_region][area_name].keys():
				secondary_lines.append('\t<optgroup label="' + str(sub_region)\
					+ '">\n')
				for spot in eval(data_dict[big_region][area_name][sub_region]):
					secondary_lines.append('\t\t<option value="' + str(spot) + '">'\
						+ str(spot) + '</option>\n')
				secondary_lines.append('\t</optgroup>\n')
			secondary_lines.append('</select>\n')
			fo.write('\t\t<option value="' + value + '">'\
				+ str(area_name) + '</option>\n')
		fo.write('\t</optgroup>\n')
	fo.write('</select>\n')
	for li in secondary_lines:
		fo.write(li)
	for li in rest:
		fo.write(li)
	fo.close()

def write_dictionary():
	fo = open('msw_dict0.txt', 'wb')
	data_dict = make_data()
	fo.write(str(data_dict))
	fo.close()

def get_data():
	info = open('msw_dict.txt', 'r')
	data_dict = eval(info.read())
	info.close()
	return data_dict
