import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
import re
import time

# 代理网关路径常量（保留，用于后续拼接子链接）
PROXY_PATH = "/wztz/https/www.yszzq.com"

def build_proxy_url(original_url):
    """重构URL构建逻辑（保留，用于处理页面内的子链接）"""
    parsed = urlparse(original_url)
    if parsed.netloc == "www.yszzq.com":
        new_path = f"{PROXY_PATH}{parsed.path}"
        return urlunparse((
            parsed.scheme,
            "wztz.wokaotianshi.eu.org",
            new_path,
            parsed.params,
            parsed.query,
            parsed.fragment
        ))
    return original_url

def get_max_page_number(proxy_base_url):
    """获取最大页码（根据实际网页源码重构逻辑）"""
    try:
        # 直接请求代理后的URL
        response = requests.get(proxy_base_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 1. 定位分页容器（class="pager"的div）
        pager_div = soup.find('div', class_='pager')
        if not pager_div:
            print("⚠️ 未找到分页容器")
            return 0
        
        # 2. 找到尾页链接
        last_page_link = pager_div.find('a', string='尾页')
        if last_page_link and 'href' in last_page_link.attrs:
            href = last_page_link['href']
            # 匹配尾页链接中的页码：index_数字.html
            match = re.search(r'index_(\d+)\.html', href)
            if match:
                max_page = int(match.group(1))
                print(f"✅ 从尾页链接提取到最大页码：{max_page}")
                return max_page
        
        # 备用方案：如果尾页链接找不到，提取所有分页数字中的最大值
        page_numbers = []
        # 匹配所有分页链接中的数字
        page_links = pager_div.find_all('a', href=re.compile(r'index_(\d+)\.html'))
        for link in page_links:
            match = re.search(r'index_(\d+)\.html', link['href'])
            if match:
                page_numbers.append(int(match.group(1)))
        
        # 匹配分页区域内的纯数字span（当前页码）
        current_page_span = pager_div.find('span', string=re.compile(r'^\d+$'))
        if current_page_span:
            page_numbers.append(int(current_page_span.text.strip()))
        
        if page_numbers:
            max_page = max(page_numbers)
            print(f"✅ 从分页数字提取到最大页码：{max_page}")
            return max_page
        
    except Exception as e:
        print(f"❌ 获取最大页码失败: {type(e).__name__} - {str(e)[:50]}")
    return 0

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'X-Forwarded-Proto': 'https'
}

# 直接使用代理后的完整基础URL
base_url = "https://wztz.wokaotianshi.eu.org/wztz/https/www.yszzq.com/tags/xmlcjjk/index.html"

# 获取最大页码
max_page = get_max_page_number(base_url)

# 生成URL列表：第一页为原base_url，第二页开始为index_2.html、index_3.html...
urls = [base_url]  # 第一页
# 从2开始生成后续页码（第二页是index_2.html）
if max_page >= 2:
    urls += [
        base_url.replace('index.html', f'index_{i}.html') 
        for i in range(2, max_page + 1)
    ]

print(f"🎯 共生成 {len(urls)} 个URL")

all_results = []

for index, url in enumerate(urls):
    try:
        if index > 0:
            time.sleep(1.5)
        # 直接请求代理URL（无需再转换）
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        pattern = re.compile(r' 接口|地址|API|资源|资源库|资源接口|资源网|json[\u4e00-\u9fa5]*', re.UNICODE)
        for element in soup.find_all(string=pattern):
            parent = element.find_parent('a')
            if not parent or 'href' not in parent.attrs:
                continue
            raw_href = parent['href']
            title = element.strip()
            if raw_href.startswith(('http://', 'https://')):
                # 页面内的子链接仍需转换为代理URL
                final_url = build_proxy_url(raw_href)
            else:
                if not raw_href.startswith('/'):
                    raw_href = '/' + raw_href.lstrip('./')
                final_url = f"https://wztz.wokaotianshi.eu.org{PROXY_PATH}{raw_href}"
            if "/ziyuan/api/" in final_url:
                print(f"Debug - Generated URL: {final_url}")
            if ("采集接口" in title or "资源库" in title or "资源接口" in title or "采集API接口" in title) and "XML" not in title:
                all_results.append(f"{title},{final_url}")
                print(f"✅ Valid: {title[:15]}... -> {final_url[:50]}...")
    except Exception as e:
        print(f"❌ Error on {url}: {type(e).__name__} - {str(e)[:50]}")

with open('pq.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(all_results))
print(f"🎯 结果已保存：共{len(all_results)}条有效记录")
