import requests
from requests_html import HTMLSession  # 网页2提到的动态内容处理库
from urllib.parse import urlparse, urlunparse, urljoin
import re
import time
import random

# 代理配置（网页5的请求头优化）
PROXY_HOST = "cfpgwztz.wofuck.rr.nu"
TARGET_DOMAIN = "www.yszzq.com"

def build_proxy_url(original_url):
    """动态路径构建（网页3的路径处理改进）"""
    parsed = urlparse(original_url)
    if parsed.netloc == TARGET_DOMAIN:
        return urlunparse((
            parsed.scheme,
            PROXY_HOST,
            f"/wztz/https/{parsed.netloc}{parsed.path}",  # 修复路径层级
            parsed.params,
            parsed.query,
            parsed.fragment
        ))
    return original_url

# 增强型请求头（网页5的反爬策略）
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': f'https://{PROXY_HOST}/',
    'X-Forwarded-Proto': 'https'
}

# 动态内容匹配模式（网页7的关键词扩展）
INTERFACE_PATTERN = re.compile(
    r'(采集(接口|API)|资源(库|网)|json|小鸡资源)[\u4e00-\u9fa5]*(接口|API|地址)',
    re.IGNORECASE | re.UNICODE
)

session = HTMLSession()  # 网页2的动态会话管理

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
]

all_results = []

for index, url in enumerate(urls):
    try:
        # 智能请求间隔（网页6的反爬策略）
        if index > 0:
            time.sleep(1.5 + random.uniform(0, 2))

        # 动态渲染页面（网页2的核心方法）
        response = session.get(url, headers=headers)
        response.html.render(sleep=2)  # 执行JavaScript渲染
        
        # 多层级元素遍历（网页7的嵌套结构处理）
        for element in response.html.find('a', containing=INTERFACE_PATTERN):
            raw_href = element.attrs.get('href')
            title = element.text.strip()
            
            # 动态路径处理（网页3的改进点）
            if raw_href.startswith(('http://', 'https://')):
                final_url = build_proxy_url(raw_href)
            else:
                # 使用urljoin处理相对路径（网页4的改进）
                final_url = urljoin(response.url, raw_href)
            
            # 结果验证
            if "/ziyuan/api/" in final_url and "XML" not in title:
                all_results.append(f"{title},{final_url}")
                print(f"✅ 捕获接口：{title[:20]}... -> {final_url[:50]}...")

    except Exception as e:
        print(f"❌ 错误：{url} -> {type(e).__name__}:{str(e)[:50]}")

# 保存结果（保持原有文件写入逻辑）
