import requests
from bs4 import BeautifulSoup
import html2text

# URL bài viết cần crawl
url = "https://tuyensinh.uet.vnu.edu.vn/ban-nen-biet/thong-bao-xet-tuyen-thang-uu-tien-xet-tuyen-xet-tuyen-theo-hsa-sat-va-thu-nhan-chung-chi-tieng-anh-quoc-te-de-quy-doi-cong-diem-trong-xet-tuyen-vao-dai-hoc-chinh-quy-nam-2025-tai-truong-dai-hoc-con/"

# Gửi request đến trang
response = requests.get(url)
response.encoding = 'utf-8'  # đảm bảo tiếng Việt không bị lỗi

# Phân tích HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Tìm phần nội dung chính của bài viết (class có thể khác nếu thay đổi giao diện)
main_content = soup.find("div", class_="page")

# Kiểm tra và chuyển sang Markdown
if main_content:
    markdown_text = html2text.html2text(str(main_content))
    
    # Lưu ra file
    with open("uet_tuyensinh_2025.md", "w", encoding="utf-8") as f:
        f.write(markdown_text)
    
    print("✅ Đã lưu nội dung thành công vào uet_tuyensinh_2025.md")
else:
    print("❌ Không tìm thấy nội dung chính trong trang.")
