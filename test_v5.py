#!/usr/bin/env python3
# test_v5.py - Context Scraper V5 基础测试

import asyncio
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server_v5_core import (
    V5LayeredEngine,
    V5IntentAnalyzer, 
    ResearchMode,
    ExecutionStage
)

async def test_v5_core():
    """测试V5核心组件"""
    print("🧪 开始V5核心组件测试")
    
    # 测试意图分析器
    print("\n1️⃣ 测试意图分析器...")
    analyzer = V5IntentAnalyzer()
    
    test_cases = [
        ("快速了解特斯拉的自动驾驶技术", ["https://tesla.com"]),
        ("深入分析OpenAI和Anthropic的竞争策略", ["https://openai.com", "https://anthropic.com"]),
        ("对比三家AI公司的产品", ["https://openai.com", "https://anthropic.com", "https://google.com"])
    ]
    
    for query, websites in test_cases:
        context = analyzer.analyze_research_intent(query, websites)
        print(f"   查询: {query}")
        print(f"   模式: {context.mode.value}")
        print(f"   预估时间: {context.estimated_time}秒")
        print(f"   需要深度爬取: {context.needs_deep_crawl}")
        print(f"   竞争分析: {context.competitive_analysis}")
        print()
    
    # 测试分层引擎
    print("2️⃣ 测试分层引擎...")
    engine = V5LayeredEngine()
    
    def progress_callback(progress_info):
        print(f"   进度: {progress_info.stage.value} ({progress_info.progress:.1f}%) - {progress_info.message}")
    
    try:
        result = await engine.execute_research(
            query="测试查询",
            websites="https://example.com",
            mode="quick",
            progress_callback=progress_callback
        )
        
        print(f"   ✅ 分层引擎测试成功")
        print(f"   执行模式: {result['context'].mode.value}")
        print(f"   Layer1结果: {result['layer1_result']['websites_crawled']} 个网站")
        print(f"   Layer2置信度: {result['layer2_result']['confidence']}")
        
    except Exception as e:
        print(f"   ❌ 分层引擎测试失败: {str(e)}")
    
    print("\n✅ V5核心组件测试完成")

async def test_v5_modes():
    """测试V5不同模式"""
    print("\n🎯 测试V5不同研究模式")
    
    analyzer = V5IntentAnalyzer()
    
    mode_tests = [
        ("快速看看这个公司", ResearchMode.QUICK),
        ("详细分析市场趋势", ResearchMode.STANDARD), 
        ("深入研究技术架构", ResearchMode.DEEP),
        ("对比竞争对手产品", ResearchMode.STANDARD)
    ]
    
    for query, expected_mode in mode_tests:
        context = analyzer.analyze_research_intent(query, ["https://example.com"])
        result = "✅" if context.mode == expected_mode else "❌"
        print(f"   {result} '{query}' -> {context.mode.value} (期望: {expected_mode.value})")

def test_v5_imports():
    """测试V5导入"""
    print("📦 测试V5模块导入")
    
    try:
        from server_v5_core import V5LayeredEngine
        print("   ✅ V5LayeredEngine 导入成功")
        
        from server_v5_core import V5ProgressTracker
        print("   ✅ V5ProgressTracker 导入成功")
        
        from server_v5_core import ResearchMode, ExecutionStage
        print("   ✅ 枚举类型导入成功")
        
        print("   📊 可用研究模式:", [mode.value for mode in ResearchMode])
        print("   📊 执行阶段:", [stage.value for stage in ExecutionStage])
        
    except ImportError as e:
        print(f"   ❌ 导入失败: {str(e)}")

async def main():
    """主测试函数"""
    print("🚀 Context Scraper V5 测试开始")
    print("=" * 50)
    
    # 基础导入测试
    test_v5_imports()
    
    # 核心组件测试
    await test_v5_core()
    
    # 模式测试
    await test_v5_modes()
    
    print("\n" + "=" * 50)
    print("🎉 V5测试完成！")
    
    # 简单性能基准
    print("\n⏱️ 简单性能基准:")
    import time
    
    start_time = time.time()
    analyzer = V5IntentAnalyzer()
    for i in range(100):
        context = analyzer.analyze_research_intent(f"测试查询{i}", ["https://example.com"])
    
    elapsed = time.time() - start_time
    print(f"   意图分析 100次: {elapsed:.3f}秒 (平均 {elapsed*10:.1f}ms/次)")

if __name__ == "__main__":
    asyncio.run(main())
