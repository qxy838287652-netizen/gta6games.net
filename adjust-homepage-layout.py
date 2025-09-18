import os
import re

def adjust_homepage_layout():
    # 读取index.html文件
    with open('index.html', 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 调整游戏卡片布局 - 从3列改为2列以适应并排布局
    # 修改游戏区域的网格布局类
    content = re.sub(
        r'(<div class="games-side">.*?<h3 class="text-2xl font-bold mb-6 text-center text-primary">Our GTA 6 Games Collection</h3>.*?<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-)3( gap-6" id="games-container">)',
        r'\g<1>2\g<2>',
        content,
        flags=re.DOTALL
    )
    
    # 添加一些额外的样式来确保两个区域的视觉平衡
    # 在<style>标签中添加额外的CSS类
    style_pattern = r'(<style type="text/tailwindcss">.*?@layer utilities \{.*?)(\s*\}\s*</style>)'
    
    additional_styles = '''
            /* 并排布局调整 */
            .games-news-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 2rem;
            }
            
            @media (max-width: 1024px) {
                .games-news-grid {
                    grid-template-columns: 1fr;
                    gap: 1.5rem;
                }
            }
            
            /* 调整游戏卡片在并排布局中的尺寸 */
            @media (min-width: 1024px) {
                .games-side .game-card {
                    min-height: 280px;
                }
            }
            
            /* 确保新闻项目在并排布局中的一致性 */
            .news-side .news-item {
                min-height: 140px;
            }
'''
    
    content = re.sub(
        style_pattern,
        rf'\g<1>{additional_styles}\g<2>',
        content,
        flags=re.DOTALL
    )
    
    # 写入修改后的内容
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("首页布局调整完成！")
    print("1. 游戏卡片网格已从3列调整为2列以适应并排布局")
    print("2. 添加了响应式样式以确保在不同屏幕尺寸下的良好显示")
    print("3. 调整了卡片尺寸以在并排布局中保持视觉平衡")

if __name__ == "__main__":
    adjust_homepage_layout()