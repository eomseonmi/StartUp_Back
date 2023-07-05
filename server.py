# -*- coding: utf-8 -*-
import ssl
import time

ssl._create_default_https_context = ssl._create_unverified_context
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import base64
import json
import http.client
import os
import openai

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

openai.organization = "org-bbagKC4X3yawNt0tPYEb8DMD"
openai.api_key = "sk-"
openai.Model.list()

def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=4,
        size="256x256"
    )
   
    image_urls = []
    for item in response['data']:
        if 'url' in item:
            image_url = item['url']
            image_urls.append(image_url)

    combined_url = '##*##*'.join(image_urls)
    print(combined_url)

    return combined_url


@app.route('/getImage', methods=['GET'])
def index():
    text = request.args.get('str')  #str : 전달된 파라미터
    text += '를 영어로 번역하면'

    print(text)
       
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0.3,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response['choices'][0]['text'])

    # 입력된 텍스트를 사용하여 이미지 생성
    image_urls = generate_image(response['choices'][0]['text'])
    print(image_urls)
    return image_urls


class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def _send_request(self, completion_request):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
        }

        conn = http.client.HTTPSConnection(self._host)
        conn.request('POST', '/testapp/v1/completions/LK-D2', json.dumps(completion_request), headers)
        response = conn.getresponse()
        result = json.loads(response.read().decode(encoding='utf-8'))

        conn.close()
        return result

    def execute(self, completion_request):
        res = self._send_request(completion_request)
        if res['status']['code'] == '20000':
            print(res['result']['outputTokens'])
            return res['result']['outputTokens']
        else:
            return 'Error'

@app.route('/getText', methods=['GET'])
def invoke_completion():
    host = 'clovastudio.apigw.ntruss.com'
 
    api_key='NTA0MjU2MWZlZTcxNDJiY4cqwRLuqRsQk6zjZ/E82EdA80+zPLK+0CduBjGUCd4E+ingzn3Qlf62n+vLFnO2s5bZ1BW++vMqmLVtd8clDHYZqJCOP6+A3342eaZCn904QxzjX+A5mKKgUkv1fxFlxSKBXJk/Q2pEuLxrDyq0PfbQ9m7UWzVJy1U544OyoHcQBMFzSr9VaOypo87liCVlc2j65ysB6yam2dy2B1Ql5+w='
    api_key_primary_val = 'NtCsDeWuLXowvJfzvqe16WRFf3mlfNZFKoN5I72Y'
    request_id='e1ce242e6fdb4c50ba83d09598a24e41'


    completion_executor = CompletionExecutor(host, api_key, api_key_primary_val, request_id)

    str_param = request.args.get('str')     #str : 전달된 파라미터

    preset_text = '사용자가 입력한 상황에 맞는 메세지카드를 작성해주세요.\n고급스러운 분위기로 부드러운 표현을 사용해주세요.\n\n###\n상황: 선생님께 스승의날 선물\n문구: 인생의 등불이 되어주신 선생님! 스승의 은혜에 보답하는 마음으로 인사를 드립니다. 감사합니다, 사랑합니다.\n###\n상황: 부모님께 새해 선물\n문구: 항상 베풀어주시는 사랑에 감사드리며 새해에도 건강하시고 행복하세요. 단 하나뿐인 나의 부모님, 사랑합니다.\n###\n상황: 팀원에게 크리스마스 선물\n문구: 메리크리스마스! 산타의 푸근한 미소처럼 사랑과 따뜻함을 느껴보는 성탄절 보내세요. \n###\n상황: 사장님께 추석 선물\n문구: 항상 가정에 화목과 행복이 충만하고 뜻하시는 모든 일에 발전과 번영이 있기를 기원합니다. 풍요로운 한가위 보내세요.\n###\n상황: 할머니께 생일 선물\n문구: 사랑하는 할머니의 생신을 진심으로 축하드립니다. 항상 건강하고 행복하세요. 사랑합니다.\n###\n상황: '    
    preset_text += str_param

    print(str_param)
    print(preset_text)
    print('***********')

    request_data = {
        'text': preset_text,
        'maxTokens': 165,
        'temperature': 0.75,
        'topK': 0,
        'topP': 0.8,
        'repeatPenalty': 7.0,
        'start': '\n문구:',
        'restart': '\n###\n상황:',
        'stopBefore': ['###\n', '상황:', '문구:', '###'],
        'includeTokens': True,
        'includeAiFilters': True,
        'includeProbs': False
        
    }
    resultword = ""

    for _ in range(4):
        response_text = completion_executor.execute(request_data)
        print(response_text)
    
        for word in response_text :
        
            if word == '###' :
                break
            else :
                resultword = resultword + word
        print('***************')
        print('******resultword*********')
        print(resultword)

        resultword = resultword.replace('#','')
        resultword = resultword + "^"

        time.sleep(0.5)  
    return resultword

if __name__ == '__main__':
    app.run()
