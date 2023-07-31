from bs4 import BeautifulSoup
import requests

response = requests.get("https://www.coupang.com/")

print(response.text)