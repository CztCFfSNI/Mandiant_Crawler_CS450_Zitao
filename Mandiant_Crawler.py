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

def crawl_and_save_blog_content_with_data_cleaning(url, file_path):
    resp = requests.get(url)
    page_soup = BeautifulSoup(resp.content, 'html.parser')
    figures, codes, paragraphs, unique_set = page_soup.find_all('img'), page_soup.find_all(['pre', 'code']), page_soup.find_all(['p', 'span']), set()
    with open(file_path, 'w', encoding='utf-8') as file:
        if codes:
            file.write("CODES:\n")
            for code in codes:
                if code.get_text() not in unique_set:
                    file.write(f"{code.get_text()}\n")
                    unique_set.add(code.get_text())
            file.write("\n")

        if paragraphs:
            file.write("PARAGRAPHS:\n")
            for paragraph in paragraphs:
                paragraph_text = paragraph.get_text(strip=True)
                if paragraph_text not in unique_set:
                    unique_set.add(paragraph_text)
                    file.write(f"{paragraph_text}\n")
            file.write("\n")

        # if figures:
        #     file.write("FIGURES:\n")
        #     for figure in figures:
        #         alt_text = figure.get('alt', 'No alt text available')
        #         file.write(f"Figure: {alt_text}\n")
        #     file.write("\n")

# 594 blogs in total.
os.makedirs('mandiant_blogs', exist_ok=True)
index, page_number_start, page_number_end = 0, 0, 59

for page_number in range(page_number_start, page_number_end + 1):
    base_url = 'https://www.mandiant.com/resources/blog'
    page_url = f'{base_url}?page={page_number}'
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    blog_links = soup.find_all('a', class_='resources-card')

    for _, link in enumerate(blog_links, start=1):
        blog_url = urljoin(base_url, link['href'])
        blog_title = link.get_text(strip=True)
        file_name = f"mandiant_blog_{index}.txt".replace("/", "_").replace(" ", "_")
        file_path = os.path.join('mandiant_blogs', file_name)
        # crawl_and_save_blog_content(blog_url, file_path)
        crawl_and_save_blog_content_with_data_cleaning(blog_url, file_path)
        index += 1
