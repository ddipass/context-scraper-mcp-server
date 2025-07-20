# server_v6.py - Context Scraper MCP Server V6
# 重构架构，消除偏见，支持多搜索引擎

import asyncio
import sys
import os
import json
import time
from typing import Optional, List, Dict, Any
from pathlib import Path

# V6 核心组件 (简化版)
from v6_core.intent_analyzer import analyze_user_intent, UserIntent, SearchEngineIntent, IntentType

# 继承 V5 的爬取功能 (保持兼容)
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from mcp.server.fastmcp import Context, FastMCP

# Create MCP server
mcp = FastMCP("ContextScraperV6")

# ===== V6 核心功能 =====

@mcp.prompt()
def smart_search_guide(search_query: str = "你想搜索什么？") -> str:
    """智能搜索指南 - AI驱动的搜索工具选择助手
    
    根据搜索内容智能推荐最适合的爬取工具，
    提供决策树和具体的执行建议。
    """
    
    # URL编码处理
    import urllib.parse
    encoded_query = urllib.parse.quote_plus(search_query)
    
    # 构建各搜索引擎URL
    google_url = f"https://www.google.com/search?q={encoded_query}"
    baidu_url = f"https://www.baidu.com/s?wd={encoded_query}"
    bing_url = f"https://www.bing.com/search?q={encoded_query}"
    duckduckgo_url = f"https://duckduckgo.com/?q={encoded_query}"
    
    # 智能分析搜索内容
    query_lower = search_query.lower()
    
    # 检测语言和内容类型
    has_chinese = any('\u4e00' <= char <= '\u9fff' for char in search_query)
    is_technical = any(word in query_lower for word in ['api', 'code', 'programming', '编程', '技术', 'github', 'stackoverflow'])
    is_academic = any(word in query_lower for word in ['research', 'paper', 'study', '研究', '论文', '学术'])
    is_news = any(word in query_lower for word in ['news', 'latest', '新闻', '最新'])
    is_sensitive = any(word in query_lower for word in ['privacy', 'anonymous', '隐私', '匿名'])
    
    # 智能推荐
    if has_chinese and not is_technical:
        primary_recommendation = "百度搜索"
        primary_url = baidu_url
        primary_reason = "检测到中文内容，百度对中文搜索优化更好"
    elif is_technical or is_academic:
        primary_recommendation = "Google搜索"
        primary_url = google_url
        primary_reason = "检测到技术/学术内容，Google在这方面资源更丰富"
    elif is_sensitive:
        primary_recommendation = "DuckDuckGo搜索"
        primary_url = duckduckgo_url
        primary_reason = "检测到隐私敏感内容，DuckDuckGo不跟踪用户"
    else:
        primary_recommendation = "Google搜索"
        primary_url = google_url
        primary_reason = "通用搜索，Google覆盖面最广"
    
    return f"""# 🔍 AI智能搜索助手

## 🎯 搜索分析
**查询内容**: {search_query}
**内容特征**: {'中文' if has_chinese else '英文'} | {'技术' if is_technical else ''} {'学术' if is_academic else ''} {'新闻' if is_news else ''} {'隐私' if is_sensitive else ''}

## 🚀 AI推荐方案 (优先使用)

### ⭐ 推荐: {primary_recommendation}
**推荐理由**: {primary_reason}

**立即执行**:
```
crawl_with_intelligence(
    url="{primary_url}",
    use_smart_analysis=True
)
```

## 🛠️ 其他可选方案

### 📋 基础搜索选项
| 引擎 | 适用场景 | 执行命令 |
|------|----------|----------|
| 🚀 Google | 技术、学术、国际内容 | `crawl_with_intelligence("{google_url}", True)` |
| 🇨🇳 百度 | 中文内容、本土信息 | `crawl_with_intelligence("{baidu_url}", True)` |
| 🌐 Bing | 微软生态、商业内容 | `crawl_with_intelligence("{bing_url}", True)` |
| 🔒 DuckDuckGo | 隐私保护、匿名搜索 | `crawl_with_intelligence("{duckduckgo_url}", True)` |

### 🛡️ 反爬虫选项 (遇到阻拦时使用)
| 工具 | 适用场景 | 执行命令 |
|------|----------|----------|
| 🥷 隐身模式 | 基础反爬虫检测 | `crawl_stealth("{primary_url}")` |
| 🌍 地理伪装 | 地区内容限制 | `crawl_with_geolocation("{primary_url}", "random")` |
| 🔄 重试模式 | 网站不稳定 | `crawl_with_retry("{primary_url}", 3)` |

## 🎯 决策流程

```
开始搜索
    ↓
使用AI推荐方案
    ↓
成功? → 是 → 完成 ✅
    ↓
    否
    ↓
尝试隐身模式
    ↓
成功? → 是 → 完成 ✅
    ↓
    否
    ↓
尝试地理伪装
    ↓
成功? → 是 → 完成 ✅
    ↓
    否
    ↓
使用重试模式 → 完成 ✅
```

## 💡 快速开始

1. **直接使用**: 复制上面的AI推荐命令
2. **遇到问题**: 按决策流程逐步尝试
3. **对比结果**: 使用不同引擎对比

## 🔄 高级用法

### 多引擎对比
```bash
# 对比Google和百度结果
crawl_with_intelligence("{google_url}", True)
crawl_with_intelligence("{baidu_url}", True)
```

### 组合使用 (严格防护网站)
```bash
# 先隐身，再重试
crawl_with_retry("{primary_url}", 3)  # 自动包含隐身模式
```

**🎉 开始搜索吧！优先使用上面的AI推荐方案。**









@mcp.tool()
async def v6_system_status(ctx: Context = None) -> str:
    """系统状态查看 - 显示V6系统运行状态
    
    功能:
    - 显示系统版本和基本配置
    - 显示爬取功能状态
    - 显示V6核心特性说明
    """
    
    try:
        result = "📊 **Context Scraper V6 系统状态**\n\n"
        result += f"🚀 **版本**: 6.0.0\n"
        result += f"🔍 **主要功能**: 智能网页爬取\n"
        result += f"🧠 **智能分析**: 已启用\n"
        result += f"🛡️ **隐身保护**: 内置支持\n\n"
        
        result += "🎉 **V6 核心特性**\n"
        result += "   🕷️ 智能网页爬取 - 自动优化策略\n"
        result += "   🔍 搜索指南 - 利用现有工具实现搜索\n"
        result += "   🧠 意图分析 - 智能调整爬取参数\n"
        result += "   🛡️ 反检测保护 - 内置隐身机制\n"
        result += "   🧪 Claude分析 - 实验性AI分析功能\n\n"
        
        result += "💡 **可用工具**\n"
        result += "   - smart_search_guide: 智能搜索指南\n"
        result += "   - crawl_with_intelligence: 智能爬取\n"
        result += "   - experimental_claude_analysis: Claude分析\n"
        result += "   - v6_system_status: 系统状态查看\n"
        
        return result
        
    except Exception as e:
        return f"❌ 系统状态查询失败: {str(e)}"

# ===== 实验性功能 - Claude 3.7 测试 =====

@mcp.tool()
async def experimental_claude_analysis(
    content: str,
    analysis_type: str = "general",
    enable_claude: bool = False,
    ctx: Context = None
) -> str:
    """实验性Claude分析 - 使用Claude 3.7进行内容分析(实验功能)
    
    参数:
    - content: 要分析的内容
    - analysis_type: 分析类型 (general/technical/academic/business)
    - enable_claude: 必须明确设置为True才会调用Claude API
    
    警告:
    - 这是实验性功能，需要配置Claude API密钥
    - 仅在enable_claude=True时才会实际调用Claude API
    - 默认情况下不会调用任何外部API
    """
    
    if not enable_claude:
        return """❌ Claude分析功能未启用
        
这是一个实验性功能，需要：
1. 明确设置 enable_claude=True
2. 配置Claude API密钥
3. 确认要使用外部API服务

如需启用，请使用：
experimental_claude_analysis(content="你的内容", enable_claude=True)
"""
    
    try:
        # 检查Claude配置
        claude_config_path = Path("v6_config/claude_config.json")
        if not claude_config_path.exists():
            return "❌ Claude配置文件不存在，请先配置Claude API"
        
        with open(claude_config_path, 'r', encoding='utf-8') as f:
            claude_config = json.load(f)
        
        if not claude_config.get("claude_api", {}).get("enabled", False):
            return "❌ Claude API未启用，请在配置文件中启用"
        
        api_key = claude_config.get("claude_api", {}).get("api_key", "")
        if not api_key:
            return "❌ Claude API密钥未配置"
        
        # 这里可以添加实际的Claude API调用逻辑
        # 暂时返回模拟结果
        return f"""🧪 **Claude分析结果** (实验性)

📝 **分析内容**: {content[:100]}...
🎯 **分析类型**: {analysis_type}
⚠️  **状态**: 实验性功能，Claude API调用逻辑待实现

💡 **提示**: 这个功能目前处于开发阶段，实际的Claude API集成正在完善中。
"""
        
    except Exception as e:
        return f"❌ Claude分析失败: {str(e)}"

# ===== V6 反爬虫工具 =====

@mcp.tool()
async def crawl_stealth(url: str, ctx: Context = None) -> str:
    """隐身爬取 - 使用反检测技术绕过反爬虫机制
    
    功能:
    - 随机User Agent和浏览器指纹
    - 隐藏自动化检测特征
    - 随机视窗大小
    - 反检测浏览器参数
    """
    
    try:
        # 导入反检测功能
        import sys
        sys.path.append('legacy/servers')
        from anti_detection import create_stealth_config
        
        # 使用隐身配置
        browser_config = create_stealth_config()
        crawl_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            word_count_threshold=50,
            delay_before_return_html=1  # 稍微延迟避免检测
        )
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=crawl_config)
            
            if result.success:
                # 显示伪装信息
                ua_info = browser_config.user_agent[:80] + "..." if len(browser_config.user_agent) > 80 else browser_config.user_agent
                viewport_info = f"{browser_config.viewport_width}x{browser_config.viewport_height}"
                
                response = f"🥷 **隐身爬取成功**\n\n"
                response += f"🔗 **URL**: {url}\n"
                response += f"🎭 **伪装UA**: {ua_info}\n"
                response += f"📱 **视窗**: {viewport_info}\n"
                response += f"🛡️ **反检测**: 已启用\n"
                response += f"📄 **标题**: {result.metadata.get('title', '未知')}\n"
                response += f"📊 **字数**: {len(result.markdown.split()) if result.markdown else 0}\n"
                response += f"\n📝 **内容**:\n\n{result.markdown[:3000]}..."
                
                return response
            else:
                return f"❌ 隐身爬取失败: {result.error_message}"
                
    except ImportError:
        return "❌ 反检测模块未找到，请检查legacy/servers/anti_detection.py是否存在"
    except Exception as e:
        return f"❌ 隐身爬取出错: {str(e)}"

@mcp.tool()
async def crawl_with_geolocation(url: str, location: str = "random", ctx: Context = None) -> str:
    """地理位置伪装爬取 - 模拟不同地理位置访问，绕过地区限制
    
    参数:
    - url: 目标网页URL
    - location: 地理位置 (random/newyork/london/tokyo/sydney/paris/berlin/toronto/singapore)
    
    功能:
    - 伪装GPS坐标
    - 绕过地区内容限制
    - 随机地理位置选择
    """
    
    try:
        # 导入地理位置伪装功能
        import sys
        sys.path.append('legacy/servers')
        from anti_detection import create_geo_spoofed_config
        
        # 创建地理位置伪装配置
        browser_config, geo_config = create_geo_spoofed_config(location)
        crawl_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            word_count_threshold=50
        )
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=crawl_config)
            
            if result.success:
                response = f"🌍 **地理位置伪装爬取成功**\n\n"
                response += f"🔗 **URL**: {url}\n"
                response += f"📍 **伪装位置**: 纬度 {geo_config.latitude:.4f}, 经度 {geo_config.longitude:.4f}\n"
                response += f"🎯 **精度**: {geo_config.accuracy:.1f}米\n"
                response += f"📄 **标题**: {result.metadata.get('title', '未知')}\n"
                response += f"📊 **字数**: {len(result.markdown.split()) if result.markdown else 0}\n"
                response += f"\n📝 **内容**:\n\n{result.markdown[:3000]}..."
                
                return response
            else:
                return f"❌ 地理位置伪装爬取失败: {result.error_message}"
                
    except ImportError:
        return "❌ 地理位置伪装模块未找到，请检查legacy/servers/anti_detection.py是否存在"
    except Exception as e:
        return f"❌ 地理位置伪装爬取出错: {str(e)}"

@mcp.tool()
async def crawl_with_retry(url: str, max_retries: int = 3, ctx: Context = None) -> str:
    """重试爬取 - 智能重试机制，适合不稳定或有反爬虫的网站
    
    参数:
    - url: 目标网页URL
    - max_retries: 最大重试次数 (1-5)
    
    功能:
    - 指数退避重试策略
    - 随机延迟避免检测
    - 自动切换隐身模式
    """
    
    try:
        # 导入重试管理器
        import sys
        sys.path.append('legacy/servers')
        from anti_detection import create_retry_manager, create_stealth_config
        
        retry_manager = create_retry_manager(max_retries)
        browser_config = create_stealth_config()  # 使用隐身模式提高成功率
        crawl_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            word_count_threshold=50
        )
        
        start_time = time.time()
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await retry_manager.execute_with_retry(crawler, url, crawl_config)
            
            elapsed_time = time.time() - start_time
            
            if result.success:
                response = f"🔄 **重试爬取成功**\n\n"
                response += f"🔗 **URL**: {url}\n"
                response += f"⏱️ **用时**: {elapsed_time:.2f}秒\n"
                response += f"🔁 **最大重试**: {max_retries}次\n"
                response += f"🛡️ **隐身模式**: 已启用\n"
                response += f"📄 **标题**: {result.metadata.get('title', '未知')}\n"
                response += f"📊 **字数**: {len(result.markdown.split()) if result.markdown else 0}\n"
                response += f"\n📝 **内容**:\n\n{result.markdown[:3000]}..."
                
                return response
            else:
                return f"❌ 重试爬取失败: {result.error_message}"
                
    except ImportError:
        return "❌ 重试管理模块未找到，请检查legacy/servers/anti_detection.py是否存在"
    except Exception as e:
        return f"❌ 重试爬取出错: {str(e)}"

# ===== 兼容性工具 - 继承V5功能 =====

@mcp.tool()
async def crawl_with_intelligence(
    url: str,
    use_smart_analysis: bool = True,
    ctx: Context = None
) -> str:
    """智能网页爬取 - 爬取指定网页内容并转换为Markdown格式
    
    参数:
    - url: 目标网页URL
    - use_smart_analysis: 是否启用智能分析优化爬取策略
    
    功能:
    - 爬取网页内容并转换为结构化Markdown
    - 智能分析网页类型，自动调整爬取策略
    - 支持动态内容加载的网页
    - 提供爬取结果的基本统计信息
    """
    
    try:
        # 分析URL意图
        if use_smart_analysis:
            intent = analyze_user_intent(f"爬取 {url}")
            
            # 根据意图调整爬取策略
            browser_config = BrowserConfig(
                headless=True,
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )
            
            crawl_config = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                word_count_threshold=50,
                delay_before_return_html=2 if intent.dynamic_content else 0
            )
        else:
            browser_config = BrowserConfig(headless=True)
            crawl_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
        
        # 执行爬取
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=crawl_config)
            
            if result.success:
                response = f"🕷️ **V6 智能爬取结果**\n\n"
                response += f"🔗 **URL**: {url}\n"
                response += f"📄 **标题**: {result.metadata.get('title', '未知')}\n"
                response += f"📊 **字数**: {len(result.markdown.split()) if result.markdown else 0}\n"
                
                if use_smart_analysis:
                    response += f"🧠 **智能分析**: 已启用\n"
                
                response += f"\n📝 **内容**:\n\n{result.markdown[:3000]}..."
                
                return response
            else:
                return f"❌ 爬取失败: {result.error_message}"
                
    except Exception as e:
        return f"❌ 爬取过程出错: {str(e)}"

# ===== 启动信息 =====

def show_v6_welcome():
    """显示V6启动信息"""
    print("🚀 Context Scraper V6 MCP Server")
    print("=" * 50)
    print("🔍 主要功能:")
    print("   - 智能网页爬取和内容提取")
    print("   - 搜索指南和最佳实践")
    print("   - 意图分析和策略优化")
    print("   - 实验性Claude分析功能")
    print("=" * 50)
    print("💡 使用说明:")
    print("   - smart_search_guide: 智能搜索指南")
    print("   - crawl_with_intelligence: 智能网页爬取")
    print("   - crawl_stealth: 隐身模式爬取")
    print("   - crawl_with_geolocation: 地理位置伪装")
    print("   - crawl_with_retry: 重试模式爬取")
    print("   - experimental_claude_analysis: Claude分析")
    print()
    print("🔍 搜索功能:")
    print("   使用 smart_search_guide 获取搜索指导")
    print("   利用现有爬取工具实现高效搜索")
    print("=" * 50)

if __name__ == "__main__":
    show_v6_welcome()
