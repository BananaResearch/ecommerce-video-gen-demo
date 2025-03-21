import os
import requests
from bs4 import BeautifulSoup

from wechat_assistant.coze_crawler.coze_urls import coze_urls

os.makedirs('output/cozecrawler', exist_ok=True)


def crawl_coze_url(url: str):
    response = requests.get(url) 
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        doc_container = soup.find('div', id='doc-container')
        
        doc_title_ele = doc_container.find('div', class_='title')
        print(doc_title_ele.text)



def main():
    for url in coze_urls:
        crawl_coze_url(url)
        print(url)


if __name__ == '__main__':
    main()
