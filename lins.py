import requests 
import re 
import os 
from urllib.parse  import urlparse  # 新增路径验证模块 
from time import sleep  # 新增延时模块 
 
# 配置请求参数 
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate'
}
TIMEOUT = 15  # 超时时间延长至15秒 
MAX_RETRY = 2  # 失败重试次数 
 
# 增强型正则表达式（支持https/http及路径变化）
URL_PATTERN = re.compile(r'https?://(?:[a-zA-Z] |[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+at/xml')
 
# 新增文件存在性验证 
if not os.path.exists('pq.txt'): 
    raise FileNotFoundError("pq.txt  文件未找到，请先运行前序脚本")
 
results = []
 
with open('pq.txt',  'r', encoding='utf-8') as file:
    lines = [line.strip() for line in file if line.strip()]   # 过滤空行 
 
for line in lines:
    try:
        title, url = line.split(',',  1)  # 限定分割次数 
        
        # 新增URL有效性验证 
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]): 
            print(f"无效URL跳过: {url}")
            continue 
 
        # 带重试机制的请求 
        for _ in range(MAX_RETRY):
            try:
                resp = requests.get(url,  headers=HEADERS, timeout=TIMEOUT)
                if resp.status_code  == 403:
                    print(f"触发反爬机制: {url}")
                    sleep(5)  # 反爬延时 
                    continue 
                resp.raise_for_status() 
                break 
            except requests.exceptions.RequestException  as e:
                print(f"请求失败: {url} - {str(e)}")
                sleep(2)
        else:
            continue  # 重试失败后跳过 
 
        # 增强匹配逻辑 
        if matches := URL_PATTERN.findall(resp.text): 
            for match in matches:
                # 标准化URL输出 
                clean_url = match.replace('\\/',  '/').strip()
                results.append(f"{title},{clean_url}") 
                print(f"成功匹配: {title} -> {clean_url}")
 
    except ValueError:
        print(f"格式错误行: {line}")
    except Exception as e:
        print(f"处理异常: {str(e)}")
 
# 结果写入优化 
if results:
    with open('maqu.txt',  'w', encoding='utf-8') as f:
        f.write('\n'.join(results)) 
    print(f"成功写入 {len(results)} 条记录")
else:
    print("无有效数据可写入")
 
# 文件清理建议（按需启用）
# if os.path.exists('pq.txt'): 
#     os.remove('pq.txt') 
#     print('临时文件已清理')
