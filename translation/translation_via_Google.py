import pandas as pd
import numpy as np
import re
import csv
import time
import os
import requests
#언어감지
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
#브라우저 제어
from selenium import webdriver
#페이지 로드
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs


#데이터 불러오기
beer_name= pd.read_csv('~/path', encoding = 'utf-8')

#데이터 내 여러 언어들도 포함되어 있다.
#하지만, 다른 언어를 한글로 바꿨을 경우 어색한 번역투가 존재하기 때문에
#영어만 추출
text_languages = []
for text in beer_name['reviews'].dropna():
    try:
        if detect(text) == 'en' :
            text_languages.append({
        'reviews' : text
    })
    except LangDetectException:
        pass

#영어만 추출한 데이터, 데이터 프레임화
df_beer = pd.DataFrame(text_languages)

#번역하기 위해서 텍스트 파일로 변경
df_beer.to_csv('~/path.txt', encoding='utf-8',  index = False, header = False)
file = open('~/path.txt', 'r', encoding = 'utf-8')
file_open = file.read()
file.close()

#chrome driver 불어오기
driver = webdriver.Chrome('/chromedriver path')

#기본 구글 번역 url 설정
base_url = 'https://translate.google.com/?um=1&ie=UTF-8&hl=ko&client=tw-ob#view=home&op=translate&sl=auto&tl=ko'
driver.get(base_url)

#구글API를 사용하는 것이 아닌 구글 번역기를 통해 직접 데이터를 입력하다.
#하지만 sendkeys로 데이터를 입력하면 시간이 너무 소비되고 글이 중간부터는 잘리기때문에
#변환한 txt파일을 복사 붙여넣기로 직접 입력하는 것이 좋다.
#timw.wait로 잠깐 멈춘 후에 직접 데이터를 넣는다.
time.wait(60)

review_list = []
for i in range(0,900):
    soup = bs(driver.page_source, 'html.parser')
    time.sleep(3)
    #해당 내용만 찾아 선택한다.
    reviews = soup.find("span","tlid-translation translation")
    #reviews를 contents 형식으로 변환해서 각 리스트를 하나씩 가져온다.
    for review in reviews.contents:
        try:
            #</br>이 아닌 경우
            if type(review) != type(reviews.contents[1]):
                #contents내 태그 지우기
                review  = re.sub('<.+?>', '', review, 0).strip()
                review_list.append(review)
        except:pass
    #'5000자 이상은 다음페이지' 버튼 클릭하기
    try:
        driver.find_element_by_css_selector('span#gt-ovfl-xlt').click()
        time.sleep(3)
    except: break

df = pd.DataFrame(review_list)
df.to_csv('translation_data.csv')



