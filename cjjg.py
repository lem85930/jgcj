import requests
from bs4 import BeautifulSoup

def scrape_xml_cjjk():
    url = "https://www.yszzq.com/tags/xmlcjjk/"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('h2', class_='entry-title')
        
        with open('pq.txt', 'w', encoding='utf-8') as file:
            for result in results:
                title = result.get_text().strip()
                link = result.a['href']
                file.write(f"{title},{link}\n")
        
        print("Titles and links successfully scraped and saved in pq.txt.")
    else:
        print("Failed to fetch data from the website.")

if __name__ == '__main__':
    scrape_xml_cjjk()
