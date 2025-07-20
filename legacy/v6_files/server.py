# server.py - Context Scraper MCP Server V6
# Clean version without problematic characters

import asyncio
import sys
import os
import json
import time
from typing import Optional, List, Dict, Any
from pathlib import Path

# V6 core components (simplified)
from v6_core.intent_analyzer import analyze_user_intent, UserIntent, SearchEngineIntent, IntentType

# Inherit V5 crawling functionality (maintain compatibility)
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from mcp.server.fastmcp import Context, FastMCP

# Create MCP server
mcp = FastMCP("ContextScraperV6")

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

# ===== V6 Anti-Detection Tools =====

@mcp.tool()
async def crawl_stealth(url: str, ctx: Context = None) -> str:
    """Stealth Crawling - Use anti-detection techniques to bypass anti-bot mechanisms
    
    Features:
    - Random User Agent and browser fingerprints
    - Hide automation detection features
    - Random viewport sizes
    - Anti-detection browser parameters
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
async def crawl_with_geolocation(url: str, location: str = "random", ctx: Context = None) -> str:
    """Geolocation Spoofing Crawl - Simulate access from different geographic locations
    
    Parameters:
    - url: Target webpage URL
    - location: Geographic location (random/newyork/london/tokyo/sydney/paris/berlin/toronto/singapore)
    
    Features:
    - Spoof GPS coordinates
    - Bypass regional content restrictions
    - Random geographic location selection
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
async def crawl_with_retry(url: str, max_retries: int = 3, ctx: Context = None) -> str:
    """Retry Crawling - Smart retry mechanism for unstable or anti-bot websites
    
    Parameters:
    - url: Target webpage URL
    - max_retries: Maximum retry attempts (1-5)
    
    Features:
    - Exponential backoff retry strategy
    - Random delays to avoid detection
    - Automatic stealth mode switching
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
    use_smart_analysis: bool = True,
    ctx: Context = None
) -> str:
    """Smart Web Crawling - Crawl specified webpage content and convert to Markdown format
    
    Parameters:
    - url: Target webpage URL
    - use_smart_analysis: Whether to enable smart analysis to optimize crawling strategy
    
    Features:
    - Crawl webpage content and convert to structured Markdown
    - Smart analysis of webpage types, automatically adjust crawling strategy
    - Support dynamic content loading webpages
    - Provide basic statistics of crawling results
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
                response = f"V6 Smart Crawling Results\n\n"
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
    enable_claude: bool = False,
    ctx: Context = None
) -> str:
    """Experimental Claude Analysis - Use Claude 3.7 for content analysis (experimental feature)
    
    Parameters:
    - content: Content to analyze
    - analysis_type: Analysis type (general/technical/academic/business)
    - enable_claude: Must be explicitly set to True to call Claude API
    
    Warning:
    - This is an experimental feature that requires Claude API key configuration
    - Only calls Claude API when enable_claude=True
    - Does not call any external APIs by default
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
async def v6_system_status(ctx: Context = None) -> str:
    """System Status View - Display V6 system running status
    
    Features:
    - Display system version and basic configuration
    - Display crawling function status
    - Display V6 core features description
    """
    
    try:
        result = "Context Scraper V6 System Status\n\n"
        result += f"Version: 6.0.0\n"
        result += f"Main Function: Smart Web Crawling\n"
        result += f"Smart Analysis: Enabled\n"
        result += f"Stealth Protection: Built-in Support\n\n"
        
        result += "V6 Core Features\n"
        result += "   Smart Web Crawling - Auto-optimize strategy\n"
        result += "   Search Guide - Use existing tools for search\n"
        result += "   Intent Analysis - Smart adjust crawling parameters\n"
        result += "   Anti-Detection Protection - Built-in stealth mechanism\n"
        result += "   Claude Analysis - Experimental AI analysis feature\n\n"
        
        result += "Available Tools\n"
        result += "   - smart_search_guide: Smart search guide\n"
        result += "   - crawl_with_intelligence: Smart crawling\n"
        result += "   - crawl_stealth: Stealth mode crawling\n"
        result += "   - crawl_with_geolocation: Geolocation spoofing\n"
        result += "   - crawl_with_retry: Retry mode crawling\n"
        result += "   - experimental_claude_analysis: Claude analysis\n"
        result += "   - v6_system_status: System status view\n"
        
        return result
        
    except Exception as e:
        return f"System status query failed: {str(e)}"

# ===== Startup Information =====

def show_v6_welcome():
    """Display V6 startup information"""
    print("Context Scraper V6 MCP Server")
    print("=" * 50)
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
    show_v6_welcome()
