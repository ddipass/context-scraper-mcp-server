# smart_prompts.py - 智能口语化提示模块
from typing import Dict, List, Tuple
import re

class SmartPromptRouter:
    """智能提示路由器 - 理解中文口语化需求"""
    
    def __init__(self):
        # 意图识别关键词映射
        self.intent_keywords = {
            "research": [
                "研究", "分析", "了解", "看看", "调查", "查查", 
                "搞清楚", "弄明白", "深入了解", "详细分析"
            ],
            "extract_data": [
                "抓数据", "提取", "获取", "收集", "整理", "抓取",
                "拿到", "搞到", "弄出来", "导出", "爬取"
            ],
            "monitor": [
                "监控", "盯着", "关注", "跟踪", "定期看", "持续观察",
                "盯住", "看着", "注意", "观察变化"
            ],
            "check": [
                "检查", "测试", "看看", "体检", "诊断", "评估",
                "审计", "检测", "验证", "确认"
            ],
            "stealth": [
                "偷偷", "悄悄", "隐身", "不被发现", "绕过", "避开",
                "躲避", "隐蔽", "暗中", "秘密"
            ],
            "competitive": [
                "竞争对手", "对手", "同行", "友商", "竞品", "其他家",
                "别人家", "同类", "竞争者"
            ],
            "price": [
                "价格", "报价", "定价", "收费", "费用", "成本",
                "多少钱", "贵不贵", "便宜", "优惠"
            ],
            "product": [
                "产品", "商品", "货物", "东西", "物品", "服务",
                "项目", "方案"
            ],
            "contact": [
                "联系方式", "电话", "邮箱", "地址", "微信", "QQ",
                "联系人", "客服", "咨询"
            ]
        }
        
        # 困难场景关键词
        self.difficulty_keywords = {
            "access_problem": [
                "打不开", "访问不了", "进不去", "连不上", "加载不出来",
                "404", "403", "超时", "失败", "错误"
            ],
            "anti_crawler": [
                "反爬虫", "被封", "被限制", "验证码", "人机验证",
                "IP被封", "访问限制", "检测到爬虫"
            ],
            "dynamic_content": [
                "动态加载", "需要等待", "慢慢加载", "异步", "JavaScript",
                "SPA", "单页应用", "Ajax"
            ]
        }
    
    def analyze_intent(self, user_input: str) -> Dict:
        """分析用户意图"""
        user_input = user_input.lower()
        
        # 检测主要意图
        main_intent = "general"
        intent_scores = {}
        
        for intent, keywords in self.intent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in user_input)
            if score > 0:
                intent_scores[intent] = score
        
        if intent_scores:
            main_intent = max(intent_scores, key=intent_scores.get)
        
        # 检测特殊场景
        special_scenarios = []
        for scenario, keywords in self.difficulty_keywords.items():
            if any(keyword in user_input for keyword in keywords):
                special_scenarios.append(scenario)
        
        # 检测数据类型
        data_types = []
        for data_type in ["price", "product", "contact"]:
            if any(keyword in user_input for keyword in self.intent_keywords[data_type]):
                data_types.append(data_type)
        
        return {
            "main_intent": main_intent,
            "intent_scores": intent_scores,
            "special_scenarios": special_scenarios,
            "data_types": data_types,
            "is_stealth_needed": "stealth" in intent_scores,
            "is_competitive": "competitive" in intent_scores
        }
    
    def generate_strategy(self, analysis: Dict, urls: str) -> Dict:
        """根据分析结果生成执行策略"""
        strategy = {
            "tools": [],
            "config": {},
            "approach": "standard"
        }
        
        # 根据主要意图选择工具
        if analysis["main_intent"] == "research":
            if analysis["is_competitive"]:
                strategy["tools"] = ["crawl_concurrent_optimized", "crawl_smart_batch"]
                strategy["approach"] = "competitive_analysis"
            elif analysis["is_stealth_needed"]:
                strategy["tools"] = ["crawl_stealth", "crawl_with_geolocation"]
                strategy["approach"] = "stealth_research"
            else:
                strategy["tools"] = ["crawl_clean", "crawl_smart_batch"]
                strategy["approach"] = "standard_research"
        
        elif analysis["main_intent"] == "extract_data":
            if analysis["data_types"]:
                strategy["config"]["content_type"] = analysis["data_types"][0]
            strategy["tools"] = ["crawl_smart_batch", "crawl_with_selector"]
            strategy["approach"] = "data_extraction"
        
        elif analysis["main_intent"] == "monitor":
            strategy["tools"] = ["crawl_clean", "crawl_with_screenshot"]
            strategy["approach"] = "monitoring_setup"
        
        elif analysis["main_intent"] == "check":
            strategy["tools"] = ["health_check", "crawl_stealth", "crawl_with_retry"]
            strategy["approach"] = "comprehensive_audit"
        
        # 处理特殊场景
        if "access_problem" in analysis["special_scenarios"]:
            strategy["tools"].insert(0, "crawl_with_retry")
        
        if "anti_crawler" in analysis["special_scenarios"]:
            strategy["tools"].insert(0, "crawl_stealth")
        
        if "dynamic_content" in analysis["special_scenarios"]:
            strategy["tools"].append("crawl_dynamic")
        
        return strategy

# 全局路由器实例
smart_router = SmartPromptRouter()

def analyze_user_request(user_input: str, urls: str = "") -> str:
    """分析用户请求并生成执行计划"""
    analysis = smart_router.analyze_intent(user_input)
    strategy = smart_router.generate_strategy(analysis, urls)
    
    # 生成执行计划的自然语言描述
    plan_description = f"""
🤖 **我理解你的需求：**
- 主要意图: {get_intent_description(analysis['main_intent'])}
- 特殊情况: {', '.join(analysis['special_scenarios']) if analysis['special_scenarios'] else '无'}
- 数据类型: {', '.join(analysis['data_types']) if analysis['data_types'] else '通用'}

🚀 **执行计划：**
- 使用工具: {' → '.join(strategy['tools'])}
- 处理方式: {get_approach_description(strategy['approach'])}

💡 **我会帮你：**
{generate_action_list(analysis, strategy)}
"""
    
    return plan_description

def get_intent_description(intent: str) -> str:
    """获取意图的中文描述"""
    descriptions = {
        "research": "研究分析",
        "extract_data": "数据提取", 
        "monitor": "监控观察",
        "check": "检查测试",
        "general": "综合处理"
    }
    return descriptions.get(intent, "综合处理")

def get_approach_description(approach: str) -> str:
    """获取处理方式的中文描述"""
    descriptions = {
        "competitive_analysis": "竞争对手分析模式",
        "stealth_research": "隐身研究模式",
        "standard_research": "标准研究模式", 
        "data_extraction": "智能数据提取模式",
        "monitoring_setup": "监控设置模式",
        "comprehensive_audit": "全面审计模式"
    }
    return descriptions.get(approach, "标准处理模式")

def generate_action_list(analysis: Dict, strategy: Dict) -> str:
    """生成具体行动清单"""
    actions = []
    
    if analysis["is_stealth_needed"]:
        actions.append("✅ 使用隐身技术，避免被检测")
    
    if analysis["is_competitive"]:
        actions.append("✅ 并发处理多个竞争对手网站")
    
    if "access_problem" in analysis["special_scenarios"]:
        actions.append("✅ 自动重试，解决访问问题")
    
    if analysis["data_types"]:
        actions.append(f"✅ 专门提取{', '.join(analysis['data_types'])}相关信息")
    
    if analysis["main_intent"] == "monitor":
        actions.append("✅ 建立监控基线，跟踪变化")
    
    actions.append("✅ 整理结果，保存到规则文件")
    
    return '\n'.join(actions)
