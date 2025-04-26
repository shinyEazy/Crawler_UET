import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def crawl_internal_urls(base_url):
    try:
        response = requests.get(base_url, verify=False)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {base_url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    urls = set()
    base_domain = urlparse(base_url).netloc

    body_div = soup.find("div", id="body")
    if not body_div:
        print("Không tìm thấy <div id='body'> trong trang.")
        return []

    for link in body_div.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(base_url, href)
        parsed_url = urlparse(full_url)

        if parsed_url.netloc == base_domain:
            # 🚫 Bỏ qua các link chứa '/category/'
            if "/category/" not in parsed_url.path:
                urls.add(full_url)

    return urls

if __name__ == "__main__":
    url = f"https://uet.vnu.edu.vn/co-cau-to-chuc/"
    urls = crawl_internal_urls(url)
    if urls:
        print(f"Đã tìm thấy {len(urls)} URL trong trang {url}")
        with open("url.txt", "a", encoding="utf-8") as file:
            for url in urls:
                file.write(url + "\n")
    else:
        print(f"Không tìm thấy URL nào trong trang {url}")