#!/usr/bin/env python3
"""
检查新闻栏日期与新闻页日期一致性的脚本
以新闻栏的日期为准，检查新闻页面的日期是否匹配
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

def extract_news_page_date(file_path):
    """从新闻页面提取日期信息"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 查找包含日期的元素
        date_patterns = [
            r'(?:Published|Posted|Date):?\s*([A-Za-z]+\s+\d{1,2},\s+\d{4})',
            r'<span[^>]*class=["\'][^"\']*date[^"\']*["\'][^>]*>([A-Za-z]+\s+\d{1,2},\s+\d{4})',
            r'<time[^>]*>([A-Za-z]+\s+\d{1,2},\s+\d{4})',
            r'<i class="fa fa-calendar[^>]*></i>\s*([A-Za-z]+\s+\d{1,2},\s+\d{4})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)
        
        # 如果正则匹配失败，尝试查找包含日期的元素
        date_elements = soup.find_all(string=re.compile(r'[A-Za-z]+\s+\d{1,2},\s+\d{4}'))
        for element in date_elements:
            if re.match(r'^[A-Za-z]+\s+\d{1,2},\s+\d{4}$', element.strip()):
                return element.strip()
        
        return "日期未找到"
        
    except Exception as e:
        return f"读取错误: {str(e)}"

def check_date_consistency():
    """检查所有新闻页面的日期一致性"""
    news_dir = os.path.join(os.getcwd(), 'news')
    
    print("=" * 80)
    print("新闻栏与新闻页日期一致性检查")
    print("=" * 80)
    
    inconsistencies = []
    consistent_count = 0
    
    for filename, expected_date in news_bar_dates.items():
        file_path = os.path.join(news_dir, filename)
        
        if os.path.exists(file_path):
            actual_date = extract_news_page_date(file_path)
            
            status = "✓ 一致" if actual_date == expected_date else "✗ 不一致"
            
            print(f"{filename:<35} | 新闻栏: {expected_date:<18} | 新闻页: {actual_date:<18} | {status}")
            
            if actual_date != expected_date:
                inconsistencies.append({
                    'file': filename,
                    'expected': expected_date,
                    'actual': actual_date
                })
            else:
                consistent_count += 1
        else:
            print(f"{filename:<35} | 文件不存在")
    
    print("=" * 80)
    print(f"检查完成: {consistent_count}/{len(news_bar_dates)} 个文件日期一致")
    
    if inconsistencies:
        print("\n需要修复的不一致文件:")
        for item in inconsistencies:
            print(f"  - {item['file']}: 应为 '{item['expected']}', 实际为 '{item['actual']}'")
        
        # 提供修复建议
        print("\n修复建议:")
        print("运行以下命令修复日期不一致:")
        print("python fix-date-inconsistencies.py")
    else:
        print("所有新闻页面日期与新闻栏一致！")

if __name__ == "__main__":
    check_date_consistency()