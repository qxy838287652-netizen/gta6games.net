#!/usr/bin/env python3
"""
修复新闻页面布局美观性的脚本
统一新闻正文部分的边距和布局效果
"""

import os
import re

def fix_news_layout(file_path):
    """修复单个新闻页面的布局"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 修复1: 替换 prose max-w-none 为 prose max-w-4xl，添加适当的padding
        content = content.replace(
            '<div class="prose max-w-none">',
            '<div class="prose max-w-4xl mx-auto px-8 py-8">'
        )
        
        # 修复2: 确保新闻头部有适当的padding
        content = re.sub(
            r'(<div class="p-12 border-b border-gray-100 text-center">)',
            r'<div class="p-12 border-b border-gray-100 text-center">',
            content
        )
        
        # 修复3: 为段落添加更好的间距
        content = re.sub(
            r'(<p class="text-lg mb-6">)',
            r'<p class="text-lg mb-8 leading-relaxed">',
            content
        )
        
        # 修复4: 为标题添加更好的间距
        content = re.sub(
            r'(<h2 class="text-2xl font-semibold mb-4 mt-8">)',
            r'<h2 class="text-2xl font-semibold mb-6 mt-12">',
            content
        )
        
        # 修复5: 为引用块添加更好的样式
        content = re.sub(
            r'(<blockquote class="border-l-4 border-primary pl-6 py-4 my-8 bg-accent rounded-r-xl">)',
            r'<blockquote class="border-l-4 border-primary pl-8 py-6 my-12 bg-accent/20 rounded-r-xl shadow-sm">',
            content
        )
        
        # 写入更新后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"  ✗ 修复 {file_path} 时出错: {str(e)}")
        return False

def fix_all_news_layouts():
    """修复所有新闻页面的布局"""
    news_dir = os.path.join(os.getcwd(), 'news')
    
    print("=" * 80)
    print("修复新闻页面布局美观性")
    print("=" * 80)
    
    # 获取所有新闻HTML文件（排除备份文件）
    news_files = []
    for filename in os.listdir(news_dir):
        if filename.endswith('.html') and not filename.endswith('.backup'):
            news_files.append(filename)
    
    fixed_count = 0
    error_count = 0
    
    for filename in news_files:
        file_path = os.path.join(news_dir, filename)
        
        print(f"正在修复 {filename}...")
        
        if fix_news_layout(file_path):
            print(f"  ✓ 布局修复成功")
            fixed_count += 1
        else:
            error_count += 1
    
    print("=" * 80)
    print(f"修复完成: {fixed_count} 个文件已修复, {error_count} 个文件出错")
    
    if fixed_count > 0:
        print("\n布局改进包括:")
        print("  • 正文内容添加适当边距 (px-8 py-8)")
        print("  • 限制最大宽度 (max-w-4xl)")
        print("  • 改进段落间距 (mb-8 leading-relaxed)")
        print("  • 增强标题间距 (mb-6 mt-12)")
        print("  • 美化引用块样式")

if __name__ == "__main__":
    fix_all_news_layouts()