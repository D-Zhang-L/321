from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage
import os
import json
from datetime import datetime, timedelta
import random
import requests

nowtime = datetime.utcnow() + timedelta(hours=8)
today = datetime.strptime(str(nowtime.date()), "%Y-%m-%d")


def get_time():
    dictDate = {'Monday': '星期一', 'Tuesday': '星期二', 'Wednesday': '星期三', 'Thursday': '星期四',
                'Friday': '星期五', 'Saturday': '星期六', 'Sunday': '星期天'}
    a = dictDate[nowtime.strftime('%A')]
    return nowtime.strftime("%Y年%m月%d日") + a


def get_words():  
    # 这里返回一个示例字符串，实际中您可能从某处获取它  
    return "这是一个非常长的字符串，需要被分割成多个部分，这是一个非常长的字符串，需要被分割成多个部分，这是一个非常长的字符串，需要被分割成多个部分"  

def get_weather(city, key):
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?city=210200&key=d59056d227370d057687bfceeba83cf2"
    res = requests.get(url).json()
    print(res)
    weather = res['lives'][0]
    return '大连', weather

def get_count(born_date):
    delta = today - datetime.strptime(born_date, "%Y-%m-%d")
    return delta.days


def get_birthday(birthday):
    nextdate = datetime.strptime(str(today.year) + "-" + birthday, "%Y-%m-%d")
    if nextdate < today:
        nextdate = nextdate.replace(year=nextdate.year + 1)
    return (nextdate - today).days
    
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


if __name__ == '__main__':
    app_id = os.getenv("APP_ID")
    app_secret = os.getenv("APP_SECRET")
    template_id = os.getenv("TEMPLATE_ID")
    weather_key = os.getenv("WEATHER_API_KEY")

    client = WeChatClient(app_id, app_secret)
    wm = WeChatMessage(client)

    f = open("./users_info.json", encoding="utf-8")
    js_text = json.load(f)
    f.close()
    data = js_text['data']
    num = 0
    
    for user_info in data:
        born_date = user_info['born_date']
        birthday = born_date[5:]
        city = user_info['city']
        user_id = user_info['user_id']
        name = user_info['user_name'].upper()
        words = get_words()
        out_time = get_time()
        print(words, out_time)
        
  

        wea_city,weather = get_weather(city,weather_key)
        data = dict()
        data['time'] = {'value': out_time}
        data['words'] = {'value': words}
        
        words_length = len(words) 
        start = 0  
        end = 16  
        index = 1  
        while start < words_length:  
            # 计算当前片段的结束位置，但不超过words的总长度  
            end = min(end, words_length)  
            # 提取当前片段并添加到message_data中  
            data[f'words{index}'] = {'value': words[start:end]}  
            # 更新start和end以及index以准备下一个片段  
            start += 16  
            end += 16  
            index += 1
        data['weather'] = {'value': weather['weather']}
        data['city'] = {'value': wea_city}
        data['tem_high'] = {'value': weather['temperature']}
        data['tem_low'] = {'value': weather['temperature']}
        data['born_days'] = {'value': get_count(born_date)}
        data['birthday_left'] = {'value': get_birthday(birthday)}
        data['wind'] = {'value': weather['winddirection']}
        data['name'] = {'value': name}

        res = wm.send_template(user_id, template_id, data)
        print(res)
        num += 1
    print(f"成功发送{num}条信息")
