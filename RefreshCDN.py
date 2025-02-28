from hashlib import sha1
import hmac
import requests
import json
import urllib
import os

def dogecloud_api(api_path, data={}, json_mode=False):
    """
    调用多吉云API。

    :param api_path: 调用的 API 接口地址，包含 URL 请求参数 QueryString。
    :param data: POST 的数据，字典格式。
    :param json_mode: 数据 data 是否以 JSON 格式请求，默认为 false 则使用表单形式。

    :return dict: 返回的数据。
    """
    access_key = os.environ.get('DOGECLOUD_ACCESS_KEY')  # 从环境变量获取 AccessKey
    secret_key = os.environ.get('DOGECLOUD_SECRET_KEY')  # 从环境变量获取 SecretKey

    if not access_key or not secret_key:
        raise ValueError("Access Key or Secret Key is not set in environment variables.")

    body = ''
    mime = ''
    if json_mode:
        body = json.dumps(data)
        mime = 'application/json'
    else:
        body = urllib.parse.urlencode(data)
        mime = 'application/x-www-form-urlencoded'

    sign_str = api_path + "\n" + body
    signed_data = hmac.new(secret_key.encode('utf-8'), sign_str.encode('utf-8'), sha1)
    sign = signed_data.digest().hex()
    authorization = 'TOKEN ' + access_key + ':' + sign

    response = requests.post('https://api.dogecloud.com' + api_path, data=body, headers={
        'Authorization': authorization,
        'Content-Type': mime
    })
    return response.json()

# 从环境变量中获取 URL 列表，使用逗号分隔
url_list_env = os.environ.get('CDN_URL_LIST')
if not url_list_env:
    raise ValueError("CDN_URL_LIST is not set in environment variables.")

url_list = url_list_env.split(',')

api = dogecloud_api('/cdn/refresh/add.json', {
    'rtype': 'path',
    'urls': json.dumps(url_list)
})
if api['code'] == 200:
    print(api['data']['task_id'])
else:
    print("API failed: " + api['msg'])