import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin

# -------------------------- 反爬配置 --------------------------
# 模拟浏览器请求头，避免被爬虫检测识别
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.yszzq.com/",  # 模拟站内跳转
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

# 基础URL配置
BASE_URL = "https://www.yszzq.com/ziyuan/api/"
HOME_PAGE = f"{BASE_URL}index.html"
OUTPUT_FILE = "pq.txt"

def get_last_page_number():
    """获取尾页数字：访问首页解析尾页链接中的数字"""
    try:
        # 发送请求，添加超时和重试机制
        response = requests.get(HOME_PAGE, headers=HEADERS, timeout=10)
        response.encoding = response.apparent_encoding  # 自动识别编码
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 查找尾页链接（通常尾页按钮的a标签包含"尾页"文字）
        last_page_link = soup.find("a", string="尾页")
        if not last_page_link:
            print("未找到尾页按钮，默认尾页为1")
            return 1
        
        # 提取尾页链接中的数字（如index_10.html中的10）
        href = last_page_link.get("href", "")
        match = re.search(r"index_(\d+)\.html", href)
        if match:
            last_page = int(match.group(1))
            print(f"识别到尾页数字：{last_page}")
            return last_page
        else:
            print("尾页链接格式异常，默认尾页为1")
            return 1
    except Exception as e:
        print(f"获取尾页数字失败：{e}")
        return 1

def get_page_url(page_num):
    """根据页码生成页面URL（首页是index.html，其他是index_数字.html）"""
    if page_num == 1:
        return HOME_PAGE
    return f"{BASE_URL}index_{page_num}.html"

def parse_page(page_url):
    """解析单个页面，提取符合条件的接口名称和URL"""
    result = []
    try:
        # 延时1秒，避免请求过快触发反爬
        time.sleep(1)
        response = requests.get(page_url, headers=HEADERS, timeout=10)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 查找所有a标签，筛选包含指定关键词的接口名称
        keywords = ["采集接口", "接口大全", "规则地址", "接口地址"]
        a_tags = soup.find_all("a")
        for a in a_tags:
            text = a.get_text(strip=True)
            href = a.get("href", "")
            
            # 过滤条件：包含关键词 + 有有效链接
            if any(keyword in text for keyword in keywords) and href:
                # 拼接完整URL（处理相对路径）
                full_url = urljoin(BASE_URL, href)
                result.append((text, full_url))
                print(f"提取到：{text} -> {full_url}")
        
        return result
    except Exception as e:
        print(f"解析页面 {page_url} 失败：{e}")
        return []

def main():
    """主流程：获取尾页 -> 遍历所有页面 -> 提取数据 -> 写入文件"""
    # 1. 获取尾页数字
    last_page = get_last_page_number()
    
    # 2. 遍历所有页面，收集数据（去重）
    all_data = []
    seen = set()  # 用于去重（接口名称+URL）
    for page_num in range(1, last_page + 1):
        print(f"\n正在处理第 {page_num}/{last_page} 页")
        page_url = get_page_url(page_num)
        page_data = parse_page(page_url)
        
        # 去重后添加
        for text, url in page_data:
            key = (text, url)
            if key not in seen:
                seen.add(key)
                all_data.append((text, url))
    
    # 3. 写入pq.txt文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for text, url in all_data:
            # 按要求格式写入：接口名称,url
            f.write(f"{text},{url}\n")
    
    print(f"\n任务完成！共提取 {len(all_data)} 条有效数据，已写入 {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
