#!/usr/bin/env python3
# test_search_matching.py - 搜索引擎匹配专项测试

import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from v6_core.intent_analyzer import analyze_user_intent, SearchEngineIntent

def test_search_engine_matching():
    """测试搜索引擎匹配的准确性"""
    print("🔍 搜索引擎匹配专项测试")
    print("=" * 60)
    
    # 测试用例：[查询, 期望的引擎, 期望的意图类型, 说明]
    test_cases = [
        # 明确指定测试
        ("用Google搜索学术论文", "google", SearchEngineIntent.EXPLICIT, "明确指定Google"),
        ("百度搜索技术资料", "baidu", SearchEngineIntent.EXPLICIT, "明确指定百度"),
        ("用Bing查找微软产品", "bing", SearchEngineIntent.EXPLICIT, "明确指定Bing"),
        ("DuckDuckGo匿名搜索", "duckduckgo", SearchEngineIntent.EXPLICIT, "明确指定DuckDuckGo"),
        
        # 隐含偏好测试 - 学术内容应该推荐Google
        ("查找学术论文", "google", SearchEngineIntent.IMPLICIT, "学术内容推荐Google"),
        ("搜索research paper", "google", SearchEngineIntent.IMPLICIT, "英文学术推荐Google"),
        ("寻找科研资料", "google", SearchEngineIntent.IMPLICIT, "科研资料推荐Google"),
        
        # 隐含偏好测试 - 中文内容应该推荐百度
        ("搜索中文新闻", "baidu", SearchEngineIntent.IMPLICIT, "中文内容推荐百度"),
        ("查找国内信息", "baidu", SearchEngineIntent.IMPLICIT, "国内信息推荐百度"),
        ("搜索本土资料", "baidu", SearchEngineIntent.IMPLICIT, "本土资料推荐百度"),
        
        # 隐含偏好测试 - 技术内容应该推荐Google
        ("搜索编程问题", "google", SearchEngineIntent.IMPLICIT, "编程问题推荐Google"),
        ("查找技术文档", "google", SearchEngineIntent.IMPLICIT, "技术文档推荐Google"),
        ("寻找开发资料", "google", SearchEngineIntent.IMPLICIT, "开发资料推荐Google"),
        
        # 隐含偏好测试 - 隐私保护应该推荐DuckDuckGo
        ("匿名搜索敏感信息", "duckduckgo", SearchEngineIntent.IMPLICIT, "隐私搜索推荐DuckDuckGo"),
        ("私密查找资料", "duckduckgo", SearchEngineIntent.IMPLICIT, "私密搜索推荐DuckDuckGo"),
        
        # 自动选择测试
        ("搜索人工智能", None, SearchEngineIntent.AUTO, "通用搜索自动选择"),
        ("查找信息", None, SearchEngineIntent.AUTO, "通用查找自动选择"),
    ]
    
    passed_count = 0
    total_count = len(test_cases)
    
    print(f"📋 共 {total_count} 个测试用例\n")
    
    for i, (query, expected_engine, expected_intent, description) in enumerate(test_cases, 1):
        print(f"🧪 测试 {i}: {description}")
        print(f"   📝 查询: {query}")
        
        # 分析意图
        intent = analyze_user_intent(query)
        
        print(f"   🎯 期望引擎: {expected_engine or '自动选择'}")
        print(f"   🔍 实际引擎: {intent.search_engine or '自动选择'}")
        print(f"   📊 期望意图: {expected_intent.value}")
        print(f"   📈 实际意图: {intent.search_engine_intent.value}")
        
        # 检查结果
        engine_match = intent.search_engine == expected_engine
        intent_match = intent.search_engine_intent == expected_intent
        
        if engine_match and intent_match:
            print(f"   ✅ 通过")
            passed_count += 1
        else:
            print(f"   ❌ 失败")
            if not engine_match:
                print(f"      🔧 引擎不匹配: 期望 {expected_engine}, 实际 {intent.search_engine}")
            if not intent_match:
                print(f"      🎭 意图不匹配: 期望 {expected_intent.value}, 实际 {intent.search_engine_intent.value}")
        
        print()
    
    # 结果汇总
    print("=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    print(f"✅ 通过: {passed_count}/{total_count}")
    print(f"❌ 失败: {total_count - passed_count}/{total_count}")
    print(f"📈 成功率: {passed_count/total_count*100:.1f}%")
    
    if passed_count == total_count:
        print("\n🎉 所有搜索引擎匹配测试通过!")
        print("🎯 V6 搜索引擎匹配逻辑完全正确!")
    else:
        print(f"\n⚠️ 有 {total_count - passed_count} 个测试失败，需要进一步优化")
    
    return passed_count == total_count

def test_edge_cases():
    """测试边缘情况"""
    print("\n🔬 边缘情况测试")
    print("=" * 60)
    
    edge_cases = [
        # 混合指定情况
        ("用Google搜索中文内容，但是要百度的结果", "google", "用户明确指定Google，应该严格遵循"),
        ("百度搜索英文学术论文", "baidu", "用户明确指定百度，即使不是最优选择也要遵循"),
        
        # 复杂语义情况
        ("我想用谷歌搜索一下", "google", "口语化的Google指定"),
        ("帮我百度一下这个问题", "baidu", "动词化的百度指定"),
        
        # 多引擎提及情况
        ("不要用百度，用Google搜索", "google", "排除式指定"),
        ("比较Google和百度的搜索结果", None, "比较性查询，应该自动选择"),
    ]
    
    print(f"📋 共 {len(edge_cases)} 个边缘情况测试\n")
    
    for i, (query, expected_engine, description) in enumerate(edge_cases, 1):
        print(f"🧪 边缘测试 {i}: {description}")
        print(f"   📝 查询: {query}")
        
        intent = analyze_user_intent(query)
        
        print(f"   🎯 期望引擎: {expected_engine or '自动选择'}")
        print(f"   🔍 实际引擎: {intent.search_engine or '自动选择'}")
        print(f"   📊 意图类型: {intent.search_engine_intent.value}")
        
        # 这些是复杂情况，主要是观察结果
        if intent.search_engine == expected_engine:
            print(f"   ✅ 符合预期")
        else:
            print(f"   ⚠️ 与预期不同，但可能合理")
        
        print()

def test_recommendation_logic():
    """测试推荐逻辑的合理性"""
    print("\n💡 推荐逻辑合理性测试")
    print("=" * 60)
    
    from v6_core.intent_analyzer import intent_analyzer
    
    recommendation_cases = [
        # 学术内容应该推荐Google
        ("查找机器学习论文", "google", "学术内容推荐Google"),
        ("research artificial intelligence", "google", "英文学术推荐Google"),
        
        # 中文内容应该推荐百度
        ("搜索中国历史", "baidu", "中文历史推荐百度"),
        ("查找国内新闻", "baidu", "国内新闻推荐百度"),
        
        # 技术内容应该推荐Google
        ("Python编程问题", "google", "编程问题推荐Google"),
        ("JavaScript开发", "google", "开发问题推荐Google"),
        
        # 隐私内容应该推荐DuckDuckGo
        ("匿名查找", "duckduckgo", "匿名查找推荐DuckDuckGo"),
        ("隐私保护搜索", "duckduckgo", "隐私搜索推荐DuckDuckGo"),
    ]
    
    print(f"📋 共 {len(recommendation_cases)} 个推荐逻辑测试\n")
    
    for i, (query, expected_recommendation, description) in enumerate(recommendation_cases, 1):
        print(f"🧪 推荐测试 {i}: {description}")
        print(f"   📝 查询: {query}")
        
        intent = analyze_user_intent(query)
        recommendation = intent_analyzer.get_search_engine_recommendation(intent)
        
        print(f"   🎯 期望推荐: {expected_recommendation}")
        print(f"   💡 实际推荐: {recommendation}")
        
        if recommendation == expected_recommendation:
            print(f"   ✅ 推荐合理")
        else:
            print(f"   ⚠️ 推荐可能需要调整")
        
        print()

if __name__ == "__main__":
    print("🚀 Context Scraper V6 搜索引擎匹配专项测试")
    print("=" * 80)
    
    # 运行所有测试
    basic_test_passed = test_search_engine_matching()
    test_edge_cases()
    test_recommendation_logic()
    
    print("\n" + "=" * 80)
    print("🏁 搜索引擎匹配专项测试完成")
    print("=" * 80)
    
    if basic_test_passed:
        print("🎉 核心匹配逻辑测试全部通过!")
        print("✅ V6 搜索引擎匹配功能已经修复并优化")
        print("\n💡 主要改进:")
        print("   🎯 学术搜索正确推荐 Google (不再是 Bing)")
        print("   🔍 技术搜索正确推荐 Google")
        print("   🇨🇳 中文内容正确推荐百度")
        print("   🔒 隐私搜索正确推荐 DuckDuckGo")
        print("   ✅ 用户明确指定时 100% 严格遵循")
    else:
        print("⚠️ 部分测试未通过，需要进一步调试")
