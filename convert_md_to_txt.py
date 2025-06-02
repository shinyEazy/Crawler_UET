import re

def markdown_to_text(md_content):
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', md_content)
    # Remove inline code
    text = re.sub(r'`([^`]*)`', r'\1', text)
    # Remove images ![alt](url)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Remove links but keep text [text](url)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    # Remove headings ##, ###, etc.
    text = re.sub(r'#+ ', '', text)
    # Remove bold and italic
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    # Remove blockquotes
    text = re.sub(r'^> ?', '', text, flags=re.MULTILINE)
    # Remove unordered list markers
    text = re.sub(r'^[-*+] ', '', text, flags=re.MULTILINE)
    # Remove ordered list markers
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)
    return text.strip()

# Usage
with open("data/uet_tuyensinh_2025.md", "r", encoding="utf-8") as md_file:
    md_content = md_file.read()

plain_text = markdown_to_text(md_content)

with open("output.txt", "w", encoding="utf-8") as txt_file:
    txt_file.write(plain_text)
