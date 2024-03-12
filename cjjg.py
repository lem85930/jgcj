import requests
from bs4 import BeautifulSoup
import csv

# 指定搜索关键词
search_keyword = "at/xml 采集 帮助"

# Google搜索URL
url = f"https://www.google.com/search?q={search_keyword}"

# 发送请求并获取网页内容
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# 解析搜索结果
search_results = []
for index, result in enumerate(soup.find_all('div', class_='tF2Cxc'), start=1):
    title = result.find('h3').text
    link = result.find('a')['href']
    search_results.append((f"cjy{str(index).zfill(2)}", title, link))

# 将搜索结果写入CSV文件
with open('cj.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['序号', 'API名称', 'API链接'])  # 写入表头
    for item in search_results:
        writer.writerow(item)  # 写入搜索结果

print(f"已将搜索结果保存到cj.csv文件中。")
