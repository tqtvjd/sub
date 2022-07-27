import requests
import random, string
import datetime
from time import sleep
import json

V2B_REG_REL_URL = '/api/v1/passport/auth/register'
V2B_SAVE_URL = '/api/v1/user/order/save'
V2B_CHECKOUT_URL = '/api/v1/user/order/checkout'
# V2B_SUB_REL_URL = '/api/v1/user/getSubscribe'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.72'

HOME_URL = 'http://whk.life'
proxies = {
    'http': 'http://127.0.0.1:10809',
    'https': 'http://127.0.0.1:10809'
}

subs = []
headers = {
    'User-Agent': USER_AGENT
}

def _buy(newCookie):
    trade_no = _save(newCookie)
    if len(trade_no) > 0:
        _checkout(newCookie, trade_no)

def _save(cookie):
    form_data = {
        'period': 'month_price',
        'plan_id': 1
    }
    headers['Cookie'] = cookie
    try:
        response = requests.post(HOME_URL+V2B_SAVE_URL, json=form_data, headers=headers)
    except Exception as ex:
        print(f'save: {ex}')
        return ''
    print('save response result: ' + response.text.encode().decode('unicode_escape'))
    if(is_json(response.text) and response.json().has_key('data')): 
        return str(response.json()['data'])
    else:
        return ''

def _checkout(cookie, trade_no):
    form_data = {
        'trade_no': trade_no,
        'method': 1
    }
    headers['Cookie'] = cookie
    try:
        response = requests.post(HOME_URL+V2B_CHECKOUT_URL, json=form_data, headers=headers)
        print('Checkout result：' + str(response.json()['data']))
    except Exception as ex:
        print(f'checkout: {ex}')
        return
    return

wordList = ['li_', 'zhang', 'shan', 'bibi', 'zhou', 'chen', 'wang', 'majia', 'qiu', 'aii', 'linzi', 'yue99', 'zheng', '_liu2', 'tantan', 'yang', 'gao88',
    'xu002', 'baishi', 'liao', 'zhong', 'qiao', 'yao', 'yu_', 'min_66', 'sky2', 'flyin', 'ming', 'hua', 'xiao', 'lu2022', 'gong', 'yao9', 'kun7', 'huan', 'dian', 'feng',
    'nice', 'happy', '2010go', 'love', 'cc520', 'a1314', 'ding', 'qian', 'tu_22', 'jiang', 'chao'    
]
mailList = ["@163.com", "@gmail.com", "@126.com", "@yeah.net"]

def _randomWord():
    return wordList[random.randint(0, len(wordList) - 1)]

def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True

def _doTask():
    account = _randomWord() + _randomWord() + mailList[random.randint(0, len(mailList) - 1)]
    password = ''.join(random.choice(string.digits + string.ascii_letters + '-_<>?,./!@#$%^&*~') for _ in range(random.randint(10, 15)))
    subs.append('account: ' + account)
    subs.append('password: ' + password)
    form_data = {
        'email': account,
        'password': password,
        'invite_code': 'deeCjRtg',
        'email_code': ''
    }
    headers['Cookie'] = 'v2board_session=eyJ'.join(random.choice(string.ascii_letters+string.digits) for _ in range(340))

    try:
        response = requests.post(HOME_URL+V2B_REG_REL_URL, json=form_data, headers=headers, proxies=proxies)
    except Exception as ex:
        print(f'Ex: {ex}')
        print('status_code: ' + str(response.status_code))
        if str(response.status_code).startswith('4'):
            return False
    result = response.text.encode().decode('unicode_escape')
    print('result: ' + result)
    
    if 'Set-Cookie' in response.headers.keys():
        _buy(response.headers['Set-Cookie'])
    return True

if __name__ == "__main__":
    if _doTask():
        print(*subs, sep='\n')
        with open('subs.txt', 'a+') as fil:
            print(f'{datetime.datetime.now().isoformat()}\naccounts created for each site. Subscription URLs:\n----------', file=fil)
            print(*subs, sep='\n', file=fil)

