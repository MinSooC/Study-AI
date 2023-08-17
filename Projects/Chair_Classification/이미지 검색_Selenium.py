from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import os
import urllib.request
import time

chrome_options = webdriver.ChromeOptions()  # ChromeOptions 객체 생성
chrome_options.add_experimental_option('detach', True)  # 실행이 멈춰도 웹브라우저가 꺼지지 않게끔 함
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

keyword = input('키워드를 입력해주세요: ')
numbers = input('몇개의 이미지를 검색하시겠습니까? ')

driver.get("https://www.google.com/search?sxsrf=APwXEdeH9tMABgS5Z5hjjTJN-cgqOyK7gQ:1687850258687&q=" +
           keyword + "&tbm=isch&sa=X&ved=2ahUKEwjF5uiY9OL_AhVvg1YBHV6dCCUQ0pQJegQIDBAB&biw=1536&bih=714&dpr=1.25")

driver.maximize_window()

soup = BeautifulSoup(driver.page_source, features="html.parser")

subfolder_name = keyword
subfolder_path = os.path.join(os.getcwd(), subfolder_name)

if not os.path.exists(subfolder_path):
    os.makedirs(subfolder_path)

for n in range(int(numbers)):
    try:
        time.sleep(1)

        if n < 49:
            try:
                driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[' + str(n + 1) + ']/a[1]/div[1]/img').click()
            except:
                continue

        elif n < 105:
            try:
                driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[50]/div[' + str(n - 48) + ']/a[1]/div[1]/img').click()
            except:
                continue

        elif n < 209:
            try:
                driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[51]/div[' + str(n - 104) + ']/a[1]/div[1]/img').click()
            except:
                continue

        elif n < 313:
            try:
                driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[52]/div[' + str(n - 208) + ']/a[1]/div[1]/img').click()
            except:
                continue

        elif n < 417:
            try:
                driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[53]/div[' + str(n - 312) + ']/a[1]/div[1]/img').click()
            except:
                continue

        else:
            try:
                driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[54]/div[' + str(n - 416) + ']/a[1]/div[1]/img').click()
            except:
                continue

        if n < 50:
            continue

        try:
            element = driver.find_element(By.CSS_SELECTOR, 'img.r48jcc.pT0Scc.iPVvYb')
        except:
            element = driver.find_element(By.CSS_SELECTOR, 'img.r48jcc.pT0Scc')

        src = element.get_attribute('src')
        filename = keyword + '_' + str(n + 1) + '.jpg'
        filepath = os.path.join(os.getcwd() + '/' + subfolder_name, filename)
        urllib.request.urlretrieve(src, filepath)

        if n % 10 == 0 and n // 10 > 0:
            print(n, '회 진행 완료')

    except:
        pass
