# server_v3_smart.py - 智能口语化 MCP 服务器
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

# 导入反爬虫模块和智能提示
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
from smart_prompts import smart_router, analyze_user_request

# Create MCP server
mcp = FastMCP("ContextScraperSmart")

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
# ===== 保持所有原有工具（向后兼容）=====

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

# ===== 反爬虫工具 =====

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

# ===== 智能口语化提示系统 =====

@mcp.prompt()
def help_me_crawl(what_you_want: str, websites: str = "") -> str:
    """帮我爬网站 - 万能助手，告诉我你想要什么就行
    
    随便怎么说都行：
    - "帮我看看这几个网站在卖什么"
    - "我想知道竞争对手的价格策略"  
    - "这个网站访问不了，帮我想办法"
    - "定期帮我看看有没有新内容"
    - "把这些页面的数据整理出来"
    - "偷偷研究一下他们怎么做的"
    
    🤖 我会：
    ✅ 理解你的意思
    ✅ 选最合适的工具
    ✅ 绕过反爬虫限制  
    ✅ 把结果整理好给你
    
    就像有个懂技术的朋友帮你干活！
    """
    
    # 分析用户需求
    analysis_result = analyze_user_request(what_you_want, websites)
    
    # 根据分析结果生成具体执行计划
    analysis = smart_router.analyze_intent(what_you_want)
    strategy = smart_router.generate_strategy(analysis, websites)
    
    execution_plan = f"""
{analysis_result}

🎯 **具体执行步骤：**

1. **准备阶段**
   - 分析目标网站: {websites or "待指定"}
   - 选择最佳工具组合: {' + '.join(strategy['tools'])}

2. **执行阶段**
   {generate_execution_steps(analysis, strategy, websites)}

3. **整理阶段**
   - 清理和格式化数据
   - 保存到 .amazonq/rules/ 目录
   - 生成易读的分析报告

💡 **温馨提示：** 如果遇到访问问题，我会自动切换策略，你不用担心！
"""
    
    return execution_plan

@mcp.prompt()
def help_me_research(topic: str, websites: str) -> str:
    """帮我研究一下 - 像朋友一样帮你收集和分析信息
    
    你只需要说：
    - "帮我研究一下AI最新发展"
    - "看看这几个网站关于XX的内容"  
    - "分析一下竞争对手在做什么"
    - "偷偷看看他们的策略"（自动用隐身模式）
    
    我会自动选最合适的方式帮你搞定！
    """
    
    return f'''深度研究 "{topic}"，目标网站: {websites}

🔍 **研究计划：**

1. **信息收集阶段**
   - 使用 crawl_clean 获取干净的内容
   - 如果网站有反爬虫，自动切换到 crawl_stealth
   - 对于多个网站，使用 crawl_concurrent_optimized 提高效率

2. **内容分析阶段**
   - 重点关注与 "{topic}" 相关的信息
   - 提取关键数据和观点
   - 识别趋势和模式

3. **报告生成阶段**
   - 创建综合研究报告
   - 包含：执行摘要、关键发现、数据分析、结论建议
   - 保存到 "./.amazonq/rules/research_{topic.replace(' ', '_')}.md"

🤖 **我会自动处理：**
- 反爬虫检测和绕过
- 内容清理和去噪
- 多源信息整合
- 结构化报告生成

开始执行研究任务...'''

@mcp.prompt()
def help_me_get_data(websites: str, what_data: str = "我需要的信息") -> str:
    """帮我抓数据 - 把网站上的信息整理出来
    
    你可以这样说：
    - "帮我把这些网站的价格信息抓出来"
    - "我要这几个页面的联系方式"
    - "把产品信息整理一下"
    - "这个网站老是访问不了，帮我想想办法"
    
    遇到反爬虫我会自动换策略，你不用操心！
    """
    
    # 分析数据类型
    data_type = "auto"
    if "价格" in what_data or "报价" in what_data:
        data_type = "pricing"
    elif "联系" in what_data or "电话" in what_data or "邮箱" in what_data:
        data_type = "contact"
    elif "产品" in what_data or "商品" in what_data:
        data_type = "product"
    
    return f'''提取数据: {what_data}，目标网站: {websites}

📊 **数据提取计划：**

1. **智能识别阶段**
   - 数据类型: {data_type}
   - 自动选择最佳CSS选择器
   - 优化提取策略

2. **数据获取阶段**
   - 使用 crawl_smart_batch 批量处理
   - 如果遇到访问问题，自动使用 crawl_with_retry
   - 对于严格的网站，切换到 crawl_stealth

3. **数据整理阶段**
   - 清理和标准化数据格式
   - 去除重复和无效信息
   - 生成结构化数据文件

4. **结果输出**
   - 保存原始数据到 CSV/JSON 格式
   - 生成可读性报告
   - 保存到 "./.amazonq/rules/extracted_data_{data_type}.md"

🛡️ **自动处理问题：**
- 网站访问失败 → 自动重试
- 反爬虫检测 → 切换隐身模式
- 动态内容 → 等待加载完成
- 数据格式混乱 → 智能清理

开始数据提取任务...'''

@mcp.prompt()
def help_me_monitor(websites: str, watch_what: str = "内容变化") -> str:
    """帮我盯着看 - 监控网站变化，有更新就告诉你
    
    比如：
    - "帮我盯着这个网站，有新产品就告诉我"
    - "看看竞争对手有没有降价"
    - "这几个网站内容变了就提醒我"
    - "每天帮我看看有什么新动态"
    
    我会定期检查，发现变化就通知你！
    """
    
    return f'''建立监控系统，监控内容: {watch_what}，目标网站: {websites}

📈 **监控设置计划：**

1. **基线建立阶段**
   - 使用 crawl_clean 获取当前干净内容
   - 使用 crawl_with_screenshot 记录视觉状态
   - 建立内容指纹和关键指标

2. **监控配置阶段**
   - 设置监控频率（建议每日检查）
   - 配置变化检测阈值
   - 设置通知规则

3. **持续监控阶段**
   - 定期访问目标网站
   - 对比当前内容与基线
   - 识别重要变化

4. **变化报告**
   - 自动生成变化摘要
   - 标注重要更新
   - 保存历史记录

📋 **监控内容包括：**
- 页面内容变化
- 价格和产品更新  
- 新功能发布
- 结构调整

💾 **文件保存：**
- 基线数据: "./.amazonq/rules/monitor_baseline.md"
- 变化记录: "./.amazonq/rules/monitor_changes.md"
- 监控配置: "./.amazonq/rules/monitor_config.md"

🤖 **自动化特性：**
- 智能去噪，只关注重要变化
- 自动绕过反爬虫限制
- 失败自动重试
- 结构化变化报告

开始建立监控系统...'''

@mcp.prompt()
def help_me_check(website: str, check_what: str = "全面检查") -> str:
    """帮我看看这网站 - 全面体检，看看有什么问题
    
    你可以问：
    - "这网站怎么样？"
    - "为什么老是爬不到数据？"
    - "看看他们用了什么反爬虫"
    - "帮我测试一下这个网站"
    
    我会告诉你网站的情况和最佳访问策略！
    """
    
    return f'''全面检查网站: {website}，检查项目: {check_what}

🔍 **网站体检计划：**

1. **基础健康检查**
   - 使用 health_check 测试可访问性
   - 检查响应时间和状态
   - 分析基本网站信息

2. **反爬虫能力测试**
   - 普通访问测试 (crawl)
   - 隐身访问测试 (crawl_stealth)  
   - 地理位置测试 (crawl_with_geolocation)
   - 重试机制测试 (crawl_with_retry)

3. **内容分析**
   - 页面结构分析
   - 动态内容检测
   - 数据提取难度评估

4. **性能评估**
   - 加载速度测试
   - 资源使用情况
   - 移动端适配检查

📊 **检查报告包含：**
- 网站基本信息和状态
- 反爬虫机制分析
- 最佳访问策略推荐
- 数据提取建议
- 风险评估和注意事项

🛡️ **反爬虫检测项目：**
- User Agent 检测
- 浏览器指纹识别
- 访问频率限制
- IP 地理位置限制
- JavaScript 反爬虫
- 验证码机制

💡 **优化建议：**
- 推荐最佳爬取工具
- 建议访问策略
- 提供绕过方案
- 风险控制建议

📋 **保存位置：**
"./.amazonq/rules/site_audit_{website.replace('/', '_').replace(':', '')}.md"

开始网站全面体检...'''

def generate_execution_steps(analysis: Dict, strategy: Dict, websites: str) -> str:
    """生成具体执行步骤"""
    steps = []
    
    if analysis["is_stealth_needed"]:
        steps.append("   - 启用隐身模式，使用随机User Agent")
        steps.append("   - 伪装浏览器指纹，避免检测")
    
    if "access_problem" in analysis["special_scenarios"]:
        steps.append("   - 启用自动重试机制")
        steps.append("   - 如果仍然失败，尝试地理位置切换")
    
    if analysis["is_competitive"]:
        steps.append("   - 使用并发处理，提高效率")
        steps.append("   - 对比分析多个竞争对手")
    
    if analysis["data_types"]:
        data_type = analysis["data_types"][0]
        steps.append(f"   - 专门提取{data_type}相关信息")
        steps.append(f"   - 使用优化的{data_type}选择器")
    
    steps.append("   - 清理内容，去除广告和噪音")
    steps.append("   - 结构化整理数据")
    
# 导入MCP项目管理模块
from system_manager import mcp_manager

# ===== MCP项目管理工具 =====

@mcp.tool()
async def check_mcp_status(ctx: Context) -> str:
    """🔍 检查MCP状态 - 查看Context Scraper MCP服务器运行情况"""
    try:
        status_info = mcp_manager.get_mcp_server_status()
        
        response = f"# 📊 {status_info['project_name']} 状态检查\n\n"
        response += f"**项目路径**: `{status_info['project_path']}`\n\n"
        
        if status_info["success"]:
            response += "✅ **MCP服务器状态正常**\n\n"
            
            parsed = status_info["parsed_info"]
            if parsed.get("files"):
                response += "## 📁 项目文件状态\n"
                for filename, status in parsed["files"].items():
                    response += f"- {filename}: {status}\n"
                response += "\n"
            
            if parsed.get("processes"):
                response += "## 🔄 运行进程\n"
                response += f"- 运行中: {len(parsed['processes'])} 个进程\n"
                for pid in parsed["processes"]:
                    response += f"  - PID: {pid}\n"
                response += "\n"
            
            if parsed.get("version"):
                response += f"## 📦 版本信息\n- {parsed['version']}\n\n"
        else:
            response += f"❌ **MCP服务器状态异常**\n\n"
            response += f"**错误信息**: {status_info['error']}\n\n"
        
        return response
        
    except Exception as e:
        return f"❌ 检查MCP服务器状态时出错: {str(e)}"

@mcp.tool()
async def scan_mcp_junk_files(ctx: Context) -> str:
    """🗑️ 扫描MCP垃圾文件 - 检查Context Scraper项目相关的缓存和垃圾文件"""
    try:
        junk_info = mcp_manager.scan_mcp_junk_files()
        
        response = f"# 🗑️ Context Scraper MCP 垃圾文件扫描\n\n"
        response += f"**总计**: {mcp_manager.format_size(junk_info['total_size'])} ({junk_info['total_files']} 个文件)\n\n"
        
        # 扫描位置
        if junk_info["scan_locations"]:
            response += "## 📍 扫描位置\n"
            for location in junk_info["scan_locations"]:
                response += f"- {location}\n"
            response += "\n"
        
        # 分类统计
        if junk_info["categories"]:
            response += "## 📋 垃圾文件分类\n"
            for category, info in junk_info["categories"].items():
                if info["size"] > 0:
                    response += f"- **{category}**: {mcp_manager.format_size(info['size'])} ({info['files']} 个文件)\n"
            response += "\n"
        
        # 具体文件路径 (显示前10个最大的)
        if junk_info["file_details"]:
            response += "## 🔍 主要垃圾文件 (前10个)\n"
            sorted_details = sorted(junk_info["file_details"], key=lambda x: x["size"], reverse=True)[:10]
            for item in sorted_details:
                size_str = mcp_manager.format_size(item["size"])
                response += f"- `{item['path']}` - {size_str} ({item['category']})\n"
            response += "\n"
        
        # 清理建议
        if junk_info["total_size"] > 10 * 1024 * 1024:  # 大于10MB
            response += "💡 **建议**: MCP项目垃圾文件较多，建议使用 `clean_mcp_junk_files` 清理\n"
        elif junk_info["total_size"] > 1024 * 1024:  # 大于1MB
            response += "💡 **提示**: 发现一些MCP项目垃圾文件，可考虑清理\n"
        else:
            response += "✅ **状态**: MCP项目垃圾文件较少，暂不需要清理\n"
        
        return response
        
    except Exception as e:
        return f"❌ 扫描MCP垃圾文件时出错: {str(e)}"

@mcp.tool()
async def clean_mcp_junk_files(categories: str = "Python缓存,Crawl4AI缓存,临时文件", max_age_days: int = 7, ctx: Context = None) -> str:
    """🧹 清理MCP垃圾文件 - 删除Context Scraper项目相关的垃圾文件"""
    try:
        category_list = [cat.strip() for cat in categories.split(',')]
        result = mcp_manager.clean_mcp_junk_files(category_list, max_age_days)
        
        response = f"# 🧹 Context Scraper MCP 垃圾文件清理\n\n"
        
        if result["success"]:
            response += f"✅ **清理成功**\n"
            response += f"- 清理大小: {mcp_manager.format_size(result['cleaned_size'])}\n"
            response += f"- 清理文件: {result['cleaned_files']} 个\n"
            response += f"- 文件年龄: 超过 {max_age_days} 天\n"
            response += f"- 清理类别: {categories}\n\n"
            
            if result["cleaned_details"]:
                response += "## 📋 已清理文件 (前10个)\n"
                for item in result["cleaned_details"][:10]:
                    size_str = mcp_manager.format_size(item["size"])
                    response += f"- `{item['path']}` - {size_str}\n"
                
                if len(result["cleaned_details"]) > 10:
                    response += f"- ... 还有 {len(result['cleaned_details']) - 10} 个文件\n"
                response += "\n"
            
            if result["skipped_details"]:
                response += f"## ⏭️ 跳过文件: {len(result['skipped_details'])} 个\n"
                response += "- 原因: 文件太新或不在清理范围内\n\n"
        else:
            response += f"⚠️ **清理完成，但有错误**\n"
            response += f"- 成功清理: {mcp_manager.format_size(result['cleaned_size'])}\n"
            response += f"- 错误数量: {len(result['errors'])}\n\n"
            
            if result["errors"]:
                response += "## ❌ 清理错误 (前5个)\n"
                for error in result["errors"][:5]:
                    response += f"- `{error['path']}`: {error['error']}\n"
        
        return response
        
    except Exception as e:
        return f"❌ 清理MCP垃圾文件时出错: {str(e)}"

@mcp.tool()
async def get_mcp_system_info(ctx: Context) -> str:
    """💻 获取MCP系统信息 - 查看Context Scraper项目的系统资源使用情况"""
    try:
        sys_info = mcp_manager.get_mcp_system_info()
        
        if "error" in sys_info:
            return f"❌ 获取MCP系统信息失败: {sys_info['error']}"
        
        response = f"# 💻 {sys_info['project_info']['name']} 系统信息\n\n"
        
        # 项目信息
        project = sys_info["project_info"]
        response += f"## 📁 项目信息\n"
        response += f"- **项目名称**: {project['name']}\n"
        response += f"- **项目路径**: `{project['path']}`\n"
        response += f"- **项目大小**: {mcp_manager.format_size(project['size'])}\n\n"
        
        # 磁盘信息 (仅监控，不管理)
        disk = sys_info["disk"]
        response += f"## 💾 磁盘使用情况 (监控)\n"
        response += f"- **总容量**: {mcp_manager.format_size(disk['total'])}\n"
        response += f"- **已使用**: {mcp_manager.format_size(disk['used'])} ({disk['percent']:.1f}%)\n"
        response += f"- **可用空间**: {mcp_manager.format_size(disk['free'])}\n\n"
        
        # 内存信息 (仅监控)
        memory = sys_info["memory"]
        response += f"## 🧠 内存使用情况 (监控)\n"
        response += f"- **总内存**: {mcp_manager.format_size(memory['total'])}\n"
        response += f"- **已使用**: {mcp_manager.format_size(memory['used'])} ({memory['percent']:.1f}%)\n"
        response += f"- **可用内存**: {mcp_manager.format_size(memory['free'])}\n\n"
        
        # CPU信息 (仅监控)
        cpu = sys_info["cpu"]
        response += f"## ⚡ CPU使用情况 (监控)\n"
        response += f"- **CPU使用率**: {cpu['percent']:.1f}%\n"
        response += f"- **CPU核心数**: {cpu['count']}\n\n"
        
        # 健康状态提示
        response += "## 🏥 健康状态\n"
        if disk['percent'] > 90:
            response += f"⚠️ **磁盘警告**: 使用率过高 ({disk['percent']:.1f}%)，建议清理MCP垃圾文件\n"
        elif disk['percent'] > 80:
            response += f"💡 **磁盘提示**: 使用率较高 ({disk['percent']:.1f}%)，可考虑清理MCP垃圾文件\n"
        else:
            response += f"✅ **磁盘状态**: 使用率正常 ({disk['percent']:.1f}%)\n"
        
        if memory['percent'] > 90:
            response += f"⚠️ **内存警告**: 使用率过高 ({memory['percent']:.1f}%)\n"
        else:
            response += f"✅ **内存状态**: 使用率正常 ({memory['percent']:.1f}%)\n"
        
        return response
        
    except Exception as e:
        return f"❌ 获取MCP系统信息时出错: {str(e)}"

# ===== MCP项目管理提示 =====

@mcp.prompt()
def help_me_manage_mcp(what_to_do: str = "检查MCP项目状态") -> str:
    """帮我管理MCP项目 - Context Scraper MCP服务器状态、存储清理、资源监控
    
    你可以这样说：
    - "看看MCP服务器怎么样"
    - "检查一下Context Scraper状态"
    - "清理一下MCP项目的垃圾文件"
    - "MCP项目占用多少空间"
    - "Context Scraper有没有在运行"
    - "帮我清理爬虫缓存"
    
    我专门管理这个MCP项目，不会动其他系统文件！
    """
    
    # 分析用户需求
    what_to_do_lower = what_to_do.lower()
    
    if any(word in what_to_do_lower for word in ["mcp", "context scraper", "服务器", "状态", "运行", "检查"]):
        action_plan = """
🔍 **MCP服务器状态检查计划：**

1. **MCP服务器检查**
   - 使用 check_mcp_status 检查Context Scraper MCP服务器
   - 查看项目文件状态 (server.py, server_v2_enhanced.py, server_v3_smart.py)
   - 确认MCP服务器进程和版本信息

2. **项目资源监控**
   - 使用 get_mcp_system_info 获取项目相关的系统信息
   - 监控磁盘、内存、CPU使用情况
   - 评估Context Scraper项目健康状况

3. **状态报告**
   - 生成详细的MCP项目状态报告
   - 提供项目路径和文件信息
   - 给出优化建议
"""
    
    elif any(word in what_to_do_lower for word in ["清理", "垃圾", "缓存", "空间", "存储"]):
        action_plan = """
🧹 **MCP项目存储清理计划：**

1. **MCP垃圾文件扫描**
   - 使用 scan_mcp_junk_files 扫描Context Scraper相关垃圾文件
   - 检查Python缓存 (__pycache__, *.pyc)
   - 检查Crawl4AI缓存 (.crawl4ai, browser-profile-*)
   - 检查MCP日志文件 (*.log)
   - 检查临时文件 (*.tmp, .DS_Store)

2. **安全清理评估**
   - 只清理Context Scraper项目相关文件
   - 不触碰系统文件和其他项目文件
   - 根据文件年龄和类型提供清理建议

3. **执行清理操作**
   - 使用 clean_mcp_junk_files 安全清理垃圾文件
   - 优先清理Python缓存和Crawl4AI缓存
   - 保留重要的配置和日志文件

4. **清理效果验证**
   - 统计释放的磁盘空间
   - 确认清理操作的安全性
   - 提供后续维护建议
"""
    
    elif any(word in what_to_do_lower for word in ["监控", "资源", "系统", "磁盘", "内存"]):
        action_plan = """
💻 **MCP项目资源监控计划：**

1. **项目资源统计**
   - 使用 get_mcp_system_info 获取Context Scraper项目信息
   - 统计项目目录大小和文件数量
   - 监控项目相关的资源使用

2. **系统资源监控**
   - 监控磁盘使用情况 (仅监控，不管理)
   - 监控内存使用情况 (仅监控，不管理)
   - 监控CPU使用情况 (仅监控，不管理)

3. **健康状态评估**
   - 分析资源使用趋势
   - 识别潜在的存储问题
   - 提供优化建议

4. **监控报告**
   - 生成Context Scraper项目资源报告
   - 提供清理建议和优化方案
   - 设置健康状态警告阈值
"""
    
    else:
        action_plan = """
🎯 **MCP项目综合管理计划：**

1. **全面状态检查**
   - 检查Context Scraper MCP服务器运行状态
   - 获取项目相关的系统资源信息
   - 扫描MCP项目垃圾文件情况

2. **问题识别和建议**
   - 分析MCP项目健康状况
   - 识别存储和性能问题
   - 提供针对性优化建议

3. **安全维护操作**
   - 根据需要清理MCP项目垃圾文件
   - 只操作Context Scraper相关文件
   - 确保项目最佳运行状态

4. **管理报告**
   - 生成MCP项目管理报告
   - 记录执行的维护操作
   - 提供后续管理计划
"""
    
    return f'''MCP项目管理任务: {what_to_do}

{action_plan}

🤖 **我专门管理Context Scraper MCP项目：**
- MCP服务器状态监控
- 项目相关垃圾文件清理
- 项目资源使用监控
- 安全的维护操作

🛡️ **安全保证：**
- 只操作Context Scraper项目相关文件
- 不触碰系统文件和其他项目
- 清理前进行安全检查
- 提供详细操作日志

💡 **管理范围：**
- 项目路径: Context Scraper MCP Server 目录
- Python缓存: __pycache__, *.pyc 文件
- Crawl4AI缓存: .crawl4ai, browser-profile-* 目录
- MCP日志: *.log 文件
- 临时文件: *.tmp, .DS_Store 文件

开始执行MCP项目管理任务...

💡 **管理范围明确:**
- 项目路径: Context Scraper MCP Server 目录
- Python缓存: __pycache__, *.pyc 文件
- Crawl4AI缓存: .crawl4ai, browser-profile-* 目录
- MCP日志: *.log 文件
- 临时文件: *.tmp, .DS_Store 文件

🔄 **结果直接显示给用户，不保存到rules目录**'''
