import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl_and_save_blog_content(url, file_path):
    resp = requests.get(url)
    page_soup = BeautifulSoup(resp.content, 'html.parser')
    content = page_soup.find('div', class_='resource-body').get_text(separator='\n', strip=True)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

base_url = 'https://www.mandiant.com/resources/blog'
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')

blog_links = soup.find_all('a', class_='resources-card')

os.makedirs('mandiant_blogs', exist_ok=True)

for i, link in enumerate(blog_links, start=1):
    blog_url = urljoin(base_url, link['href'])
    blog_title = link.get_text(strip=True)
    file_name = f"mandiant_blog_{i}_{blog_title}.txt".replace("/", "_").replace(" ", "_")
    file_path = os.path.join('mandiant_blogs', file_name)
    crawl_and_save_blog_content(blog_url, file_path)
