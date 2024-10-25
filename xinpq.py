import requests
from bs4 import BeautifulSoup
import re

# 存储所有词语及其父节点的href属性值
all_results = []

# 多个网址需要提取
urls = [
    "https://wztz.wokaotianshi.eu.org/wztz/https/www.yszzq.com/tags/xmlcjjk/",
    "https://wztz.wokaotianshi.eu.org/wztz/https/www.yszzq.com/tags/xmlcjjk_1",
    "https://wztz.wokaotianshi.eu.org/wztz/https/www.yszzq.com/tags/xmlcjjk_2",
    "https://wztz.wokaotianshi.eu.org/wztz/https/www.yszzq.com/tags/xmlcjjk_3",
    "https://wztz.wokaotianshi.eu.org/wztz/https/www.yszzq.com/tags/xmlcjjk_4",
    "https://wztz.wokaotianshi.eu.org/wztz/https/www.yszzq.com/tags/xmlcjjk_5",
    "https://wztz.wokaotianshi.eu.org/wztz/https/www.yszzq.com/tags/xmlcjjk_6",
    "https://wztz.wokaotianshi.eu.org/wztz/https/www.yszzq.com/tags/xmlcjjk_7",
    "https://wztz.wokaotianshi.eu.org/wztz/https/www.yszzq.com/tags/xmlcjjk_8",
    "https://wztz.wokaotianshi.eu.org/wztz/https/www.yszzq.com/tags/xmlcjjk_9",
    "https://wztz.wokaotianshi.eu.org/wztz/https/www.yszzq.com/tags/xmlcjjk_10"
]

# 遍历请求多个网址
for url in urls:
    response = requests.get(url)
    if response.status_code != 200:
        continue  # 如果请求失败，跳过当前网址
    soup = BeautifulSoup(response.content, "html.parser")
    elements = soup.find_all(string=re.compile("接口|地址|资源库|资源网"))
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
            if ("采集接口" in title or "采集地址" in title or "资源库" in title or "json" in title) and not title.strip() == "采集接口" and "XML采集接口" not in title:
    # 这里是您的处理逻辑
                all_results.append(f"{title},{full_href}\n")

# 将结果写入pq.txt
with open('pq.txt', 'w', encoding='utf-8') as file:
    for result in all_results:
        file.write(result)
