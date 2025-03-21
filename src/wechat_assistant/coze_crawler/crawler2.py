import os
from slugify import slugify
from playwright.sync_api import sync_playwright
from wechat_assistant.coze_crawler.coze_urls import coze_urls

dir_path = 'output/cozecrawler'

os.makedirs(dir_path, exist_ok=True)


def crawl_coze_url(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(3000)
        # 使用CSS选择器获取元素的文本
        doc_container_elem = page.query_selector('#doc-container')
        doc_title_elem = doc_container_elem.query_selector('div.title')
        title = doc_title_elem.inner_text()

        zone_container_ele = doc_container_elem.query_selector(
            '.zone-container')
        line_elems = zone_container_ele.query_selector_all('div.ace-line')

        content_lines = []

        for line_elem in line_elems:
            content_lines.append(line_elem.inner_text().strip().strip(
                '\u200b').strip().strip('\u200b').strip().strip('\u200b'))

        filtered_content_lines = list(filter(None, content_lines))
        content = '\n'.join(filtered_content_lines)

        browser.close()
        print(f'element_text: {title}')
        print('content_lines: ', filtered_content_lines)
        print('content: ', content)

        file_content = title + '\n' + content
        file_name = slugify(f'{title}.txt', allow_unicode=True)
        file_path = os.path.join(dir_path, file_name)

        with open(file_path, 'w+', encoding='utf-8') as file:
            file.write(file_content)

        return title
    pass


def main():
    error_urls = []
    for url in coze_urls:
        try:
            crawl_coze_url(url)
            print(f'success: {url}')
        except:
            error_urls.append(url)
            print(f'error: {url}')

    print('all error urls \n')
    print(error_urls)


if __name__ == '__main__':
    main()
