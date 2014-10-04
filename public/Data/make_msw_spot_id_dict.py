import requests
from bs4 import BeautifulSoup
import re

def make_dict():
	big_dict = {}
	r = requests.get('http://magicseaweed.com/site-map.php')
	data = r.text
	soup = BeautifulSoup(data)
	pattern = re.compile('.*/.*-Surf-Report/([0-9]{1,4})/')
	for el in soup.find_all(href=pattern):
		try:
			big_dict[str(el.get_text())] = int(pattern.match(el.get('href')).group(1))
		except:
			pass
	return big_dict

def create_dict_file():
	fo = open('msw_spot_id_dict.txt', 'wb')
	data_dict = make_dict()
	fo.write(str(data_dict))
	fo.close()