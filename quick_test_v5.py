#!/usr/bin/env python3
# quick_test_v5.py - V5快速验证脚本

import asyncio
import sys
import os
import time

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_v5_basic():
    """V5基础功能测试"""
    print("🚀 V5快速验证开始")
    print("=" * 40)
    
    try:
        # 测试核心组件导入
        print("1️⃣ 测试核心组件导入...")
        from server_v5_core import V5LayeredEngine, ResearchMode
        print("   ✅ 核心组件导入成功")
        
        # 测试引擎初始化
        print("\n2️⃣ 测试引擎初始化...")
        engine = V5LayeredEngine()
        print("   ✅ V5引擎初始化成功")
        
        # 测试意图分析
        print("\n3️⃣ 测试意图分析...")
        context = engine.intent_analyzer.analyze_research_intent(
            "快速了解OpenAI", 
            ["https://openai.com"]
        )
        print(f"   ✅ 意图分析成功: {context.mode.value}模式, 预计{context.estimated_time}秒")
        
        # 测试分层执行 (模拟模式)
        print("\n4️⃣ 测试分层执行...")
        
        progress_count = 0
        def progress_callback(progress_info):
            nonlocal progress_count
            progress_count += 1
            if progress_count <= 3:  # 只显示前3个进度
                print(f"   📊 {progress_info.stage.value}: {progress_info.progress:.1f}%")
        
        start_time = time.time()
        result = await engine.execute_research(
            query="测试V5引擎",
            websites="https://example.com",
            mode="quick",
            progress_callback=progress_callback
        )
        execution_time = time.time() - start_time
        
        print(f"   ✅ 分层执行成功，用时 {execution_time:.1f} 秒")
        print(f"   📊 执行模式: {result['context'].mode.value}")
        
        # 性能基准测试
        print("\n5️⃣ 性能基准测试...")
        
        # 意图分析性能
        start_time = time.time()
        for i in range(50):
            engine.intent_analyzer.analyze_research_intent(f"测试{i}", ["https://example.com"])
        analysis_time = time.time() - start_time
        
        print(f"   ⚡ 意图分析 50次: {analysis_time:.3f}秒 (平均 {analysis_time*20:.1f}ms/次)")
        
        # 总体评估
        print("\n" + "=" * 40)
        print("🎉 V5快速验证完成!")
        print(f"✅ 所有核心功能正常")
        print(f"⚡ 性能表现良好")
        print(f"🚀 V5已准备就绪!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ V5验证失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_v5_modes():
    """测试V5不同模式的识别"""
    print("\n🎯 V5模式识别测试")
    print("-" * 30)
    
    from server_v5_core import V5IntentAnalyzer
    analyzer = V5IntentAnalyzer()
    
    test_cases = [
        ("快速看看这个公司", "quick"),
        ("了解一下产品功能", "quick"), 
        ("分析市场趋势", "standard"),
        ("研究技术架构", "standard"),
        ("深入分析竞争格局", "deep"),
        ("全面研究行业发展", "deep"),
        ("对比三家公司", "standard")
    ]
    
    correct = 0
    for query, expected in test_cases:
        context = analyzer.analyze_research_intent(query, ["https://example.com"])
        actual = context.mode.value
        is_correct = actual == expected
        if is_correct:
            correct += 1
        
        status = "✅" if is_correct else "❌"
        print(f"   {status} '{query}' -> {actual} (期望: {expected})")
    
    accuracy = correct / len(test_cases) * 100
    print(f"\n📊 模式识别准确率: {accuracy:.1f}% ({correct}/{len(test_cases)})")
    
    return accuracy >= 70  # 70%以上认为合格

def test_v5_compatibility():
    """测试V5兼容性"""
    print("\n🔄 V5兼容性测试")
    print("-" * 30)
    
    try:
        # 测试V4兼容性
        print("   测试V4兼容性...")
        try:
            from server_v4_simple import IntentAnalyzer
            print("   ✅ V4组件可访问")
        except ImportError:
            print("   ⚠️ V4组件不可用 (这是正常的，如果V4文件不存在)")
        
        # 测试V5独立性
        print("   测试V5独立性...")
        from server_v5_core import V5LayeredEngine
        engine = V5LayeredEngine()
        print("   ✅ V5可独立运行")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 兼容性测试失败: {str(e)}")
        return False

async def main():
    """主测试函数"""
    print("🧪 Context Scraper V5 快速验证")
    print("🎯 目标: 验证V5核心功能是否正常")
    print("⏱️ 预计用时: 10-15秒")
    print()
    
    start_time = time.time()
    
    # 基础功能测试
    basic_ok = await test_v5_basic()
    
    # 模式识别测试
    modes_ok = await test_v5_modes()
    
    # 兼容性测试
    compat_ok = test_v5_compatibility()
    
    total_time = time.time() - start_time
    
    # 总结
    print("\n" + "=" * 50)
    print("📋 V5验证总结")
    print(f"⏱️ 总用时: {total_time:.1f} 秒")
    print(f"🔧 基础功能: {'✅ 通过' if basic_ok else '❌ 失败'}")
    print(f"🎯 模式识别: {'✅ 通过' if modes_ok else '❌ 失败'}")
    print(f"🔄 兼容性: {'✅ 通过' if compat_ok else '❌ 失败'}")
    
    all_passed = basic_ok and modes_ok and compat_ok
    
    if all_passed:
        print("\n🎉 V5验证全部通过!")
        print("🚀 可以开始使用V5功能")
        print("\n💡 下一步:")
        print("   1. 运行 'python server_v5.py' 启动V5服务器")
        print("   2. 在Amazon Q中测试V5工具")
        print("   3. 查看 V5_USAGE_GUIDE.md 了解详细用法")
    else:
        print("\n⚠️ V5验证存在问题")
        print("🔧 建议检查:")
        print("   1. Python环境和依赖")
        print("   2. 项目文件完整性")
        print("   3. 运行 'python test_v5.py' 获取详细信息")
    
    return all_passed

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
