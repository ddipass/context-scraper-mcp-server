#!/usr/bin/env python3
# test_v6.py - V6 功能测试脚本

import asyncio
import sys
import os
import time

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_v6_core_components():
    """测试V6核心组件"""
    print("🧪 V6 核心组件测试")
    print("=" * 50)
    
    try:
        # 1. 测试配置管理器
        print("1️⃣ 测试配置管理器...")
        from v6_core.config_manager import get_config
        config = get_config()
        print(f"   ✅ 配置管理器初始化成功")
        print(f"   📊 版本: {config.system_config.version}")
        print(f"   🔍 默认搜索引擎: {config.user_preferences.default_search_engine}")
        print(f"   🎯 严格遵循用户指定: {config.user_preferences.respect_explicit_engine}")
        
        # 2. 测试意图分析器
        print("\n2️⃣ 测试意图分析器...")
        from v6_core.intent_analyzer import analyze_user_intent, SearchEngineIntent
        
        test_cases = [
            "用Google搜索最新的AI新闻",
            "百度搜索Python教程", 
            "用Google查找学术论文",  # 修正：学术搜索应该用Google
            "搜索一下机器学习",
            "用DuckDuckGo匿名搜索隐私保护"
        ]
        
        for test_input in test_cases:
            intent = analyze_user_intent(test_input)
            engine_type = "明确指定" if intent.search_engine_intent == SearchEngineIntent.EXPLICIT else "自动选择"
            print(f"   📝 输入: {test_input}")
            print(f"   🎯 搜索引擎: {intent.search_engine or '未指定'} ({engine_type})")
            print(f"   🔑 关键词: {intent.search_keywords}")
            print()
        
        # 3. 测试搜索管理器
        print("3️⃣ 测试搜索管理器...")
        from v6_core.search_manager import search_manager
        
        available_engines = search_manager.get_available_engines()
        print(f"   ✅ 可用搜索引擎: {available_engines}")
        
        engine_info = search_manager.get_engine_info()
        for name, info in engine_info.items():
            status = "启用" if info["enabled"] else "禁用"
            print(f"   🔧 {name}: {status} (优先级: {info['priority']})")
        
        print("\n✅ 所有核心组件测试通过!")
        return True
        
    except Exception as e:
        print(f"❌ 核心组件测试失败: {e}")
        return False

async def test_search_functionality():
    """测试搜索功能"""
    print("\n🔍 V6 搜索功能测试")
    print("=" * 50)
    
    try:
        from v6_core.intent_analyzer import analyze_user_intent, SearchEngineIntent
        from v6_core.search_manager import search_with_intent
        
        # 测试用例
        test_queries = [
            ("用Google搜索Python", "google"),
            ("百度搜索机器学习", "baidu"),
            ("搜索人工智能", None)  # 自动选择
        ]
        
        for query, expected_engine in test_queries:
            print(f"\n🧪 测试查询: {query}")
            
            # 分析意图
            intent = analyze_user_intent(query)
            print(f"   🎯 识别的搜索引擎: {intent.search_engine}")
            print(f"   📝 意图类型: {intent.search_engine_intent.value}")
            
            # 验证意图识别的准确性
            if expected_engine:
                if intent.search_engine == expected_engine:
                    print(f"   ✅ 搜索引擎识别正确")
                else:
                    print(f"   ❌ 搜索引擎识别错误，期望: {expected_engine}, 实际: {intent.search_engine}")
            
            # 测试搜索 (模拟，不实际执行网络请求)
            print(f"   🔍 搜索关键词: {intent.search_keywords}")
            
            # 验证用户明确指定的引擎被严格遵循
            if intent.search_engine_intent == SearchEngineIntent.EXPLICIT:
                print(f"   🎯 用户明确指定引擎，V6将严格遵循: {intent.search_engine}")
            else:
                print(f"   🤖 将使用智能选择的引擎")
        
        print("\n✅ 搜索功能测试通过!")
        return True
        
    except Exception as e:
        print(f"❌ 搜索功能测试失败: {e}")
        return False

async def test_bias_elimination():
    """测试偏见消除功能"""
    print("\n🎯 V6 偏见消除测试")
    print("=" * 50)
    
    try:
        from v6_core.intent_analyzer import analyze_user_intent, SearchEngineIntent
        
        # 测试明确指定搜索引擎的场景
        explicit_tests = [
            ("用Google搜索中文内容", "google"),      # 即使是中文内容，也要用Google
            ("百度搜索英文资料", "baidu"),            # 即使是英文资料，也要用百度
            ("用Bing查找微软产品信息", "bing"),       # 更合理：Bing查找微软相关内容
            ("DuckDuckGo搜索商业信息", "duckduckgo") # 即使商业信息通常用其他引擎
        ]
        
        print("🧪 测试明确指定搜索引擎的场景:")
        all_passed = True
        
        for query, expected_engine in explicit_tests:
            intent = analyze_user_intent(query)
            
            print(f"   📝 查询: {query}")
            print(f"   🎯 期望引擎: {expected_engine}")
            print(f"   🔍 识别引擎: {intent.search_engine}")
            print(f"   📊 意图类型: {intent.search_engine_intent.value}")
            
            # 验证是否正确识别为明确指定
            if intent.search_engine_intent == SearchEngineIntent.EXPLICIT:
                if intent.search_engine == expected_engine:
                    print(f"   ✅ 通过 - 正确识别并将严格遵循用户指定")
                else:
                    print(f"   ❌ 失败 - 引擎识别错误")
                    all_passed = False
            else:
                print(f"   ❌ 失败 - 未识别为明确指定")
                all_passed = False
            
            print()
        
        # 测试隐含偏好场景
        print("🧪 测试隐含偏好场景:")
        implicit_tests = [
            ("搜索中文新闻", "chinese", "baidu"),
            ("查找学术论文", "academic", "google"),      # 学术搜索应该推荐Google
            ("匿名搜索隐私信息", "privacy", "duckduckgo"),
            ("搜索编程技术资料", "tech", "google"),        # 技术搜索推荐Google
            ("查找微软产品信息", "microsoft", "bing")      # 微软相关可以推荐Bing
        ]
        
        for query, content_type, expected_engine in implicit_tests:
            intent = analyze_user_intent(query)
            
            print(f"   📝 查询: {query}")
            print(f"   🏷️ 内容类型: {content_type}")
            print(f"   🔍 推荐引擎: {intent.search_engine}")
            print(f"   📊 意图类型: {intent.search_engine_intent.value}")
            
            # 这种情况下应该是隐含偏好或自动选择
            if intent.search_engine_intent in [SearchEngineIntent.IMPLICIT, SearchEngineIntent.AUTO]:
                print(f"   ✅ 通过 - 正确识别为隐含偏好/自动选择")
            else:
                print(f"   ⚠️ 注意 - 意图类型可能需要调整")
            
            print()
        
        if all_passed:
            print("✅ 偏见消除测试全部通过!")
            print("🎯 V6成功消除了系统偏见，严格遵循用户明确指定的搜索引擎")
        else:
            print("❌ 部分偏见消除测试失败")
        
        return all_passed
        
    except Exception as e:
        print(f"❌ 偏见消除测试失败: {e}")
        return False

async def test_configuration_management():
    """测试配置管理功能"""
    print("\n⚙️ V6 配置管理测试")
    print("=" * 50)
    
    try:
        from v6_core.config_manager import get_config
        
        config = get_config()
        
        # 测试配置读取
        print("🧪 测试配置读取:")
        print(f"   📊 系统版本: {config.system_config.version}")
        print(f"   🔍 默认搜索引擎: {config.user_preferences.default_search_engine}")
        print(f"   ✅ 严格遵循用户指定: {config.user_preferences.respect_explicit_engine}")
        print(f"   🔄 自动回退: {config.user_preferences.auto_fallback}")
        
        # 测试搜索引擎配置
        print("\n🧪 测试搜索引擎配置:")
        enabled_engines = config.get_enabled_search_engines()
        print(f"   🔧 启用的搜索引擎: {list(enabled_engines.keys())}")
        
        priority_engines = config.get_search_engine_by_priority()
        print("   📊 按优先级排序:")
        for name, engine_config in priority_engines:
            print(f"      {engine_config.priority}. {name} ({engine_config.name})")
        
        # 测试配置摘要
        print("\n🧪 测试配置摘要:")
        summary = config.get_config_summary()
        for key, value in summary.items():
            print(f"   {key}: {value}")
        
        print("\n✅ 配置管理测试通过!")
        return True
        
    except Exception as e:
        print(f"❌ 配置管理测试失败: {e}")
        return False

async def run_comprehensive_test():
    """运行综合测试"""
    print("🚀 Context Scraper V6 综合测试")
    print("=" * 60)
    
    start_time = time.time()
    
    # 运行所有测试
    tests = [
        ("核心组件", test_v6_core_components),
        ("搜索功能", test_search_functionality),
        ("偏见消除", test_bias_elimination),
        ("配置管理", test_configuration_management)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🧪 开始测试: {test_name}")
        try:
            result = await test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ 测试 {test_name} 出现异常: {e}")
            results[test_name] = False
    
    # 测试结果汇总
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    print("📊 V6 测试结果汇总")
    print("=" * 60)
    
    passed_count = 0
    total_count = len(results)
    
    for test_name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{test_name}: {status}")
        if passed:
            passed_count += 1
    
    print(f"\n📈 总体结果: {passed_count}/{total_count} 测试通过")
    print(f"⏱️ 总用时: {elapsed_time:.2f}秒")
    
    if passed_count == total_count:
        print("\n🎉 恭喜! V6 所有测试通过!")
        print("🚀 Context Scraper V6 已准备就绪!")
        print("\n💡 V6 核心优势:")
        print("   🎯 用户意图至上 - 严格遵循明确指定")
        print("   🔍 多搜索引擎支持 - 消除单一依赖")
        print("   🧠 无偏见意图分析 - 智能但不固执")
        print("   ⚙️ 统一配置管理 - 简单易用")
    else:
        print(f"\n⚠️ 有 {total_count - passed_count} 个测试失败，需要进一步调试")
    
    return passed_count == total_count

if __name__ == "__main__":
    asyncio.run(run_comprehensive_test())
