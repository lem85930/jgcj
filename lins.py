import requests 
import re 
import time 
 
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.yszzq.com/" 
}
 
with open('pq.txt',  'r', encoding='utf-8') as file:
    lines = file.readlines() 
 
results = []
 
for line in lines:
    try:
        title, base_url = line.strip().split(',') 
        for _ in range(3):  # 重试 3 次 
            try:
                response = requests.get(base_url.strip(),  headers=headers, timeout=10)
                if response.status_code  == 200:
                    # 精准匹配首个 data-clipboard-text 中的链接 
                    match = re.search( 
                     # r"data-clipboard-text=['\"](https?://[^'\"]+?at/xml/?)/?['\"]", 
                     r"data-clipboard-text=['\"](https?://[^'\"]+?at/xml(?:/.*)?)['\"]",
                        response.text  
                    )
                    if match:
                        # 统一规范链接格式（去除尾部斜杠）
                        clean_url = match.group(1).rstrip('/') 
                        results.append(f"{title},{clean_url}/")   # 保留结构斜杠 
                        break  # 获取到首个链接即终止重试 
                    else:
                        print(f"未找到有效接口，URL：{base_url}")
                        break  # 无匹配时也终止重试 
                else:
                    print(f"请求失败，状态码：{response.status_code} ，URL：{base_url}")
            except Exception as e:
                print(f"请求异常：{str(e)}，URL：{base_url}")
            time.sleep(1)   # 每次请求间隔 1 秒 
    except ValueError:
        print(f"格式错误行：{line}")
 
with open('maqu.txt',  'w', encoding='utf-8') as file:
    file.write('\n'.join(results)) 
