import os
import re
from bs4 import BeautifulSoup
import shutil

# 模板文件路径
template_file = 'news-template.html'

# 新闻目录
news_dir = 'news'

# 需要处理的新闻文件列表
exclude_files = ['gta6-largest-launch.html', 'gta6-delay-2026.html']  # 已经处理过的文件

# 读取模板文件
with open(template_file, 'r', encoding='utf-8') as f:
    template_content = f.read()

template_soup = BeautifulSoup(template_content, 'html.parser')

def extract_news_content(html_content):
    """从现有新闻页面中提取新闻内容"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 提取标题
    title = soup.find('title')
    title_text = title.get_text() if title else "GTA 6 News - GTA6games.net"
    
    # 提取新闻标题
    news_title = soup.find('h1')
    news_title_text = news_title.get_text() if news_title else "GTA 6 News"
    
    # 提取副标题
    subtitle = soup.find('h2') or soup.find('p', class_=re.compile(r'subtitle|description'))
    subtitle_text = subtitle.get_text() if subtitle else "Latest news and updates"
    
    # 提取日期、阅读量等信息
    meta_info = soup.find('div', class_=re.compile(r'meta|info|date'))
    
    # 提取新闻正文内容
    content_div = soup.find('div', class_=re.compile(r'content|article|prose'))
    if not content_div:
        content_div = soup.find('main')
    
    # 提取统计数字区块
    stats_section = soup.find('div', class_=re.compile(r'stats|statistics|numbers'))
    
    return {
        'title': title_text,
        'news_title': news_title_text,
        'subtitle': subtitle_text,
        'meta_info': str(meta_info) if meta_info else None,
        'content': str(content_div) if content_div else None,
        'stats_section': str(stats_section) if stats_section else None
    }

def create_standardized_page(news_content, template_soup):
    """创建标准化的新闻页面"""
    # 创建新的soup对象
    new_soup = BeautifulSoup(str(template_soup), 'html.parser')
    
    # 更新页面标题
    title_tag = new_soup.find('title')
    if title_tag:
        title_tag.string = news_content['title']
    
    # 更新新闻标题
    h1_tag = new_soup.find('h1')
    if h1_tag and news_content['news_title']:
        h1_tag.string = news_content['news_title']
    
    # 更新副标题
    subtitle_tag = new_soup.find('p', class_=re.compile(r'text-2xl'))
    if subtitle_tag and news_content['subtitle']:
        subtitle_tag.string = news_content['subtitle']
    
    # 更新元信息
    meta_div = new_soup.find('div', class_=re.compile(r'flex items-center justify-center'))
    if meta_div and news_content['meta_info']:
        meta_soup = BeautifulSoup(news_content['meta_info'], 'html.parser')
        meta_div.replace_with(meta_soup)
    
    # 更新新闻内容
    content_div = new_soup.find('div', class_='prose')
    if content_div and news_content['content']:
        content_soup = BeautifulSoup(news_content['content'], 'html.parser')
        content_div.replace_with(content_soup)
    
    # 添加统计数字区块（如果有）
    if news_content['stats_section']:
        # 在新闻头部之后添加统计数字区块
        header_div = new_soup.find('div', class_='border-b')
        if header_div:
            stats_soup = BeautifulSoup(news_content['stats_section'], 'html.parser')
            header_div.insert_after(stats_soup)
    
    return str(new_soup)

def process_news_file(file_path):
    """处理单个新闻文件"""
    print(f"Processing: {file_path}")
    
    # 读取原始文件
    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # 提取新闻内容
    news_content = extract_news_content(original_content)
    
    # 创建标准化页面
    standardized_content = create_standardized_page(news_content, template_soup)
    
    # 备份原始文件
    backup_path = file_path + '.backup'
    shutil.copy2(file_path, backup_path)
    print(f"  Backup created: {backup_path}")
    
    # 写入标准化内容
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(standardized_content)
    
    print(f"  Standardized: {file_path}")

def main():
    print("Starting news layout standardization...")
    
    # 获取所有新闻文件
    news_files = []
    for file_name in os.listdir(news_dir):
        if file_name.endswith('.html') and file_name not in exclude_files:
            news_files.append(os.path.join(news_dir, file_name))
    
    print(f"Found {len(news_files)} news files to process:")
    for file_path in news_files:
        print(f"  - {os.path.basename(file_path)}")
    
    # 处理每个文件
    for file_path in news_files:
        try:
            process_news_file(file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print("\nStandardization complete!")
    print("Backup files have been created with .backup extension")

if __name__ == "__main__":
    main()