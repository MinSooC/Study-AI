import time

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

keyword = input('키워드를 입력해주세요: ')
number = int(input('가져올 페이지의 개수를 숫자로 입력해주세요: '))

# 네이버 뉴스 검색 페이지 호출 : 기본 세팅 (날짜 20200515~20230616 / 신문사 스포츠조선)
driver.get(
    "https://search.naver.com/search.naver?where=news&query=" + keyword + "&sm=tab_opt&sort=1&photo=0&field=0&pd=3&ds=2020.05.15&de=2023.06.16&docid=&related=0&mynews=1&office_type=1&office_section_code=5&news_office_checked=1076&nso=so%3Add%2Cp%3Afrom20200515to20230616&is_sug_officeid=0")

driver.maximize_window()

soup = BeautifulSoup(driver.page_source, features="html.parser")

titles_list = []
dates_list = []
texts_list = []


# 현재 열려 있는 페이지의 기사의 제목, 날짜, 본문 내용을 구하는 함수
def get_article_info():
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    # 본문 제목 저장
    titles = soup.select("h2.end_tit")
    for tag in titles:
        title = tag.text
        title = title.strip()
        titles_list.append(title)

    # 본문 날짜 저장
    dates = soup.select("div.article_info")
    for tag in dates:
        tag.find("a").decompose()
        date = tag.text
        date = date.strip()
        date = date[4:24]
        dates_list.append(date)

    # 본문 내용 저장
    for tag in soup.select("div.end_body_wrp"):
        tag.find("span").decompose()
        text = tag.text
        try:
            text = text.split("기자")[1].strip()[1:].strip()
        except:
            pass
        texts_list.append(text)


# 언론사 홈페이지 말고 네이버 뉴스에 업로드 된 기사를 새 탭으로 가져오는 변수와 함수
ems = driver.find_elements(By.CSS_SELECTOR, 'a.info')


def get_articles(ems):
    if len(ems) != 0:
        for em in ems:
            if em.text == '네이버뉴스':
                # '네이버뉴스' 탭을 클릭하기
                time.sleep(1)
                em.click()
                first_tab = driver.window_handles[0]
                last_tab = driver.window_handles[-1]

                # 가장 나중에 열린 탭으로 이동하고 기사의 제목, 날짜, 본문을 구할 수 있는 함수를 작동
                driver.switch_to.window(window_name=last_tab)
                get_article_info()

                # 탭이 하나 남을때까지 닫기
                if len(driver.window_handles) != 1:
                    driver.close()

                # 다음 페이지를 열기 위해 첫번째 탭으로 돌아가기
                driver.switch_to.window(window_name=first_tab)


# 네이버 뉴스에 업로드 된 기사들을 크롤링하고 만약 전부 크롤링했다면 다음 페이지로 넘어가기
for n in range(1, number + 1):
    time.sleep(2)
    try:
        driver.find_element(By.LINK_TEXT, str(n + 1)).click()
        ems = driver.find_elements(By.CSS_SELECTOR, 'a.info')
        get_articles(ems)
    except:
        break

# 크롤링한 데이터를 데이터프레임으로 저장하기
data = {'titles': titles_list, 'dates': dates_list, 'description': texts_list}
df = pd.DataFrame(data)
df.to_csv("naver_goldenkids_search.csv", encoding="utf-8-sig")

driver.close()