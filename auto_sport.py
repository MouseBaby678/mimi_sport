import random
import time
import datetime
import requests

with open('./token', 'r') as f:
    token = f.read().strip()

# 起点经纬度
lat = 36.56117078993056
lng = 116.80826334635417
headers = {
    "Accept-Encoding": "gzip,compress,br,deflate",
    "content-type": "application/x-www-form-urlencoded",
    "Connection": "keep-alive",
    "Referer": "https://servicewechat.com/wx5069fcccc8151ce3/41/page-frame.html",
    "Host": "admin.report.mestallion.com",
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.34(0x1800222f) NetType/WIFI Language/zh_CN",
    "token": token
}


def get_line():
    body = 'lat=' + str(lat + random.random() * 0.0001) + '&lng=' + str(lng + random.random() * 0.0001)
    x = requests.post(headers=headers, url="https://admin.report.mestallion.com/api/mini/sport/getline", data=body)
    time.sleep(1)
    print('状态码：{}'.format(x.status_code))
    print(x.json()['msg'])


def today():
    x = requests.post(headers=headers, url="https://admin.report.mestallion.com/api/mini/sport/today")
    time.sleep(1)
    response_json = x.json()
    return response_json


def daka(lat, lng, id, line):
    print('当前打卡点：{}'.format(line))
    print('lat:{} lng:{} id:{}'.format(lat, lng, id))
    body = "ble=false&gps=false&" + 'lat=' + str(lat + random.random() * 0.0001) + '&lng=' + str(
        lng + random.random() * 0.0001) + "&bs_id=&bs_name=&id=" + str(id)
    x = requests.post(headers=headers, url="https://admin.report.mestallion.com/api/mini/sport/daka", data=body)
    time.sleep(1)
    print(x.json()['msg'])
    print('<----------------------------------->')


def delay(start_time, end_time, n):
    delay_time = (end_time - start_time) * 0.5 / (n - 1)
    delay_time = delay_time + datetime.timedelta(hours=0, minutes=0, seconds=random.randrange(0, 30))
    print('下次打卡时间{}'.format(datetime.datetime.now() + delay_time))
    time.sleep(delay_time.seconds)


def show_line(lines):
    print('本次打卡路线：')
    for l in lines:
        print(l['point_name'])


if __name__ == '__main__':
    print('当前用户：{}'.format(today()['data']['user']['name']))
    get_line()
    today_response = today()
    lines = today_response['data']['line']['lines']
    show_line(lines)
    # 打卡，开启运动
    daka(float(lines[0]['lat']), float(lines[0]['lng']), int(lines[0]['id']), lines[0]['point_name'])
    today_response = today()
    start_time = datetime.datetime.strptime(today_response['data']['line']['starttime'], "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(today_response['data']['line']['max_end_time'], "%Y-%m-%d %H:%M:%S")
    n = len(lines)
    for l in lines[1:]:
        delay(start_time, end_time, n)
        daka(float(l['lat']), float(l['lng']), int(l['id']), l['point_name'])
    print('本次运动结束!')
