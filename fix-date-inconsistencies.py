#!/usr/bin/env python3
"""
修复新闻页面日期不一致的脚本
以新闻栏的日期为准，更新新闻页面的日期
"""

import os
import re
from bs4 import BeautifulSoup

# 新闻栏日期信息（从index.html中提取）
news_bar_dates = {
    "gta6-further-delay-2026.html": "September 18, 2025",
    "gta6-largest-launch.html": "September 17, 2025",
    "gta6-advanced-destruction.html": "September 16, 2025",
    "gta6-delay-2026.html": "September 15, 2025",
    "gta6-dual-protagonists.html": "September 14, 2025",
    "gta6-online-100players.html": "September 13, 2025",
    "gta6-vice-city-return.html": "September 12, 2025",
    "gta6-graphics-leak.html": "September 11, 2025",
    "gta6-preorder-bonus.html": "September 10, 2025"
}

def update_news_page_date(file_path, expected_date):
    """更新新闻页面的日期信息"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找并替换日期
        # 模式1: <i class="fa fa-calendar mr-2"></i> September 17, 2025
        pattern1 = r'(<i class="fa fa-calendar mr-2"></i>\s*)[A-Za-z]+\s+\d{1,2},\s+\d{4}'
        content = re.sub(pattern1, f'\g<1>{expected_date}', content)
        
        # 模式2: 包含日期的meta标签
        pattern2 = r'(<meta property="article:published_time" content=")[^"]([^"]*)(")'
        # 这里需要更复杂的处理，暂时不处理meta标签
        
        # 模式3: 其他可能的日期格式
        pattern3 = r'(Published|Posted|Date):?\s*[A-Za-z]+\s+\d{1,2},\s+\d{4}'
        content = re.sub(pattern3, f'\g<1>: {expected_date}', content, flags=re.IGNORECASE)
        
        # 写入更新后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"更新 {file_path} 时出错: {str(e)}")
        return False

def fix_date_inconsistencies():
    """修复所有新闻页面的日期不一致"""
    news_dir = os.path.join(os.getcwd(), 'news')
    
    print("=" * 80)
    print("修复新闻页面日期不一致")
    print("=" * 80)
    
    fixed_count = 0
    error_count = 0
    
    for filename, expected_date in news_bar_dates.items():
        file_path = os.path.join(news_dir, filename)
        
        if os.path.exists(file_path):
            print(f"正在修复 {filename}...")
            
            if update_news_page_date(file_path, expected_date):
                print(f"  ✓ 已更新为: {expected_date}")
                fixed_count += 1
            else:
                print(f"  ✗ 修复失败")
                error_count += 1
        else:
            print(f"{filename} 文件不存在，跳过")
    
    print("=" * 80)
    print(f"修复完成: {fixed_count} 个文件已修复, {error_count} 个文件出错")
    
    if fixed_count > 0:
        print("\n验证修复结果:")
        os.system("python check-date-consistency.py")

if __name__ == "__main__":
    fix_date_inconsistencies()