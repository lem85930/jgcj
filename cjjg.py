import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_google_results(keyword):
    url = f"https://www.google.com/search?q={keyword}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='tF2Cxc')
        return results
    else:
        print("Failed to fetch Google search results.")
        return None

def extract_api_info(results):
    api_data = []
    for idx, result in enumerate(results, start=1):
        title = result.find('h3').get_text()
        link = result.find('a')['href']
        api_data.append({'序号': f'cjy{idx:02}', 'api名称': title, 'api链接': link})
    return api_data

def create_csv(api_data):
    df = pd.DataFrame(api_data)
    df.to_csv('cj.csv', index=False)

if __name__ == '__main__':
    keyword = 'at/xml 采集 帮助'
    results = get_google_results(keyword)
    
    if results:
        api_data = extract_api_info(results)
        create_csv(api_data)
        print("Table successfully created and saved as cj.csv.")
