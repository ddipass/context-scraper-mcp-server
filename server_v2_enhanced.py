# server_enhanced_v2.py - 增强版 MCP 服务器（新增反爬虫功能）
import asyncio
import sys
import os
import json
from typing import Optional, List, Dict, Any
from pathlib import Path

from crawl4ai import *
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from mcp.server.fastmcp import Context, FastMCP

# 导入反爬虫模块
from anti_detection import (
    EnhancedAntiDetection, 
    GeolocationSpoofer, 
    RetryManager, 
    ConcurrencyManager,
    create_stealth_config,
    create_geo_spoofed_config,
    create_retry_manager,
    create_concurrency_manager
)

# Create MCP server
mcp = FastMCP("ContextScraperProV2")

# ===== 内部工具函数 =====

def suppress_output():
    """抑制 Crawl4AI 的输出"""
    return open("/dev/null", "w")

def get_smart_browser_config(stealth: bool = False) -> BrowserConfig:
    """获取智能浏览器配置"""
    return BrowserConfig(
        headless=True,
        verbose=False,
        java_script_enabled=True,
        ignore_https_errors=True,
        extra_args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu"
        ] if stealth else None
    )

def get_smart_run_config(
    cache_mode: CacheMode = CacheMode.ENABLED,
    css_selector: Optional[str] = None,
    use_content_filter: bool = False,
    extraction_strategy: Optional[Any] = None,
    screenshot: bool = False
) -> CrawlerRunConfig:
    """获取智能运行配置"""
    
    # 智能内容过滤
    markdown_generator = None
    if use_content_filter:
        content_filter = PruningContentFilter(threshold=0.48, threshold_type="fixed")
        markdown_generator = DefaultMarkdownGenerator(content_filter=content_filter)
    
    return CrawlerRunConfig(
        cache_mode=cache_mode,
        css_selector=css_selector,
        extraction_strategy=extraction_strategy,
        markdown_generator=markdown_generator,
        word_count_threshold=10,
        remove_overlay_elements=True,
        screenshot=screenshot,
        page_timeout=30000,
        delay_before_return_html=2.0
    )

def get_smart_selector(content_type: str) -> str:
    """根据内容类型返回最佳 CSS 选择器"""
    selector_map = {
        "article": "article, .article, .post, .entry, .content, main, [role='main']",
        "product": ".product, .item, [data-product], .product-card, .product-info, .product-details",
        "news": ".news, .article, .story, .post, [data-article], .news-item",
        "blog": ".blog-post, .post, .entry, article, .content, .blog-content",
        "navigation": "nav, .nav, .navigation, .menu, .navbar, header nav",
        "sidebar": ".sidebar, .aside, aside, .widget-area, .secondary",
        "footer": "footer, .footer, .site-footer, .page-footer",
        "header": "header, .header, .site-header, .masthead, .page-header",
        "comments": ".comments, .comment-section, #comments, .comment-list",
        "form": "form, .form, .contact-form, .search-form",
        "table": "table, .table, .data-table, .pricing-table",
        "list": "ul, ol, .list, .listing, .item-list",
        "gallery": ".gallery, .images, .photo-gallery, .image-grid",
        "video": "video, .video, .video-container, .video-wrapper",
        "social": ".social, .social-media, .share-buttons, .social-links",
        "contact": ".contact, .contact-info, .contact-details, .address",
        "pricing": ".pricing, .price, .cost, .fee, .rate, .tariff"
    }
    return selector_map.get(content_type.lower(), content_type)

# ===== 保持原有 8 个工具（向后兼容）=====

@mcp.tool()
async def crawl(url: str, ctx: Context) -> str:
    """基础网页爬取，返回 Markdown 格式内容"""
    sys.stdout = suppress_output()
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        return result.markdown

@mcp.tool()
async def crawl_with_selector(url: str, css_selector: str, ctx: Context) -> str:
    """使用 CSS 选择器精确提取特定内容"""
    sys.stdout = suppress_output()
    
    try:
        browser_config = get_smart_browser_config()
        run_config = get_smart_run_config(css_selector=css_selector)
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=run_config)
            return result.markdown if result.success else f"Failed: {result.error_message}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def crawl_multiple(urls_str: str, ctx: Context) -> str:
    """批量爬取多个 URL，用逗号分隔"""
    sys.stdout = suppress_output()
    
    try:
        urls = [url.strip() for url in urls_str.split(',') if url.strip()]
        if not urls:
            return "No valid URLs provided"
        
        browser_config = get_smart_browser_config()
        run_config = get_smart_run_config()
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            results = await crawler.arun_many(urls=urls, config=run_config)
            
            combined_content = []
            for i, result in enumerate(results):
                if result.success:
                    combined_content.append(f"## URL {i+1}: {urls[i]}\n\n{result.markdown}\n\n---\n")
                else:
                    combined_content.append(f"## URL {i+1}: {urls[i]} - FAILED\n\nError: {result.error_message}\n\n---\n")
            
            return "\n".join(combined_content)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def health_check(url: str, ctx: Context) -> str:
    """检查网站可访问性和基本信息"""
    sys.stdout = suppress_output()
    
    try:
        browser_config = get_smart_browser_config()
        run_config = get_smart_run_config(cache_mode=CacheMode.BYPASS)
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=run_config)
            
            if result.success:
                return f"✅ {url} is accessible\nStatus: Success\nContent length: {len(result.markdown)} characters\nTitle: {result.metadata.get('title', 'N/A') if result.metadata else 'N/A'}"
            else:
                return f"❌ {url} is not accessible\nError: {result.error_message}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def crawl_clean(url: str, ctx: Context) -> str:
    """智能清理爬取 - 自动过滤广告、导航等噪音内容，返回纯净内容"""
    sys.stdout = suppress_output()
    
    try:
        browser_config = get_smart_browser_config()
        run_config = get_smart_run_config(use_content_filter=True)
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=run_config)
            
            if not result.success:
                return f"❌ 爬取失败: {result.error_message}"
            
            # 返回过滤后的内容
            clean_content = result.markdown.fit_markdown if hasattr(result.markdown, 'fit_markdown') else result.markdown
            return f"# 🧹 智能清理内容 - {url}\n\n{clean_content}"
            
    except Exception as e:
        return f"❌ 错误: {str(e)}"

@mcp.tool()
async def crawl_with_screenshot(url: str, ctx: Context) -> str:
    """爬取网页并生成截图"""
    sys.stdout = suppress_output()
    
    try:
        browser_config = get_smart_browser_config()
        run_config = get_smart_run_config(screenshot=True)
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=run_config)
            
            if not result.success:
                return f"❌ 爬取失败: {result.error_message}"
            
            response = f"# 📸 网页截图 - {url}\n\n"
            if result.screenshot:
                response += f"✅ 截图已生成 (Base64 长度: {len(result.screenshot)} 字符)\n\n"
                response += "💡 截图数据已包含在结果中，可用于进一步处理\n\n"
            
            response += f"## 页面内容\n{result.markdown}"
            return response
            
    except Exception as e:
        return f"❌ 错误: {str(e)}"

@mcp.tool()
async def crawl_dynamic(url: str, wait_time: int = 3, ctx: Context = None) -> str:
    """动态内容爬取 - 等待 JavaScript 渲染完成，适合 SPA 应用和动态加载内容"""
    sys.stdout = suppress_output()
    
    try:
        browser_config = get_smart_browser_config()
        
        # 动态内容配置
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            delay_before_return_html=float(wait_time),
            page_timeout=45000,
            word_count_threshold=10,
            remove_overlay_elements=True
        )
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=run_config)
            
            if not result.success:
                return f"❌ 爬取失败: {result.error_message}"
            
            return f"# 🔄 动态内容爬取 - {url}\n\n等待时间: {wait_time}秒\n\n{result.markdown}"
            
    except Exception as e:
        return f"❌ 错误: {str(e)}"

@mcp.tool()
async def crawl_smart_batch(urls_str: str, content_type: str = "auto", ctx: Context = None) -> str:
    """智能批量爬取 - 根据内容类型自动优化爬取策略，支持多种内容类型识别"""
    sys.stdout = suppress_output()
    
    try:
        urls = [url.strip() for url in urls_str.split(',') if url.strip()]
        if not urls:
            return "❌ 没有提供有效的URL"
        
        browser_config = get_smart_browser_config()
        
        # 根据内容类型选择策略
        if content_type != "auto":
            css_selector = get_smart_selector(content_type)
            use_filter = content_type in ["article", "news", "blog"]  # 这些类型需要内容过滤
        else:
            css_selector = None
            use_filter = True  # 默认使用内容过滤
        
        run_config = get_smart_run_config(
            css_selector=css_selector,
            use_content_filter=use_filter
        )
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            results = await crawler.arun_many(urls=urls, config=run_config)
            
            combined_content = []
            success_count = 0
            
            for i, result in enumerate(results):
                if result.success:
                    success_count += 1
                    # 使用过滤后的内容（如果可用）
                    content = result.markdown.fit_markdown if hasattr(result.markdown, 'fit_markdown') and use_filter else result.markdown
                    combined_content.append(f"## 📄 网站 {i+1}: {urls[i]}\n\n{content}\n\n---\n")
                else:
                    combined_content.append(f"## ❌ 网站 {i+1}: {urls[i]} - 失败\n\n错误: {result.error_message}\n\n---\n")
            
            strategy_info = f"内容类型: {content_type}, 选择器: {css_selector or '自动'}, 内容过滤: {'是' if use_filter else '否'}"
            summary = f"# 🚀 智能批量爬取结果\n\n{strategy_info}\n✅ 成功: {success_count}/{len(urls)} 个网站\n\n"
            return summary + "\n".join(combined_content)
            
    except Exception as e:
        return f"❌ 错误: {str(e)}"

# ===== 新增 4 个反爬虫工具 =====

@mcp.tool()
async def crawl_stealth(url: str, ctx: Context) -> str:
    """🥷 隐身爬取 - 使用随机 UA、浏览器指纹伪装和反检测技术"""
    sys.stdout = suppress_output()
    
    try:
        # 使用隐身配置
        browser_config = create_stealth_config()
        run_config = get_smart_run_config(cache_mode=CacheMode.BYPASS)
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=run_config)
            
            if not result.success:
                return f"❌ 隐身爬取失败: {result.error_message}"
            
            # 显示使用的伪装信息
            ua_info = browser_config.user_agent[:100] + "..." if len(browser_config.user_agent) > 100 else browser_config.user_agent
            viewport_info = f"{browser_config.viewport_width}x{browser_config.viewport_height}"
            
            return f"# 🥷 隐身爬取成功 - {url}\n\n**伪装信息:**\n- User Agent: {ua_info}\n- 视窗大小: {viewport_info}\n- 反检测: 已启用\n\n**页面内容:**\n{result.markdown}"
            
    except Exception as e:
        return f"❌ 错误: {str(e)}"

@mcp.tool()
async def crawl_with_geolocation(url: str, location: str = "random", ctx: Context = None) -> str:
    """🌍 地理位置伪装爬取 - 模拟不同地理位置访问"""
    sys.stdout = suppress_output()
    
    try:
        # 创建地理位置伪装配置
        browser_config, geo_config = create_geo_spoofed_config(location)
        run_config = get_smart_run_config(cache_mode=CacheMode.BYPASS)
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=run_config)
            
            if not result.success:
                return f"❌ 地理位置伪装爬取失败: {result.error_message}"
            
            return f"# 🌍 地理位置伪装爬取 - {url}\n\n**伪装位置:**\n- 纬度: {geo_config.latitude}\n- 经度: {geo_config.longitude}\n- 精度: {geo_config.accuracy}m\n\n**页面内容:**\n{result.markdown}"
            
    except Exception as e:
        return f"❌ 错误: {str(e)}"

@mcp.tool()
async def crawl_with_retry(url: str, max_retries: int = 3, ctx: Context = None) -> str:
    """🔄 重试爬取 - 自动重试失败的请求，适合不稳定的网站"""
    sys.stdout = suppress_output()
    
    try:
        browser_config = create_stealth_config()
        run_config = get_smart_run_config(cache_mode=CacheMode.BYPASS)
        retry_manager = create_retry_manager(max_retries)
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await retry_manager.execute_with_retry(crawler, url, run_config)
            
            if not result.success:
                return f"❌ 重试爬取失败: {result.error_message}"
            
            return f"# 🔄 重试爬取成功 - {url}\n\n**重试配置:** 最大重试 {max_retries} 次\n\n**页面内容:**\n{result.markdown}"
            
    except Exception as e:
        return f"❌ 错误: {str(e)}"

@mcp.tool()
async def crawl_concurrent_optimized(urls_str: str, max_concurrent: int = 5, ctx: Context = None) -> str:
    """⚡ 并发优化爬取 - 智能并发控制，提升批量爬取效率"""
    sys.stdout = suppress_output()
    
    try:
        urls = [url.strip() for url in urls_str.split(',') if url.strip()]
        if not urls:
            return "❌ 没有提供有效的URL"
        
        browser_config = create_stealth_config()
        run_config = get_smart_run_config(cache_mode=CacheMode.BYPASS)
        concurrency_manager = create_concurrency_manager(max_concurrent)
        retry_manager = create_retry_manager(2)  # 较少重试次数以提升速度
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            # 创建并发任务
            tasks = []
            for url in urls:
                task = concurrency_manager.execute_with_limit(
                    retry_manager.execute_with_retry(crawler, url, run_config)
                )
                tasks.append(task)
            
            # 执行所有任务
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            combined_content = []
            success_count = 0
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    combined_content.append(f"## ❌ 网站 {i+1}: {urls[i]} - 异常\n\n错误: {str(result)}\n\n---\n")
                elif hasattr(result, 'success') and result.success:
                    success_count += 1
                    combined_content.append(f"## ✅ 网站 {i+1}: {urls[i]}\n\n{result.markdown}\n\n---\n")
                else:
                    error_msg = getattr(result, 'error_message', '未知错误')
                    combined_content.append(f"## ❌ 网站 {i+1}: {urls[i]} - 失败\n\n错误: {error_msg}\n\n---\n")
            
            summary = f"# ⚡ 并发优化爬取结果\n\n**配置:** 最大并发 {max_concurrent}\n✅ 成功: {success_count}/{len(urls)} 个网站\n\n"
            return summary + "\n".join(combined_content)
            
    except Exception as e:
        return f"❌ 错误: {str(e)}"

# ===== 增强版智能提示系统 =====

@mcp.prompt()
def stealth_research(topic: str, urls: str) -> str:
    """🥷 隐身研究 - 使用反爬虫技术进行深度研究"""
    return f'''使用隐身爬取技术研究 "{topic}"，目标网站: {urls}

**执行步骤:**
1. 使用 crawl_stealth 对每个URL进行隐身爬取，避免被检测
2. 如果遇到访问限制，使用 crawl_with_geolocation 尝试不同地理位置
3. 对于不稳定的网站，使用 crawl_with_retry 确保数据完整性
4. 分析收集的信息，重点关注 {topic}

**输出要求:**
- 创建综合研究报告，包含执行摘要、关键发现、数据分析
- 标注使用的反爬虫技术和成功率
- 保存到 "./.amazonq/rules/stealth_research_{topic.lower().replace(' ', '_')}.md"

**注意:** 使用隐身技术时请遵守网站的robots.txt和使用条款'''

@mcp.prompt()
def competitive_intelligence(competitor_urls: str, focus_areas: str) -> str:
    """🕵️ 竞争情报收集 - 使用高级爬取技术分析竞争对手"""
    return f'''收集竞争情报，分析领域: {focus_areas}，目标: {competitor_urls}

**执行策略:**
1. 使用 crawl_concurrent_optimized 进行高效批量爬取
2. 对于重要页面使用 crawl_stealth 避免被识别为爬虫
3. 使用 crawl_with_geolocation 模拟不同地区用户访问
4. 针对动态内容使用 crawl_dynamic 确保完整性

**分析重点:**
- {focus_areas} 相关的产品、服务、策略信息
- 价格策略和市场定位
- 用户体验和技术实现
- 内容策略和营销方法

**输出格式:**
- 竞争对手分析矩阵
- 优势劣势对比
- 市场机会识别
- 战略建议

保存到 "./.amazonq/rules/competitive_intelligence_{focus_areas.lower().replace(' ', '_')}.md"'''

@mcp.prompt()
def market_monitoring_setup(urls: str, monitoring_frequency: str = "daily") -> str:
    """📊 市场监控设置 - 建立持续监控系统"""
    return f'''建立市场监控系统，目标网站: {urls}，频率: {monitoring_frequency}

**设置步骤:**
1. 使用 crawl_stealth 建立基线数据，避免被识别
2. 使用 crawl_with_screenshot 记录视觉基线
3. 设置监控指标和变化阈值
4. 创建监控脚本和自动化流程

**监控内容:**
- 价格变化和促销活动
- 产品更新和新功能发布
- 内容策略变化
- 技术架构更新
- 用户体验改进

**输出:**
- 监控基线报告
- 自动化监控脚本
- 变化检测规则
- 报告模板

保存监控配置到 "./.amazonq/rules/market_monitoring_config.md"
保存基线数据到 "./.amazonq/rules/monitoring_baseline_{monitoring_frequency}.md"'''

@mcp.prompt()
def anti_detection_audit(url: str) -> str:
    """🛡️ 反检测审计 - 测试网站的爬虫检测机制"""
    return f'''对 {url} 进行反检测审计，测试其爬虫检测能力

**测试步骤:**
1. 使用 crawl 进行基础爬取，记录响应
2. 使用 crawl_stealth 测试隐身效果
3. 使用 crawl_with_geolocation 测试地理位置检测
4. 使用 crawl_with_retry 测试频率限制
5. 使用 crawl_concurrent_optimized 测试并发限制

**检测项目:**
- User Agent 检测
- 浏览器指纹检测
- 地理位置限制
- 访问频率限制
- IP 封禁机制
- JavaScript 反爬虫

**输出报告:**
- 检测机制分析
- 绕过成功率统计
- 推荐爬取策略
- 风险评估

保存到 "./.amazonq/rules/anti_detection_audit_{url.replace('/', '_').replace(':', '')}.md"'''

@mcp.prompt()
def data_extraction_optimization(url: str, data_type: str) -> str:
    """🎯 数据提取优化 - 针对特定数据类型优化提取策略"""
    return f'''优化 {url} 的 {data_type} 数据提取

**优化策略:**
1. 使用 crawl_stealth 避免检测
2. 根据数据类型使用 crawl_smart_batch 优化选择器
3. 对于动态加载数据使用 crawl_dynamic
4. 使用 crawl_with_retry 确保数据完整性

**数据类型优化:**
- 如果是产品数据: 重点提取价格、规格、评价
- 如果是文章内容: 重点提取标题、正文、作者、时间
- 如果是联系信息: 重点提取邮箱、电话、地址
- 如果是表格数据: 保持结构化格式

**输出:**
- 优化后的提取策略
- 数据质量评估
- 提取效率报告
- 结构化数据文件

保存到 "./.amazonq/rules/extraction_optimization_{data_type}_{url.split('/')[-1]}.md"'''

# Run the server
if __name__ == "__main__":
    mcp.run()
