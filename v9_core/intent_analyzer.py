# v9_core/intent_analyzer.py - V9 无偏见意图分析器
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class IntentType(Enum):
    """意图类型"""
    SEARCH = "search"           # 搜索请求
    CRAWL = "crawl"            # 爬取请求  
    RESEARCH = "research"       # 研究分析
    EXTRACT = "extract"         # 数据提取
    MONITOR = "monitor"         # 监控任务
    COMPARE = "compare"         # 对比分析

class SearchEngineIntent(Enum):
    """搜索引擎意图"""
    EXPLICIT = "explicit"       # 明确指定
    IMPLICIT = "implicit"       # 隐含偏好
    AUTO = "auto"              # 自动选择

@dataclass
class UserIntent:
    """用户意图分析结果"""
    # 主要意图
    primary_intent: IntentType
    confidence: float
    
    # 搜索引擎相关
    search_engine: Optional[str] = None
    search_engine_intent: SearchEngineIntent = SearchEngineIntent.AUTO
    search_keywords: List[str] = None
    
    # 内容类型
    content_type: Optional[str] = None
    language_preference: Optional[str] = None
    
    # 特殊需求
    stealth_required: bool = False
    dynamic_content: bool = False
    batch_processing: bool = False
    
    # 原始输入
    raw_input: str = ""
    processed_tokens: List[str] = None

class V6IntentAnalyzer:
    """V9 无偏见意图分析器"""
    
    def __init__(self):
        # 搜索引擎关键词映射 (支持多语言)
        self.search_engine_keywords = {
            "google": [
                "google", "谷歌", "Google", "GOOGLE",
                "用google", "用谷歌", "google搜索", "谷歌搜索",
                "在google", "在谷歌", "通过google", "通过谷歌"
            ],
            "baidu": [
                "baidu", "百度", "Baidu", "BAIDU", 
                "用百度", "百度搜索", "在百度", "通过百度",
                "用baidu", "baidu搜索", "在baidu", "通过baidu"
            ],
            "bing": [
                "bing", "必应", "Bing", "BING",
                "用bing", "用必应", "bing搜索", "必应搜索",
                "在bing", "在必应", "通过bing", "通过必应"
            ],
            "yahoo": [
                "yahoo", "雅虎", "Yahoo", "YAHOO",
                "用yahoo", "用雅虎", "yahoo搜索", "雅虎搜索",
                "在yahoo", "在雅虎", "通过yahoo", "通过雅虎"
            ],
            "duckduckgo": [
                "duckduckgo", "duck", "ddg", "DuckDuckGo",
                "用duckduckgo", "duckduckgo搜索", "用ddg", "ddg搜索"
            ]
        }
        
        # 意图关键词
        self.intent_keywords = {
            IntentType.SEARCH: [
                "搜索", "查找", "找", "search", "find", "look for",
                "搜一下", "查一下", "找一下", "搜搜", "查查"
            ],
            IntentType.CRAWL: [
                "爬取", "抓取", "获取", "crawl", "scrape", "fetch",
                "爬一下", "抓一下", "取一下", "爬", "抓"
            ],
            IntentType.RESEARCH: [
                "研究", "分析", "调研", "research", "analyze", "study",
                "深入了解", "详细分析", "全面研究", "调查"
            ],
            IntentType.EXTRACT: [
                "提取", "导出", "整理", "extract", "export", "organize",
                "提取数据", "导出数据", "整理数据", "获取信息"
            ],
            IntentType.MONITOR: [
                "监控", "跟踪", "观察", "monitor", "track", "watch",
                "持续关注", "定期检查", "实时监控"
            ],
            IntentType.COMPARE: [
                "对比", "比较", "compare", "contrast", "vs",
                "对比分析", "比较分析", "竞品分析"
            ]
        }
        
        # 内容类型关键词
        self.content_type_keywords = {
            "news": ["新闻", "资讯", "消息", "news", "article"],
            "academic": ["论文", "学术", "研究", "paper", "academic", "scholar"],
            "product": ["产品", "商品", "价格", "product", "price", "shopping"],
            "social": ["社交", "微博", "推特", "social", "twitter", "weibo"],
            "video": ["视频", "影片", "video", "movie", "film"],
            "image": ["图片", "照片", "图像", "image", "photo", "picture"]
        }
        
        # 语言偏好关键词
        self.language_keywords = {
            "chinese": ["中文", "中国", "国内", "chinese", "china"],
            "english": ["英文", "英语", "国外", "english", "international"],
            "japanese": ["日文", "日语", "日本", "japanese", "japan"],
            "korean": ["韩文", "韩语", "韩国", "korean", "korea"]
        }
    
    def analyze(self, user_input: str) -> UserIntent:
        """分析用户意图"""
        # 预处理输入
        processed_input = user_input.lower().strip()
        tokens = self._tokenize(processed_input)
        
        # 分析搜索引擎意图 (最高优先级)
        search_engine, engine_intent = self._analyze_search_engine_intent(user_input)
        
        # 分析主要意图
        primary_intent, confidence = self._analyze_primary_intent(processed_input)
        
        # 分析内容类型
        content_type = self._analyze_content_type(processed_input)
        
        # 分析语言偏好
        language_preference = self._analyze_language_preference(processed_input)
        
        # 分析特殊需求
        special_needs = self._analyze_special_needs(processed_input)
        
        # 提取搜索关键词
        search_keywords = self._extract_search_keywords(user_input, search_engine)
        
        return UserIntent(
            primary_intent=primary_intent,
            confidence=confidence,
            search_engine=search_engine,
            search_engine_intent=engine_intent,
            search_keywords=search_keywords,
            content_type=content_type,
            language_preference=language_preference,
            stealth_required=special_needs.get("stealth", False),
            dynamic_content=special_needs.get("dynamic", False),
            batch_processing=special_needs.get("batch", False),
            raw_input=user_input,
            processed_tokens=tokens
        )
    
    def _tokenize(self, text: str) -> List[str]:
        """分词处理"""
        # 简单的分词，支持中英文
        tokens = re.findall(r'\w+', text)
        return tokens
    
    def _analyze_search_engine_intent(self, user_input: str) -> tuple[Optional[str], SearchEngineIntent]:
        """分析搜索引擎意图 - 核心功能，必须准确"""
        
        # 检查明确指定的搜索引擎
        for engine, keywords in self.search_engine_keywords.items():
            for keyword in keywords:
                if keyword in user_input:
                    # 找到明确指定的搜索引擎
                    return engine, SearchEngineIntent.EXPLICIT
        
        # 检查隐含偏好 (基于内容类型) - 按优化后的优先级顺序检查
        
        # 1. 学术内容偏好 - 最高优先级，Google 在学术搜索方面最强
        academic_indicators = ["学术", "论文", "研究", "paper", "research", "academic", "scholar", "科研", "期刊", "文献"]
        if any(word in user_input.lower() for word in academic_indicators):
            return "google", SearchEngineIntent.IMPLICIT
        
        # 2. 隐私保护偏好 - 高优先级，DuckDuckGo 专注隐私
        privacy_indicators = ["隐私", "匿名", "privacy", "anonymous", "私密", "保护", "安全搜索"]
        if any(word in user_input.lower() for word in privacy_indicators):
            return "duckduckgo", SearchEngineIntent.IMPLICIT
        
        # 3. 技术内容偏好 - 高优先级，Google 在技术搜索方面更强（扩展关键词，提升优先级）
        tech_indicators = [
            "编程", "代码", "技术", "开发", "programming", "coding", "development", 
            "api", "github", "教程", "tutorial", "框架", "framework", "库", "library",
            "算法", "algorithm", "数据结构", "机器学习", "人工智能", "AI", "软件", "software",
            "python", "java", "javascript", "react", "vue", "node", "数据库", "database"
        ]
        if any(word in user_input.lower() for word in tech_indicators):
            return "google", SearchEngineIntent.IMPLICIT
        
        # 4. 明确的中文地域偏好 - 中等优先级，更精确匹配（避免覆盖技术内容）
        chinese_local_indicators = [
            "中国新闻", "国内资讯", "本土品牌", "大陆政策", "中文小说", "国产", 
            "内地", "中文论坛", "国内网站", "中国公司", "国内服务"
        ]
        if any(phrase in user_input.lower() for phrase in chinese_local_indicators):
            return "baidu", SearchEngineIntent.IMPLICIT
        
        # 5. 新闻资讯偏好 - 较低优先级，根据明确的地域需求选择
        news_indicators = ["新闻", "资讯", "消息", "news", "breaking", "latest"]
        if any(word in user_input.lower() for word in news_indicators):
            # 只有明确提到中国/国内的新闻才用百度
            if any(phrase in user_input.lower() for phrase in ["中国新闻", "国内新闻", "大陆新闻"]):
                return "baidu", SearchEngineIntent.IMPLICIT
            else:
                return "google", SearchEngineIntent.IMPLICIT
        
        # 默认选择 Google（全球化考虑，技术内容更全面）
        return "google", SearchEngineIntent.AUTO
    
    def _analyze_primary_intent(self, processed_input: str) -> tuple[IntentType, float]:
        """分析主要意图"""
        intent_scores = {}
        
        for intent_type, keywords in self.intent_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in processed_input:
                    score += 1
            
            if score > 0:
                intent_scores[intent_type] = score
        
        if intent_scores:
            # 找到得分最高的意图
            primary_intent = max(intent_scores, key=intent_scores.get)
            max_score = intent_scores[primary_intent]
            total_keywords = sum(len(keywords) for keywords in self.intent_keywords.values())
            confidence = min(max_score / 3.0, 1.0)  # 标准化置信度
            return primary_intent, confidence
        
        # 默认为搜索意图
        return IntentType.SEARCH, 0.5
    
    def _analyze_content_type(self, processed_input: str) -> Optional[str]:
        """分析内容类型"""
        for content_type, keywords in self.content_type_keywords.items():
            if any(keyword in processed_input for keyword in keywords):
                return content_type
        return None
    
    def _analyze_language_preference(self, processed_input: str) -> Optional[str]:
        """分析语言偏好"""
        for language, keywords in self.language_keywords.items():
            if any(keyword in processed_input for keyword in keywords):
                return language
        
        # 基于输入文本的字符判断
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', processed_input))
        total_chars = len(processed_input.replace(' ', ''))
        
        if total_chars > 0 and chinese_chars / total_chars > 0.3:
            return "chinese"
        
        return None
    
    def _analyze_special_needs(self, processed_input: str) -> Dict[str, bool]:
        """分析特殊需求"""
        stealth_keywords = ["隐身", "偷偷", "悄悄", "绕过", "避开", "stealth", "anonymous"]
        dynamic_keywords = ["动态", "异步", "等待", "加载", "dynamic", "ajax", "spa"]
        batch_keywords = ["批量", "多个", "一批", "batch", "multiple", "bulk"]
        
        return {
            "stealth": any(keyword in processed_input for keyword in stealth_keywords),
            "dynamic": any(keyword in processed_input for keyword in dynamic_keywords),
            "batch": any(keyword in processed_input for keyword in batch_keywords)
        }
    
    def _extract_search_keywords(self, user_input: str, search_engine: Optional[str]) -> List[str]:
        """提取搜索关键词"""
        # 移除搜索引擎相关的词汇
        cleaned_input = user_input
        
        if search_engine:
            for keyword in self.search_engine_keywords.get(search_engine, []):
                cleaned_input = cleaned_input.replace(keyword, "")
        
        # 移除常见的动作词
        action_words = ["搜索", "查找", "找", "search", "find", "用", "在", "通过"]
        for word in action_words:
            cleaned_input = cleaned_input.replace(word, "")
        
        # 提取关键词
        keywords = [word.strip() for word in cleaned_input.split() if word.strip()]
        keywords = [word for word in keywords if len(word) > 1]  # 过滤单字符
        
        return keywords[:5]  # 限制关键词数量
    
    def get_search_engine_recommendation(self, intent: UserIntent) -> str:
        """根据意图推荐搜索引擎 - 基于各引擎的实际优势"""
        # 如果用户明确指定，必须尊重
        if intent.search_engine_intent == SearchEngineIntent.EXPLICIT:
            return intent.search_engine
        
        # 如果已经有隐含偏好的搜索引擎，直接使用
        if intent.search_engine_intent == SearchEngineIntent.IMPLICIT and intent.search_engine:
            return intent.search_engine
        
        # 基于内容类型和语言偏好的精确推荐（优化后的优先级）
        
        # 学术内容 - Google 是学术搜索的首选
        if intent.content_type == "academic":
            return "google"
        
        # 隐私保护需求 - DuckDuckGo 专业
        if intent.stealth_required:
            return "duckduckgo"
        
        # 技术内容 - Google 技术搜索更强（提升优先级，优于语言偏好）
        if intent.content_type in ["programming", "tech", "development"]:
            return "google"
        
        # 明确的中文地域内容 - 百度更适合（降低优先级，更精确匹配）
        if intent.language_preference == "chinese" and intent.content_type in ["news", "local", "culture"]:
            return "baidu"
        
        # 新闻内容 - 根据语言偏好
        if intent.content_type == "news":
            if intent.language_preference == "chinese":
                return "baidu"
            else:
                return "google"
        
        # 商业/产品信息 - Google 商业搜索较全面
        if intent.content_type in ["product", "business", "commercial"]:
            return "google"
        
        # 社交媒体内容 - 根据平台选择
        if intent.content_type == "social":
            return "google"  # Google 对社交媒体索引较好
        
        # 默认推荐 - Google 作为综合性最强的搜索引擎
        return "google"
    
    def explain_intent(self, intent: UserIntent) -> str:
        """解释意图分析结果"""
        explanation = f"🎯 意图分析结果:\n"
        explanation += f"主要意图: {intent.primary_intent.value} (置信度: {intent.confidence:.2f})\n"
        
        if intent.search_engine:
            engine_type = "明确指定" if intent.search_engine_intent == SearchEngineIntent.EXPLICIT else "智能推荐"
            explanation += f"搜索引擎: {intent.search_engine} ({engine_type})\n"
        
        if intent.search_keywords:
            explanation += f"搜索关键词: {', '.join(intent.search_keywords)}\n"
        
        if intent.content_type:
            explanation += f"内容类型: {intent.content_type}\n"
        
        if intent.language_preference:
            explanation += f"语言偏好: {intent.language_preference}\n"
        
        special_needs = []
        if intent.stealth_required:
            special_needs.append("隐身模式")
        if intent.dynamic_content:
            special_needs.append("动态内容")
        if intent.batch_processing:
            special_needs.append("批量处理")
        
        if special_needs:
            explanation += f"特殊需求: {', '.join(special_needs)}\n"
        
        return explanation

# 全局意图分析器实例
intent_analyzer = V6IntentAnalyzer()

def analyze_user_intent(user_input: str) -> UserIntent:
    """分析用户意图的便捷函数"""
    return intent_analyzer.analyze(user_input)
