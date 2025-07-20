# Context Scraper MCP Server - Python 文件依存关系分析

## 📊 项目架构概览

本项目采用**分层演进架构**，从 V1 到 V5 逐步增强功能，每个版本都向下兼容。

## 🏗️ 核心文件依存关系图

```
server.py (主入口)
├── 基于 Crawl4AI + FastMCP
├── 独立实现，无内部依赖
└── 提供基础爬取功能

server_v3_smart.py (V3智能版)
├── 基于 server.py 的功能
├── 依赖: anti_detection.py
├── 依赖: smart_prompts.py
└── 增加智能提示和反爬虫功能

server_v4_simple.py (V4研究版)
├── 导入: from server_v3_smart import *
├── 依赖: simple_config.py
├── 增加智能研究助手功能
└── 支持 Claude API 集成

server_v5.py (V5分层版)
├── 导入: from server_v4_simple import *
├── 依赖: server_v5_core.py
├── 增加分层执行引擎
└── 实时进度反馈

server_v5_core.py (V5核心引擎)
├── 独立核心架构
├── 无内部依赖
└── 提供分层执行和进度跟踪
```

## 📁 文件分类和功能

### 🚀 主服务器文件 (4个)

#### 1. `server.py` - 基础版本
- **功能**: 基础网页爬取和内容提取
- **依赖**: 仅外部库 (crawl4ai, mcp)
- **状态**: 独立运行，无内部依赖

#### 2. `server_v3_smart.py` - 智能版本
- **功能**: 智能提示路由 + 反爬虫检测
- **依赖**: 
  - `anti_detection.py` (反爬虫模块)
  - `smart_prompts.py` (智能提示模块)
- **继承**: 基于 server.py 的功能概念

#### 3. `server_v4_simple.py` - 研究版本
- **功能**: 智能研究助手 + Claude API 集成
- **依赖**:
  - `from server_v3_smart import *` (完全继承V3)
  - `simple_config.py` (配置管理)
- **新增**: IntentAnalyzer, SmartResearchAssistant

#### 4. `server_v5.py` - 分层版本 (最新)
- **功能**: 分层执行引擎 + 实时进度反馈
- **依赖**:
  - `from server_v4_simple import *` (完全继承V4)
  - `server_v5_core.py` (V5核心引擎)
- **新增**: 4种研究模式，实时进度跟踪

### 🧠 核心功能模块 (4个)

#### 1. `server_v5_core.py` - V5核心引擎
- **功能**: 分层执行架构，进度跟踪系统
- **依赖**: 无内部依赖，纯核心逻辑
- **提供**: V5LayeredEngine, V5ProgressTracker, ResearchMode

#### 2. `anti_detection.py` - 反爬虫模块
- **功能**: 用户代理生成，地理位置伪装，重试管理
- **依赖**: 仅外部库 (crawl4ai)
- **提供**: EnhancedAntiDetection, GeolocationSpoofer, RetryManager

#### 3. `smart_prompts.py` - 智能提示模块
- **功能**: 中文口语化需求理解，智能路由
- **依赖**: 无依赖，纯逻辑处理
- **提供**: SmartPromptRouter, analyze_user_request

#### 4. `simple_config.py` - 配置管理
- **功能**: Claude API 配置管理
- **依赖**: 无依赖，文件操作
- **提供**: SimpleConfig 类

### 🛠️ 工具和管理文件 (4个)

#### 1. `system_manager.py` - 系统管理
- **功能**: 项目状态监控，垃圾文件清理
- **依赖**: 仅系统库 (psutil, pathlib)
- **提供**: MCPProjectManager

#### 2. `manage_server.py` - 服务器管理
- **功能**: 服务器启动/停止/重启
- **依赖**: 无内部依赖
- **提供**: MCPServerManager

#### 3. `quick_test_v5.py` - V5测试脚本
- **功能**: V5功能快速验证
- **依赖**: 
  - `server_v5_core.py` (测试核心组件)
  - 动态导入其他模块进行测试

#### 4. `server_v2_enhanced.py` - 历史版本
- **状态**: 已废弃，保留作为参考
- **功能**: V2增强功能实现

## 🔄 版本演进路径

```
V1 (基础) → V2 (增强) → V3 (智能) → V4 (研究) → V5 (分层)
    ↓           ↓           ↓           ↓           ↓
server.py → [废弃] → v3_smart → v4_simple → v5.py
                        ↓           ↓           ↓
                anti_detection  simple_config  v5_core
                smart_prompts
```

## 📊 依赖关系矩阵

| 文件 | 内部依赖 | 外部依赖 | 被依赖 |
|------|----------|----------|--------|
| `server.py` | 无 | crawl4ai, mcp | 概念被V3继承 |
| `anti_detection.py` | 无 | crawl4ai | V3, V4, V5 |
| `smart_prompts.py` | 无 | 无 | V3, V4, V5 |
| `server_v3_smart.py` | anti_detection, smart_prompts | crawl4ai, mcp | V4, V5 |
| `simple_config.py` | 无 | 无 | V4, V5 |
| `server_v4_simple.py` | server_v3_smart, simple_config | crawl4ai, mcp, aiohttp | V5 |
| `server_v5_core.py` | 无 | 无 | V5 |
| `server_v5.py` | server_v4_simple, server_v5_core | crawl4ai, mcp | 无 |
| `system_manager.py` | 无 | psutil, pathlib | 工具调用 |
| `manage_server.py` | 无 | subprocess | 独立工具 |
| `quick_test_v5.py` | server_v5_core | asyncio | 测试工具 |

## 🎯 关键设计模式

### 1. **分层继承模式**
- V3 → V4 → V5 逐层继承
- 每层增加新功能，保持向下兼容
- 使用 `from previous_version import *`

### 2. **模块化设计**
- 核心功能独立成模块 (anti_detection, smart_prompts)
- 配置管理独立 (simple_config)
- 核心引擎独立 (server_v5_core)

### 3. **工具分离**
- 管理工具独立 (manage_server, system_manager)
- 测试工具独立 (quick_test_v5)
- 不与主服务器耦合

## 🚀 当前推荐使用

### 生产环境
- **主服务器**: `server_v5.py` (最新功能)
- **备选**: `server_v4_simple.py` (稳定版本)

### 开发测试
- **测试工具**: `quick_test_v5.py`
- **管理工具**: `manage_server.py`

### 功能模块
- **反爬虫**: `anti_detection.py`
- **智能提示**: `smart_prompts.py`
- **配置管理**: `simple_config.py`

## 📝 维护建议

1. **主要维护**: 专注于 V5 相关文件
2. **兼容性**: 保持 V3/V4 的向下兼容
3. **模块化**: 新功能优先考虑独立模块
4. **测试**: 使用 quick_test_v5.py 验证功能

## 🔧 部署配置

当前项目使用 `server.py` 作为主入口，但实际上应该使用 `server_v5.py` 获得最新功能。

建议更新部署配置：
```json
{
    "mcpServers": {
        "ContextScraper": {
            "command": "uv",
            "args": ["run", "--with", "mcp", "mcp", "run", "server_v5.py"],
            "cwd": "/path/to/context-scraper-mcp-server"
        }
    }
}
```
