#구글 번역
import os
from google.cloud import translate

#google cloud을 가입해서 json파일 타입의 api키 값을 저장한다.
#  api 불러오기
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/~your path"

#구글 언어 자동감지가 됨
#target= 'ko'
def translate_text(text, target='ko'):
    translate_client = translate.Client()
    result = translate_client.translate(
        text, target_language=target)

    # print(u'Text: {}'.format(result['input']))
    print(u'Translation: {}'.format(result['translatedText']))
    # print(u'Detected source language: {}'.format(
    # result['detectedSourceLanguage']))

    translate_client = translate.Client()