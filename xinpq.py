import requests
from bs4 import BeautifulSoup
import re

# 存储所有词语及其父节点的href属性值
all_results = []

# 多个网址需要提取
urls = [
    "https://www.yszzq.com/tags/xmlcjjk/",
    "https://www.yszzq.com/tags/xmlcjjk_1",
    "https://www.yszzq.com/tags/xmlcjjk_2"
]

# 遍历请求多个网址
for url in urls:
    response = requests.get(url)
    if response.status_code != 200:
        continue  # 如果请求失败，跳过当前网址
    soup = BeautifulSoup(response.content, "html.parser")
    elements = soup.find_all(string=re.compile("采集接口"))
    for element in elements:
        parent = element.find_parent("a")
        if parent:
            title = element
            href = parent['href']
            if href.startswith("http"):
                full_href = href
            else:
                full_href = f"https://www.yszzq.com{href}"
            # 检查词语是否包含"采集接口"，但不仅仅包含"采集接口"，如果是，则添加到结果中
            if "采集接口" in title and not title.strip() == "采集接口" and "XML采集接口" not in title:
                all_results.append(f"{title},{full_href}\n")

# 将结果写入pq.txt
with open('pq.txt', 'w', encoding='utf-8') as file:
    for result in all_results:
        file.write(result)