// News Click Counter System
class NewsCounter {
    constructor() {
        this.storageKey = 'gta6_news_clicks';
        this.init();
    }

    init() {
        // 监听新闻链接点击
        document.addEventListener('click', (e) => {
            const newsLink = e.target.closest('a[href*="news/"]');
            if (newsLink && newsLink.href.includes('.html')) {
                this.incrementClick(newsLink.href);
            }
        });

        // 页面加载时更新点击计数显示
        this.updateClickCounts();
    }

    incrementClick(url) {
        const clicks = this.getClicks();
        const newsKey = this.getNewsKey(url);
        
        clicks[newsKey] = (clicks[newsKey] || 0) + 1;
        localStorage.setItem(this.storageKey, JSON.stringify(clicks));
    }

    getClickCount(url) {
        const clicks = this.getClicks();
        const newsKey = this.getNewsKey(url);
        return clicks[newsKey] || 0;
    }

    getClicks() {
        try {
            return JSON.parse(localStorage.getItem(this.storageKey)) || {};
        } catch {
            return {};
        }
    }

    getNewsKey(url) {
        // 从URL中提取新闻文件名
        const match = url.match(/news\/([^/]+\.html)/);
        return match ? match[1] : url;
    }

    updateClickCounts() {
        const clicks = this.getClicks();
        const newsLinks = document.querySelectorAll('a[href*="news/"]');
        
        newsLinks.forEach(link => {
            if (link.href.includes('.html')) {
                const newsKey = this.getNewsKey(link.href);
                const count = clicks[newsKey] || 0;
                
                // 更新点击计数显示
                const eyeIcon = link.querySelector('.fa-eye');
                if (eyeIcon) {
                    const countSpan = eyeIcon.nextElementSibling;
                    if (countSpan && countSpan.textContent) {
                        // 格式化数字显示
                        const formattedCount = this.formatCount(count);
                        countSpan.textContent = formattedCount;
                    }
                }
            }
        });
    }

    formatCount(count) {
        if (count >= 1000000) {
            return (count / 1000000).toFixed(1) + 'M';
        } else if (count >= 1000) {
            return (count / 1000).toFixed(1) + 'K';
        }
        return count.toString();
    }

    // 获取所有新闻的点击统计（用于管理面板）
    getAllStats() {
        return this.getClicks();
    }

    // 重置所有统计
    resetAll() {
        localStorage.removeItem(this.storageKey);
        this.updateClickCounts();
    }

    // 同步首页阅读量到新闻页面
    syncHomePageViews() {
        const clicks = this.getClicks();
        const currentUrl = window.location.href;
        const currentCount = this.getClickCount(currentUrl);
        
        // 更新页面上的阅读量显示
        const eyeIcons = document.querySelectorAll('.fa-eye');
        eyeIcons.forEach(eyeIcon => {
            const countSpan = eyeIcon.nextElementSibling;
            if (countSpan && countSpan.textContent) {
                countSpan.textContent = this.formatCount(currentCount);
            }
        });
        
        return currentCount;
    }
}

// 初始化计数器
const newsCounter = new NewsCounter();