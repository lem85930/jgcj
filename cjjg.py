import csv
import requests
from bs4 import BeautifulSoup

# 搜索关键词
query = "at/xml 采集 帮助"

# 构建Google搜索URL
url = f"https://www.google.com/search?q={query}&sca_esv=e1f0b68dea977417&sxsrf=ACQVn09YtSv75TWfD_SiXFkwhbrT3Wtt_g%3A1710226915992&source=hp&ei=4_3vZevpOYvR2roPop--0As&iflsig=ANes7DEAAAAAZfAL8875oZz0PIej1rrOGIfTTw92LAsc&ved=0ahUKEwir573ek-6EAxWLqFYBHaKPD7oQ4dUDCBU&oq=at%2Fxml+%E9%87%87%E9%9B%86+%E5%B8%AE%E5%8A%A9&gs_lp=Egdnd3Mtd2l6IhRhdC94bWwg6YeH6ZuGIOW4ruWKqTIHECMYrgIYJ0i_IFAAWABwAHgAkAEAmAGtBaABrQWqAQM1LTG4AQzIAQD4AQL4AQGYAgGgArAFmAMAkgcDNS0xoAedAg&sclient=gws-wiz"

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
