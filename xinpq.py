import requests
from bs4 import BeautifulSoup
import re
import time

def get_max_page_number(base_url, headers):
    """
    根据提供的 HTML 结构获取最大页码
    逻辑：查找带有“尾页”文本的 <a> 标签，并提取 href 中 index_(d+).html 的数字
    """
    try:
        response = requests.get(base_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 定位分页器部分
        pager = soup.find('div', class_='pager')
        if not pager:
            print("⚠️ 未找到分页器 div (class='pager')")
            return 1
            
        last_page_link = pager.find('a', string='尾页')
        if last_page_link and 'href' in last_page_link.attrs:
            href = last_page_link['href']
            # 从 'index_12.html' 这种格式中提取数字 12
            match = re.search(r'index_(d+).html', href)
            if match:
                return int(match.group(1))
    except Exception as e:
        print(f"❌ 获取最大页码失败: {type(e).__name__} - {str(e)[:50]}")
    return 1

# 请求头配置
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

# 基础URL配置
domain = "https://www.yszzq.com"
tag_path = "/tags/xmlcjjk/"
base_url = f"{domain}{tag_path}index.html"

# 1. 获取最大页码
max_page = get_max_page_number(base_url, headers)
print(f"📊 探测到最大页数: {max_page}")

# 2. 生成所有分页 URL
# 第一页固定为 index.html
urls = [base_url]
# 从第二页开始为 index_2.html, index_3.html ...
if max_page > 1:
    urls += [f"{domain}{tag_path}index_{i}.html" for i in range(2, max_page + 1)]

print(f"🎯 待处理 URL 总数: {len(urls)}")

all_results = []

# 3. 循环爬取每一页
for index, url in enumerate(urls):
    try:
        if index > 0:
            time.sleep(1.2)  # 避免请求过快
            
        print(f"[{index + 1}/{len(urls)}] 正在抓取: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 匹配关键词：接口、地址、API、资源库等
        pattern = re.compile(r'接口|地址|API|资源|资源库|资源接口|资源网|json[\u4e00-\u9fa5]*', re.UNICODE)
        
        # 在页面中寻找符合条件的文本
        for element in soup.find_all(string=pattern):
            # 找到文本所在的 <a> 标签
            parent = element.find_parent('a')
            if not parent or 'href' not in parent.attrs:
                continue
                
            raw_href = parent['href']
            title = element.strip()
            
            # 构建完整的资源 URL
            if raw_href.startswith(('http://', 'https://')):
                final_url = raw_href
            else:
                if not raw_href.startswith('/'):
                    raw_href = '/' + raw_href.lstrip('./')
                final_url = f"{domain}{raw_href}"

            # 过滤逻辑：包含特定关键词 且 排除标题中带 XML 的项（按原逻辑）
            valid_keywords = ["采集接口", "资源库", "资源接口", "采集API接口"]
            is_valid = any(kw in title for kw in valid_keywords) and "XML" not in title
            
            if is_valid:
                entry = f"{title},{final_url}"
                if entry not in all_results:  # 去重
                    all_results.append(entry)
                    print(f"  ✅ 发现: {title[:15]}...")
                
    except Exception as e:
        print(f"  ❌ 出错 {url}: {type(e).__name__}")

# 4. 保存结果
with open('pq.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(all_results))

print(f"\n🎯 处理完成！共保存 {len(all_results)} 条记录到 pq.txt")
