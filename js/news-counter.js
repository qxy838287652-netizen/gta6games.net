// News Click Counter System
class NewsCounter {
    constructor() {
        this.storageKey = 'gta6_news_clicks';
        this.init();
    }

    init() {
        // 先做一次历史数据规范化迁移，避免多种URL形式导致的键不一致
        this.normalizeStorage();

        // 监听新闻链接点击（首页与其它页面通用）
        document.addEventListener('click', (e) => {
            const newsLink = e.target.closest('a[href*=".html"]');
            if (newsLink) {
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
        return this.normalizeKey(url);
    }

    // 统一把各种URL形式折叠为“文件名.html”
    normalizeKey(url) {
        try {
            // 去掉查询串和hash
            const clean = url.split('#')[0].split('?')[0];
            // 取最后一个/后的部分
            const file = clean.substring(clean.lastIndexOf('/') + 1);
            return file || clean;
        } catch {
            return url;
        }
    }

    // 迁移已有localStorage数据到统一键（文件名）上，合并累加后写回
    normalizeStorage() {
        const raw = this.getClicks();
        const merged = {};
        Object.entries(raw).forEach(([k, v]) => {
            const nk = this.normalizeKey(k);
            merged[nk] = (merged[nk] || 0) + (typeof v === 'number' ? v : 0);
        });
        // 仅当有变化时写回，避免无谓写入
        const changed = JSON.stringify(raw) !== JSON.stringify(merged);
        if (changed) {
            localStorage.setItem(this.storageKey, JSON.stringify(merged));
        }
    }

    updateClickCounts() {
        const clicks = this.getClicks();
        // 首页/其它位置可能使用相对或绝对URL，统一匹配所有指向 .html 的链接
        const newsLinks = document.querySelectorAll('a[href*=".html"]');
        
        newsLinks.forEach(link => {
            const href = link.href;
            if (!href) return;
            const newsKey = this.getNewsKey(href);
            const count = clicks[newsKey] || 0;

            // 更新点击计数显示
            const eyeIcon = link.querySelector('.fa-eye');
            const countSpan = eyeIcon ? eyeIcon.nextElementSibling : null;
            if (countSpan && countSpan.textContent !== undefined) {
                countSpan.textContent = this.formatCount(count);
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

    // 专门用于首页的初始化
    initHomePage() {
        // 立即更新阅读量显示
        this.updateClickCounts();
        
        // 监听新闻链接点击
        document.addEventListener('click', (e) => {
            const newsLink = e.target.closest('a[href*="news/"]');
            if (newsLink && newsLink.href.includes('.html')) {
                this.incrementClick(newsLink.href);
                // 点击后立即更新显示
                setTimeout(() => this.updateClickCounts(), 100);
            }
        });
    }

    // 同步首页阅读量到新闻页面
    syncHomePageViews() {
        const currentUrl = window.location.href;
        const currentCount = this.getClickCount(currentUrl);
        // 仅更新当前页面区域内的计数（避免误覆盖其它链接的显示）
        const eyeIcons = document.querySelectorAll('.fa-eye');
        eyeIcons.forEach(eyeIcon => {
            const countSpan = eyeIcon.nextElementSibling;
            if (countSpan && countSpan.textContent !== undefined) {
                countSpan.textContent = this.formatCount(currentCount);
            }
        });
        return currentCount;
    }
}

// 初始化计数器
const newsCounter = new NewsCounter();