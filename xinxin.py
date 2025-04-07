import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, urljoin
import re
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 代理网关配置
PROXY_HOST = "cfpgwztz.wofuck.rr.nu"
PROXY_SCHEME = "https"
TARGET_DOMAIN = "www.yszzq.com"

def build_proxy_url(original_url):
    """动态构建代理URL（修复路径层级问题）"""
    parsed = urlparse(original_url)
    if parsed.netloc == TARGET_DOMAIN:
        # 保留原始路径结构（关键修复点）
        new_path = f"/wztz/https/{parsed.netloc}{parsed.path}"
        return urlunparse((
            PROXY_SCHEME,
            PROXY_HOST,
            new_path,
            parsed.params,
            parsed.query,
            parsed.fragment
        ))
    return original_url

# 增强型请求头（防反爬策略）
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://cfpgwztz.wofuck.rr.nu/',
    'X-Forwarded-Proto': 'https'
}

# 初始化Selenium（处理动态内容）
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # 无头模式
service = Service(executable_path='chromedriver')  # 需提前配置chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# 增强型正则匹配（网页5提到的关键词扩展）
INTERFACE_PATTERN = re.compile(
    r'(采集(接口|API)|资源(库|网)|json|小鸡资源)[\u4e00-\u9fa5]*(接口|API|地址)',
    re.IGNORECASE | re.UNICODE
)

urls = [
    "https://cfpgwztz.wofuck.rr.nu/wztz/https/www.yszzq.com/tags/xmlcjjk/",
    # 其他URL...
]

all_results = set()  # 使用集合避免重复

for index, url in enumerate(urls):
    try:
        # 智能请求间隔（网页5提到的反爬策略）
        if index > 0:
            time.sleep(1.5 + random.uniform(0, 2))

        # 使用Selenium获取动态内容（网页6/7/8的核心方法）
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # 多层级元素遍历（解决嵌套结构问题）
        for element in soup.find_all(string=INTERFACE_PATTERN):
            parent = element.find_parent(['a', 'div', 'li', 'span'])
            link = None
            if parent and parent.name == 'a':
                link = parent
            elif parent and parent.find('a'):
                link = parent.find('a')
            
            if link and 'href' in link.attrs:
                raw_href = link['href']
                title = element.strip()
                
                # 动态路径处理（关键修复点）
                if raw_href.startswith(('http://', 'https://')):
                    final_url = build_proxy_url(raw_href)
                else:
                    # 使用urljoin处理相对路径（网页2/3的改进点）
                    base_url = urlunparse((
                        PROXY_SCHEME,
                        PROXY_HOST,
                        urlparse(url).path, '', '', ''
                    ))
                    final_url = urljoin(base_url, raw_href)
                
                # 结果过滤与验证
                if any(keyword in title for keyword in ["采集接口", "资源库", "API接口"]):
                    all_results.add(f"{title},{final_url}")
                    print(f"✅ 捕获接口：{title[:20]}... -> {final_url[:50]}...")

    except Exception as e:
        print(f"❌ 错误：{url} -> {type(e).__name__}:{str(e)[:50]}")

# 关闭浏览器实例
driver.quit()

# 保存结果（网页1的数据存储方式）
with open('pq.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(all_results))
print(f"🎯 结果已保存：共{len(all_results)}条有效记录")
