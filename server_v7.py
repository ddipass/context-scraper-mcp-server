# server_v7.py - Context Scraper MCP Server V7
# Professional version with optimized tool descriptions and standardized parameters

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
mcp = FastMCP("ContextScraperV7")

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
        status_info = """Context Scraper MCP Server V7

Version: 7.0.0
Status: Active
Total Tools: 7

Available Tools:
• crawl - Basic webpage crawling
• crawl_with_intelligence - Smart crawling with optimization  
• crawl_stealth - Anti-detection crawling
• crawl_with_retry - Retry mechanism for unstable sites
• crawl_with_geolocation - Geographic location spoofing
• experimental_claude_analysis - AI content analysis (experimental)
• system_status - Display system information

Features:
- Professional tool descriptions
- Standardized parameters
- Enhanced error handling
- Comprehensive crawling capabilities

System: Ready for web crawling operations"""

        return status_info
        
    except Exception as e:
        return f"System Status Error: {str(e)}"

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
