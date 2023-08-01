from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qs



# 실제 유저가 접속하는 것처럼 보이게 하기 위해 options 사용
options = Options()
options.add_argument("authority="+"www.coupang.com")
options.add_argument("method=" + "GET")
options.add_argument("accept=" + "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
options.add_argument("accept-encoding=" + "gzip, deflate, br")
options.add_argument("user-agent=" + "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.104 Whale/3.13.131.36 Safari/537.36")
options.add_argument("sec-ch-ua-platform=" + "macOS")
options.add_argument("cookie=" + "PCID=31489593180081104183684; _fbp=fb.1.1644931520418.1544640325; gd1=Y; X-CP-PT-locale=ko_KR; MARKETID=31489593180081104183684; sid=03ae1c0ed61946c19e760cf1a3d9317d808aca8b; x-coupang-origin-region=KOREA; x-coupang-target-market=KR; x-coupang-accept-language=ko_KR;")

# 제품 이름을 입력하면 가장 첫번째로 뜨는 상품의 제목과 가격, 링크를 반환하는 함수
def find_product_by_name(search_query):
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.coupang.com/np/search?q={search_query}")
    product_name = driver.find_element(By.CLASS_NAME, "name")
    product_price = driver.find_element(By.CLASS_NAME, "price")
    product_link = driver.find_element(By.CLASS_NAME, "search-product-link")

    return [product_name.text, product_price.text, product_link.text]

# 제품 이름을 입력하면 가장 첫번쨰로 뜨는 상품의 itemId를 반환하는 함수
def get_item_id(search_query):
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.coupang.com/np/search?q={search_query}")
    product_link = driver.find_element(By.CLASS_NAME, "search-product-link").get_property("href")
    item_id = parse_qs(urlparse(product_link).query)['itemId'][0]
    return item_id

print(get_item_id("맥북에어"))





