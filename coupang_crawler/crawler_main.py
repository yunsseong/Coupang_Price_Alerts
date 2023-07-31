from bs4 import BeautifulSoup
from urllib.parse import quote
import requests

search_query = "Apple 2022 맥북에어"
encoded_query = quote(search_query)

base_url = "https://www.coupang.com/np/search?q="
full_url = base_url + encoded_query
print(full_url)

# Coupang에서 "Apple 2022 맥북에어" 검색
# https://www.coupang.com/np/search?q=Apple%202022%20%EB%A7%A5%EB%B6%81%20%EC%97%90%EC%96%B4&channel=recent
# URL 인코딩 함수를 만들어야함
#
# response = requests.get("https://www.coupang.com/")
#
# print(response.text)

