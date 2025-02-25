import requests 
import re 
import os 
 
# 读取pq.txt 中的每一行 
with open('pq.txt',  'r', encoding='utf-8') as file:
    lines = file.readlines() 
 
# 存储结果的列表 
results = []
 
# 遍历每行并处理每个网址 
for line in lines:
    try:
        title, url = line.strip().split(',') 
        attempts = 3  # 设置最大尝试次数 
        while attempts > 0:
            try:
                response = requests.get(url,  timeout=10)
                if response.status_code  == 200:
                    content = response.text  
                    # 使用更简洁的正则表达式 
                    match = re.search(r'(https?://[^"]+at/xml)',  content)
                    if match:
                        result = f"{title},{match.group(1)}" 
                        results.append(result) 
                    break  # 成功匹配后跳出循环 
                else:
                    print(f"请求失败，状态码：{response.status_code} ，URL：{url}")
                    attempts -= 1 
            except requests.RequestException as e:
                print(f"请求异常：{str(e)}，URL：{url}")
                attempts -= 1 
        if attempts == 0:
            print(f"经过多次尝试，无法访问URL：{url}")
    except ValueError:
        print(f"格式错误行：{line}")
 
# 将结果写入maqu.txt  
with open('maqu.txt',  'w', encoding='utf-8') as file:
    for result in results:
        file.write(result  + '\n')
 
# 清理临时文件（可选）
# if os.path.exists(file_path): 
#     os.remove(file_path) 
#     print('pq.txt 已删除')
# else:
#     print('pq.txt 不存在')
