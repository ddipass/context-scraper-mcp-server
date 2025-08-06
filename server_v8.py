#!/usr/bin/env python3
# server_v8.py - Context Scraper MCP Server V8
# Enhanced version with automatic virtual environment activation

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
print("🚀 正在启动 Context Scraper MCP Server V8...")
activate_virtual_environment()

# ===== 以下是完整的 server_v7.py 内容 =====

# server_v7.py - Context Scraper MCP Server V7
# Professional version with optimized tool descriptions and standardized parameters

import asyncio
import json
import time
from typing import Optional, List, Dict, Any

# V6 core components (simplified)
from v6_core.intent_analyzer import analyze_user_intent, UserIntent, SearchEngineIntent, IntentType

# Inherit V5 crawling functionality (maintain compatibility)
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from mcp.server.fastmcp import Context, FastMCP

# Create MCP server
mcp = FastMCP("ContextScraperV8")

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
    
    return f"""# 🔍 AI Smart Search Assistant

## 📊 Search Analysis
**Query**: {search_query}
**Content Features**: {features_display}
**Confidence**: {'High' if len([f for f in [is_technical, is_academic, is_news, is_sensitive] if f]) > 0 else 'Medium'}

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
| Retry Mode | Unstable websites | `crawl_with_retry("{primary_url}", 3)` |

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

## 📋 Pro Tips

- **First try**: Always start with AI recommendation
- **General searches**: Google usually works best
- **Privacy matters**: Use DuckDuckGo for sensitive topics
- **Getting blocked**: Try stealth mode or geo spoofing
- **Unstable sites**: Use retry mode with multiple attempts

## ⚠️ Important Notes

- Use reasonable delays between requests
- Some websites may still block automated access

**🚀 Ready to search? Start with the AI recommended solution above!**
"""

# ===== Basic Crawling Tool =====

@mcp.tool()
async def crawl(url: str) -> str:
    """
    Basic webpage crawling with Markdown conversion.
    
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
        browser_config = BrowserConfig(headless=True, browser_type="chromium")
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            config = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                page_timeout=30000,
                wait_until="domcontentloaded"
            )
            
            result = await crawler.arun(url=url, config=config)
            
            if result.success:
                return f"Basic Crawl Success\n\nURL: {url}\nTitle: {result.metadata.get('title', 'N/A')}\nWord Count: {len(result.markdown.split())}\n\nContent:\n\n{result.markdown}"
            else:
                return f"Basic Crawl Failed\n\nURL: {url}\nError: {result.error_message}"
                
    except Exception as e:
        return f"Basic Crawl Error\n\nURL: {url}\nException: {str(e)}"

# ===== V6 Anti-Detection Tools =====

@mcp.tool()
async def crawl_stealth(url: str) -> str:
    """
    Stealth web crawling with anti-detection techniques.
    
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
        # Import anti-detection functionality
        import sys
        sys.path.append('legacy/servers')
        from anti_detection import create_stealth_config
        
        # Use stealth configuration
        browser_config = create_stealth_config()
        crawl_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            word_count_threshold=50,
            delay_before_return_html=1  # Slight delay to avoid detection
        )
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=crawl_config) 
            if result.success:
                # Show disguise information
                ua_info = browser_config.user_agent[:80] + "..." if len(browser_config.user_agent) > 80 else browser_config.user_agent
                viewport_info = f"{browser_config.viewport_width}x{browser_config.viewport_height}"
                
                response = f"Stealth Crawling Success\n\n"
                response += f"URL: {url}\n"
                response += f"Disguised UA: {ua_info}\n"
                response += f"Viewport: {viewport_info}\n"
                response += f"Anti-Detection: Enabled\n"
                response += f"Title: {result.metadata.get('title', 'Unknown')}\n"
                response += f"Word Count: {len(result.markdown.split()) if result.markdown else 0}\n"
                response += f"\nContent:\n\n{result.markdown[:3000]}..."
                
                return response
            else:
                return f"Stealth crawling failed: {result.error_message}"
                
    except ImportError:
        return "Anti-detection module not found, please check legacy/servers/anti_detection.py"
    except Exception as e:
        return f"Stealth crawling error: {str(e)}"

@mcp.tool()
async def crawl_with_geolocation(url: str, location: str = "random") -> str:
    """
    Geolocation spoofing crawl to bypass regional restrictions.
    
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
        # Import geolocation spoofing functionality
        import sys
        sys.path.append('legacy/servers')
        from anti_detection import create_geo_spoofed_config
        
        # Create geolocation spoofing configuration
        browser_config, geo_config = create_geo_spoofed_config(location)
        crawl_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            word_count_threshold=50
        )
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=crawl_config)
            
            if result.success:
                response = f"Geolocation Spoofing Crawl Success\n\n"
                response += f"URL: {url}\n"
                response += f"Spoofed Location: Lat {geo_config.latitude:.4f}, Lng {geo_config.longitude:.4f}\n"
                response += f"Accuracy: {geo_config.accuracy:.1f}m\n"
                response += f"Title: {result.metadata.get('title', 'Unknown')}\n"
                response += f"Word Count: {len(result.markdown.split()) if result.markdown else 0}\n"
                response += f"\nContent:\n\n{result.markdown[:3000]}..."
                
                return response
            else:
                return f"Geolocation spoofing crawl failed: {result.error_message}"
                
    except ImportError:
        return "Geolocation spoofing module not found, please check legacy/servers/anti_detection.py"
    except Exception as e:
        return f"Geolocation spoofing crawl error: {str(e)}"

@mcp.tool()
async def crawl_with_retry(url: str, max_retries: int = 3) -> str:
    """
    Retry crawling with exponential backoff for unstable websites.
    
    Args:
        url: Target webpage URL
        max_retries: Maximum number of retry attempts (1-5)
        
    Returns:
        Webpage content with retry attempt information
        
    Use cases:
        - Handle unstable network connections
        - Retry temporarily unavailable websites
        - Overcome intermittent failures
    """
    
    try:
        # Import retry manager
        import sys
        sys.path.append('legacy/servers')
        from anti_detection import create_retry_manager, create_stealth_config
        
        retry_manager = create_retry_manager(max_retries)
        browser_config = create_stealth_config()  # Use stealth mode to improve success rate
        crawl_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            word_count_threshold=50
        )
        
        start_time = time.time()
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await retry_manager.execute_with_retry(crawler, url, crawl_config)
            
            elapsed_time = time.time() - start_time
            
            if result.success:
                response = f"Retry Crawling Success\n\n"
                response += f"URL: {url}\n"
                response += f"Time Taken: {elapsed_time:.2f}s\n"
                response += f"Max Retries: {max_retries}\n"
                response += f"Stealth Mode: Enabled\n"
                response += f"Title: {result.metadata.get('title', 'Unknown')}\n"
                response += f"Word Count: {len(result.markdown.split()) if result.markdown else 0}\n"
                response += f"\nContent:\n\n{result.markdown[:3000]}..."
                
                return response
            else:
                return f"Retry crawling failed: {result.error_message}"
                
    except ImportError:
        return "Retry management module not found, please check legacy/servers/anti_detection.py"
    except Exception as e:
        return f"Retry crawling error: {str(e)}"

# ===== Compatibility Tools - Inherit V5 Features =====

@mcp.tool()
async def crawl_with_intelligence(
    url: str,
    use_smart_analysis: bool = True
) -> str:
    """
    Smart web crawling with content optimization and analysis.
    
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
        # Analyze URL intent
        if use_smart_analysis:
            intent = analyze_user_intent(f"crawl {url}")
            
            # Adjust crawling strategy based on intent
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
        
        # Execute crawling
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=crawl_config)
            
            if result.success:
                response = f"V8 Smart Crawling Results\n\n"
                response += f"URL: {url}\n"
                response += f"Title: {result.metadata.get('title', 'Unknown')}\n"
                response += f"Word Count: {len(result.markdown.split()) if result.markdown else 0}\n"
                
                if use_smart_analysis:
                    response += f"Smart Analysis: Enabled\n"
                
                response += f"\nContent:\n\n{result.markdown[:3000]}..."
                
                return response
            else:
                return f"Crawling failed: {result.error_message}"
                
    except Exception as e:
        return f"Crawling process error: {str(e)}"

# ===== Experimental Features - Claude 3.7 Testing =====

@mcp.tool()
async def experimental_claude_analysis(
    content: str,
    analysis_type: str = "general",
    enable_claude: bool = False
) -> str:
    """
    Experimental AI-powered content analysis using Claude 3.7.
    
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
        # Check Claude configuration
        claude_config_path = Path("v6_config/claude_config.json")
        if not claude_config_path.exists():
            return "Claude configuration file not found, please configure Claude API first"
        
        with open(claude_config_path, 'r', encoding='utf-8') as f:
            claude_config = json.load(f)
        
        if not claude_config.get("claude_api", {}).get("enabled", False):
            return "Claude API not enabled, please enable in configuration file"
        
        api_key = claude_config.get("claude_api", {}).get("api_key", "")
        if not api_key:
            return "Claude API key not configured"
        
        # Here you can add actual Claude API call logic
        # Currently returning mock results
        return f"""Claude Analysis Results (Experimental)

Content: {content[:100]}...
Analysis Type: {analysis_type}
Status: Experimental feature, Claude API call logic to be implemented

Note: This feature is currently in development, actual Claude API integration is being improved.
"""
        
    except Exception as e:
        return f"Claude analysis failed: {str(e)}"

@mcp.tool()
async def system_status() -> str:
    """
    Display system status and available tools information.
    
    Returns:
        Current system status, version info, and tool availability
        
    Use cases:
        - Check system health
        - View available tools
        - Verify server configuration
    """
    try:
        # 检测当前Python版本
        current_python = f"Python {sys.version.split()[0]}"
        
        # 检测虚拟环境状态
        venv_status = "未激活"
        venv_path = Path(__file__).parent.absolute() / ".venv"
        if venv_path.exists() and os.environ.get('VIRTUAL_ENV'):
            venv_status = f"已激活 ({venv_path})"
        
        status_info = f"""Context Scraper MCP Server V8

Version: 8.0.0
Status: Active
Python: {current_python}
Virtual Environment: {venv_status}
Enhancement: Dynamic Python Version Detection
Total Tools: 7

Available Tools:
• crawl - Basic webpage crawling
• crawl_with_intelligence - Smart crawling with optimization  
• crawl_stealth - Anti-detection crawling
• crawl_with_retry - Retry mechanism for unstable sites
• crawl_with_geolocation - Geographic location spoofing
• experimental_claude_analysis - AI content analysis (experimental)
• system_status - Display system information

V8 New Features:
- ✅ Automatic virtual environment activation
- 🔧 Enhanced PATH management
- 📦 Dynamic Python version detection (支持所有版本，包括未来版本)
- 🚀 No manual 'source .venv/bin/activate' required
- 🔍 Smart lib directory scanning
- 📋 Detailed startup diagnostics

Python Version Support:
- 🎯 Current: Supports all existing Python versions
- 🚀 Future-proof: Automatically detects new Python versions
- 🔄 Dynamic: Scans .venv/lib/ directory for python* folders
- 📊 Priority: Uses the latest available version

System: Ready for web crawling operations with auto-activated environment"""

        return status_info
        
    except Exception as e:
        return f"System Status Error: {str(e)}"

# ===== Startup Information =====

def show_v8_welcome():
    """Display V8 startup information"""
    print("Context Scraper V8 MCP Server")
    print("=" * 50)
    print("🆕 V8 New Features:")
    print("   ✅ Automatic virtual environment activation")
    print("   🔧 Enhanced dependency management")
    print("   📦 Dynamic Python version detection (支持未来版本)")
    print("   🚀 No manual activation required")
    print("   🔍 Smart lib directory scanning")
    print("   📋 Detailed startup diagnostics")
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
    print("=" * 50)
    print("Usage Instructions:")
    print("   - smart_search_guide: Smart search guide")
    print("   - crawl_with_intelligence: Smart web crawling")
    print("   - crawl_stealth: Stealth mode crawling")
    print("   - crawl_with_geolocation: Geolocation spoofing")
    print("   - crawl_with_retry: Retry mode crawling")
    print("   - experimental_claude_analysis: Claude analysis")
    print()
    print("Search Function:")
    print("   Use smart_search_guide to get search guidance")
    print("   Use existing crawling tools for efficient search")
    print("=" * 50)

if __name__ == "__main__":
    show_v8_welcome()
