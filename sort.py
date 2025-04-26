def sort_urls(input_file, output_file):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            urls = f.readlines()
        
        urls = [url.strip() for url in urls if url.strip()]
        
        urls = list(set(urls))  
        urls.sort()         


        with open(output_file, "w", encoding="utf-8") as f:
            for url in urls:
                f.write(url + "\n")

        print(f"Đã sắp xếp {len(urls)} URL và lưu vào {output_file}")
    except FileNotFoundError:
        print(f"Không tìm thấy file {input_file}")

if __name__ == "__main__":
    input_file = "url.txt"
    output_file = "url2.txt"
    sort_urls(input_file, output_file)
