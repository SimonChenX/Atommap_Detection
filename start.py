import json
import requests
import time
import socks
import socket

# 设置代理参数
proxies = {
    'http': 'socks5://127.0.0.1:7890',
    'https': 'socks5://127.0.0.1:7890'
}

# 读取config.json文件中的X起始值
with open('config.json') as f:
    config = json.load(f)
    X = config['number']

# 循环请求URL
while True:
    url = f"https://server.atomicalmarket.com/mainnet/v1/atommap/block/{X}"

    # 设置请求头
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'server.atomicalmarket.com',
        'Origin': 'https://atomicalmarket.com',
        'Pragma': 'no-cache',
        'Referer': 'https://atomicalmarket.com/',
        'Sec-Ch-Ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }

    # 发送请求
    response = requests.get(url, proxies=proxies, headers=headers)
    try:
        # 将response的内容转换为JSON格式
        data = response.json()
    except json.decoder.JSONDecodeError:
        print("Error: Failed to decode JSON response")
        continue
    print(response.text)
    # 判断返回参数中的code是否为404
    if data['code'] == 404:
        result = f"X={X}, True, {data['message']}, https://atomicalmarket.com/atomical/{X}.atommap\n"
    else:
        result = f"X={X}, False, {data['data']['AtomicNumber']}\n"

    # 写入结果到result.txt文件中
    with open('result.txt', 'a') as f:
        f.write(result)

    # 判断返回参数中的code是否为404
    if data['code'] == 404:
        message = data['message']
        # 判断message中是否包含"Please try again in 5 minutes"
        if "Please try again in 5 minutes" in message:
            print("Program will pause for 5 minutes...")
            time.sleep(300)  # 暂停5分钟（300秒）
            X -= 1

    # X加1后执行下一次请求
    X += 1

    # 将当前的X值存储到config.json文件中
    config['number'] = X
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file)
