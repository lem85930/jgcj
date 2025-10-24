import requests
import re
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.yszzq.com/"
}

# 读取待采集列表
with open('pq.txt', 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]

results = []

for line in lines:
    try:
        title, base_url = line.split(',', 1)          # 只切一次，防止名称里带逗号
    except ValueError:
        # 格式不对直接跳过
        continue

    base_url = base_url.strip()
    api_link = None

    # 重试 3 次
    for _ in range(3):
        try:
            resp = requests.get(base_url, headers=headers, timeout=15)
            if resp.status_code != 200:
                continue

            # 提取包含 /api.php/ 的完整 URL（末尾必须有斜杠）
            # 正则里用非贪婪，防止跨行
            m = re.search(
                r'(https?://[^\'"\s]+/api\.php/[^\'"\s]*)',
                resp.text,
                flags=re.I
            )
            if m:
                api_link = m.group(1).strip()
                break          # 拿到就跳出重试
        except Exception as e:
            # 网络异常等，继续重试
            pass
        time.sleep(1)

    if api_link:
        # 取域名部分
        domain = api_link.split('/api.php')[0]
        new_url = f"{domain}/api.php/provide/vod/at/xml/"
        results.append(f"{title},{new_url}")
        print(f"成功提取：{title} -> {new_url}")
    # 未提取到的不写入，保持沉默

# 保存结果
with open('maqu.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))
