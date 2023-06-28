# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, render_template
import base64
import json
import http.client
import os
import openai

app = Flask(__name__)
openai.organization = "org-bbagKC4X3yawNt0tPYEb8DMD"
openai.api_key = "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"
openai.Model.list()

def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=2,
        size="256x256"
    )
   
    image_urls = []
    for item in response['data']:
        if 'url' in item:
            image_url = item['url']
            image_urls.append(image_url)

    combined_url = ''.join(image_urls)
    print(combined_url)

    return combined_url


@app.route('/getImage', methods=['GET'])
def index():
    text = request.args.get('str')  #str : 전달된 파라미터
    
    # 입력된 텍스트를 사용하여 이미지 생성
    image_urls = generate_image(text)
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
            return res['result']['text']
        else:
            return 'Error'

@app.route('/getText', methods=['GET'])
def invoke_completion():
    host = 'clovastudio.apigw.ntruss.com'
  
    api_key='NTA0MjU2MWZlZTcxNDJiY2Vuw9hOjyf1wgG7wXI2WbIvJDJsk7lfXX7e15ByQr+4PTAy7K8RBPh7GN379TRUEcLc+MZ9n+yMoV4xkZ1nHdaiwfZU+Yzb5s6K5HanO/5n+kBFNpSLa3AWI4fmvzj7y0WlZ2v4CLbBKqDwkdv4wKw4MK2+aMG6YFUy/39evqYQvDRTD9+ZEIOJbt1v7wfTfpFSjk+wBR41o1cxSJx0qqM='
    api_key_primary_val = 'NtCsDeWuLXowvJfzvqe16WRFf3mlfNZFKoN5I72Y'
    request_id='ec3db1ce8825484c876fb7a3483dbb02'


    completion_executor = CompletionExecutor(host, api_key, api_key_primary_val, request_id)

    str_param = request.args.get('str')     #str : 전달된 파라미터
    preset_text = '사용자가 입력한 상황에 맞는 메세지카드를 작성해주세요.\n\n###\n상황: 부모님께 새해 인사\n문구: 사랑하는 나의 부모님, 새해에는 더욱 웃음 가득한 한 해 되세요. 감사합니다, 사랑합니다.\n###\n상황: 선생님께 스승의날 감사\n문구: 사랑으로 이끌어 주신 선생님의 가르침에 깊이 감사드립니다. 스승의 은혜, 잊지 않겠습니다. 사랑합니다.\n###\n상황: 선생님께 스승의날 감사\n문구: 하늘같은 가르침에 작은 마음을 전합니다. 감사합니다, 사랑합니다, 나의 선생님.\n###\n상황: 선생님께 스승의날 감사\n문구: 사랑하는 선생님의 베풀어주신 은혜에 깊이 감사드립니다. 항상 건강하세요.\n###\n상황: 고등학교 때 선생님께 오랜만에 스승의날 인사\n문구: 늘 선생님의 가르침을 마음에 새기고 열심히 살고 있습니다. 선생님의 은혜에 깊이 감사드립니다.\n###\n상황: 졸업하며 선생님께 인사\n문구: 선생님께서 저에게 주신 가르침과 은혜를 늘 잊지 않고 마음 속 깊이 간직하며 살아가겠습니다. 감사합니다.\n###\n상황: 선생님께 스승의날 감사\n문구: 고맙다는 말로 다 갚지도 못할 스승님의 깊은 사랑, 항상 느끼며 살아가고 있습니다. 존경합니다. 감사합니다.\n###\n상황: 중학교때 선생님께 스승의날 인사\n문구: 부족함 투성이인 저를 이렇게 이끌어주시고 희망을 주셨던 선생님의 가르침이 떠오릅니다. 가슴 깊이 존경하며 감사드립니다.\n###\n상황: 선생님께 스승의날 인사\n문구: 가르쳐주신 깊은 은혜와 넓은 사랑, 평생 소중하게 기억하겠습니다. 항상 건강하시고 행복하세요.\n###\n상황: 선생님께 스승의날 인사\n문구: 언제나 따뜻한 미소로 저희를 보듬어주시던 선생님의 모습이 그립습니다. 그 크신 은혜에 진심으로 감사드립니다.\n###\n상황: 선생님께 스승의날 인사\n문구: 인생의 등불이 되어주신 선생님! 제가 받은 큰 사랑은 절대 잊지 않겠습니다. 고맙습니다.\n###\n상황: 선생님께 스승의날 인사\n문구: 바른 길로 인도해주신 선생님의 은혜는 결코 잊지 않겠습니다. 더 크게 보답할 수 있도록 노력하겠습니다.\n###\n상황: 초등학교때 선생님께 스승의날 인사\n문구: 감사하는 마음 다 갚을 길이 없지만, 언제나 가슴 깊이 스승님의 은혜를 간직하고 있겠습니다. 항상 건강하시고, 행복하세요.\n###\n상황: 학원 선생님께 스승의날 인사\n문구: 선생님께 고마움과 존경의 마음을 담아 감사의 인사를 전합니다. 감사합니다 그리고 사랑합니다.\n###\n상황: '

    preset_text = ''.join(str_param)

   
    request_data = {
        'text': preset_text,
        'maxTokens': 165,
        'temperature': 0.55,
        'topK': 0,
        'topP': 0.8,
        'repeatPenalty': 5.0,
        'start': '\n문구:',
        'restart': '###\n상황:',
        'stopBefore': ['###\n', '상황:', '문구:'],
        'includeTokens': True,
        'includeAiFilters': True,
        'includeProbs': False
    }

    response_text = completion_executor.execute(request_data)
    print(response_text)

    return response_text



if __name__ == '__main__':
    app.run()
