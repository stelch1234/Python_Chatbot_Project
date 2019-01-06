from googletrans import Translator
import pandas as pd
import numpy as np
import re
import langdetect
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from google.cloud import translate

# 데이터 불러오기
beer_Pilsen = pd.read_csv('/Users/stella/Downloads/beer_필스너.csv', encoding='utf-8')

beer_Pilsen1 = beer_Pilsen[:200]

# 영어만 추출하기
text_languages = []
for text in beer_Pilsen1['reviews'].dropna():
    try:
        if detect(text) == 'en':
            text_languages.append({
                'reviews': text
            })
    except LangDetectException:
        pass

df_Pilsen = pd.DataFrame(text_languages)

# 텍스트 파일로 바꾸기
df_Pilsen.to_csv(r'/Users/stella/Downloads/beer_필스너.text', encoding='utf-8')

Pilsen_file = open('/Users/stella/Downloads/beer_필스너.text', 'r', encoding='utf-8')
Pilsentext = Pilsen_file.read()
Pilsen_file.close()
print(Pilsentext)

#특수문자 제거
Pilsentext1 = re.sub(r'[*.\-\"\,\n@!\'\"=…:?/;]', '', Pilsentext)
print(Pilsentext1)

#구글 번역
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/stella/Downloads/My First Project-d86323cb9c64.json"

def translate_text(text, target='ko'):
    translate_client = translate.Client()
    result = translate_client.translate(
        text, target_language=target)

    # print(u'Text: {}'.format(result['input']))
    print(u'Translation: {}'.format(result['translatedText']))
    # print(u'Detected source language: {}'.format(
    # result['detectedSourceLanguage']))

    translate_client = translate.Client()


example_text = Pilsentext1
translate_text(example_text, target='ko')