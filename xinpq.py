import requests 
from bs4 import BeautifulSoup 
from urllib.parse  import urlparse, urlunparse 
import re 
import time 
 
# 代理网关路径常量（核心修复点）
PROXY_PATH = "/wztz/https/www.yszzq.com" 
 
def build_proxy_url(original_url):
    """重构URL构建逻辑（关键修复函数）"""
    parsed = urlparse(original_url)
    if parsed.netloc  == "www.yszzq.com": 
        # 构造完整代理路径：原始路径插入到代理网关路径后 
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
 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'X-Forwarded-Proto': 'https'  # 新增协议头 
}
 
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
 
all_results = []
 
for index, url in enumerate(urls):
    try:
        # 智能请求间隔（避免触发反爬）
        if index > 0:
            time.sleep(1.5) 
            
        response = requests.get(url,  headers=headers, timeout=15)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text,  'lxml')
        pattern = re.compile(r' 接口|地址|API|资源|资源库|资源接口|资源网|json[\u4e00-\u9fa5]*', re.UNICODE)
        
        for element in soup.find_all(string=pattern): 
            parent = element.find_parent('a') 
            if not parent or 'href' not in parent.attrs: 
                continue 
                
            raw_href = parent['href']
            title = element.strip() 
            
            # 路径处理流程（核心修复）
            if raw_href.startswith(('http://',  'https://')):
                final_url = build_proxy_url(raw_href)
            else:
                # 相对路径处理 
                if not raw_href.startswith('/'): 
                    raw_href = '/' + raw_href.lstrip('./') 
                final_url = f"https://wztz.wokaotianshi.eu.org{PROXY_PATH}{raw_href}" 
 
            # 验证示例格式 
            if "/ziyuan/api/" in final_url:
                print(f"Debug - Generated URL: {final_url}")
                
            if ("采集接口" in title or "资源库" in title or "资源接口" in title or "采集API接口" in title ) \
            and "XML" not in title:
                all_results.append(f"{title},{final_url}") 
                print(f"✅ Valid: {title[:15]}... -> {final_url[:50]}...")
 
    except Exception as e:
        print(f"❌ Error on {url}: {type(e).__name__} - {str(e)[:50]}")
 
# 文件写入 
with open('pq.txt',  'w', encoding='utf-8') as f:
    f.write('\n'.join(all_results)) 
print(f"🎯 结果已保存：共{len(all_results)}条有效记录")
