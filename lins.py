import requests
import re
import os
# 读取pq.txt中的每一行
with open('pq.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 存储结果的列表
results = []

# 遍历每行并处理每个网址
for line in lines:
    title, url = line.strip().split(',')
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text
        match = re.search(r'https?[^"\']+at/xml', content)
        if match:
            result = f"{title},{match.group(0)}"
            results.append(result)

# 将结果写入maqu.txt
with open('maqu.txt', 'w', encoding='utf-8') as file:
    for result in results:
        file.write(result + '\n')
file_path = 'pq.txt'

if os.path.exists(file_path):
    os.remove(file_path)
    print('pq.txt已删除')
else:
    print('pq.txt不存在')
