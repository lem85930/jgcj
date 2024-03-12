import csv
import requests
from bs4 import BeautifulSoup

# 搜索关键词
query = "at/xml 采集 帮助"

# 构建Google搜索URL
url = f"https://www.google.com/search?q={query}"

# 发送请求并获取响应
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# 从HTML中提取搜索结果
search_results = []
count = 1
for result in soup.select(".g"):
    title = result.select_one(".LC20lb").text
    link = result.select_one(".yuRUbf > a")["href"]
    item_no = f"cjy{count:02d}"
    search_results.append((item_no, title, link))
    count += 1

# 将结果写入CSV文件
with open("cj.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["序号", "API名称", "API链接"])
    writer.writerows(search_results)

print("搜索结果已保存到cj.csv文件中。")
