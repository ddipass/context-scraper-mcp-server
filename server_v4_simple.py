# server_v4_simple.py - Context Scraper MCP Server V4
# 在V3基础上增加智能研究助手功能

import asyncio
import sys
import os
import json
import time
from typing import Optional, List, Dict, Any
from pathlib import Path

# 导入V3的所有功能 (保持向下兼容)
from server_v3_smart import *

# 导入V4新增的配置系统
from simple_config import config

# 导入Crawl4AI深度爬取功能
from crawl4ai.deep_crawling import BestFirstCrawlingStrategy, BFSDeepCrawlStrategy
from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer
from crawl4ai.deep_crawling.filters import FilterChain, URLPatternFilter, DomainFilter

# 导入HTTP客户端用于Claude API调用
import aiohttp

# ===== V4核心功能：智能研究助手 =====

class IntentAnalyzer:
    """简单的意图分析器"""
    
    @staticmethod
    def analyze_intent(user_input: str, websites: str = "") -> Dict[str, Any]:
        """分析用户意图并返回处理策略"""
        user_lower = user_input.lower()
        
        intent = {
            "type": "standard",
            "strategy": "standard",
            "keywords": [],
            "estimated_time": "5-10分钟",
            "needs_deep_crawl": False
        }
        
        # 提取关键词
        intent["keywords"] = user_input.split()[:5]
        
        # 检测研究类型
        if any(word in user_lower for word in ["对比", "竞争", "vs", "比较", "竞品"]):
            intent["type"] = "competitive"
            intent["strategy"] = "competitive"
            intent["estimated_time"] = "10-15分钟"
            
        elif any(word in user_lower for word in ["深入", "详细", "全面", "完整", "深度"]):
            intent["type"] = "deep"
            intent["strategy"] = "deep"
            intent["needs_deep_crawl"] = True
            intent["estimated_time"] = "15-25分钟"
            
        elif any(word in user_lower for word in ["快速", "简单", "概览", "看看", "了解"]):
            intent["type"] = "quick"
            intent["strategy"] = "quick"
            intent["estimated_time"] = "3-5分钟"
        
        return intent

intent_analyzer = IntentAnalyzer()

@mcp.tool()
async def smart_research_assistant(
    research_query: str,
    target_websites: str = "",
    depth_level: str = "auto",
    ctx: Context = None
) -> str:
    """🧠 智能研究助手 - V4核心功能
    
    这是V4的核心工具，整合了所有爬取和分析能力：
    
    参数：
    - research_query: 你的研究需求（自然语言）
    - target_websites: 目标网站（用逗号分隔）
    - depth_level: 研究深度 (auto/quick/standard/deep)
    
    示例：
    - smart_research_assistant("分析特斯拉的自动驾驶技术", "https://tesla.com")
    - smart_research_assistant("对比OpenAI和Anthropic的产品策略", "https://openai.com,https://anthropic.com")
    """
    
    try:
        print(f"🚀 V4智能研究助手启动")
        print(f"📋 研究问题: {research_query}")
        
        # 阶段1: 智能意图分析
        print("🔍 阶段1: 分析研究意图...")
        intent = intent_analyzer.analyze_intent(research_query, target_websites)
        print(f"   识别类型: {intent['type']}")
        print(f"   处理策略: {intent['strategy']}")
        print(f"   预计用时: {intent['estimated_time']}")
        
        if not target_websites:
            return "❌ 请提供目标网站URL (用逗号分隔多个网站)"
        
        urls = [url.strip() for url in target_websites.split(',') if url.strip()]
        print(f"   目标网站: {len(urls)} 个")
        
        # 阶段2: 执行爬取策略
        print("🕷️ 阶段2: 执行智能爬取...")
        
        if intent["strategy"] == "deep" and intent["needs_deep_crawl"]:
            crawl_result = await _execute_deep_crawl(urls[0], research_query)
        elif intent["strategy"] == "competitive":
            crawl_result = await _execute_competitive_crawl(urls, research_query)
        else:
            crawl_result = await _execute_standard_crawl(urls, research_query)
        
        print(f"   爬取完成，获得内容长度: {len(crawl_result)} 字符")
        
        # 阶段3: Claude智能分析
        print("🧠 阶段3: Claude智能分析...")
        analysis_result = await _analyze_with_claude(crawl_result, research_query, intent)
        
        # 生成最终报告
        final_report = _generate_research_report(
            research_query, intent, urls, crawl_result, analysis_result
        )
        
        print("✅ 智能研究完成!")
        return final_report
        
    except Exception as e:
        error_msg = f"❌ 研究过程出错: {str(e)}"
        print(error_msg)
        return error_msg

async def _execute_deep_crawl(url: str, query: str) -> str:
    """执行深度爬取 - 使用Crawl4AI的深度能力"""
    print("   🔍 启动深度爬取模式...")
    
    try:
        # 使用查询关键词作为评分依据
        keywords = query.split()[:5]
        scorer = KeywordRelevanceScorer(keywords=keywords, weight=1.0)
        
        # 配置深度爬取策略
        deep_config = CrawlerRunConfig(
            deep_crawl_strategy=BestFirstCrawlingStrategy(
                max_depth=2,  # 2层深度，避免太慢
                max_pages=12,  # 限制页面数量
                include_external=False,
                url_scorer=scorer,
                score_threshold=0.2  # 降低阈值，获取更多相关页面
            ),
            cache_mode=CacheMode.BYPASS,
            stream=True,  # 启用流式处理
            verbose=False
        )
        
        results = []
        browser_config = get_smart_browser_config()
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            print(f"   📄 开始深度爬取: {url}")
            
            async for result in await crawler.arun(url=url, config=deep_config):
                if result.success:
                    results.append(result)
                    depth = result.metadata.get("depth", 0)
                    score = result.metadata.get("score", 0)
                    print(f"   📄 发现页面 (深度:{depth}, 相关性:{score:.2f}): {result.url[:60]}...")
        
        print(f"   ✅ 深度爬取完成，共发现 {len(results)} 个相关页面")
        
        # 合并所有内容，按相关性排序
        sorted_results = sorted(results, key=lambda x: x.metadata.get("score", 0), reverse=True)
        
        combined_content = ""
        for i, result in enumerate(sorted_results[:8]):  # 取前8个最相关的页面
            score = result.metadata.get("score", 0)
            depth = result.metadata.get("depth", 0)
            combined_content += f"\n\n=== 页面 {i+1} (深度:{depth}, 相关性:{score:.2f}) ===\n"
            combined_content += f"URL: {result.url}\n"
            combined_content += result.markdown[:1500]  # 每个页面限制1500字符
        
        return combined_content
        
    except Exception as e:
        print(f"   ❌ 深度爬取失败: {str(e)}")
        # 降级到标准爬取
        return await _execute_standard_crawl([url], query)

async def _execute_competitive_crawl(urls: List[str], query: str) -> str:
    """执行竞争分析爬取"""
    print("   🏆 启动竞争分析模式...")
    
    try:
        # 使用并发爬取多个网站
        results = []
        browser_config = get_smart_browser_config()
        run_config = get_smart_run_config(use_content_filter=True)
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            # 并发爬取所有网站
            crawl_tasks = []
            for url in urls[:5]:  # 最多5个网站
                crawl_tasks.append(crawler.arun(url=url, config=run_config))
            
            crawl_results = await asyncio.gather(*crawl_tasks, return_exceptions=True)
            
            for i, result in enumerate(crawl_results):
                if isinstance(result, Exception):
                    print(f"   ❌ 网站 {i+1} 爬取失败: {str(result)}")
                elif hasattr(result, 'success') and result.success:
                    results.append(result)
                    print(f"   ✅ 网站 {i+1} 爬取成功: {urls[i]}")
        
        print(f"   ✅ 竞争分析爬取完成，成功 {len(results)}/{len(urls)} 个网站")
        
        # 组织竞争对手内容
        combined_content = ""
        for i, result in enumerate(results):
            combined_content += f"\n\n=== 竞争对手 {i+1} ===\n"
            combined_content += f"网站: {result.url}\n"
            combined_content += result.markdown[:2000]  # 每个网站限制2000字符
        
        return combined_content
        
    except Exception as e:
        print(f"   ❌ 竞争分析爬取失败: {str(e)}")
        return f"竞争分析爬取出错: {str(e)}"

async def _execute_standard_crawl(urls: List[str], query: str) -> str:
    """执行标准爬取"""
    print("   📄 启动标准爬取模式...")
    
    try:
        if len(urls) == 1:
            # 单个网站，使用智能清理
            result = await crawl_clean(urls[0], None)
            print(f"   ✅ 标准爬取完成: {urls[0]}")
            return result
        else:
            # 多个网站，使用智能批量处理
            urls_str = ",".join(urls[:3])  # 最多3个网站
            result = await crawl_smart_batch(urls_str, "auto", None)
            print(f"   ✅ 批量爬取完成: {len(urls)} 个网站")
            return result
            
    except Exception as e:
        print(f"   ❌ 标准爬取失败: {str(e)}")
        return f"标准爬取出错: {str(e)}"

async def _analyze_with_claude(content: str, query: str, intent: Dict) -> str:
    """使用Claude分析内容"""
    print("   🧠 调用Claude 3.7进行分析...")
    
    try:
        llm_config = config.get_llm_config()
        
        # 根据意图类型定制分析提示
        if intent["type"] == "competitive":
            analysis_prompt = f"""
作为专业的商业分析师，请对以下竞争对手信息进行深度对比分析。

研究问题: {query}

请按以下结构分析：

1. **执行摘要** (150字以内)
   - 核心发现和关键差异

2. **竞争对手对比**
   - 各家的核心优势
   - 产品/服务差异
   - 市场定位对比

3. **深度洞察**
   - 竞争格局分析
   - 市场机会识别
   - 威胁和风险评估

4. **战略建议**
   - 关键成功因素
   - 可学习的最佳实践

请用中文回答，保持客观和专业。

内容:
{content[:4000]}
"""
        elif intent["type"] == "deep":
            analysis_prompt = f"""
作为专业研究分析师，请对以下深度收集的信息进行全面分析。

研究主题: {query}

请按以下结构进行深度分析：

1. **核心发现** (200字以内)
   - 最重要的发现和洞察

2. **详细分析**
   - 关键数据和事实
   - 重要趋势和模式
   - 技术和商业要点

3. **深层洞察**
   - 行业影响和意义
   - 未来发展预测
   - 潜在机会和挑战

4. **结论建议**
   - 关键要点总结
   - 实用建议和启示

请用中文回答，注重深度和洞察力。

内容:
{content[:4000]}
"""
        else:
            analysis_prompt = f"""
作为专业分析师，请分析以下内容并回答研究问题。

研究问题: {query}

请提供：

1. **核心回答** (100字以内)
   - 直接回答研究问题

2. **关键发现**
   - 重要信息和数据
   - 值得关注的要点

3. **分析洞察**
   - 深层含义和影响
   - 趋势和机会

4. **总结建议**
   - 关键结论
   - 实用建议

请用中文回答，简洁而有价值。

内容:
{content[:3000]}
"""
        
        # 调用Claude API
        claude_response = await _call_claude_api(analysis_prompt, llm_config)
        
        if claude_response:
            print("   ✅ Claude分析完成")
            return claude_response
        else:
            print("   ⚠️ Claude分析失败，返回基础分析")
            return f"基于内容的基础分析:\n\n针对'{query}'的研究，从收集的信息中可以看出...\n\n[Claude分析暂时不可用，这里是基于爬取内容的基础整理]"
            
    except Exception as e:
        print(f"   ❌ Claude分析出错: {str(e)}")
        return f"分析过程出错: {str(e)}"

async def _call_claude_api(prompt: str, llm_config: Dict) -> Optional[str]:
    """调用Claude API"""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {llm_config['api_key']}"
        }
        
        payload = {
            "model": llm_config['model'],
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{llm_config['base_url']}/chat/completions",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    return result['choices'][0]['message']['content']
                else:
                    error_text = await response.text()
                    print(f"   ❌ Claude API错误 {response.status}: {error_text}")
                    return None
                    
    except Exception as e:
        print(f"   ❌ Claude API调用异常: {str(e)}")
        return None

def _generate_research_report(query: str, intent: Dict, urls: List[str], crawl_result: str, analysis_result: str) -> str:
    """生成最终研究报告"""
    
    report = f"""
# 🔬 智能研究报告: {query}

## 📊 研究概览
- **研究类型**: {intent['type']} ({intent['strategy']}策略)
- **目标网站**: {len(urls)} 个
- **处理时间**: {intent['estimated_time']}
- **分析模型**: Claude 3.7 Sonnet

## 🧠 Claude智能分析

{analysis_result}

## 📚 信息来源
"""
    
    for i, url in enumerate(urls, 1):
        report += f"\n{i}. [{url}]({url})"
    
    report += f"""

## 📋 技术详情
- **V4智能研究助手**: 自动意图识别 + 策略选择
- **深度爬取**: {'✅ 已启用' if intent.get('needs_deep_crawl') else '❌ 未使用'}
- **内容长度**: {len(crawl_result)} 字符
- **配置文件**: config.json

---
*由Context Scraper MCP Server V4生成*
"""
    
    return report

# ===== V4配置管理工具 =====

@mcp.tool()
async def update_claude_config(
    api_key: str = "",
    base_url: str = "",
    model: str = "",
    ctx: Context = None
) -> str:
    """🔧 更新Claude配置 - V4配置管理"""
    
    try:
        config.update_llm_config(
            api_key=api_key if api_key else None,
            base_url=base_url if base_url else None,
            model=model if model else None
        )
        return "✅ Claude配置已更新"
    except Exception as e:
        return f"❌ 配置更新失败: {str(e)}"

@mcp.tool()
async def show_current_config(ctx: Context = None) -> str:
    """📋 查看当前配置 - V4配置查看"""
    try:
        llm_config = config.get_llm_config()
        is_valid, messages = config.validate_config()
        
        return f"""
# 🔧 Context Scraper V4 配置状态

## 🧠 Claude配置
- **API地址**: {llm_config['base_url']}
- **模型**: {llm_config['model']}
- **API密钥**: {llm_config['api_key'][:20]}...

## ✅ 配置验证
- **状态**: {'✅ 正常' if is_valid else '❌ 异常'}
- **详情**: {', '.join(messages)}

## 📁 文件位置
- **配置文件**: `config.json`
- **V4主文件**: `server_v4_simple.py`

## 🚀 V4新功能
- ✅ 智能研究助手 (`smart_research_assistant`)
- ✅ 深度网站爬取 (Crawl4AI集成)
- ✅ Claude 3.7分析 (Bedrock Gateway)
- ✅ 极简配置管理
"""
    except Exception as e:
        return f"❌ 配置查看失败: {str(e)}"

@mcp.tool()
async def test_claude_connection(ctx: Context = None) -> str:
    """🧪 测试Claude连接 - V4连接测试"""
    
    try:
        llm_config = config.get_llm_config()
        
        # 验证配置完整性
        is_valid, messages = config.validate_config()
        if not is_valid:
            return f"❌ 配置验证失败: {', '.join(messages)}"
        
        # 测试API连接
        test_prompt = "请回复'连接测试成功'，确认Claude 3.7正常工作。"
        
        print("🧪 正在测试Claude API连接...")
        response = await _call_claude_api(test_prompt, llm_config)
        
        if response:
            return f"""
✅ Claude连接测试成功!

**API地址**: {llm_config['base_url']}
**模型**: {llm_config['model']}
**响应**: {response[:200]}...

🎉 V4智能研究助手已就绪!
"""
        else:
            return f"""
❌ Claude连接测试失败

**API地址**: {llm_config['base_url']}
**模型**: {llm_config['model']}

请检查：
1. API密钥是否正确
2. 网络连接是否正常
3. Bedrock Gateway是否运行
"""
            
    except Exception as e:
        return f"❌ 连接测试异常: {str(e)}"

# ===== V4智能提示系统 =====

@mcp.prompt()
def research_anything_v4(research_topic: str = "你想研究什么？") -> str:
    """🔬 V4智能研究助手 - 一句话搞定所有研究需求
    
    🎯 **直接告诉我你想研究什么：**
    - "分析特斯拉的自动驾驶技术发展"
    - "对比OpenAI和Anthropic的产品策略"  
    - "深入研究量子计算的商业应用"
    - "快速了解这家公司的业务模式"
    
    🚀 **V4智能特性：**
    ✅ 自动意图识别 - 理解你的真实需求
    ✅ 智能策略选择 - 自动选择最佳爬取方案
    ✅ 深度网站爬取 - 发现更多相关内容
    ✅ Claude 3.7分析 - 最强推理模型深度分析
    ✅ 实时进度反馈 - 每个步骤都有提示
    ✅ 专业研究报告 - 结构化输出，可直接使用
    
    💡 **使用方法：**
    直接调用 `smart_research_assistant` 工具，提供：
    1. 研究问题（必需）
    2. 目标网站（必需，用逗号分隔）
    3. 深度级别（可选：auto/quick/standard/deep）
    """
    
    return f"""
# 🔬 V4智能研究助手

## 🎯 研究主题
{research_topic}

## 🚀 V4执行流程

### 阶段1️⃣: 智能意图识别 (30秒)
```
🧠 自动分析研究需求
🎯 识别最佳处理策略
📊 预估处理时间和资源
```

### 阶段2️⃣: 智能爬取执行 (2-20分钟)
```
📄 标准模式: 智能清理 + 批量处理
🏆 竞争模式: 并发爬取 + 对比分析  
🔍 深度模式: 多层爬取 + 相关性评分
⚡ 快速模式: 高效爬取 + 核心提取
```

### 阶段3️⃣: Claude深度分析 (1-3分钟)
```
🧠 使用Claude 3.7 Sonnet
📊 专业级分析和洞察
🎯 针对性回答研究问题
📋 结构化报告生成
```

## 💡 智能适应能力

🔄 **自动策略选择**
- 根据问题类型自动选择最佳方案
- 单网站 → 深度爬取
- 多网站 → 竞争分析
- 复杂问题 → 深度研究

🛡️ **智能容错处理**
- API失败 → 自动降级到基础分析
- 网站限制 → 自动切换爬取策略
- 内容过长 → 智能截断和优化

⚡ **性能优化**
- 并发处理提升效率
- 流式输出实时反馈
- 智能缓存避免重复

## 🎮 开始使用

**工具调用**:
```
smart_research_assistant(
    research_query="{research_topic}",
    target_websites="网站1,网站2,网站3",
    depth_level="auto"
)
```

**配置管理**:
- `show_current_config()` - 查看配置
- `test_claude_connection()` - 测试连接
- `update_claude_config()` - 更新配置

准备开始智能研究...
"""

print("✅ Context Scraper MCP Server V4 已加载")
print("🚀 新功能: 智能研究助手 (smart_research_assistant)")
print("🔧 配置文件: config.json")
print("🧠 AI模型: Claude 3.7 Sonnet")
