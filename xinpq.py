import requests
from bs4 import BeautifulSoup
from urllib.parse  import urljoin  # 更安全的URL拼接方式
import re

all_results = []

# 添加浏览器头信息规避反爬
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

urls = [
    "https://cfpgwztz.wofuck.rr.nu/wztz/https/www.yszzq.com/tags/xmlcjjk/",
    "https://cfpgwztz.wofuck.rr.nu/wztz/https/www.yszzq.com/tags/xmlcjjk_1",
    "https://cfpgwztz.wofuck.rr.nu/wztz/https/www.yszzq.com/tags/xmlcjjk_2",
    "https://cfpgwztz.wofuck.rr.nu/wztz/https/www.yszzq.com/tags/xmlcjjk_3",
    "https://cfpgwztz.wofuck.rr.nu/wztz/https/www.yszzq.com/tags/xmlcjjk_4",
    "https://cfpgwztz.wofuck.rr.nu/wztz/https/www.yszzq.com/tags/xmlcjjk_5",
    "https://cfpgwztz.wofuck.rr.nu/wztz/https/www.yszzq.com/tags/xmlcjjk_6",
    "https://cfpgwztz.wofuck.rr.nu/wztz/https/www.yszzq.com/tags/xmlcjjk_7",
    "https://cfpgwztz.wofuck.rr.nu/wztz/https/www.yszzq.com/tags/xmlcjjk_8",
    "https://cfpgwztz.wofuck.rr.nu/wztz/https/www.yszzq.com/tags/xmlcjjk_9",
    "https://cfpgwztz.wofuck.rr.nu/wztz/https/www.yszzq.com/tags/xmlcjjk_10"
]  # 保持原有URL列表不变

for url in urls:
    try:
        # 添加超时和请求头参数
        response = requests.get(url,  headers=headers, timeout=10)
        response.raise_for_status()   # 主动抛出HTTP错误
        
        # 明确指定解析器避免环境差异
        soup = BeautifulSoup(response.text,  'lxml' if 'lxml' in locals() else 'html.parser') 
        
        # 优化正则表达式匹配模式
        pattern = re.compile(r' 接口|地址|资源库|资源网|json', re.UNICODE)
        elements = soup.find_all(string=pattern) 

        for element in elements:
            parent = element.find_parent('a') 
            if not parent or not parent.has_attr('href'): 
                continue
                
            # 使用urljoin处理相对路径
            href = urljoin(url, parent['href'])
            title = element.strip()   # 去除首尾空白字符
            
            # 优化过滤条件逻辑
            if any(keyword in title for keyword in ["采集接口", "采集地址", "资源库"]) \
            and "XML采集接口" not in title \
            and title not in ["采集接口", "采集地址"]:
                all_results.append(f"{title},{href}\n") 
                # 添加控制台输出用于调试
                print(f"Found: {title} -> {href}")

    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        continue

# 确保文件写入UTF-8编码
with open('pq.txt',  'w', encoding='utf-8') as f:
    f.writelines(all_results) 
print(f"Total {len(all_results)} records saved.")  # 添加结果统计
