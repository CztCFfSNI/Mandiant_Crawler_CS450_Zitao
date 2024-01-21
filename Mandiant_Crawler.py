import requests
from bs4 import BeautifulSoup

def crawl_and_save(url, file_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    article_content = soup.find('div', class_='resource-body').find_all(['p', 'h1', 'h2', 'h3', 'li']) 

    with open(file_name, 'w', encoding='utf-8') as file:
        for paragraph in article_content:
            file.write(paragraph.get_text())
            file.write('\n')
    
    print(f"Content saved to {file_name}")

url = 'https://www.mandiant.com/resources/blog/chinese-vmware-exploitation-since-2021'
file_name = 'mandiant_article.txt'
crawl_and_save(url, file_name)
