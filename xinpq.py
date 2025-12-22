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

# 优化请求头，增加更多兼容性配置
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'X-Forwarded-Proto': 'https',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
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

print(f"🎯 共生成 {len(urls)} 个URL: {urls}")

all_results = []

# 优化匹配规则：1. 去掉开头多余的空格 2. 增加匹配精度 3. 不区分大小写
target_pattern = re.compile(r'采集接口|资源库|资源接口|采集API接口', re.UNICODE | re.IGNORECASE)
# 辅助匹配：用于先筛选可能包含目标内容的a标签
pre_filter_pattern = re.compile(r'接口|地址|API|资源|资源库|资源接口|资源网|json', re.UNICODE | re.IGNORECASE)

for index, url in enumerate(urls):
    try:
        if index > 0:
            time.sleep(1.5)  # 增加延迟，避免被反爬
        print(f"\n🔍 正在处理第 {index+1} 页: {url}")
        
        # 直接请求代理URL（无需再转换）
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        # 强制设置编码为UTF-8，避免中文乱码导致匹配失败
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 关键修改1：先找到所有a标签（目标链接都在a标签里），再筛选包含目标关键词的
        all_a_tags = soup.find_all('a', href=True)  # 只找有href属性的a标签
        print(f"📌 本页找到 {len(all_a_tags)} 个带链接的a标签")
        
        matched_count = 0
        for a_tag in all_a_tags:
            # 获取a标签的所有文本内容（包括子节点）和title属性
            a_text = a_tag.get_text(strip=True)  # 去掉首尾空格
            a_title = a_tag.get('title', '').strip()  # 获取title属性
            combined_text = f"{a_text} {a_title}"  # 合并文本和title，扩大匹配范围
            
            # 先过滤：如果不包含基础关键词，直接跳过
            if not pre_filter_pattern.search(combined_text):
                continue
            
            # 核心匹配：检查是否包含目标关键词
            if target_pattern.search(combined_text):
                matched_count += 1
                raw_href = a_tag['href']
                # 确定最终标题（优先用title，没有则用文本）
                title = a_title if a_title else a_text
                
                # 处理链接，转换为代理URL
                if raw_href.startswith(('http://', 'https://')):
                    final_url = build_proxy_url(raw_href)
                else:
                    if not raw_href.startswith('/'):
                        raw_href = '/' + raw_href.lstrip('./')
                    final_url = f"https://wztz.wokaotianshi.eu.org{PROXY_PATH}{raw_href}"
                
                # 过滤掉包含XML的标题（可选，根据你的需求调整）
                if "XML" not in title:
                    result_item = f"{title},{final_url}"
                    all_results.append(result_item)
                    print(f"✅ 匹配到有效内容: {title[:30]}... -> {final_url[:60]}...")
                else:
                    print(f"⚠️ 匹配到但包含XML，已过滤: {title[:30]}...")
        
        print(f"📊 本页匹配到 {matched_count} 个包含目标关键词的a标签")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求第 {index+1} 页失败: {type(e).__name__} - {str(e)[:50]}")
    except Exception as e:
        print(f"❌ 处理第 {index+1} 页异常: {type(e).__name__} - {str(e)[:50]}")

# 关键修改2：确保无论是否有结果，都生成pq.txt文件
try:
    with open('pq.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_results))
    print(f"\n🎯 结果已保存到 pq.txt：共 {len(all_results)} 条有效记录")
    # 如果没有结果，提示可能的原因
    if len(all_results) == 0:
        print("⚠️ 未生成任何有效记录，可能原因：1. 页面无匹配内容 2. 匹配规则需调整 3. 网络/代理问题")
except Exception as e:
    print(f"❌ 写入pq.txt失败: {type(e).__name__} - {str(e)[:50]}")
