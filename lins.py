import requests 
import re 
import os 
from urllib.parse  import urlparse 
from time import sleep 
 
# 增强请求头配置 
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://www.yszzq.com/' 
}
 
TIMEOUT = 20 
MAX_RETRY = 3 
 
# 修正后的正则表达式 
URL_PATTERN = re.compile( 
    r'https?:\/\/(?:[a-zA-Z0-9\-\.]+\.)*yszzq\.com[\w\/\-\.%]+at\/xml(?:\?[\w=&]*)?',
    re.IGNORECASE 
)
 
def add_proxy_prefix(url):
    """动态代理路径转换"""
    parsed = urlparse(url)
    if 'yszzq.com'  in parsed.netloc: 
        new_path = f"/wztz/https/{parsed.netloc}{parsed.path}" 
        return parsed._replace(
            scheme="https",
            netloc="cfpgwztz.wofuck.rr.nu", 
            path=new_path 
        ).geturl()
    return url 
 
if not os.path.exists('pq.txt'): 
    raise FileNotFoundError("pq.txt  文件未找到")
 
results = []
 
with open('pq.txt',  'r', encoding='utf-8') as file:
    lines = [line.strip() for line in file if line.strip()] 
 
for line in lines:
    try:
        title, url = line.split(',',  1)
        parsed = urlparse(url)
        
        if not all([parsed.scheme, parsed.netloc]): 
            print(f"🚫 无效URL: {url}")
            continue 
 
        success = False 
        for retry in range(MAX_RETRY):
            try:
                resp = requests.get(url,  headers=HEADERS, 
                                  timeout=TIMEOUT + retry*3)
                
                # 处理特殊反爬机制 
                if resp.status_code  == 403:
                    print(f"⏳ 触发反爬 [{url}] 第{retry+1}次重试...")
                    sleep(2 ** retry)
                    continue 
                
                resp.raise_for_status() 
                success = True 
                break 
                
            except requests.exceptions.RequestException  as e:
                print(f"⚠️ 请求异常: {type(e).__name__} - {str(e)[:50]}")
 
        if not success:
            continue 
 
        # 增强型匹配 
        if matches := URL_PATTERN.findall(resp.text): 
            for match in matches:
                final_url = add_proxy_prefix(match)
                results.append(f"{title},{final_url}") 
                print(f"✅ 匹配成功: {title[:15]}... -> {final_url[:60]}...")
 
    except Exception as e:
        print(f"❌ 处理异常: {str(e)[:50]}")
 
if results:
    with open('maqu.txt',  'w', encoding='utf-8') as f:
        f.write('\n'.join(results)) 
    print(f"🎯 成功写入 {len(results)} 条记录")
else:
    print("⚠️ 无有效数据输出，建议检查：\n1. 源文件内容格式\n2. 网络请求成功率\n3. 正则匹配模式")
