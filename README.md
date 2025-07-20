# Context Scraper MCP Server

一个基于 [Crawl4AI](https://github.com/unclecode/crawl4ai) 的下一代 Model Context Protocol (MCP) 服务器，为 Amazon Q Developer 和其他 AI 工具提供强大的网页爬取和智能研究功能。

## 🚀 V6 核心特性 (最新)

### 🎯 用户意图至上
- **严格遵循用户指定**: 当用户明确指定搜索引擎时，系统 100% 遵循，绝不替换
- **消除系统偏见**: 不再有固化的搜索引擎偏好，用户选择至上
- **智能但不固执**: 提供建议但不强制执行

### 🔍 多搜索引擎生态
- **5大搜索引擎支持**: Google、百度、Bing、Yahoo、DuckDuckGo
- **智能引擎选择**: 基于内容类型和语言偏好自动推荐
- **智能回退机制**: 主引擎失败时自动切换备用引擎
- **实时健康检查**: 监控所有搜索引擎可用性

### 🧠 无偏见意图分析
- **精确意图识别**: 区分明确指定、隐含偏好、自动选择
- **多语言支持**: 中英文关键词智能识别
- **特殊需求检测**: 隐身模式、动态内容、批量处理

### ⚙️ 统一配置管理
- **分层配置系统**: 系统配置、用户偏好、搜索引擎配置
- **运行时热更新**: 无需重启即可修改配置
- **用户偏好持久化**: 自动保存和恢复用户设置

## 🛠️ 完整工具矩阵 (35+ 工具)

### 🚀 V6 智能搜索引擎 (4个核心工具)
- `crawl_with_intelligence` - 智能网页爬取，支持搜索引擎结果页面
- `smart_research_v6` - 基于搜索的深度研究助手
- `configure_search_engines` - 搜索引擎配置管理
- `analyze_search_intent` - 用户意图分析和解释
- `v6_system_status` - V6 系统状态监控

### 🔍 V5 分层研究引擎 (4个)
- `research_anything_v5` - 主力研究工具，支持所有模式
- `research_quick_v5` - 3-8秒快速研究
- `research_deep_v5` - 30-60秒深度分析
- `research_competitive_v5` - 专业竞争分析

### 🧠 基础爬取工具 (8个)
- `crawl` - 基础网页爬取，返回 Markdown 格式
- `crawl_clean` - 智能清理，自动过滤噪音内容
- `crawl_dynamic` - 动态内容处理，支持 JavaScript 渲染
- `crawl_with_selector` - CSS 选择器精确提取
- `crawl_multiple` - 批量爬取多个 URL
- `crawl_smart_batch` - 智能批量处理，内容类型优化
- `crawl_with_screenshot` - 网页截图 + 内容提取
- `health_check` - 网站可访问性检查

### 🎯 增强功能工具 (18个)
包括隐身爬取、地理位置伪装、重试机制、并发优化等专业功能

## 📦 安装

### 前置要求
- Python 3.12+
- uv (推荐，现代 Python 包管理器)

### 方法一：从 GitHub 克隆（推荐）

```bash
# 克隆项目
git clone https://github.com/ddipass/context-scraper-mcp-server.git
cd context-scraper-mcp-server

# 使用 uv 安装依赖
uv sync

# 激活虚拟环境
source .venv/bin/activate

# 运行 Crawl4AI 后安装设置
crawl4ai-setup
```

### 方法二：使用传统 pip

```bash
# 克隆项目
git clone https://github.com/ddipass/context-scraper-mcp-server.git
cd context-scraper-mcp-server

# 安装依赖
pip install -e .

# 安装浏览器依赖
python -m playwright install chromium

# 运行 Crawl4AI 设置
crawl4ai-setup
```

### 关于 uv

我们推荐使用 [uv](https://github.com/astral-sh/uv) - 这是一个用 Rust 构建的现代 Python 包管理器，它：
- 比传统的 pip 快得多
- 是 Python MCP SDK 推荐的标准工具
- 提供更好的依赖管理和虚拟环境处理

## 🛠️ 使用方法

### 启动服务器

```bash
# 使用 uv (推荐)
uv run --with mcp mcp run server.py

# 或使用 pip
python -m mcp run server.py
```

### 在 Amazon Q Developer 中配置

将以下配置添加到你的 MCP 客户端配置中：

#### 方法一：创建 MCP 配置文件

在 `.amazonq` 目录中创建 `mcp.json` 文件：

```json
{
    "mcpServers": {
        "ContextScraper": {
            "command": "uv",
            "args": ["run", "--with", "mcp", "mcp", "run", "server.py"],
            "cwd": "/path/to/context-scraper-mcp-server"
        }
    }
}
```

#### 方法二：直接配置（如果使用其他 MCP 客户端）

```json
{
  "mcpServers": {
    "context-scraper": {
      "command": "uv",
      "args": ["run", "--with", "mcp", "mcp", "run", "server.py"],
      "cwd": "/path/to/context-scraper-mcp-server"
    }
  }
}
```

### 验证安装

启动服务器后，你应该能看到类似以下的输出：
```
MCP Server running on stdio
```

## ⚙️ 配置说明

### Claude API 配置 (可选)

V6 支持 Claude 3.7 API 集成，用于高级内容分析功能。

#### 配置步骤

1. **编辑 Claude 配置文件**
   ```bash
   # 编辑配置文件
   nano v6_config/claude_config.json
   ```

2. **填入你的 API Key**
   ```json
   {
     "claude_api": {
       "api_key": "你的Claude API Key",
       "base_url": "http://Bedroc-Proxy-dZmq8lX6J5TY-92025060.us-west-2.elb.amazonaws.com/api/v1",
       "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
       "enabled": true,
       "timeout": 30,
       "max_tokens": 4000,
       "temperature": 0.7
     }
   }
   ```

3. **重启服务器使配置生效**
   ```bash
   python tools/manage_server.py restart
   ```

#### 配置参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `api_key` | Claude API 密钥 | `""` (必填) |
| `base_url` | API 基础URL | Bedrock代理地址 |
| `model` | 使用的模型 | `claude-3-7-sonnet` |
| `enabled` | 是否启用Claude功能 | `false` |
| `timeout` | 请求超时时间(秒) | `30` |
| `max_tokens` | 最大token数 | `4000` |
| `temperature` | 生成温度 | `0.7` |

#### 安全提醒
- 🔒 请妥善保管 API Key，不要提交到版本控制系统
- 🚫 不要在公共场所或文档中暴露 API Key
- 🔄 建议定期更换 API Key

### 搜索引擎配置

V6 支持多搜索引擎配置，详见 `v6_config/search_engines.json`：

```json
{
  "google": {
    "name": "Google",
    "enabled": true,
    "priority": 1
  },
  "baidu": {
    "name": "百度", 
    "enabled": true,
    "priority": 2
  }
}
```

## 🎮 服务器管理

项目提供了便捷的服务器管理工具：

```bash
# 查看服务器状态
python tools/manage_server.py status

# 停止服务器
python tools/manage_server.py stop

# 启动服务器
python tools/manage_server.py start

# 重启服务器
python tools/manage_server.py restart
```

## 💡 使用示例

### 🚀 V6 智能搜索（推荐）
严格遵循用户指定的搜索引擎，消除系统偏见：

```
"用Google搜索最新的AI新闻"     → 严格使用Google
"百度搜索Python教程"          → 严格使用百度  
"用必应查找学术论文"          → 严格使用Bing
"DuckDuckGo匿名搜索隐私保护"  → 严格使用DuckDuckGo
```

### 🎯 V6 核心工具直接调用

#### 智能搜索引擎
```python
# 使用crawl_with_intelligence进行搜索
await crawl_with_intelligence("https://www.google.com/search?q=AI新闻")
await crawl_with_intelligence("https://www.baidu.com/s?wd=Python教程")

# 智能研究，通过prompt引导选择搜索引擎
await smart_research_v6("机器学习发展", preferred_engine="google")

# 意图分析 - 了解V6如何理解你的需求
await analyze_search_intent("用Google搜索最新科技新闻")
```

#### 配置管理
```python
# 查看所有搜索引擎状态
await configure_search_engines("list")

# 设置默认搜索引擎
await configure_search_engines("set_default", engine="baidu")

# 健康检查
await configure_search_engines("health_check")
```

### 🔍 V5 分层研究引擎

#### 智能研究引擎
```python
# 自动模式 - AI 选择最佳策略
result = await research_anything_v5("分析特斯拉自动驾驶技术", "https://tesla.com")

# 快速模式 - 3-8秒获取核心信息
result = await research_quick_v5("了解公司基本情况", "https://company.com")

# 深度模式 - 30-60秒全面分析
result = await research_deep_v5("市场竞争分析", "https://competitor1.com,https://competitor2.com")

# 竞争分析 - 专业对比研究
result = await research_competitive_v5("产品功能对比", "https://product1.com,https://product2.com")
```

### 🛠️ 基础爬取工具

#### 基础爬取
```python
# 基础网页爬取
result = await crawl("https://example.com")

# CSS 选择器提取
result = await crawl_with_selector("https://example.com", "article, .content")

# 批量处理
result = await crawl_multiple("https://site1.com,https://site2.com,https://site3.com")
```

#### 增强功能
```python
# 智能内容过滤
result = await crawl_clean("https://news-site.com/article")

# 动态内容处理
result = await crawl_dynamic("https://spa-app.com", wait_time=5)

# 智能批量处理
result = await crawl_smart_batch("https://shop1.com,https://shop2.com", content_type="product")

# 截图功能
result = await crawl_with_screenshot("https://example.com")
```

## 📁 项目结构

```
context-scraper-mcp-server/
├── server.py                 # 🚀 主服务器 (V6)
├── v6_core/                  # 🧠 V6 核心模块
│   ├── config_manager.py     #   ⚙️ 统一配置管理
│   ├── intent_analyzer.py    #   🎯 无偏见意图分析
│   └── search_manager.py     #   🔍 多搜索引擎管理
├── v6_config/                # 📋 V6 配置文件
│   ├── search_engines.json   #   🔧 搜索引擎配置
│   ├── user_preferences.json #   👤 用户偏好设置
│   ├── system_config.json    #   🖥️ 系统配置
│   └── claude_config.json    #   🤖 Claude API配置
├── docs/                     # 📚 文档目录
│   ├── architecture/         #   🏗️ 架构文档
│   ├── development/          #   🔧 开发文档
│   └── versions/             #   📋 版本文档
├── tools/                    # 🛠️ 管理工具
│   └── manage_server.py      #   🎮 服务器管理
├── legacy/                   # 📦 历史版本
│   ├── servers/              #   🗂️ 历史服务器文件
│   ├── tests/                #   🧪 历史测试文件
│   └── configs/              #   ⚙️ 历史配置文件
└── README.md                 # 📖 项目说明
```

## 🔗 V6 依赖关系

### 核心依赖
```python
server.py (主服务器)
├── v6_core/
│   ├── config_manager.py     # 配置管理 (独立模块)
│   ├── intent_analyzer.py    # 意图分析 (独立模块)
│   └── search_manager.py     # 搜索管理 (依赖 config_manager + intent_analyzer)
├── v6_config/               # 配置文件 (JSON格式)
│   ├── search_engines.json  # 搜索引擎配置
│   ├── user_preferences.json # 用户偏好
│   ├── system_config.json   # 系统配置
│   └── claude_config.json   # Claude API配置
└── 外部依赖
    ├── crawl4ai             # 网页爬取引擎
    ├── mcp                  # Model Context Protocol
    ├── aiohttp              # 异步HTTP客户端
    └── beautifulsoup4       # HTML解析
```

### 模块关系
- **`server.py`** → 主入口，集成所有V6功能
- **`config_manager.py`** → 被所有模块使用的配置中心
- **`intent_analyzer.py`** → 独立的意图分析引擎
- **`search_manager.py`** → 依赖配置管理器和意图分析器
- **配置文件** → 所有模块的数据源

### 与历史版本的区别
- **V6**: 模块化设计，清晰的依赖关系，无循环依赖
- **V5及以前**: 通过继承链获得功能，依赖关系复杂

## 🎯 适用场景

### 研究人员
- 学术论文和资料收集
- 多源信息对比分析
- 结构化数据提取

### 商业分析师
- 市场调研和趋势分析
- 竞争对手监控
- 产品信息收集

### 开发者
- API 数据源构建
- 内容聚合服务
- 自动化数据收集

### 内容创作者
- 素材收集和整理
- 趋势监控
- 灵感来源挖掘

## 🏆 技术优势

- **完全免费**: 无需任何外部 API 密钥
- **智能优化**: 根据内容类型自动选择最佳策略
- **高性能**: 基于 Crawl4AI v0.6.3 最新优化
- **易于使用**: 自然语言描述，AI 自动选择工具
- **模块化设计**: 代码清晰，易于维护和扩展

## 📚 文档

- [V6 依赖关系分析](./docs/architecture/V6_DEPENDENCY_ANALYSIS.md) - V6 架构和依赖关系详解
- [V6 升级完成报告](./docs/development/V6_UPGRADE_COMPLETE.md) - V6 新功能和升级详情
- [V6 升级规划](./docs/development/V6_UPGRADE_PLAN.md) - V6 开发规划和设计理念
- [搜索引擎分析](./docs/architecture/SEARCH_ENGINE_ANALYSIS.md) - 搜索引擎优势分析和匹配策略
- [搜索引擎修复总结](./docs/development/SEARCH_ENGINE_FIX_SUMMARY.md) - 搜索引擎匹配问题修复
- [V5 使用指南](./docs/versions/V5_USAGE_GUIDE.md) - V5 新功能详细说明
- [使用指南](./docs/USAGE_GUIDE.md) - 详细的功能使用说明
- [服务器管理指南](./docs/SERVER_MANAGEMENT_GUIDE.md) - 服务器管理和故障排除
- [版本文档](./docs/versions/) - 各版本详细文档
- [依存关系分析](./docs/architecture/DEPENDENCY_ANALYSIS.md) - 项目架构和依存关系

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 MIT 许可证。

## 🙏 致谢

- [Crawl4AI](https://github.com/unclecode/crawl4ai) - 强大的网页爬取库
- [FastMCP](https://github.com/jlowin/fastmcp) - 简化的 MCP 服务器框架

## 📚 相关链接

- [Crawl4AI 文档](https://docs.crawl4ai.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Amazon Q Developer](https://aws.amazon.com/q/developer/)
