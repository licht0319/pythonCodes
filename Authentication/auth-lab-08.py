# import requests
# import grequests
import sys
# import urllib3
# import urllib
# from bs4 import BeautifulSoup
# import re
# from random import random
# import time

with open('../password_list.txt') as p:
    passwords = p.readlines()

for password in passwords:
    print("\\\"%s\\\"," % (password.strip("\n")))