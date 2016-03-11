from bs4 import BeautifulSoup
import urllib.request
import re
import datetime
import csv

def get_scripts():
	pretty = []
	url = 'http://www.vim.org/scripts/script_search_results.php?&show_me=6000&result_ptr=0'
	req = urllib.request.Request(url)
	req.add_header('User-Agent', 'prive crawler (Python3, urllib), harm@mindshards.com')

	with urllib.request.urlopen(req) as response:
		html = response.read()
		soup = BeautifulSoup(html,'html.parser')
		scripts = soup.find('h1', string='Search Results').next_sibling.next_sibling.find_all('tr')[2:]

		for script in scripts:
			url = script.find('td').find('a')['href']
			name = script.find('td').find('a').string
			kind = script.find_all('td')[1].string
			rating = int(script.find_all('td')[2].string)
			downloads = int(script.find_all('td')[3].string)
			pretty.append({'url': url, 'name': name, 'kind': kind, 'rating': rating, 'downloads': downloads})

	return pretty

def write_to_disk(scripts):
	filename = datetime.datetime.now().strftime("%Y-%m-%d") + ".csv"
	with open(filename, 'w', newline='') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=['url', 'name', 'kind', 'rating', 'downloads'])
		writer.writeheader()
		for script in scripts:
			writer.writerow(script)


write_to_disk(get_scripts())
