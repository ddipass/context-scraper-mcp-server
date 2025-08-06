#!/usr/bin/env python3
# server_v9.py - Context Scraper MCP Server V9
# Enhanced version with unified configuration management and user-configurable parameters

import sys
import os
from pathlib import Path

# ===== 自动激活虚拟环境功能 =====
def activate_virtual_environment():
    """
    自动激活当前项目的虚拟环境
    这个函数会在导入其他模块之前执行，确保使用正确的Python环境
    支持所有Python版本，包括未来版本
    """
    # 获取当前脚本所在目录
    current_dir = Path(__file__).parent.absolute()
    venv_path = current_dir / ".venv"
    
    print(f"🔍 检查虚拟环境: {venv_path}")
    
    if venv_path.exists():
        print(f"✅ 找到虚拟环境目录: {venv_path}")
        
        # 动态检测所有可用的Python版本
        lib_path = venv_path / "lib"
        site_packages_path = None
        detected_version = None
        
        if lib_path.exists():
            print(f"🔍 扫描lib目录: {lib_path}")
            
            # 获取所有python*目录，自动支持未来版本
            python_dirs = []
            for item in lib_path.iterdir():
                if item.is_dir() and item.name.startswith('python'):
                    python_dirs.append(item.name)
            
            # 按版本号排序，优先使用最新版本
            python_dirs.sort(reverse=True)
            print(f"🔍 发现Python版本: {python_dirs}")
            
            # 查找第一个包含site-packages的版本
            for py_version in python_dirs:
                potential_path = lib_path / py_version / "site-packages"
                print(f"🔍 检查路径: {potential_path}")
                if potential_path.exists():
                    site_packages_path = potential_path
                    detected_version = py_version
                    print(f"✅ 找到可用的Python版本: {py_version}")
                    break
        
        if site_packages_path:
            # 将虚拟环境的 site-packages 添加到 sys.path 的最前面
            site_packages_str = str(site_packages_path)
            if site_packages_str not in sys.path:
                sys.path.insert(0, site_packages_str)
                print(f"✅ 虚拟环境已自动激活!")
                print(f"📦 Python版本: {detected_version}")
                print(f"📦 Site-packages路径: {site_packages_str}")
            else:
                print(f"ℹ️  虚拟环境已在sys.path中")
                print(f"📦 当前Python版本: {detected_version}")
            
            # 设置虚拟环境相关的环境变量
            os.environ['VIRTUAL_ENV'] = str(venv_path)
            
            # 更新PATH环境变量，确保使用虚拟环境的可执行文件
            venv_bin = venv_path / "bin"
            if venv_bin.exists():
                current_path = os.environ.get('PATH', '')
                if str(venv_bin) not in current_path:
                    os.environ['PATH'] = f"{venv_bin}:{current_path}"
                    print(f"🔧 PATH已更新，优先使用虚拟环境的可执行文件")
                else:
                    print(f"ℹ️  虚拟环境bin目录已在PATH中")
        else:
            print(f"⚠️  虚拟环境存在但未找到site-packages目录")
            if lib_path.exists():
                print(f"📁 lib目录内容:")
                for item in lib_path.iterdir():
                    print(f"   - {item.name} ({'目录' if item.is_dir() else '文件'})")
            else:
                print(f"📁 lib目录不存在: {lib_path}")
    else:
        print(f"⚠️  虚拟环境目录不存在: {venv_path}")
        print("💡 提示: 请确保已创建虚拟环境 (.venv)")
        print("💡 创建命令: uv sync 或 python -m venv .venv")

# 在导入任何其他模块之前激活虚拟环境
print("🚀 正在启动 Context Scraper MCP Server V9...")
activate_virtual_environment()

# ===== 导入依赖模块 =====

import asyncio
import json
import time
from typing import Optional, List, Dict, Any

# V9 core components
from v9_core.intent_analyzer import analyze_user_intent, UserIntent, SearchEngineIntent, IntentType
from v9_core.crawl_config_manager import get_crawl_config, reload_crawl_config

# Crawl4AI components
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from mcp.server.fastmcp import Context, FastMCP

# 初始化配置管理器
config = get_crawl_config()
print(f"⚙️  配置管理器已初始化")

# Create MCP server
mcp = FastMCP("ContextScraperV9")

# ===== 配置管理工具 =====

@mcp.tool()
async def configure_crawl_settings(
    action: str = "show",
    setting_type: str = "all",
    **kwargs
) -> str:
    """
    配置爬取参数设置
    
    Args:
        action: 操作类型 (show/update/reset)
        setting_type: 设置类型 (content_limits/quality_control/timing_control/user_preferences/all)
        **kwargs: 具体的配置参数
        
    Returns:
        配置操作结果
        
    Use cases:
        - 查看当前配置: configure_crawl_settings("show", "all")
        - 更新内容限制: configure_crawl_settings("update", "content_limits", markdown_display_limit=5000)
        - 更新用户偏好: configure_crawl_settings("update", "user_preferences", show_word_count=False)
    """
    
    try:
        global config
        
        if action == "show":
            if setting_type == "all":
                return config.get_config_summary()
            elif setting_type == "content_limits":
                return f"""📄 内容限制配置:
- Markdown显示限制: {config.content_limits.markdown_display_limit} 字符
- Claude预览限制: {config.content_limits.claude_preview_limit} 字符
- 基础爬取无限制: {config.content_limits.basic_crawl_unlimited}"""
            elif setting_type == "quality_control":
                return f"""🎯 质量控制配置:
- 词数阈值: {config.quality_control.word_count_threshold} 词
- 最小质量: {config.quality_control.min_content_quality}"""
            elif setting_type == "timing_control":
                return f"""⏱️ 时间控制配置:
- 页面超时: {config.timing_control.page_timeout_ms}ms
- 隐身延迟: {config.timing_control.stealth_delay_seconds}s
- 动态内容延迟: {config.timing_control.dynamic_content_delay_seconds}s"""
            elif setting_type == "user_preferences":
                return f"""👤 用户偏好设置:
- 详细日志: {config.user_preferences.show_detailed_logs}
- 显示词数: {config.user_preferences.show_word_count}
- 显示时间: {config.user_preferences.show_timing_info}
- 紧凑输出: {config.user_preferences.compact_output}"""
        
        elif action == "update":
            if setting_type == "content_limits":
                config.update_content_limits(**kwargs)
                return f"✅ 内容限制配置已更新: {kwargs}"
            elif setting_type == "quality_control":
                config.update_quality_control(**kwargs)
                return f"✅ 质量控制配置已更新: {kwargs}"
            elif setting_type == "timing_control":
                config.update_timing_control(**kwargs)
                return f"✅ 时间控制配置已更新: {kwargs}"
            elif setting_type == "user_preferences":
                config.update_user_preferences(**kwargs)
                return f"✅ 用户偏好设置已更新: {kwargs}"
        
        elif action == "reset":
            config = reload_crawl_config()
            return "✅ 配置已重置为默认值"
        
        return f"❌ 不支持的操作: action={action}, setting_type={setting_type}"
        
    except Exception as e:
        return f"❌ 配置操作失败: {str(e)}"

@mcp.tool()
async def quick_config_content_limit(limit: int = 3000) -> str:
    """
    快速设置内容显示限制
    
    Args:
        limit: 内容显示字符数限制
        
    Returns:
        设置结果
        
    Use cases:
        - 设置5000字符限制: quick_config_content_limit(5000)
        - 设置1000字符限制: quick_config_content_limit(1000)
    """
    try:
        global config
        config.update_content_limits(markdown_display_limit=limit)
        return f"✅ 内容显示限制已设置为: {limit} 字符"
    except Exception as e:
        return f"❌ 设置失败: {str(e)}"

@mcp.tool()
async def quick_config_word_threshold(threshold: int = 50) -> str:
    """
    快速设置词数阈值
    
    Args:
        threshold: 最小词数阈值
        
    Returns:
        设置结果
        
    Use cases:
        - 设置100词阈值: quick_config_word_threshold(100)
        - 设置20词阈值: quick_config_word_threshold(20)
    """
    try:
        global config
        config.update_quality_control(word_count_threshold=threshold)
        return f"✅ 词数阈值已设置为: {threshold} 词"
    except Exception as e:
        return f"❌ 设置失败: {str(e)}"

# ===== 辅助函数 =====

def format_crawl_result(result, url: str, tool_name: str, extra_info: Dict[str, Any] = None) -> str:
    """
    格式化爬取结果，使用配置管理器的设置
    
    Args:
        result: 爬取结果对象
        url: 目标URL
        tool_name: 工具名称
        extra_info: 额外信息字典
        
    Returns:
        格式化的结果字符串
    """
    global config
    
    if not result.success:
        return f"{tool_name} 失败\n\nURL: {url}\nError: {result.error_message}"
    
    # 基础信息
    response = f"{tool_name} 成功\n\nURL: {url}\n"
    
    # 标题信息
    title = result.metadata.get('title', 'Unknown')
    response += f"Title: {title}\n"
    
    # 词数统计（根据用户偏好）
    if config.user_preferences.show_word_count:
        word_count = len(result.markdown.split()) if result.markdown else 0
        response += f"Word Count: {word_count}\n"
    
    # 额外信息
    if extra_info:
        for key, value in extra_info.items():
            response += f"{key}: {value}\n"
    
    # 内容显示
    if result.markdown:
        if config.content_limits.basic_crawl_unlimited and tool_name == "Basic Crawl":
            # 基础爬取显示完整内容
            response += f"\nContent:\n\n{result.markdown}"
        else:
            # 其他工具使用配置的限制
            limit = config.content_limits.markdown_display_limit
            if len(result.markdown) > limit:
                response += f"\nContent (前{limit}字符):\n\n{result.markdown[:limit]}..."
            else:
                response += f"\nContent:\n\n{result.markdown}"
    else:
        response += "\nContent: 无内容"
    
    return response

def get_crawler_config(tool_type: str = "default") -> CrawlerRunConfig:
    """
    根据工具类型获取爬取配置
    
    Args:
        tool_type: 工具类型 (default/stealth/geolocation/retry/intelligence)
        
    Returns:
        配置好的CrawlerRunConfig对象
    """
    global config
    
    # 基础配置
    cache_mode = CacheMode.BYPASS if config.cache_control.default_cache_mode == "BYPASS" else CacheMode.ENABLED
    
    base_config = {
        "cache_mode": cache_mode,
        "word_count_threshold": config.quality_control.word_count_threshold,
    }
    
    # 根据工具类型添加特定配置
    if tool_type == "default":
        base_config.update({
            "page_timeout": config.timing_control.page_timeout_ms,
            "wait_until": config.browser_control.default_wait_until
        })
    elif tool_type == "stealth":
        base_config.update({
            "delay_before_return_html": config.timing_control.stealth_delay_seconds
        })
    elif tool_type == "intelligence":
        # 智能模式根据内容类型动态设置延迟
        base_config.update({
            "delay_before_return_html": config.timing_control.dynamic_content_delay_seconds
        })
    
    return CrawlerRunConfig(**base_config)

# ===== V6 Core Features =====

@mcp.prompt()
def smart_search_guide(search_query: str = "What do you want to search?") -> str:
    """Smart Search Guide - AI-driven search tool selection assistant
    
    Intelligently recommends the most suitable crawling tools based on search content,
    provides decision trees and specific execution suggestions.
    """
    
    # URL encoding
    import urllib.parse
    encoded_query = urllib.parse.quote_plus(search_query)
    
    # Build search engine URLs
    google_url = f"https://www.google.com/search?q={encoded_query}"
    baidu_url = f"https://www.baidu.com/s?wd={encoded_query}"
    bing_url = f"https://www.bing.com/search?q={encoded_query}"
    duckduckgo_url = f"https://duckduckgo.com/?q={encoded_query}"
    
    # Smart analysis of search content
    query_lower = search_query.lower()
    
    # Detect language and content type
    has_chinese = any('\u4e00' <= char <= '\u9fff' for char in search_query)
    
    # Technical keywords (expanded)
    technical_keywords = [
        'api', 'code', 'programming', 'github', 'stackoverflow', 'python', 'javascript', 'java', 'react', 'vue',
        'docker', 'kubernetes', 'aws', 'cloud', 'database', 'sql', 'nosql', 'mongodb', 'redis', 'nginx',
        'linux', 'ubuntu', 'centos', 'bash', 'shell', 'git', 'devops', 'ci/cd', 'jenkins', 'terraform',
        'machine learning', 'ai', 'deep learning', 'tensorflow', 'pytorch', 'data science', 'algorithm',
        'framework', 'library', 'sdk', 'compiler', 'debugger', 'ide', 'vscode', 'intellij',
        '编程', '代码', '开发', '技术', '算法', '数据库', '服务器', '云计算', '人工智能', '机器学习'
    ]
    
    # Academic keywords (expanded)
    academic_keywords = [
        'research', 'paper', 'study', 'journal', 'publication', 'thesis', 'dissertation', 'conference',
        'academic', 'scholar', 'university', 'college', 'professor', 'phd', 'master', 'bachelor',
        'citation', 'bibliography', 'peer review', 'methodology', 'analysis', 'experiment', 'survey',
        '研究', '论文', '学术', '期刊', '会议', '大学', '学者', '博士', '硕士', '实验', '调研'
    ]
    
    # News keywords (expanded)
    news_keywords = [
        'news', 'latest', 'breaking', 'update', 'report', 'announcement', 'press release', 'headline',
        'current', 'today', 'yesterday', 'recent', 'happening', 'event', 'incident', 'story',
        '新闻', '最新', '今日', '昨日', '最近', '事件', '报道', '消息', '头条', '快讯'
    ]
    
    # Privacy keywords (expanded)
    privacy_keywords = [
        'privacy', 'anonymous', 'private', 'secure', 'confidential', 'hidden', 'secret', 'vpn',
        'tor', 'encryption', 'security', 'protect', 'safe', 'incognito', 'stealth',
        '隐私', '匿名', '私密', '安全', '保护', '加密', '秘密', '隐身'
    ]
    
    is_technical = any(keyword in query_lower for keyword in technical_keywords)
    is_academic = any(keyword in query_lower for keyword in academic_keywords)
    is_news = any(keyword in query_lower for keyword in news_keywords)
    is_sensitive = any(keyword in query_lower for keyword in privacy_keywords)
    
    # Smart recommendation with priority logic
    if is_sensitive:
        # Privacy is highest priority
        primary_recommendation = "DuckDuckGo Search"
        primary_url = duckduckgo_url
        primary_reason = "Privacy-sensitive content detected, DuckDuckGo doesn't track users"
    elif is_technical:
        # Technical content gets Google
        primary_recommendation = "Google Search"
        primary_url = google_url
        primary_reason = "Technical content detected, Google has the richest technical resources"
    elif is_academic:
        # Academic content gets Google
        primary_recommendation = "Google Search"
        primary_url = google_url
        primary_reason = "Academic content detected, Google Scholar and academic resources are more comprehensive"
    else:
        # Default to Google for general English content
        primary_recommendation = "Google Search"
        primary_url = google_url
        primary_reason = "General search, Google has the widest coverage and best algorithms"
    
    # Build feature analysis display
    features = []
    if has_chinese:
        features.append("Chinese")
    else:
        features.append("English")
    
    if is_technical:
        features.append("Technical")
    if is_academic:
        features.append("Academic")
    if is_news:
        features.append("News")
    if is_sensitive:
        features.append("Privacy-Sensitive")
    
    if len(features) == 1:  # Only language detected
        features.append("General")
    
    features_display = " | ".join(features)
    
    # 获取当前配置信息
    global config
    content_limit = config.content_limits.markdown_display_limit
    
    return f"""# 🔍 AI Smart Search Assistant (V9 配置增强版)

## 📊 Search Analysis
**Query**: {search_query}
**Content Features**: {features_display}
**Confidence**: {'High' if len([f for f in [is_technical, is_academic, is_news, is_sensitive] if f]) > 0 else 'Medium'}
**Current Content Limit**: {content_limit} 字符

## 🎯 AI Recommended Solution (Use First)

### ⭐ Recommended: {primary_recommendation}
**Analysis**: {primary_reason}

**🚀 Execute Now**:
```
crawl_with_intelligence(
    url="{primary_url}",
    use_smart_analysis=True
)
```

## Other Options

### Basic Search Options
| Engine | Use Case | Command |
|--------|----------|---------|
| Google | Technical, academic, international | `crawl_with_intelligence("{google_url}", True)` |
| Baidu | Chinese content, local info | `crawl_with_intelligence("{baidu_url}", True)` |
| Bing | Microsoft ecosystem, business | `crawl_with_intelligence("{bing_url}", True)` |
| DuckDuckGo | Privacy protection, anonymous | `crawl_with_intelligence("{duckduckgo_url}", True)` |

### Anti-Detection Options (Use when blocked)
| Tool | Use Case | Command |
|------|----------|---------|
| Stealth Mode | Basic anti-bot detection | `crawl_stealth("{primary_url}")` |
| Geo Spoofing | Regional content restrictions | `crawl_with_geolocation("{primary_url}", "random")` |
| Retry Mode | Unstable websites | `crawl_with_retry("{primary_url}")` |

## 🔧 Configuration Options

### Quick Config Commands
- 调整内容限制: `quick_config_content_limit(5000)`
- 调整词数阈值: `quick_config_word_threshold(100)`
- 查看所有配置: `configure_crawl_settings("show", "all")`

## Decision Flow

```
Start Search
    ↓
Use AI Recommendation
    ↓
Success? → Yes → Done ✅
    ↓
    No
    ↓
Try Stealth Mode
    ↓
Success? → Yes → Done ✅
    ↓
    No
    ↓
Try Geo Spoofing
    ↓
Success? → Yes → Done ✅
    ↓
    No
    ↓
Use Retry Mode → Done ✅
```

## 💡 Quick Start

1. **🎯 Direct Use**: Copy the AI recommended command above
2. **🔄 If Problems**: Follow decision flow step by step  
3. **📊 Compare Results**: Use different engines for comparison
4. **🛡️ If Blocked**: Try anti-detection options
5. **⚙️ Customize**: Use config commands to adjust settings

## 📋 Pro Tips

- **First try**: Always start with AI recommendation
- **General searches**: Google usually works best
- **Privacy matters**: Use DuckDuckGo for sensitive topics
- **Getting blocked**: Try stealth mode or geo spoofing
- **Unstable sites**: Use retry mode with multiple attempts
- **Content too long**: Use `quick_config_content_limit()` to adjust

## ⚠️ Important Notes

- Use reasonable delays between requests
- Some websites may still block automated access
- Current settings can be viewed with `configure_crawl_settings("show")`

**🚀 Ready to search? Start with the AI recommended solution above!**
"""
# ===== 配置化爬取工具 =====

@mcp.tool()
async def crawl(url: str) -> str:
    """
    Basic webpage crawling with Markdown conversion (配置化版本).
    
    Args:
        url: Target webpage URL
        
    Returns:
        Webpage content in Markdown format
        
    Use cases:
        - Simple content extraction
        - Static webpage crawling  
        - Quick content preview
    """
    try:
        global config
        
        browser_config = BrowserConfig(
            headless=config.browser_control.headless_mode,
            browser_type=config.browser_control.browser_type
        )
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            crawl_config = get_crawler_config("default")
            result = await crawler.arun(url=url, config=crawl_config)
            
            return format_crawl_result(result, url, "Basic Crawl")
                
    except Exception as e:
        return f"Basic Crawl Error\n\nURL: {url}\nException: {str(e)}"

@mcp.tool()
async def crawl_stealth(url: str) -> str:
    """
    Stealth web crawling with anti-detection techniques (配置化版本).
    
    Args:
        url: Target webpage URL
        
    Returns:
        Webpage content crawled with stealth techniques
        
    Use cases:
        - Bypass anti-bot protection
        - Avoid rate limiting detection
        - Privacy-focused crawling
    """
    
    try:
        global config
        
        # Import anti-detection functionality
        import sys
        sys.path.append('legacy/servers')
        from anti_detection import create_stealth_config
        
        # Use stealth configuration
        browser_config = create_stealth_config()
        crawl_config = get_crawler_config("stealth")
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=crawl_config) 
            
            if result.success:
                # Show disguise information
                ua_info = browser_config.user_agent[:80] + "..." if len(browser_config.user_agent) > 80 else browser_config.user_agent
                viewport_info = f"{browser_config.viewport_width}x{browser_config.viewport_height}"
                
                extra_info = {
                    "Disguised UA": ua_info,
                    "Viewport": viewport_info,
                    "Anti-Detection": "Enabled",
                    "Stealth Delay": f"{config.timing_control.stealth_delay_seconds}s"
                }
                
                return format_crawl_result(result, url, "Stealth Crawling", extra_info)
            else:
                return f"Stealth crawling failed: {result.error_message}"
                
    except ImportError:
        return "Anti-detection module not found, please check legacy/servers/anti_detection.py"
    except Exception as e:
        return f"Stealth crawling error: {str(e)}"

@mcp.tool()
async def crawl_with_geolocation(url: str, location: str = "random") -> str:
    """
    Geolocation spoofing crawl to bypass regional restrictions (配置化版本).
    
    Args:
        url: Target webpage URL
        location: Geographic location (random/newyork/london/tokyo/paris/berlin/toronto/singapore/sydney)
        
    Returns:
        Webpage content with geolocation spoofing information
        
    Use cases:
        - Access region-locked content
        - Test location-based features
        - Bypass geographic restrictions
    """
    
    try:
        global config
        
        # Import geolocation spoofing functionality
        import sys
        sys.path.append('legacy/servers')
        from anti_detection import create_geo_spoofed_config
        
        # Create geolocation spoofing configuration
        browser_config, geo_config = create_geo_spoofed_config(location)
        crawl_config = get_crawler_config("geolocation")
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=crawl_config)
            
            if result.success:
                extra_info = {
                    "Spoofed Location": f"Lat {geo_config.latitude:.4f}, Lng {geo_config.longitude:.4f}",
                    "Accuracy": f"{geo_config.accuracy:.1f}m"
                }
                
                return format_crawl_result(result, url, "Geolocation Spoofing Crawl", extra_info)
            else:
                return f"Geolocation spoofing crawl failed: {result.error_message}"
                
    except ImportError:
        return "Geolocation spoofing module not found, please check legacy/servers/anti_detection.py"
    except Exception as e:
        return f"Geolocation spoofing crawl error: {str(e)}"

@mcp.tool()
async def crawl_with_retry(url: str, max_retries: Optional[int] = None) -> str:
    """
    Retry crawling with exponential backoff for unstable websites (配置化版本).
    
    Args:
        url: Target webpage URL
        max_retries: Maximum number of retry attempts (如果不指定，使用配置文件中的值)
        
    Returns:
        Webpage content with retry attempt information
        
    Use cases:
        - Handle unstable network connections
        - Retry temporarily unavailable websites
        - Overcome intermittent failures
    """
    
    try:
        global config
        
        # 使用配置文件中的重试次数，除非用户明确指定
        if max_retries is None:
            max_retries = config.retry_control.max_retries
        
        # Import retry manager
        import sys
        sys.path.append('legacy/servers')
        from anti_detection import create_retry_manager, create_stealth_config
        
        retry_manager = create_retry_manager(max_retries)
        browser_config = create_stealth_config()  # Use stealth mode to improve success rate
        crawl_config = get_crawler_config("retry")
        
        start_time = time.time()
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await retry_manager.execute_with_retry(crawler, url, crawl_config)
            
            elapsed_time = time.time() - start_time
            
            if result.success:
                extra_info = {
                    "Time Taken": f"{elapsed_time:.2f}s",
                    "Max Retries": str(max_retries),
                    "Stealth Mode": "Enabled"
                }
                
                return format_crawl_result(result, url, "Retry Crawling", extra_info)
            else:
                return f"Retry crawling failed: {result.error_message}"
                
    except ImportError:
        return "Retry management module not found, please check legacy/servers/anti_detection.py"
    except Exception as e:
        return f"Retry crawling error: {str(e)}"

@mcp.tool()
async def crawl_with_intelligence(
    url: str,
    use_smart_analysis: bool = True
) -> str:
    """
    Smart web crawling with content optimization and analysis (配置化版本).
    
    Args:
        url: Target webpage URL
        use_smart_analysis: Enable intelligent content analysis and optimization
        
    Returns:
        Optimized webpage content in Markdown format
        
    Use cases:
        - Dynamic content websites
        - Complex page structures
        - Content-heavy websites requiring optimization
    """
    
    try:
        global config
        
        # Analyze URL intent
        if use_smart_analysis and config.advanced_settings.enable_smart_analysis:
            intent = analyze_user_intent(f"crawl {url}")
            
            # Adjust crawling strategy based on intent
            browser_config = BrowserConfig(
                headless=config.browser_control.headless_mode,
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )
            
            # 动态调整延迟时间
            delay_time = config.timing_control.dynamic_content_delay_seconds if intent.dynamic_content else config.timing_control.default_delay_seconds
            
            crawl_config = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS if config.cache_control.default_cache_mode == "BYPASS" else CacheMode.ENABLED,
                word_count_threshold=config.quality_control.word_count_threshold,
                delay_before_return_html=delay_time
            )
        else:
            browser_config = BrowserConfig(headless=config.browser_control.headless_mode)
            crawl_config = get_crawler_config("intelligence")
        
        # Execute crawling
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=crawl_config)
            
            if result.success:
                extra_info = {}
                if use_smart_analysis and config.advanced_settings.enable_smart_analysis:
                    extra_info["Smart Analysis"] = "Enabled"
                
                return format_crawl_result(result, url, "V9 Smart Crawling", extra_info)
            else:
                return f"Crawling failed: {result.error_message}"
                
    except Exception as e:
        return f"Crawling process error: {str(e)}"
# ===== 实验性功能 =====

@mcp.tool()
async def experimental_claude_analysis(
    content: str,
    analysis_type: str = "general",
    enable_claude: bool = False
) -> str:
    """
    Experimental AI-powered content analysis using Claude 3.7 (配置化版本).
    
    Args:
        content: Content to analyze
        analysis_type: Analysis type (general/technical/academic/business)
        enable_claude: Must be explicitly set to True to call Claude API
        
    Returns:
        AI-powered content analysis results
        
    Use cases:
        - Advanced content summarization
        - Technical document analysis
        - Academic paper insights
        
    Warning:
        This is an experimental feature requiring Claude API configuration.
        Only calls external API when enable_claude=True.
    """
    
    if not enable_claude:
        return """Claude analysis feature not enabled
        
This is an experimental feature that requires:
1. Explicitly set enable_claude=True
2. Configure Claude API key
3. Confirm use of external API service

To enable, use:
experimental_claude_analysis(content="your content", enable_claude=True)
"""
    
    try:
        global config
        
        # Check Claude configuration
        claude_config_path = Path("v9_config/claude_config.json")
        if not claude_config_path.exists():
            return "Claude configuration file not found, please configure Claude API first"
        
        with open(claude_config_path, 'r', encoding='utf-8') as f:
            claude_config = json.load(f)
        
        if not claude_config.get("claude_api", {}).get("enabled", False):
            return "Claude API not enabled, please enable in configuration file"
        
        api_key = claude_config.get("claude_api", {}).get("api_key", "")
        if not api_key:
            return "Claude API key not configured"
        
        # 使用配置管理器的预览限制
        preview_limit = config.content_limits.claude_preview_limit
        content_preview = content[:preview_limit] if len(content) > preview_limit else content
        
        # Here you can add actual Claude API call logic
        # Currently returning mock results
        return f"""Claude Analysis Results (Experimental)

Content Preview ({preview_limit} chars): {content_preview}{'...' if len(content) > preview_limit else ''}
Analysis Type: {analysis_type}
Status: Experimental feature, Claude API call logic to be implemented

Note: This feature is currently in development, actual Claude API integration is being improved.
Preview limit can be adjusted with: configure_crawl_settings("update", "content_limits", claude_preview_limit=200)
"""
        
    except Exception as e:
        return f"Claude analysis failed: {str(e)}"

# ===== 系统状态和信息工具 =====

@mcp.tool()
async def system_status() -> str:
    """
    Display system status and available tools information (配置化版本).
    
    Returns:
        Current system status, version info, and tool availability
        
    Use cases:
        - Check system health
        - View available tools
        - Verify server configuration
    """
    try:
        global config
        
        # 检测当前Python版本
        current_python = f"Python {sys.version.split()[0]}"
        
        # 检测虚拟环境状态
        venv_status = "未激活"
        venv_path = Path(__file__).parent.absolute() / ".venv"
        if venv_path.exists() and os.environ.get('VIRTUAL_ENV'):
            venv_status = f"已激活 ({venv_path})"
        
        status_info = f"""Context Scraper MCP Server V9

Version: 9.0.0
Status: Active
Python: {current_python}
Virtual Environment: {venv_status}
Enhancement: Unified Configuration Management + User Configurable Parameters
Total Tools: 10

Available Tools:
• crawl - Basic webpage crawling (配置化)
• crawl_with_intelligence - Smart crawling with optimization (配置化)
• crawl_stealth - Anti-detection crawling (配置化)
• crawl_with_retry - Retry mechanism for unstable sites (配置化)
• crawl_with_geolocation - Geographic location spoofing (配置化)
• experimental_claude_analysis - AI content analysis (配置化)
• configure_crawl_settings - 配置管理工具
• quick_config_content_limit - 快速设置内容限制
• quick_config_word_threshold - 快速设置词数阈值
• system_status - Display system information

V9 New Features:
- ✅ Unified configuration management
- 🔧 User-configurable parameters
- 📦 Dynamic Python version detection (支持所有版本，包括未来版本)
- 🚀 No manual 'source .venv/bin/activate' required
- 🔍 Smart lib directory scanning
- 📋 Detailed startup diagnostics
- ⚙️ Real-time configuration updates

Current Configuration:
- 📄 Content Display Limit: {config.content_limits.markdown_display_limit} chars
- 🎯 Word Count Threshold: {config.quality_control.word_count_threshold} words
- ⏱️ Page Timeout: {config.timing_control.page_timeout_ms}ms
- 🔄 Max Retries: {config.retry_control.max_retries}
- 👤 Show Word Count: {config.user_preferences.show_word_count}
- 👤 Show Detailed Logs: {config.user_preferences.show_detailed_logs}

Configuration Management:
- 🔧 View all settings: configure_crawl_settings("show", "all")
- ⚡ Quick content limit: quick_config_content_limit(5000)
- ⚡ Quick word threshold: quick_config_word_threshold(100)
- 🔄 Reset to defaults: configure_crawl_settings("reset")

System: Ready for web crawling operations with unified configuration management"""

        return status_info
        
    except Exception as e:
        return f"System Status Error: {str(e)}"

# ===== 启动信息 =====

def show_v9_welcome():
    """Display V9 startup information"""
    global config
    
    print("Context Scraper V9 MCP Server")
    print("=" * 50)
    print("🆕 V9 New Features:")
    print("   ✅ Unified configuration management")
    print("   🔧 User-configurable parameters")
    print("   📦 Dynamic Python version detection (支持未来版本)")
    print("   🚀 No manual activation required")
    print("   🔍 Smart lib directory scanning")
    print("   📋 Detailed startup diagnostics")
    print("   ⚙️ Real-time configuration updates")
    print()
    print("Configuration Status:")
    print(f"   📄 Content Limit: {config.content_limits.markdown_display_limit} chars")
    print(f"   🎯 Word Threshold: {config.quality_control.word_count_threshold} words")
    print(f"   ⏱️ Page Timeout: {config.timing_control.page_timeout_ms}ms")
    print(f"   👤 Show Word Count: {config.user_preferences.show_word_count}")
    print()
    print("Python Version Support:")
    print("   🎯 Current: All existing Python versions")
    print("   🚀 Future-proof: Automatically detects new versions")
    print("   🔄 Dynamic: Scans .venv/lib/ for python* directories")
    print("   📊 Priority: Uses latest available version")
    print()
    print("Main Features:")
    print("   - Smart web crawling and content extraction")
    print("   - Search guide and best practices")
    print("   - Intent analysis and strategy optimization")
    print("   - Experimental Claude analysis feature")
    print("   - Unified configuration management")
    print("=" * 50)
    print("Usage Instructions:")
    print("   - smart_search_guide: Smart search guide")
    print("   - crawl_with_intelligence: Smart web crawling")
    print("   - crawl_stealth: Stealth mode crawling")
    print("   - crawl_with_geolocation: Geolocation spoofing")
    print("   - crawl_with_retry: Retry mode crawling")
    print("   - experimental_claude_analysis: Claude analysis")
    print("   - configure_crawl_settings: Configuration management")
    print()
    print("Configuration Commands:")
    print("   - configure_crawl_settings('show', 'all'): View all settings")
    print("   - quick_config_content_limit(5000): Set content limit")
    print("   - quick_config_word_threshold(100): Set word threshold")
    print()
    print("Search Function:")
    print("   Use smart_search_guide to get search guidance")
    print("   Use existing crawling tools for efficient search")
    print("=" * 50)

if __name__ == "__main__":
    show_v9_welcome()
