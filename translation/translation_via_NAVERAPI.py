# -*- coding: utf-8 -*-
import os
import sys
import urllib.request

#네이버 파파고는 2가지 종류의 번역이 있습니다
#NMT:인공신경망(문장 전체를 바탕으로 번역 수행,SMT 번역보다 더욱 정확)
#SMT:통계기반(속도 빠름, 신조어 번역에 장점)
def papago_translate_text(text):
    client_id = 'gsqIEpceMVBCQy_VZBzq'
    client_secret = 'DH99oGELVB'
    encText = urllib.parse.quote(text)
    #한국어를 영어로 바꿔
    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)
    return response_body.decode("utf-8")
