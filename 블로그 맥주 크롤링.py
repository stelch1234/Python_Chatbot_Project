import requests
import os
import pandas
import time

site = 'https://openapi.naver.com/v1/search/blog.json'
#header 정보
client_id= 'u0mNqMsAQlQ_zizpeVT3'
client_secret = 'R1NPsYx2Yv'
#파라미터
query = '맥주','리뷰'
display = 100
start = 1
sort = 'sim'

# 서버로 전달할 파라미터 데이터
header = {
    'X-Naver-Client-Id' : client_id,
    'X-Naver-Client-Secret' : client_secret
}

param = {
    'query' : query,
    'display' : display,
    'start' : start,
    'sort' : sort
}

# 요청한다.

while True :
    time.sleep(1)
    response = requests.get(site, headers=header, params=param)
    root = response.json()
    # 데이터가 들어있는 태그들 객체를 가져온다.

    for item in root['items'] :
        title = item['title']
        link = item['link']
        description = item['description']
        postdate = item['postdate']

        df = pandas.DataFrame([[title, link, description, postdate]])

        #print(title, link, description, cafename, cafeurl)
        if os.path.exists('blog_review.csv') == False :
            df.columns = ['title', 'link', 'description', 'postdate']
            df.to_csv('blog_review.csv', index = False, encoding = 'utf-8-sig')
        else :
            df.to_csv('blog_review.csv', index = False, encoding = 'utf-8-sig', mode = 'a', header = False)

    #최대 글 개수를 가져온다.
    total_tag = root['total']
    total = int(total_tag)
    print('start :', start)

    if start < 1000 and start < total :
        start += display
        if start > 1000 :
            start = 1000

        param['start'] = start
    else :
        break