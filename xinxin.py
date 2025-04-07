import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

def extract_interface_links(url, keywords):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        
        # 发送HTTP请求
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = response.apparent_encoding  # 自动检测编码
        
        if response.status_code != 200:
            print(f"请求失败，状态码：{response.status_code}")
            return []

        # 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找包含关键词的链接
        results = []
        for link in soup.find_all('a'):
            text = link.get_text(strip=True)
            href = link.get('href')
            
            if any(keyword in text for keyword in keywords):
                # 处理相对路径
                full_url = urljoin(url, href)
                results.append((text, full_url))
        
        return results

    except Exception as e:
        print(f"发生错误：{str(e)}")
        return []

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['接口名称', '接口地址'])
        writer.writerows(data)
    print(f"数据已保存到 {filename}")

if __name__ == "__main__":
    target_url = "https://cfpgwztz.wofuck.rr.nu/wztz/https/www.yszzq.com/tags/xmlcjjk/"
    search_keywords = ["采集接口", "API", "数据接口"]  # 可根据需要添加关键词
    output_file = "interface_links.csv"

    # 执行采集
    interface_links = extract_interface_links(target_url, search_keywords)
    
    if interface_links:
        # 保存结果
        save_to_csv(interface_links, output_file)
    else:
        print("未找到符合要求的接口链接")

# 注意事项：
# 1. 请确保遵守目标网站的robots.txt协议
# 2. 适当调整请求头信息（User-Agent）
# 3. 如果遇到反爬机制，需要添加代理或请求间隔
# 4. 根据实际网页结构调整解析逻辑
