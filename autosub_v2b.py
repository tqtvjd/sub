import requests
import random, string
import datetime
from time import sleep

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
cookie = ''
headers = {
    'User-Agent': USER_AGENT
}

def _buy():
    trade_no = _save()
    _checkout(trade_no)

def _save():
    form_data = {
        'period': 'month_price',
        'plan_id': 1
    }
    headers['Cookie'] = cookie
    try:
        response = requests.post(HOME_URL+V2B_SAVE_URL, json=form_data, headers=headers)
    except:
        return ''
    return str(response.json()['data'])

def _checkout(trade_no):
    form_data = {
        'trade_no': 'trade_no',
        'method': 1
    }
    headers['Cookie'] = cookie
    try:
        response = requests.post(HOME_URL+V2B_CHECKOUT_URL, json=form_data, headers=headers)
        print(response.json()['data'])
    except:
        return
    return

mailList = ['@qq.com', "@163.com", "@gmail.com"]

def _doTask():
    account = ''.join(random.choice(string.digits) for _ in range(10)).strip('0') + mailList[random.randint(0,2)]
    password = ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(12))
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
        response = requests.post(HOME_URL+V2B_REG_REL_URL, json=form_data, headers=headers)
        subscription_url = f'{HOME_URL}/api/v1/client/subscribe?token={response.json()["data"]["token"]}'
        subs.append(subscription_url)
        # _buy()
    except:
        result = response.text.encode().decode('unicode_escape')
        print('status_code: ' + str(response.status_code))
        if result.find('token') != -1:
            subscription_url = f'{HOME_URL}/api/v1/client/subscribe?token={response.json()["data"]["token"]}'
            subs.append(subscription_url)
            # _buy()
            return True
        else:
            print(f'Invalid response: {result}')
            return False
    else:
        print(f'Number succeeded: \t{subscription_url}')
        return True

if __name__ == "__main__":
    if _doTask():
        print(*subs, sep='\n')
        with open('subs.txt', 'a+') as fil:
            print(f'{datetime.datetime.now().isoformat()}\n accounts created for each site. Subscription URLs:\n----------', file=fil)
            print(*subs, sep='\n', file=fil)

