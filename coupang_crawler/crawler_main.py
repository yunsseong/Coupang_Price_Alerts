from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import schedule
import time



# 실제 유저가 접속하는 것처럼 보이게 하기 위해 options 사용
options = Options()
options.add_argument("authority="+"www.coupang.com")
# options.add_argument('headless')
options.add_argument("method=" + "GET")
options.add_argument("accept=" + "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
options.add_argument("accept-encoding=" + "gzip, deflate, br")
options.add_argument("user-agent=" + "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.104 Whale/3.13.131.36 Safari/537.36")
options.add_argument("sec-ch-ua-platform=" + "macOS")
options.add_argument("cookie=" + "PCID=31489593180081104183684; _fbp=fb.1.1644931520418.1544640325; gd1=Y; X-CP-PT-locale=ko_KR; MARKETID=31489593180081104183684; sid=03ae1c0ed61946c19e760cf1a3d9317d808aca8b; x-coupang-origin-region=KOREA; x-coupang-target-market=KR; x-coupang-accept-language=ko_KR;")

# selenium 파싱 결과 객체를 받아 첫 번째 요소가 광고 상품이면 두 번째 요소를 반환하고
# 첫 번째 요소가 일반 상품이면 첫 번째 요소를 반혼하는 함수
def ad_checker(products):
    try:
        ad_check = products[0].find_element(By.CLASS_NAME, "ad-badge ad-position-D")
        return products[0]
    except:
        return products[1]

# 제품 이름을 매개변수로 받아 해당 상품의 URL을 String으로 반환하는 함수
def get_product_url(product_name):
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.coupang.com/np/search?q={product_name}")
    product_link_list = driver.find_elements(By.CLASS_NAME, "search-product-link")
    product = ad_checker(product_link_list)
    product_link = product.get_attribute("href")
    return product_link

# 제품의 이름 리스트를 매개변수로 받아 제품의 url 리스트를 반환하는 함수
def get_product_url_list(product_name_list):
    product_url_list = []
    for product_name in product_name_list:
        product_url_list.append(get_product_url(product_name))
    return product_url_list

# 제품의 이름 url 리스트를 매개변수로 받아 제품의 가격 정보 리스트를 반환하는 함수
def get_product_info_list(product_url_list):
    product_info_list = []
    for product_url in product_url_list:
        product_info_list.append([get_product_info_through_url(product_url)])
    return product_info_list

# driver와 파싱을 원하는 요소의 class_name을 매개변수로 받음
# class_name으로 요소를 찾는데 없는 경우에 에러를 일으키므로 try-except문 사용
# 해당 요소가 있을 경우 요소의 텍스트를 반환하고 없으면 None을 반환함
def get_element_text(driver, class_name):
    try:
        element_text = driver.find_element(By.CLASS_NAME, class_name).text
        return element_text
    except:
        return None

# driver를 매개변수로 받아 제품 가격 정보와 조회 시간을 딕셔너리로 반환하는 함수
def get_product_price(driver):
    request_time = datetime.now()
    product_real_name = driver.find_element(By.CLASS_NAME, "prod-buy-header__title").text
    product_price_div = driver.find_element(By.CLASS_NAME, "prod-price")
    origin_price = get_element_text(product_price_div, "origin-price")
    discount_rate = get_element_text(product_price_div, "discount-rate")
    total_price = get_element_text(product_price_div, "total-price")

    product_price = {"product_name": product_real_name, "request_time": request_time, "origin_price": origin_price,
                     "discount_rate": discount_rate, "total_price": total_price}
    print(product_price)
    return product_price

# 제품의 이름을 매개변수로 받으면 제품의 가격 정보와 조회 정보를 딕셔너리로 반환하는 함수
def get_product_info(product_name):
    url = get_product_url(product_name)
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return get_product_price(driver)

# 제품의 url을 매개변수로 받으면 제품의 가격 정보와 조회 정보를 딕셔너리로 반환하는 함수
def get_product_info_through_url(product_url):
    driver = webdriver.Chrome(options=options)
    driver.get(product_url)
    return get_product_price(driver)
