import requests
import random, string
import datetime

V2B_REG_REL_URL = '/api/v1/passport/auth/register'
# V2B_SUB_REL_URL = '/api/v1/user/getSubscribe'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49'

# home_urls = 'http://whk.life'
# home_urls = 'https://v2board.co'
home_urls = 'https://daydaygeek.icu'

times = 1
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

account = ''.join(random.choice(string.digits) for _ in range(9))
form_data = {
    'email': '3'.join(account) + '@qq.com',
    'password': ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(12)),
    'invite_code': 'deeCjRtg',
    'email_code': ''
}
content = ""

def _request():
    try:
        response = requests.post(home_urls+V2B_REG_REL_URL, json=form_data)
        subscription_url = f'{home_urls}/api/v1/client/subscribe?token={response.json()["data"]["token"]}'
        print(subscription_url)
        content = requests.get(subscription_url)
        print(f'content: {content.text}')
        
        with open('nodes.txt', 'w') as fil:
            fil.write(content.text)

        # 订阅获取成功以后，刷新CDN缓存
        requests.get("https://purge.jsdelivr.net/gh/tqtvjd/sub@main/nodes.txt")
    except Exception as ex:
        print(f'Error: {ex}')

_request()
