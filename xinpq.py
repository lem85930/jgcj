import requests
from bs4 import BeautifulSoup
import re
import time

def get_max_page_number(base_url, headers):
    """
    根据提供的 HTML 结构精确获取最大页码
    逻辑：在 class='pager' 的容器中遍历 <a> 标签，寻找包含“尾页”文字的链接，
    并从中提取 index_(d+).html 里的数字。
    """
    try:
        response = requests.get(base_url, headers=headers, timeout=15)
        response.raise_for_status()
        # 使用 lxml 提高解析效率，如未安装请改为 'html.parser'
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 1. 优先在 pager 容器内查找
        pager = soup.find('div', class_='pager')
        links = pager.find_all('a') if pager else soup.find_all('a')
        
        for link in links:
            text = link.get_text(strip=True)
            if '尾页' in text:
                href = link.get('href', '')
                # 正则匹配 index_数字.html
                match = re.search(r'index_(\d+)\.html', href)
                if match:
                    return int(match.group(1))
                # 备选匹配：如果链接中只有 index_数字 (不带.html)
                match = re.search(r'index_(\d+)', href)
                if match:
                    return int(match.group(1))
        
        # 2. 如果没找到“尾页”，尝试找最后一个数字页码
        # 在 <div class="pager"> 中找数字
        if pager:
            page_numbers = []
            for a in pager.find_all('a'):
                if a.text.isdigit():
                    page_numbers.append(int(a.text))
            if page_numbers:
                return max(page_numbers)

    except Exception as e:
        print(f"❌ 获取最大页码失败: {type(e).__name__} - {str(e)[:50]}")
    
    return 1 # 默认返回第一页

# 请求头配置
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

# 基础URL配置
domain = "https://www.yszzq.com"
tag_path = "/tags/xmlcjjk/"
base_url = f"{domain}{tag_path}index.html"

# 1. 获取最大页码
print(f"🔍 正在从 {base_url} 分析分页信息...")
max_page = get_max_page_number(base_url, headers)
print(f"📊 探测到最大页数: {max_page}")

# 2. 生成所有分页 URL
# 第一页为 index.html，后续为 index_2.html, index_3.html ...
urls = [base_url]
if max_page > 1:
    urls += [f"{domain}{tag_path}index_{i}.html" for i in range(2, max_page + 1)]

print(f"🎯 待处理 URL 总数: {len(urls)}")

all_results = []

# 3. 循环爬取每一页
for index, url in enumerate(urls):
    try:
        if index > 0:
            time.sleep(1.2)  # 礼貌延时
            
        print(f"[{index + 1}/{len(urls)}] 正在抓取: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 匹配关键词：接口、地址、API、资源库等
        pattern = re.compile(r'接口|地址|API|资源|资源库|资源接口|资源网|json[\\u4e00-\\u9fa5]*', re.UNICODE)
        
        # 在 list_txt 容器内寻找符合条件的链接
        list_container = soup.find('div', class_='list_txt')
        target_elements = list_container.find_all(string=pattern) if list_container else soup.find_all(string=pattern)

        for element in target_elements:
            parent = element.find_parent('a')
            if not parent or 'href' not in parent.attrs:
                continue
                
            raw_href = parent['href']
            title = element.strip()
            
            # 构建完整的资源 URL (排除外链干扰)
            if raw_href.startswith(('http://', 'https://')):
                final_url = raw_href
            else:
                if not raw_href.startswith('/'):
                    raw_href = '/' + raw_href.lstrip('./')
                final_url = f"{domain}{raw_href}"

            # 过滤逻辑：包含关键词，且排除标题带 XML 的项
            valid_keywords = ["采集接口", "资源库", "资源接口", "采集API接口"]
            is_valid = any(kw in title for kw in valid_keywords) and "XML" not in title
            
            if is_valid:
                entry = f"{title},{final_url}"
                if entry not in all_results:
                    all_results.append(entry)
                    print(f"  ✅ 发现: {title[:20]}...")
                
    except Exception as e:
        print(f"  ❌ 出错 {url}: {type(e).__name__}")

# 4. 保存结果
with open('pq.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(all_results))

print(f"\n🎯 处理完成！共提取到 {len(all_results)} 条接口记录，已保存至 pq.txt")
