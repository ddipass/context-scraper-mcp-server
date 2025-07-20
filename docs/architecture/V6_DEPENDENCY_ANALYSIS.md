# V6 依赖关系分析

## 🎯 V6 架构概述

Context Scraper V6 采用模块化设计，彻底重构了依赖关系，消除了历史版本中复杂的继承链。

## 📊 核心依赖图

```
server.py (主服务器)
├── 🧠 V6 核心模块
│   ├── v6_core/config_manager.py     ← 配置管理中心
│   ├── v6_core/intent_analyzer.py    ← 意图分析引擎
│   └── v6_core/search_manager.py     ← 搜索引擎管理
│       ├── → config_manager.py       (依赖配置管理)
│       └── → intent_analyzer.py      (依赖意图分析)
├── 📋 V6 配置文件
│   ├── v6_config/search_engines.json
│   ├── v6_config/user_preferences.json
│   ├── v6_config/system_config.json
│   └── v6_config/claude_config.json
└── 🔗 外部依赖
    ├── crawl4ai                      ← 网页爬取引擎
    ├── mcp                           ← Model Context Protocol
    ├── aiohttp                       ← 异步HTTP客户端
    └── beautifulsoup4                ← HTML解析
```

## 🔧 模块详细分析

### 1. server.py (主服务器)
**职责**: MCP 服务器主入口，提供所有工具函数

**直接依赖**:
```python
# V6 核心模块
from v6_core.config_manager import get_config, get_user_preferences
from v6_core.intent_analyzer import analyze_user_intent, UserIntent, SearchEngineIntent
from v6_core.search_manager import search_with_intent, search_manager

# 外部依赖
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from mcp.server.fastmcp import Context, FastMCP
```

**提供的工具**:
- `search_with_engine` - 智能搜索
- `smart_research_v6` - 智能研究助手
- `configure_search_engines` - 配置管理
- `analyze_search_intent` - 意图分析
- `v6_system_status` - 系统状态
- `crawl_with_v6_intelligence` - 智能爬取

### 2. v6_core/config_manager.py (配置管理中心)
**职责**: 统一配置管理，支持分层配置和热更新

**依赖关系**:
```python
# 标准库
import json, os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# 无内部依赖 - 独立模块
```

**提供的功能**:
- `V6ConfigManager` - 主配置管理器
- `SearchEngineConfig` - 搜索引擎配置
- `UserPreferences` - 用户偏好配置
- `SystemConfig` - 系统配置
- `ClaudeConfig` - Claude API配置

**配置文件映射**:
```python
search_engines.json    → SearchEngineConfig
user_preferences.json  → UserPreferences  
system_config.json     → SystemConfig
claude_config.json     → ClaudeConfig
```

### 3. v6_core/intent_analyzer.py (意图分析引擎)
**职责**: 无偏见用户意图分析，严格遵循用户指定

**依赖关系**:
```python
# 标准库
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

# 无内部依赖 - 独立模块
```

**核心功能**:
- `V6IntentAnalyzer` - 主分析器
- `UserIntent` - 意图分析结果
- `SearchEngineIntent` - 搜索引擎意图类型
- `IntentType` - 主要意图类型

**分析流程**:
```python
用户输入 → 分词处理 → 搜索引擎意图分析 → 主要意图分析 → 内容类型分析 → 特殊需求分析 → UserIntent
```

### 4. v6_core/search_manager.py (搜索引擎管理)
**职责**: 多搜索引擎管理，智能选择和回退

**依赖关系**:
```python
# 标准库
import asyncio, aiohttp, time
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod
from urllib.parse import quote, urlencode

# V6 内部依赖
from .config_manager import get_config, SearchEngineConfig
from .intent_analyzer import UserIntent, SearchEngineIntent

# 外部依赖
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from bs4 import BeautifulSoup
```

**核心组件**:
- `V6SearchManager` - 主搜索管理器
- `BaseSearchEngine` - 搜索引擎基类
- `GoogleSearchEngine` - Google搜索实现
- `BaiduSearchEngine` - 百度搜索实现
- `BingSearchEngine` - Bing搜索实现

**搜索流程**:
```python
搜索请求 → 意图分析 → 引擎选择 → 搜索执行 → 结果解析 → 回退处理 → SearchResponse
```

## 🔄 数据流分析

### 配置数据流
```
JSON配置文件 → ConfigManager → 各模块使用
```

### 搜索数据流
```
用户查询 → IntentAnalyzer → SearchManager → SearchEngine → 网络请求 → 结果解析 → 用户
```

### 爬取数据流
```
URL → Crawl4AI → HTML → BeautifulSoup → Markdown → 用户
```

## 🆚 与历史版本对比

### V5及以前的依赖关系
```python
# 复杂的继承链
server_v5.py
├── from server_v4_simple import *
│   ├── from server_v3_smart import *
│   │   ├── anti_detection.py
│   │   ├── smart_prompts.py
│   │   └── system_manager.py
│   └── simple_config.py
└── server_v5_core.py
```

**问题**:
- 继承链过长，难以维护
- 循环依赖风险
- 功能耦合度高
- 难以独立测试

### V6的模块化设计
```python
# 清晰的模块边界
server.py
├── v6_core/config_manager.py     (独立)
├── v6_core/intent_analyzer.py    (独立)
└── v6_core/search_manager.py     (依赖前两者)
```

**优势**:
- 模块职责单一
- 依赖关系清晰
- 无循环依赖
- 易于测试和维护

## 🧪 依赖验证

### 模块独立性测试
```python
# 配置管理器独立性
from v6_core.config_manager import get_config
config = get_config()  # ✅ 无外部依赖

# 意图分析器独立性  
from v6_core.intent_analyzer import analyze_user_intent
intent = analyze_user_intent("test")  # ✅ 无外部依赖

# 搜索管理器依赖性
from v6_core.search_manager import search_manager  # ✅ 依赖明确
```

### 配置文件依赖
```python
# 所有配置文件都是JSON格式，无代码依赖
v6_config/
├── search_engines.json    # ✅ 纯数据
├── user_preferences.json  # ✅ 纯数据
├── system_config.json     # ✅ 纯数据
└── claude_config.json     # ✅ 纯数据
```

## 📋 依赖管理最佳实践

### 1. 单向依赖
- 高层模块依赖低层模块
- 避免循环依赖
- 明确依赖边界

### 2. 接口隔离
- 每个模块职责单一
- 提供清晰的公共接口
- 隐藏内部实现细节

### 3. 配置外部化
- 配置与代码分离
- 支持运行时配置更新
- 提供配置验证

### 4. 依赖注入
- 通过参数传递依赖
- 便于单元测试
- 提高代码灵活性

## 🚀 扩展性分析

### 添加新搜索引擎
```python
# 1. 继承BaseSearchEngine
class NewSearchEngine(BaseSearchEngine):
    async def search(self, query: str) -> SearchResponse:
        # 实现搜索逻辑
        pass

# 2. 在SearchManager中注册
def _initialize_engines(self):
    engines["new_engine"] = NewSearchEngine(config)
```

### 添加新配置类型
```python
# 1. 定义配置数据类
@dataclass
class NewConfig:
    setting1: str = "default"
    setting2: int = 100

# 2. 在ConfigManager中集成
def _load_new_config(self) -> NewConfig:
    # 加载逻辑
    pass
```

### 添加新意图类型
```python
# 1. 扩展IntentType枚举
class IntentType(Enum):
    EXISTING_TYPE = "existing"
    NEW_TYPE = "new_type"

# 2. 更新分析逻辑
def _analyze_primary_intent(self, input: str):
    # 添加新类型的识别逻辑
    pass
```

## 🎯 总结

V6的模块化架构实现了：

1. **清晰的依赖关系** - 无循环依赖，易于理解
2. **高内聚低耦合** - 每个模块职责明确
3. **良好的可测试性** - 模块可独立测试
4. **强扩展性** - 易于添加新功能
5. **配置灵活性** - 支持多层配置管理

这为项目的长期维护和发展奠定了坚实的基础。
