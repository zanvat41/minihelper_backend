import requests


def weather(city_name):
    # 聚合天气API的URL
    url = "http://apis.juhe.cn/simpleWeather/query"

    # 聚合天气API需要的key
    api_key = "yourkey"

    # 请求参数
    params = {
        "city": city_name,
        "key": api_key
    }

    try:
        # 发送GET请求
        response = requests.get(url, params=params)
        response.raise_for_status()  # 检查请求是否成功
        result = response.json()

        # 检查API返回状态
        if result.get("error_code") == 0:
            # return result["result"]
            return result["result"].get('realtime', {})
        else:
            print(f"获取天气失败: {result.get('reason', '未知错误')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
        return None
    except ValueError:
        print("解析JSON响应出错")
        return None

def stock(market, code):
    apiUrl = 'http://web.juhe.cn/finance/stock/hs'
    apiKey = 'yourkey'

    # 接口请求入参配置
    requestParams = {
        'key': apiKey,
        'gid': market+code
    }

    # 发起接口网络请求
    response = requests.get(apiUrl, params=requestParams)

    # 解析响应结果
    if response.status_code == 200:
        result = response.json()
        # 网络请求成功。可依据业务逻辑和接口文档说明自行处理。
        if len(result['result']) > 0:
            responseData = result['result'][0].get('data', {})
            increase = responseData.get('increase', '0')
            if not increase.startswith('-'):
                increase = '+' + increase
            data = {
                'name': responseData.get('name', '无'),
                'now_price': responseData.get('nowPri', '0'),
                'today_min': responseData.get('todayMin', '0'),
                'today_max': responseData.get('todayMax', '0'),
                'start_price': responseData.get('todayStartPri', '0'),
                'date': responseData.get('date', '1900-01-01'),
                'time': responseData.get('time', '00:00:00'),
                'increase': increase
            }
            return data

        return {}
    else:
        # 网络异常等因素，解析结果异常。可依据业务逻辑自行处理。
        print('请求异常')

def constellation(xz):
    apiUrl = 'http://apis.juhe.cn/fapig/constellation/query'
    apiKey = 'yourkey'

    # 接口请求入参配置
    requestParams = {
        'key': apiKey,
        'keyword': xz,
    }

    # 发起接口网络请求
    response = requests.get(apiUrl, params=requestParams)

    # 解析响应结果
    if response.status_code == 200:
        result = response.json()

        if result:
            responseData = result.get('result', {})
            data = {
                'name': responseData.get('name', '无'),
                'text': responseData.get('jbtz', '跟那啥似的'),
            }
            return data

        return result
    else:
        # 网络异常等因素，解析结果异常。可依据业务逻辑自行处理。
        print('请求异常')


# 使用示例
if __name__ == "__main__":
    city = "佛山"
    weather_data = None # weather(city)
    stock_data = None # stock('sz', '000001')
    xz_data = constellation('白羊座')

    if xz_data:
        print(xz_data)

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
    if stock_data:
        print(stock_data)