import requests
from bs4 import BeautifulSoup
import re
import time

def get_max_page_number(base_url, headers):
    """
    获取最大页码
    逻辑：在 index.html 中寻找“尾页”链接，提取 index_数字.html 中的数字
    """
    try:
        response = requests.get(base_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        last_page_link = soup.find('a', string='尾页')
        if last_page_link and 'href' in last_page_link.attrs:
            href = last_page_link['href']
            # 匹配 index_(d+).html 格式
            match = re.search(r'index_(d+)', href)
            if match:
                return int(match.group(1))
    except Exception as e:
        print(f"❌ 获取最大页码失败: {type(e).__name__} - {str(e)[:50]}")
    return 1

# 请求头配置
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

# 基础URL配置 (直接访问主站)
domain = "https://www.yszzq.com"
tag_path = "/tags/xmlcjjk/"
base_url = f"{domain}{tag_path}index.html"

# 获取最大页码
max_page = get_max_page_number(base_url, headers)
print(f"📊 检测到最大页数: {max_page}")

# 自动生成待爬取的URL列表
# 第一页是 index.html，后续是 index_2.html, index_3.html ...
urls = [base_url]
if max_page > 1:
    urls += [f"{domain}{tag_path}index_{i}.html" for i in range(2, max_page + 1)]

print(f"🎯 共生成 {len(urls)} 个目标URL")

all_results = []

for index, url in enumerate(urls):
    try:
        if index > 0:
            time.sleep(1.2)  # 礼貌性延时
            
        print(f"正在爬取 ({index + 1}/{len(urls)}): {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 关键词正则匹配
        pattern = re.compile(r' 接口|地址|API|资源|资源库|资源接口|资源网|json[\u4e00-\u9fa5]*', re.UNICODE)
        
        for element in soup.find_all(string=pattern):
            parent = element.find_parent('a')
            if not parent or 'href' not in parent.attrs:
                continue
                
            raw_href = parent['href']
            title = element.strip()
            
            # 构建完整URL
            if raw_href.startswith(('http://', 'https://')):
                final_url = raw_href
            else:
                if not raw_href.startswith('/'):
                    raw_href = '/' + raw_href.lstrip('./')
                final_url = f"{domain}{raw_href}"

            # 数据过滤与保存逻辑
            valid_keywords = ["采集接口", "资源库", "资源接口", "采集API接口"]
            is_valid = any(kw in title for kw in valid_keywords) and "XML" not in title
            
            if is_valid:
                all_results.append(f"{title},{final_url}")
                print(f"✅ 发现有效接口: {title[:15]}... -> {final_url[:50]}...")
                
    except Exception as e:
        print(f"❌ 访问出错 {url}: {type(e).__name__} - {str(e)[:50]}")

# 最终结果持久化
with open('pq.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(all_results))

print(f"\n🎯 抓取完成！")
print(f"✅ 结果已保存至 pq.txt，共计 {len(all_results)} 条有效记录。")
