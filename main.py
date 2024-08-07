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
    # 这里模拟 get_words() 函数的返回值，实际情况可能从文件、数据库或其他来源获取  
    return "这是一个示例文本，用于展示如何每16个字符后换行。请确保您的文本足够长以便看到效果。"  
  
def format_words(words, line_length=16):  
    # 使用列表推导式和字符串的切片功能来分割字符串  
    # 并用 '\n' 来连接每一段  
    formatted_words = '\n'.join(words[i:i+line_length] for i in range(0, len(words), line_length))  
    return formatted_words  

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
        formatted_words = format_words(words)
        out_time = get_time()
        color1 = get_random_color()
        print(formatted_words, out_time,color1)

        wea_city,weather = get_weather(city,weather_key)
        data = {"name":{"value": name, "color": color1},"wind":{"value":weather['winddirection']},"birthday_left":{"value":get_birthday(birthday)},"time":{"value":out_time},"words":{'value': formatted_words, "color": get_random_color()},"weather":{'value': weather['weather']},"city":{"value":wea_city},"tem_low":{"value":weather['temperature']},"born_days":{"value":get_count(born_date)}}

        res = wm.send_template(user_id, template_id, data)
        print(res)
        num += 1
    print(f"成功发送{num}条信息")
