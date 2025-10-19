import requests

# 设置 API Key
api_key = "yourkey"
# 构建请求头
headers = {
    "X-QW-Api-Key": api_key
}
# 城市的代码
cities = {
    "北京": "101010100",
    "广州": "101280101",
    "佛山": "101280800",
    "上海": "101020100",
    "北京市": "101010100",
    "广州市": "101280101",
    "佛山市": "101280800",
    "上海市": "101020100"
}

# 定义请求的 URL
url = 'https://ku487rfjm3.re.qweatherapi.com/v7/weather/now?location='


def weather(city):
    try:
        # 发送 GET 请求，并传递请求头
        response = requests.get(url+cities.get(city, "101010100"), headers=headers)
        # 检查响应状态码，如果不是 200 则抛出异常
        response.raise_for_status()
        # 解析响应的 JSON 数据
        data = response.json()

        print(data)
        data = data['now']

        res = {'temperature': data['temp'], 'humidity': data['humidity'], 'info': data['text'],
               'direct': data['windDir'], 'power': data['windScale'] + '级', 'city': city}

        return res
    except requests.RequestException as e:
        # 处理请求过程中可能出现的异常
        print(f"请求发生错误: {e}")

if __name__ == "__main__":
    city = "佛山"
    weather_data = weather(city)

    if weather_data:
        print(weather_data)
        '''
        print("\n天气信息:")
        print(f"城市: {weather_data.get('city')}")
        print(f"天气: {weather_data.get('realtime', {}).get('info')}")
        print(f"温度: {weather_data.get('realtime', {}).get('temperature')}℃")
        print(f"湿度: {weather_data.get('realtime', {}).get('humidity')}%")
        print(f"风向: {weather_data.get('realtime', {}).get('direct')}")
        print(f"风力: {weather_data.get('realtime', {}).get('power')}")

        # 打印未来几天天气预报
        print("\n未来天气预报:")
        for forecast in weather_data.get("future", []):
            print(f"{forecast.get('date')}: {forecast.get('weather')}, "
                  f"温度: {forecast.get('temperature')}")
        '''