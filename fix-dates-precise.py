#!/usr/bin/env python3
"""
精确修复新闻页面日期不一致的脚本
直接定位并替换日期元素
"""

import os
import re

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

def update_date_in_file(file_path, expected_date):
    """在文件中精确更新日期"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 精确匹配日期行
        pattern = r'(<span><i class="fa fa-calendar-alt mr-2"></i>\s*)[A-Za-z]+\s+\d{1,2},\s+\d{4}(</span>)'
        
        # 检查是否找到匹配
        match = re.search(pattern, content)
        if not match:
            print(f"  ⚠ 在 {file_path} 中未找到日期模式")
            return False
        
        # 替换日期
        new_content = re.sub(pattern, f'\g<1>{expected_date}\g<2>', content)
        
        # 写入更新后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"  ✗ 更新 {file_path} 时出错: {str(e)}")
        return False

def fix_all_dates():
    """修复所有新闻页面的日期"""
    news_dir = os.path.join(os.getcwd(), 'news')
    
    print("=" * 80)
    print("精确修复新闻页面日期")
    print("=" * 80)
    
    fixed_count = 0
    error_count = 0
    
    for filename, expected_date in news_bar_dates.items():
        file_path = os.path.join(news_dir, filename)
        
        if os.path.exists(file_path):
            print(f"正在修复 {filename} -> {expected_date}")
            
            if update_date_in_file(file_path, expected_date):
                print(f"  ✓ 成功更新")
                fixed_count += 1
            else:
                error_count += 1
        else:
            print(f"{filename} 文件不存在，跳过")
    
    print("=" * 80)
    print(f"修复完成: {fixed_count} 个文件已修复, {error_count} 个文件出错")
    
    # 验证修复结果
    if fixed_count > 0:
        print("\n验证修复结果:")
        os.system("python check-date-consistency.py")

if __name__ == "__main__":
    fix_all_dates()