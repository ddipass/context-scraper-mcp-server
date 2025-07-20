# server_v6.py - Context Scraper MCP Server V6
# 重构架构，消除偏见，支持多搜索引擎

import asyncio
import sys
import os
import json
import time
from typing import Optional, List, Dict, Any
from pathlib import Path

# V6 核心组件
from v6_core.config_manager import get_config, get_user_preferences
from v6_core.intent_analyzer import analyze_user_intent, UserIntent, SearchEngineIntent
from v6_core.search_manager import search_with_intent, search_manager

# 继承 V5 的爬取功能 (保持兼容)
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from mcp.server.fastmcp import Context, FastMCP

# Create MCP server
mcp = FastMCP("ContextScraperV6")

# ===== V6 核心功能 =====

@mcp.tool()
async def search_with_engine(
    query: str,
    engine: str = None,
    max_results: int = 10,
    ctx: Context = None
) -> str:
    """🔍 V6 智能搜索 - 支持多搜索引擎，尊重用户选择
    
    参数:
    - query: 搜索查询词
    - engine: 指定搜索引擎 (google/baidu/bing/yahoo/duckduckgo)
    - max_results: 最大结果数量
    
    特性:
    - 🎯 严格遵循用户指定的搜索引擎
    - 🔄 智能回退机制
    - 🌐 支持多语言和地区偏好
    - ⚡ 并发搜索优化
    """
    
    try:
        # 分析用户意图
        intent = analyze_user_intent(f"{engine or ''} {query}".strip())
        
        # 如果用户明确指定了搜索引擎，强制使用
        if engine:
            intent.search_engine = engine.lower()
            intent.search_engine_intent = SearchEngineIntent.EXPLICIT
        
        # 执行搜索
        response = await search_with_intent(query, intent, max_results)
        
        if response.success and response.results:
            # 格式化搜索结果
            result_text = f"🔍 **搜索结果** (引擎: {response.engine})\n"
            result_text += f"📊 查询: {response.query}\n"
            result_text += f"⏱️ 用时: {response.search_time:.2f}秒\n"
            result_text += f"📈 结果数: {len(response.results)}\n\n"
            
            for i, result in enumerate(response.results, 1):
                result_text += f"**{i}. {result.title}**\n"
                result_text += f"🔗 {result.url}\n"
                if result.snippet:
                    result_text += f"📝 {result.snippet}\n"
                result_text += "\n"
            
            return result_text
        else:
            error_msg = f"❌ 搜索失败\n"
            error_msg += f"🔍 查询: {query}\n"
            error_msg += f"🔧 引擎: {response.engine}\n"
            if response.error_message:
                error_msg += f"💬 错误: {response.error_message}\n"
            
            return error_msg
            
    except Exception as e:
        return f"❌ 搜索过程出错: {str(e)}"

@mcp.tool()
async def smart_research_v6(
    research_query: str,
    preferred_engine: str = None,
    depth: str = "standard",
    ctx: Context = None
) -> str:
    """🧠 V6 智能研究助手 - 基于搜索结果的深度研究
    
    参数:
    - research_query: 研究问题
    - preferred_engine: 首选搜索引擎
    - depth: 研究深度 (quick/standard/deep)
    
    特性:
    - 🎯 意图驱动的研究策略
    - 🔍 多引擎搜索聚合
    - 📊 结构化研究报告
    - 🚀 实时进度反馈
    """
    
    try:
        start_time = time.time()
        
        # 分析研究意图
        intent = analyze_user_intent(f"{preferred_engine or ''} {research_query}".strip())
        
        if preferred_engine:
            intent.search_engine = preferred_engine.lower()
            intent.search_engine_intent = SearchEngineIntent.EXPLICIT
        
        # 生成搜索关键词
        search_keywords = intent.search_keywords or [research_query]
        
        # 执行多轮搜索
        all_results = []
        for keyword in search_keywords[:3]:  # 限制关键词数量
            response = await search_with_intent(keyword, intent, 5)
            if response.success:
                all_results.extend(response.results)
        
        if not all_results:
            return f"❌ 未找到相关搜索结果: {research_query}"
        
        # 去重和排序
        unique_results = {}
        for result in all_results:
            if result.url not in unique_results:
                unique_results[result.url] = result
        
        sorted_results = sorted(unique_results.values(), key=lambda x: x.rank)
        
        # 根据深度决定爬取数量
        crawl_count = {"quick": 2, "standard": 5, "deep": 10}.get(depth, 5)
        
        # 爬取详细内容
        detailed_content = []
        for result in sorted_results[:crawl_count]:
            try:
                browser_config = BrowserConfig(headless=True)
                async with AsyncWebCrawler(config=browser_config) as crawler:
                    crawl_result = await crawler.arun(
                        url=result.url,
                        config=CrawlerRunConfig(
                            cache_mode=CacheMode.BYPASS,
                            word_count_threshold=100
                        )
                    )
                    
                    if crawl_result.success and crawl_result.markdown:
                        detailed_content.append({
                            "title": result.title,
                            "url": result.url,
                            "content": crawl_result.markdown[:2000]  # 限制长度
                        })
            except Exception as e:
                continue
        
        # 生成研究报告
        elapsed_time = time.time() - start_time
        
        report = f"📋 **V6 智能研究报告**\n\n"
        report += f"🎯 **研究主题**: {research_query}\n"
        report += f"🔍 **搜索引擎**: {intent.search_engine or '智能选择'}\n"
        report += f"📊 **研究深度**: {depth}\n"
        report += f"⏱️ **用时**: {elapsed_time:.2f}秒\n"
        report += f"📈 **数据源**: {len(detailed_content)}个网站\n\n"
        
        # 意图分析结果
        if intent.search_engine_intent == SearchEngineIntent.EXPLICIT:
            report += f"✅ **用户指定搜索引擎**: {intent.search_engine} (已严格遵循)\n\n"
        
        # 搜索结果摘要
        report += f"## 🔍 搜索结果摘要\n\n"
        for i, result in enumerate(sorted_results[:10], 1):
            report += f"**{i}. {result.title}**\n"
            report += f"   🔗 {result.url}\n"
            if result.snippet:
                report += f"   📝 {result.snippet[:200]}...\n"
            report += "\n"
        
        # 详细内容分析
        if detailed_content:
            report += f"## 📊 详细内容分析\n\n"
            for i, content in enumerate(detailed_content, 1):
                report += f"### {i}. {content['title']}\n\n"
                report += f"🔗 来源: {content['url']}\n\n"
                report += f"📄 内容摘要:\n{content['content'][:1000]}...\n\n"
                report += "---\n\n"
        
        return report
        
    except Exception as e:
        return f"❌ 研究过程出错: {str(e)}"

@mcp.tool()
async def configure_search_engines(
    action: str,
    engine: str = None,
    setting: str = None,
    value: str = None,
    ctx: Context = None
) -> str:
    """⚙️ V6 搜索引擎配置管理
    
    参数:
    - action: 操作类型 (list/enable/disable/set_default/set_priority)
    - engine: 搜索引擎名称
    - setting: 设置项
    - value: 设置值
    
    示例:
    - list: 列出所有搜索引擎
    - enable google: 启用Google搜索
    - set_default baidu: 设置百度为默认搜索引擎
    """
    
    try:
        config = get_config()
        
        if action == "list":
            # 列出所有搜索引擎
            engines_info = search_manager.get_engine_info()
            
            result = "🔧 **搜索引擎配置**\n\n"
            result += f"🎯 **默认引擎**: {config.user_preferences.default_search_engine}\n"
            result += f"✅ **严格遵循用户指定**: {config.user_preferences.respect_explicit_engine}\n"
            result += f"🔄 **自动回退**: {config.user_preferences.auto_fallback}\n\n"
            
            result += "## 📋 可用搜索引擎\n\n"
            
            for name, info in engines_info.items():
                status = "✅ 启用" if info["enabled"] else "❌ 禁用"
                result += f"**{info['name']}** ({name})\n"
                result += f"   状态: {status}\n"
                result += f"   优先级: {info['priority']}\n"
                result += f"   超时: {info['timeout']}秒\n"
                result += f"   最大结果: {info['max_results']}\n\n"
            
            return result
            
        elif action == "enable" and engine:
            config.enable_search_engine(engine)
            return f"✅ 已启用搜索引擎: {engine}"
            
        elif action == "disable" and engine:
            config.disable_search_engine(engine)
            return f"❌ 已禁用搜索引擎: {engine}"
            
        elif action == "set_default" and engine:
            config.update_user_preference("default_search_engine", engine)
            return f"🎯 已设置默认搜索引擎: {engine}"
            
        elif action == "health_check":
            health_status = await search_manager.health_check_all()
            
            result = "🏥 **搜索引擎健康检查**\n\n"
            for engine, is_healthy in health_status.items():
                status = "✅ 正常" if is_healthy else "❌ 异常"
                result += f"**{engine}**: {status}\n"
            
            return result
            
        else:
            return "❌ 无效的配置操作。支持的操作: list, enable, disable, set_default, health_check"
            
    except Exception as e:
        return f"❌ 配置操作失败: {str(e)}"

@mcp.tool()
async def analyze_search_intent(
    user_input: str,
    ctx: Context = None
) -> str:
    """🎯 V6 意图分析 - 分析用户搜索意图和偏好
    
    参数:
    - user_input: 用户输入的搜索请求
    
    功能:
    - 识别明确指定的搜索引擎
    - 分析内容类型和语言偏好
    - 检测特殊需求 (隐身、动态内容等)
    - 提供搜索建议
    """
    
    try:
        # 分析用户意图
        intent = analyze_user_intent(user_input)
        
        # 格式化分析结果
        result = "🎯 **用户意图分析**\n\n"
        result += f"📝 **原始输入**: {user_input}\n\n"
        
        # 主要意图
        result += f"🎪 **主要意图**: {intent.primary_intent.value}\n"
        result += f"📊 **置信度**: {intent.confidence:.2f}\n\n"
        
        # 搜索引擎意图
        if intent.search_engine:
            engine_type_map = {
                SearchEngineIntent.EXPLICIT: "🎯 明确指定",
                SearchEngineIntent.IMPLICIT: "💡 隐含偏好", 
                SearchEngineIntent.AUTO: "🤖 自动选择"
            }
            engine_type = engine_type_map.get(intent.search_engine_intent, "未知")
            
            result += f"🔍 **搜索引擎**: {intent.search_engine}\n"
            result += f"🎭 **指定方式**: {engine_type}\n\n"
            
            if intent.search_engine_intent == SearchEngineIntent.EXPLICIT:
                result += "✅ **V6承诺**: 将严格使用您指定的搜索引擎\n\n"
        else:
            result += "🔍 **搜索引擎**: 将智能选择最适合的引擎\n\n"
        
        # 搜索关键词
        if intent.search_keywords:
            result += f"🔑 **搜索关键词**: {', '.join(intent.search_keywords)}\n\n"
        
        # 内容类型和语言偏好
        if intent.content_type:
            result += f"📄 **内容类型**: {intent.content_type}\n"
        
        if intent.language_preference:
            result += f"🌐 **语言偏好**: {intent.language_preference}\n"
        
        # 特殊需求
        special_needs = []
        if intent.stealth_required:
            special_needs.append("🥷 隐身模式")
        if intent.dynamic_content:
            special_needs.append("⚡ 动态内容")
        if intent.batch_processing:
            special_needs.append("📦 批量处理")
        
        if special_needs:
            result += f"🎪 **特殊需求**: {', '.join(special_needs)}\n"
        
        result += "\n"
        
        # 推荐的搜索引擎
        from v6_core.intent_analyzer import intent_analyzer
        recommended_engine = intent_analyzer.get_search_engine_recommendation(intent)
        result += f"💡 **推荐搜索引擎**: {recommended_engine}\n"
        
        # 如果用户没有明确指定，提供建议
        if intent.search_engine_intent != SearchEngineIntent.EXPLICIT:
            result += f"💭 **建议**: 如需使用特定搜索引擎，请在查询中明确指定，如 '用Google搜索...' 或 '百度搜索...'\n"
        
        return result
        
    except Exception as e:
        return f"❌ 意图分析失败: {str(e)}"

@mcp.tool()
async def v6_system_status(ctx: Context = None) -> str:
    """📊 V6 系统状态 - 查看系统运行状态和配置
    """
    
    try:
        config = get_config()
        
        # 系统基本信息
        result = "📊 **Context Scraper V6 系统状态**\n\n"
        result += f"🚀 **版本**: {config.system_config.version}\n"
        result += f"🐛 **调试模式**: {config.system_config.debug_mode}\n"
        result += f"📝 **日志级别**: {config.system_config.log_level}\n\n"
        
        # 搜索引擎状态
        available_engines = search_manager.get_available_engines()
        result += f"🔍 **可用搜索引擎**: {len(available_engines)}个\n"
        result += f"📋 **引擎列表**: {', '.join(available_engines)}\n"
        result += f"🎯 **默认引擎**: {config.user_preferences.default_search_engine}\n\n"
        
        # 用户偏好
        prefs = config.user_preferences
        result += "⚙️ **用户偏好**\n"
        result += f"   ✅ 严格遵循指定引擎: {prefs.respect_explicit_engine}\n"
        result += f"   🔄 自动回退: {prefs.auto_fallback}\n"
        result += f"   🇨🇳 中文内容引擎: {prefs.chinese_content_engine}\n"
        result += f"   🎓 学术内容引擎: {prefs.academic_content_engine}\n"
        result += f"   🔒 隐私保护引擎: {prefs.privacy_focused_engine}\n\n"
        
        # 性能配置
        sys_config = config.system_config
        result += "⚡ **性能配置**\n"
        result += f"   🔄 最大并发请求: {sys_config.max_concurrent_requests}\n"
        result += f"   ⏱️ 请求超时: {sys_config.request_timeout}秒\n"
        result += f"   🔁 重试次数: {sys_config.retry_attempts}\n"
        result += f"   💾 缓存启用: {sys_config.cache_enabled}\n\n"
        
        # 健康检查
        try:
            health_status = await search_manager.health_check_all()
            healthy_count = sum(1 for status in health_status.values() if status)
            total_count = len(health_status)
            
            result += f"🏥 **健康状态**: {healthy_count}/{total_count} 引擎正常\n"
            
            for engine, is_healthy in health_status.items():
                status_icon = "✅" if is_healthy else "❌"
                result += f"   {status_icon} {engine}\n"
        
        except Exception as e:
            result += f"🏥 **健康检查**: 检查失败 - {str(e)}\n"
        
        result += "\n🎉 **V6 核心特性**\n"
        result += "   🎯 用户意图至上 - 严格遵循明确指定\n"
        result += "   🔍 多搜索引擎支持 - Google/百度/Bing等\n"
        result += "   🧠 无偏见意图分析 - 消除系统固化偏好\n"
        result += "   ⚙️ 统一配置管理 - 一站式设置中心\n"
        result += "   🔄 智能回退机制 - 确保搜索成功率\n"
        
        return result
        
    except Exception as e:
        return f"❌ 系统状态查询失败: {str(e)}"

# ===== 兼容性工具 - 继承V5功能 =====

@mcp.tool()
async def crawl_with_v6_intelligence(
    url: str,
    use_smart_analysis: bool = True,
    ctx: Context = None
) -> str:
    """🕷️ V6 智能爬取 - 结合意图分析的网页爬取
    
    参数:
    - url: 目标网址
    - use_smart_analysis: 是否使用智能分析
    
    特性:
    - 🧠 基于URL的智能分析
    - 🎯 自适应爬取策略
    - 📊 结构化内容提取
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
    """显示V6欢迎信息"""
    print("🚀 Context Scraper V6 启动成功!")
    print("=" * 50)
    print("🎯 核心特性:")
    print("   ✅ 用户意图至上 - 严格遵循明确指定")
    print("   🔍 多搜索引擎支持 - Google/百度/Bing/Yahoo/DuckDuckGo")
    print("   🧠 无偏见意图分析 - 消除系统固化偏好")
    print("   ⚙️ 统一配置管理 - 一站式设置中心")
    print("   🔄 智能回退机制 - 确保搜索成功率")
    print("=" * 50)
    print("💡 使用提示:")
    print("   - 明确指定搜索引擎: '用Google搜索AI新闻'")
    print("   - 查看系统状态: v6_system_status")
    print("   - 配置搜索引擎: configure_search_engines")
    print("   - 分析搜索意图: analyze_search_intent")
    print("=" * 50)

if __name__ == "__main__":
    show_v6_welcome()
