import os
import re

def remove_footer_from_news_pages():
    # 新闻目录路径
    news_dir = 'news'
    
    # 获取所有新闻HTML文件（排除备份文件）
    news_files = [f for f in os.listdir(news_dir) if f.endswith('.html') and not f.endswith('.backup')]
    
    # 需要保留的脚本引用
    news_navigation_script = '<script src="../js/news-navigation.js"></script>'
    
    # 页脚开始标记
    footer_start = '<!-- 页脚 -->'
    footer_end = '</footer>'
    
    # 需要添加的初始化代码
    init_code = '''            // 初始化新闻导航（上一页/下一页）
            if (typeof initializeNewsNavigation === 'function') {
                initializeNewsNavigation();
            }'''
    
    for news_file in news_files:
        file_path = os.path.join(news_dir, news_file)
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经处理过（避免重复处理）
        if 'initializeNewsNavigation' in content and '<!-- 页脚 -->' not in content:
            print(f"Skipping {news_file} - already processed")
            continue
        
        # 确保news-navigation.js脚本引用存在
        if 'news-navigation.js' not in content:
            # 查找news-counter.js引用位置
            if 'news-counter.js' in content:
                # 在news-counter.js后面添加news-navigation.js引用
                content = content.replace(
                    '<script src="../js/news-counter.js"></script>',
                    '<script src="../js/news-counter.js"></script>\n<script src="../js/news-navigation.js"></script>'
                )
            else:
                print(f"Warning: Could not find news-counter.js reference in {news_file}")
        
        # 查找并移除页脚
        if footer_start in content and footer_end in content:
            # 找到页脚开始和结束位置
            footer_start_index = content.find(footer_start)
            footer_end_index = content.find(footer_end, footer_start_index) + len(footer_end)
            
            # 移除页脚部分
            content = content[:footer_start_index] + content[footer_end_index:]
            
            # 查找在</script>标签前添加初始化代码的位置
            script_end_pattern = r'(</script>\s*<script>\s*//\s*页面加载时自动记录一次点击.*?document\.addEventListener\([^}]+\}\);)'
            match = re.search(script_end_pattern, content, re.DOTALL)
            
            if match:
                # 在匹配的脚本结束前插入初始化代码
                replacement = match.group(1).replace(
                    '});',
                    f'{init_code}\n        }});'
                )
                content = content.replace(match.group(1), replacement)
            else:
                print(f"Warning: Could not find script initialization section in {news_file}")
        
        # 写入修改后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Processed {news_file}")
    
    print("All news pages processed successfully!")

if __name__ == "__main__":
    remove_footer_from_news_pages()