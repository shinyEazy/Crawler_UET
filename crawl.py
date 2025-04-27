import requests
from bs4 import BeautifulSoup
import urllib3
import pandas as pd
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_time_meta(soup):
    meta_properties = [
        "og:updated_time",
        "article:modified_time",
        "article:published_time"
    ]
    for prop in meta_properties:
        meta_tag = soup.find("meta", property=prop)
        if meta_tag and meta_tag.get("content"):
            return meta_tag["content"]
    return None

def crawl_articles(base_url):
    try:
        response = requests.get(base_url, verify=False)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {base_url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    body_div = soup.find("div", id="body")
    if not body_div:
        print(f"Không tìm thấy <div id='body'> trong trang {base_url}.")
        return []

    articles = body_div.find_all("article")
    if not articles:
        print(f"Không tìm thấy thẻ <article> trong {base_url}.")
        return []

    records = []

    for article in articles:
        # Tìm content ở "single-post-content-text content-pad"
        content_div = article.find("div", class_="single-post-content-text content-pad")
        
        if not content_div:
            # Nếu không có, tìm ở "content-dropcap"
            content_div = article.find("div", class_="content-dropcap")

        if not content_div:
            continue

        content = content_div.get_text(separator="\n", strip=True)

        # Ưu tiên tìm title ở "single-content-title"
        title_tag = article.find(class_="single-content-title")
        if title_tag:
            title = title_tag.get_text(strip=True)
        else:
            # Nếu không có, tìm <a class="logo"> và lấy title attribute
            logo_tag = soup.find("a", class_="logo")
            if logo_tag and logo_tag.get("title"):
                title = logo_tag["title"]
            else:
                title = ""  # Nếu vẫn không có, để title rỗng

        time = get_time_meta(soup)

        records.append({
            "content": content,
            "title": title,
            "url": base_url,
            "time": time
        })

    return records

if __name__ == "__main__":
    input_file = "url.txt"
    output_file = "articles13.xlsx"

    if not os.path.exists(input_file):
        print(f"Không tìm thấy file {input_file}")
        exit(1)

    if os.path.exists(output_file):
        df_all = pd.read_excel(output_file)
    else:
        df_all = pd.DataFrame(columns=["content", "title", "url", "time"])

    with open(input_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    cnt = 1

    for url in urls:
        
        print(f"{cnt}. Đang xử lý {url} ...")
        records = crawl_articles(url)
        cnt += 1
        
        if records:
            df_new = pd.DataFrame(records)
            df_all = pd.concat([df_all, df_new], ignore_index=True)
            df_all.to_excel(output_file, index=False)
            print(f"Đã lưu {len(records)} bài viết từ {url}")
        else:
            print(f"Không có bài viết hợp lệ từ {url}")

    print(f"Đã hoàn thành! Tổng cộng: {len(df_all)} bài viết được lưu vào {output_file}")
