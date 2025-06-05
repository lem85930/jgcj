import requests
import re
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.yszzq.com/" 
}

with open('pq.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines() 

results = []

for line in lines:
    try:
        title, base_url = line.strip().split(',', 1)  # 只分割一次，避免名称中有逗号
        base_url = base_url.strip()
        found = False
        
        for _ in range(3):  # 重试 3 次 
            try:
                response = requests.get(base_url, headers=headers, timeout=15)
                if response.status_code == 200:
                    # 精准匹配 data-clipboard-text 属性中的 API 链接
                    match = re.search(
                        r"data-clipboard-text=['\"](https?://[^'\"]+?/api\.php[^'\"]*?)['\"]", 
                        response.text
                    )
                    
                    if match:
                        # 提取完整的 API 链接
                        api_url = match.group(1).strip()
                        
                        # 提取域名部分（/api.php 之前的内容）
                        domain_match = re.search(r'(https?://[^/]+)/api\.php', api_url)
                        if domain_match:
                            domain = domain_match.group(1)
                        else:
                            domain = api_url.split('/api.php')[0]
                        
                        # 构建新链接
                        new_url = f"{domain}/api.php/provide/vod/at/xml/"
                        results.append(f"{title},{new_url}")
                        found = True
                        print(f"成功提取：{title} -> {new_url}")
                        break  # 获取到链接即终止重试
                    else:
                        print(f"未找到 data-clipboard-text 中的 API 链接，URL：{base_url}")
                        # 尝试备用方案：直接查找包含 /api.php 的链接
                        backup_match = re.search(
                            r'["\'](https?://[^"\']+?/api\.php[^"\']*?)["\']', 
                            response.text
                        )
                        if backup_match:
                            api_url = backup_match.group(1).strip()
                            domain = api_url.split('/api.php')[0]
                            new_url = f"{domain}/api.php/provide/vod/at/xml/"
                            results.append(f"{title},{new_url}")
                            found = True
                            print(f"备用方案提取：{title} -> {new_url}")
                            break
                        else:
                            print(f"也未找到备用链接，URL：{base_url}")
                            break
                else:
                    print(f"请求失败，状态码：{response.status_code}，URL：{base_url}")
            except Exception as e:
                print(f"请求异常：{str(e)}，URL：{base_url}")
            time.sleep(1)   # 每次请求间隔 1 秒 
        
        # 移除未找到有效链接时的输出
        # 原代码：if not found: results.append(f"{title},未找到有效链接")
            
    except ValueError:
        print(f"格式错误行：{line}")
        # 格式错误行也不输出
        # 原代码：results.append(f"{line.strip()},格式错误")

with open('maqu.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(results))
