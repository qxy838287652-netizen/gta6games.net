// 新闻页面导航和阅读量同步功能
class NewsNavigation {
    constructor() {
        this.newsList = [
            {
                title: "GTA 6 Pre-orders Tipped For November: Standard, Deluxe, Ultimate Editions",
                url: "gta6-preorders-and-editions.html",
                date: "September 24, 2025"
            },
            {
                title: "GTA 6 Story Trailer 2 Rumored For October Reveal",
                url: "gta6-trailer-2-october-rumor.html",
                date: "September 23, 2025"
            },
            {
                title: "GTA 6 Soundtrack: Licensed Classics And AI-Enhanced Dynamic Radio",
                url: "gta6-soundtrack-ai-radio.html",
                date: "September 22, 2025"
            },
            {
                title: "GTA 6 Performance Targets: 60 FPS With Ray Tracing On Next-Gen Consoles",
                url: "gta6-performance-targets.html",
                date: "September 21, 2025"
            },
            {
                title: "Rockstar Teases Next-Gen NPC AI: Memory, Routines, And Reactive Crowds",
                url: "gta6-ai-npc-system.html",
                date: "September 20, 2025"
            },
            {
                title: "GTA 6 Map Leak: 2x GTA 5 Size With Dynamic Region Expansion",
                url: "gta6-map-size-expansion.html",
                date: "September 19, 2025"
            },
            {
                title: "GTA 6 May Face Further Delay to October 2026 - Industry Insider Suggests Holiday Release Strategy",
                url: "gta6-further-delay-2026.html",
                date: "September 18, 2025"
            },
            {
                title: "GTA 6 Set to Become the Largest Game Launch in History - Rockstar Hiring Spree Indicates Massive Scale",
                url: "gta6-largest-launch.html",
                date: "September 17, 2025"
            },
            {
                title: "GTA 6 to Feature Revolutionary Advanced Environmental Destruction - 60% of Buildings Can Be Destroyed",
                url: "gta6-advanced-destruction.html",
                date: "September 16, 2025"
            },
            {
                title: "GTA 6 Officially Delayed to May 2026 - Rockstar Apologizes, Promises Uncompromising Quality",
                url: "gta6-delay-2026.html",
                date: "September 15, 2025"
            },
            {
                title: "GTA 6 Dual Protagonists Revealed: Jason & Lucia - The Ultimate Crime Duo",
                url: "gta6-dual-protagonists.html",
                date: "September 14, 2025"
            },
            {
                title: "GTA 6 Online Confirmed: 100-Player Servers - The Largest Open World Multiplayer Ever",
                url: "gta6-online-100players.html",
                date: "September 13, 2025"
            },
            {
                title: "GTA 6 Returns to Vice City! Miami Vibes, Neon Nights & 80s Retro Aesthetics Confirmed",
                url: "gta6-vice-city-return.html",
                date: "September 12, 2025"
            },
            {
                title: "GTA 6 Gameplay Leak! Ray Tracing, 4K Textures & Physics Destruction Stun the Community",
                url: "gta6-graphics-leak.html",
                date: "September 11, 2025"
            },
            {
                title: "GTA 6 Preorder Bonuses Revealed: Exclusive Vehicles, Weapon Skins, Properties & Vice City Legends DLC",
                url: "gta6-preorder-bonus.html",
                date: "September 10, 2025"
            }
        ];
        
        this.currentPage = this.getCurrentPage();
    }

    // 获取当前页面信息
    getCurrentPage() {
        const currentUrl = window.location.pathname.split('/').pop();
        return this.newsList.find(news => news.url === currentUrl);
    }

    // 获取上一篇和下一篇
    getAdjacentNews() {
        if (!this.currentPage) return { prev: null, next: null };
        
        const currentIndex = this.newsList.findIndex(news => news.url === this.currentPage.url);
        
        return {
            prev: currentIndex > 0 ? this.newsList[currentIndex - 1] : null,
            next: currentIndex < this.newsList.length - 1 ? this.newsList[currentIndex + 1] : null
        };
    }

    // 创建导航HTML
    createNavigationHTML() {
        const { prev, next } = this.getAdjacentNews();
        
        let html = '<div class="news-navigation border-t border-gray-200 pt-8 mt-8">';
        html += '<div class="flex flex-col md:flex-row justify-between gap-4">';
        
        // Previous article
        if (prev) {
            html += `<div class="flex-1 nav-item bg-gray-50 hover:bg-gray-100 transition-smooth rounded-lg">`;
            html += `<p class="text-sm text-gray-500 mb-2 nav-label">Previous Article</p>`;
            html += `<a href="${prev.url}" class="block p-4">`;
            html += `<h4 class="font-medium text-gray-800 line-clamp-2">${prev.title}</h4>`;
            html += `<p class="text-xs text-gray-500 mt-1">${prev.date}</p>`;
            html += '</a></div>';
        } else {
            html += '<div class="flex-1"></div>';
        }
        
        // Next article
        if (next) {
            html += `<div class="flex-1 nav-item bg-gray-50 hover:bg-gray-100 transition-smooth rounded-lg">`;
            html += `<p class="text-sm text-gray-500 mb-2 text-right nav-label">Next Article</p>`;
            html += `<a href="${next.url}" class="block p-4 text-right">`;
            html += `<h4 class="font-medium text-gray-800 line-clamp-2">${next.title}</h4>`;
            html += `<p class="text-xs text-gray-500 mt-1">${next.date}</p>`;
            html += '</a></div>';
        } else {
            html += '<div class="flex-1"></div>';
        }
        
        html += '</div></div>';
        return html;
    }

    // 兼容性增强：找不到 .prose 时多级回退，确保移动端也能挂载
    getContentContainer() {
        return (
            document.querySelector('article .prose') ||
            document.querySelector('article') ||
            document.querySelector('main.container') ||
            document.querySelector('main') ||
            document.body
        );
    }

    // 同步首页阅读量
    syncHomePageViews() {
        if (typeof newsCounter !== 'undefined') {
            // 使用新的同步方法
            newsCounter.syncHomePageViews();
        }
    }

    // 初始化
    init() {
        // 同步阅读量
        this.syncHomePageViews();
        
        // 添加上一篇下一篇导航
        this.addNavigation();
        
        // 添加移动端优化样式
        this.addMobileStyles();
    }

    // 添加导航（防重复插入，确保可见）
    addNavigation() {
        // 避免重复
        if (document.querySelector('.news-navigation')) return;

        const articleContent = this.getContentContainer();
        if (articleContent) {
            const navigationHTML = this.createNavigationHTML();
            articleContent.insertAdjacentHTML('beforeend', navigationHTML);

            // 可见性保障：若父级有 overflow 或样式干扰，给导航加清除
            const navEl = document.querySelector('.news-navigation');
            if (navEl) {
                navEl.style.clear = 'both';
                navEl.style.display = 'block';
            }
        }
    }

    // 添加移动端优化样式
    addMobileStyles() {
        const style = document.createElement('style');
        style.textContent = `
            /* 导航样式 */
            .news-navigation {
                margin-top: 2rem;
            }
            
            .nav-item {
                transition: all 0.3s ease;
                border-radius: 0.5rem;
            }
            
            .nav-label {
                font-weight: 500;
            }
            
            .line-clamp-2 {
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
            }
            
            .transition-smooth {
                transition: all 0.3s ease;
            }
            
            /* 移动端优化 */
            @media (max-width: 768px) {
                /* 确保图片响应式 */
                .prose img {
                    max-width: 100%;
                    height: auto;
                    border-radius: 0.75rem;
                }
                
                /* 移动端标题优化 */
                .text-3xl {
                    font-size: 1.75rem !important;
                }
                
                .text-2xl {
                    font-size: 1.5rem !important;
                }
                
                /* 移动端内边距优化 */
                .container {
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
                
                article {
                    padding: 1.5rem !important;
                }
                
                /* 移动端导航优化 */
                .news-navigation {
                    margin-top: 1.5rem;
                    padding-top: 1.5rem;
                }
                
                .nav-item {
                    margin-bottom: 1rem;
                }
                
                .nav-item:last-child {
                    margin-bottom: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// 页面加载时初始化函数（供外部调用）
function initializeNewsNavigation() {
    const newsNav = new NewsNavigation();
    newsNav.init();
}