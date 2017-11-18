import requests
import json
import datetime

def getAttributes(csv_name):
    key, sec_key, username, password = '', '', '', ''
    with open(csv_name) as f:
        lines = f.readlines()
        key_line = lines[1]
        keys = key_line.split(",")
        key, sec_key, username, password =\
            keys[0], keys[1], keys[2], keys[3]
    return (key, sec_key, username, password)

def getHttp(url, moduleName, **kwargs):
    response = requests.get(url, **kwargs)

    if response.status_code == 200:
        print('{} GET Access Success'.format(moduleName))
    else:
        print('{} GET Access Failed'.format(moduleName))
        print('Error Number {}'.format(response.status_code))

    return response

def postHttp(url, moduleName, **kwargs):
    response = requests.post(url, **kwargs)
    if response.status_code == 200:
        print('{} POST Access Success'.format(moduleName))
    else:
        print('{} POST Access Failed'.format(moduleName))
        print('Error Number {}'.format(response.status_code))

    return response
# print(r_token.status_code)
# print(json.dumps(r.content))

def getToken(username, password, key, sec_key):
    access_token_url = "https://api.korbit.co.kr/v1/oauth2/access_token"
    access_token_data = {'client_id': key, 'client_secret': sec_key,
                         'username': username, 'password': password, 'grant_type': 'password'}
    r_token = postHttp(access_token_url, moduleName='get_token', data=access_token_data)
    response_data = r_token.json()
    access, refresh, type = \
        response_data['access_token'], response_data['refresh_token'], response_data['token_type']

    return (access, refresh, type)

def getUserInfo(token, type):
    get_user_inform_url = "https://api.korbit.co.kr/v1/user/info"
    get_user_inform_data = {'Authorization': '{} {}'.format(type, token)}
    user_info = getHttp(get_user_inform_url, 'user_inform', headers=get_user_inform_data)
    user_info_json = user_info.json()
    birth, gender, level, name, phone, email = \
        user_info_json['birthday'], user_info_json['gender'], user_info_json['userLevel'], \
        user_info_json['name'], user_info_json['phone'], user_info_json['email']

    return (birth, gender, level, name, phone, email)



if __name__ == "__main__":
    attr = getAttributes('../keys.csv')
    key, sec_key, username, password = attr[0], attr[1], attr[2], attr[3]

#토큰 획득
    token = getToken(username, password, key, sec_key)
    access_token, token_type = token[0], token[2]
#유저 정보
    userInfo = getUserInfo(access_token, token_type)


#환전가
    # currency_pair = {1:"btc_krw", 2:"eth_krw", 3:"etc_krw", 4:"xrp_krw", 5:"bch_krw"}
    # korean_currency = {1:"비트코인", 2:"이더리움", 3:"이더리움 클래식", 4:"리플", 5:"비트코인 캐시"}
    # for i in range(1, 6):
    #     print(korean_currency[i])
    #     d_ticker_url = "https://api.korbit.co.kr/v1/ticker/detailed?currency_pair="+currency_pair[i]
    #     detailed_ticker = getHttp(d_ticker_url, moduleName="d_ticker")
    #     d_ticker = detailed_ticker.json()
    #     changePer, askPrice, bidPrice, high, low, time, volume, change, last = \
    #         d_ticker['changePercent'], d_ticker['ask'], d_ticker['bid'], d_ticker['high'], d_ticker['low'], \
    #         datetime.datetime.fromtimestamp(d_ticker['timestamp']/1000).strftime('%Y-%m-%d %H:%M:%S'),\
    #         d_ticker['volume'], d_ticker['change'], d_ticker['last']
    #     print("최근 거래 시간: ", time)
    #     print("최근 가격 : {}원".format(last))
    #     print("지정 매도 최고가 : {}원".format(askPrice))
    #     print("지정 매수 최고가 : {}원".format(bidPrice))
    #     print("최근 24시간 하한가 : {}원".format(low))
    #     print("최근 24시간 상한가 : {}원".format(high))
    #     print("최근 24시간 거래량 : {}".format(volume))
