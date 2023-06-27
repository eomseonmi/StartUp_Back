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
        n=1,
        size="1024x1024"
    )
    #image_urls = [image.url for image in response.images]
    image_urls = response['data'][0]['url']
    print(response['data'][0]['url'])
    return image_urls

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        # 입력된 텍스트를 사용하여 이미지 생성
        image_urls = generate_image(text)
        return render_template('images.html', image_urls=image_urls)
    return render_template('images.html')


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

@app.route('/a', methods=['GET'])
def invoke_completion():
    host = 'clovastudio.apigw.ntruss.com'
 
    api_key='NTA0MjU2MWZlZTcxNDJiY/63AdFamemdYLqegws5nlFYbsFydFURWurW5YN+7o+L5XpjOcWXG1GZUqCHYZX0wARW2fSshwQ9Gz6vx71wxqcR3wm+v4eoTUtuh403Y0hCJkzMFXD5XiIbTidf8Tzdyxd5mG5oFzOxFDSLTb7SCQObOqGvkj5/dr4vAZUEiAS5zxccF0cXDhO9lVBljP5YZg2XRJSzvJwgDvfOTjHdQ9M='
    api_key_primary_val = 'NtCsDeWuLXowvJfzvqe16WRFf3mlfNZFKoN5I72Y'
    request_id='9bbaddfe5bab4b35a1309b1f3fbfaf57'
   

    completion_executor = CompletionExecutor(host, api_key, api_key_primary_val, request_id)


    preset_text = '스승의 날을 기념하여 고등학교 시절 선생님께 드릴 선물에 작성한 선물 메시지 5가지를 작성하세요'

    request_data = {
        'text': preset_text,
        'maxTokens': 32,
        'temperature': 0.5,
        'topK': 0,
        'topP': 0.8,
        'repeatPenalty': 5.0,
        'start': '',
        'restart': '',
        'stopBefore': [],
        'includeTokens': True,
        'includeAiFilters': True,
        'includeProbs': False
    }

    response_text = completion_executor.execute(request_data)
    return response_text



if __name__ == '__main__':
    app.run()
