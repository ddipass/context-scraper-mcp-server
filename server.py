# server_enhanced.py - 增强版 MCP 服务器（无需外部 API）
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

# Create MCP server
mcp = FastMCP("ContextScraperPro")

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

# ===== 保持原有 4 个工具（向后兼容）=====

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

# ===== 新增 4 个核心工具（无需外部 API）=====

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

# ===== 增强版提示系统 =====

@mcp.prompt()
def create_context_from_url(url: str) -> str:
    """将网页内容保存到 Amazon Q 上下文规则"""
    return f'''Use the crawl_clean tool to get clean content from {url}, then save it to "./.amazonq/rules/" directory.

Steps:
1. Use crawl_clean to get filtered, clean content without ads and navigation
2. Create .amazonq/rules/ directory if needed
3. Save content with a descriptive filename based on the page title
4. Confirm successful creation'''

@mcp.prompt()
def research_with_sources(topic: str, urls: str) -> str:
    """基于多个来源进行深度研究"""
    return f'''Research "{topic}" using multiple sources: {urls}

Process:
1. Use crawl_smart_batch with content_type="article" to gather clean article content
2. Analyze information focusing on {topic}
3. Create comprehensive research document with:
   - Executive Summary about {topic}
   - Key Findings organized by source
   - Comparative Analysis across sources
   - Best Practices identified
   - Actionable Insights and Recommendations
   - Source References

Save to "./.amazonq/rules/research_{topic.lower().replace(' ', '_')}.md"
Create directories if needed.'''

@mcp.prompt()
def extract_product_data(urls: str) -> str:
    """智能提取产品信息"""
    return f'''Extract product information from: {urls}

1. Use crawl_smart_batch with content_type="product" to focus on product-related content
2. Extract and organize:
   - Product names and titles
   - Pricing information
   - Product descriptions and features
   - Availability and stock status
   - Technical specifications
   - Customer reviews (if available)

3. Create structured product comparison document
4. Save to "./.amazonq/rules/product_analysis.md"
Create directories if needed.'''

@mcp.prompt()
def monitor_site_content(url: str) -> str:
    """设置网站内容监控基线"""
    return f'''Set up content monitoring baseline for {url}:

1. Use crawl_clean to get current clean content snapshot
2. Use crawl_with_screenshot to capture visual state
3. Create monitoring baseline document with:
   - Current timestamp
   - Clean content snapshot
   - Screenshot reference (Base64 data included)
   - Key content indicators and metrics
   - Content structure analysis

4. Save baseline to "./.amazonq/rules/monitor_baseline_{url.replace('/', '_').replace(':', '')}.md"
Create directories if needed.

Note: For ongoing monitoring, run this periodically and compare with baseline.'''

@mcp.prompt()
def analyze_competitor_sites(competitor_urls: str, focus_area: str) -> str:
    """竞争对手网站分析"""
    return f'''Analyze competitor websites focusing on {focus_area}: {competitor_urls}

Process:
1. Use crawl_smart_batch with appropriate content_type based on {focus_area}
2. For each competitor, extract information about {focus_area}
3. Create comparative analysis including:
   - Feature comparison matrix
   - Content strategy analysis
   - User experience insights
   - Best practices identified
   - Competitive advantages and gaps
   - Strategic recommendations

4. Save to "./.amazonq/rules/competitor_analysis_{focus_area.lower().replace(' ', '_')}.md"
Create directories if needed.'''

@mcp.prompt()
def capture_dynamic_content(url: str, wait_seconds: int = 5) -> str:
    """捕获动态加载的内容"""
    return f'''Capture dynamic content from {url}:

1. Use crawl_dynamic with wait_time={wait_seconds} to allow JavaScript to load content
2. If content appears incomplete, try increasing wait time or use crawl_with_screenshot for visual verification
3. Extract and organize the dynamically loaded content
4. Compare with basic crawl results to identify what content is dynamically loaded

5. Save comprehensive dynamic content analysis to "./.amazonq/rules/dynamic_content_{url.split('/')[-1] or 'analysis'}.md"
Create directories if needed.'''

@mcp.prompt()
def extract_structured_data(url: str, data_type: str) -> str:
    """提取结构化数据"""
    return f'''Extract structured {data_type} data from {url}:

1. Use crawl_smart_batch with content_type="{data_type}" to focus on relevant content
2. Extract and structure the data based on type:
   - For "contact": emails, phones, addresses, social links
   - For "pricing": prices, plans, features, comparisons
   - For "navigation": menu structure, site hierarchy, page links
   - For "form": form fields, validation, submission endpoints
   - For "table": tabular data, headers, relationships

3. Organize extracted data in a clear, structured format
4. Save to "./.amazonq/rules/structured_{data_type}_data.md"
Create directories if needed.'''

@mcp.prompt()
def quick_site_audit(url: str) -> str:
    """快速网站审计"""
    return f'''Perform comprehensive site audit for {url}:

1. Use health_check to verify accessibility and basic metrics
2. Use crawl_clean to analyze content quality and structure
3. Use crawl_with_screenshot to capture visual state
4. Provide audit report including:
   - Site accessibility and performance
   - Content quality and organization
   - Visual design assessment
   - Technical recommendations
   - SEO and usability insights

5. Save audit report to "./.amazonq/rules/site_audit_{url.split('/')[-1] or 'report'}.md"
Create directories if needed.'''

# Run the server
if __name__ == "__main__":
    mcp.run()
