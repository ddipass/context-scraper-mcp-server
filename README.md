# Context Scraper MCP Server

一个基于 [Crawl4AI](https://github.com/unclecode/crawl4ai) 的 Model Context Protocol (MCP) 服务器，为 Amazon Q Developer 和其他 AI 工具提供强大的网页爬取、学术搜索和智能研究功能。

## 🚀 核心特性

- **智能网页爬取**: 支持基础、隐身、地理位置伪装等多种爬取模式
- **学术搜索引擎**: 集成 Google Scholar、arXiv、PubMed 等学术数据库
- **智能配置管理**: 灵活的配置系统，支持运行时调整
- **实验性AI分析**: 可选的Claude API集成用于高级内容分析

## 📦 安装

### 前置要求
- Python 3.12+
- uv (推荐) 或 pip

### 方法一：使用 uv (推荐)

```bash
# 1. 克隆项目
git clone https://github.com/ddipass/context-scraper-mcp-server.git
cd context-scraper-mcp-server

# 2. 使用 uv 同步依赖
uv sync

# 3. 激活虚拟环境
source .venv/bin/activate

# 4. 运行 Crawl4AI 设置
crawl4ai-setup
```

### 方法二：使用传统 pip

```bash
# 1. 克隆项目
git clone https://github.com/ddipass/context-scraper-mcp-server.git
cd context-scraper-mcp-server

# 2. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或 .venv\Scripts\activate  # Windows

# 3. 安装项目依赖
pip install -e .

# 4. 安装浏览器依赖
python -m playwright install chromium

# 5. 运行 Crawl4AI 设置
crawl4ai-setup
```

### 关于 uv

我们推荐使用 [uv](https://github.com/astral-sh/uv) - 这是一个用 Rust 构建的现代 Python 包管理器：

- ⚡ **速度快**: 比传统 pip 快 10-100 倍
- 🛡️ **可靠性**: 更好的依赖解析和冲突检测
- 🎯 **MCP 官方推荐**: Python MCP SDK 推荐的标准工具

安装 uv:
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或使用 pip
pip install uv
```

## 🔧 MCP 配置

### Amazon Q Developer 配置

在 `~/.aws/amazonq/mcp.json` 文件中添加以下配置：

```json
{
  "mcpServers": {
    "ContextScraper": {
      "command": "/absolute/path/to/context-scraper-mcp-server/.venv/bin/mcp",
      "args": [
        "run",
        "/absolute/path/to/context-scraper-mcp-server/server_v9.py"
      ],
      "cwd": "/absolute/path/to/context-scraper-mcp-server"
    }
  }
}
```

**重要**: 请将 `/absolute/path/to/context-scraper-mcp-server` 替换为你的实际项目路径。

### 获取项目绝对路径

```bash
cd context-scraper-mcp-server
pwd
# 将输出的路径复制到配置文件中
```

### 验证配置

启动 Amazon Q Developer 后，你应该能看到 ContextScraper 工具可用。可以使用以下命令测试：

```
使用 system_status 工具检查服务器状态
```

## 🛠️ 主要工具

### 🎓 学术搜索工具
- `academic_search` - 多数据源学术搜索 (Google Scholar, arXiv, PubMed)

### 🕷️ 网页爬取工具
- `crawl` - 基础网页爬取
- `crawl_stealth` - 隐身模式爬取
- `crawl_with_geolocation` - 地理位置伪装爬取
- `crawl_with_retry` - 重试机制爬取
- `crawl_with_intelligence` - 智能爬取模式

### ⚙️ 配置管理工具
- `configure_crawl_settings` - 爬取参数配置
- `quick_config_content_limit` - 快速设置内容显示限制
- `quick_config_word_threshold` - 快速设置词数阈值
- `system_status` - 系统状态监控

### 🔬 实验性工具
- `experimental_claude_analysis` - Claude AI 内容分析 (需要API配置)

## 💡 使用示例

### 学术搜索
```python
# 在 arXiv 搜索机器学习论文
result = await academic_search("machine learning transformers", "arxiv")

# 在 PubMed 搜索医学文献
result = await academic_search("COVID-19 vaccine effectiveness", "pubmed")

# 在 Google Scholar 搜索
result = await academic_search("climate change", "google_scholar")
```

### 网页爬取
```python
# 基础爬取
result = await crawl("https://example.com")

# 隐身模式爬取
result = await crawl_stealth("https://protected-site.com")

# 智能爬取
result = await crawl_with_intelligence("https://news-site.com", "smart")

# 地理位置伪装爬取
result = await crawl_with_geolocation("https://geo-restricted.com", "newyork")

# 重试机制爬取
result = await crawl_with_retry("https://unstable-site.com", max_retries=3)
```

### 配置管理
```python
# 快速设置内容显示限制
result = await quick_config_content_limit(5000)

# 快速设置词数阈值
result = await quick_config_word_threshold(100)

# 查看系统状态
result = await system_status()

# 配置爬取参数
result = await configure_crawl_settings("update", "content_limits", markdown_display_limit=8000)
```

### 实验性功能
```python
# Claude AI 内容分析 (需要配置API)
result = await experimental_claude_analysis("分析这段文本的主要观点", "general", enable_claude=True)
```

## 📁 项目结构

```
context-scraper-mcp-server/
├── server_v9.py              # 🚀 主服务器文件 (当前版本)
├── server_v8.py              # V8 版本服务器
├── server_v7.py              # V7 版本服务器
├── v9_core/                  # 🧠 V9 核心模块
│   ├── intent_analyzer.py    #   🎯 用户意图分析引擎
│   ├── crawl_config_manager.py #   ⚙️ 爬取配置管理器
│   └── config_manager.py     #   📋 通用配置管理器
├── v9_config/                # 📋 V9 配置文件
│   └── crawl_config.json     #   🔧 爬取参数配置
├── config/                   # 🗂️ 通用配置目录
│   ├── claude_config_example.json # Claude API 配置示例
│   └── v6_config/            #   历史版本配置
├── docs/                     # 📚 文档目录
│   ├── architecture/         #   🏗️ 架构文档
│   ├── development/          #   🔧 开发文档
│   └── versions/             #   📋 版本文档
├── legacy/                   # 📦 历史版本和备份
├── .venv/                    # 🐍 Python 虚拟环境
├── pyproject.toml            # 📋 项目配置文件
├── uv.lock                   # 🔒 依赖锁定文件
└── README.md                 # 📖 项目说明文档
```

## 🔗 Server V9 依赖关系

### 核心依赖结构
```
server_v9.py (主服务器)
├── v9_core/
│   ├── intent_analyzer.py    # 用户意图分析 (独立模块)
│   └── crawl_config_manager.py # 爬取配置管理 (独立模块)
├── v9_config/
│   └── crawl_config.json     # 配置文件 (JSON格式)
└── 外部依赖
    ├── crawl4ai             # 网页爬取引擎
    ├── mcp                  # Model Context Protocol
    └── aiohttp              # 异步HTTP客户端
```

### 模块职责
- **`server_v9.py`** - 主服务器，集成所有V9功能，提供MCP工具接口
- **`intent_analyzer.py`** - 分析用户意图，支持搜索、爬取、研究等多种意图类型
- **`crawl_config_manager.py`** - 管理爬取配置，支持运行时动态调整参数
- **`crawl_config.json`** - 存储用户偏好和系统配置

## 🚀 V9 核心功能

### 🎯 智能意图分析
- **多意图识别**: 自动识别搜索、爬取、研究、提取、监控、对比等意图类型
  - 相关函数: `analyze_user_intent()` (v9_core/intent_analyzer.py)
- **搜索引擎智能选择**: 支持明确指定、隐含偏好、自动选择三种模式
  - 相关枚举: `SearchEngineIntent`, `IntentType`
- **置信度评估**: 为每个意图分析提供置信度评分
  - 相关类: `UserIntent` (包含confidence字段)

### ⚙️ 动态配置管理
- **运行时配置**: 无需重启即可调整爬取参数
  - 相关函数: `configure_crawl_settings()`, `reload_crawl_config()`
- **分层配置**: 内容限制、质量控制、时间控制、用户偏好分离管理
  - 相关函数: `get_crawl_config()` (v9_core/crawl_config_manager.py)
- **配置持久化**: 自动保存用户配置偏好
  - 配置文件: `v9_config/crawl_config.json`
- **快速配置工具**: 提供便捷的参数调整接口
  - 相关函数: `quick_config_content_limit()`, `quick_config_word_threshold()`
- **自动虚拟环境**: 启动时自动激活项目虚拟环境
  - 相关函数: `activate_virtual_environment()` (server_v9.py)
- **工作目录修正**: 自动切换到正确的工作目录
  - 实现位置: server_v9.py 启动脚本

### 🕷️ 增强爬取能力
- **多模式爬取**: 基础、隐身、地理位置伪装、重试机制
  - 相关函数: `crawl()`, `crawl_stealth()`, `crawl_with_geolocation()`, `crawl_with_retry()`
- **智能内容处理**: 自动过滤噪音、提取核心内容
  - 相关函数: `crawl_with_intelligence()`
- **批量处理**: 支持并发爬取多个URL
  - 相关函数: `crawl_multiple()` (如果存在)

### 🎓 学术搜索集成
- **多数据源**: Google Scholar、arXiv、PubMed等学术数据库
  - 相关函数: `academic_search()`
- **深度爬取**: 支持搜索结果的深度内容提取
  - 参数: `deep_crawl_count` in `academic_search()`
- **结果优化**: 智能去重和内容结构化
  - 内置于学术搜索函数中

### 🔧 实验性功能
- **Claude AI 分析**: 可选的Claude API集成，用于高级内容分析
  - 相关函数: `experimental_claude_analysis()`
- **系统状态监控**: 实时监控服务器状态和性能
  - 相关函数: `system_status()`

## ⚙️ 高级配置

### Claude API 配置 (可选)

如果需要使用 Claude API 功能，可以配置 `config/claude_config_example.json`：

```json
{
  "claude_api": {
    "api_key": "your-api-key-here",
    "base_url": "https://api.anthropic.com",
    "model": "claude-3-sonnet-20240229",
    "enabled": false,
    "timeout": 30,
    "max_tokens": 4000,
    "temperature": 0.7
  }
}
```

### 爬取配置

编辑 `v9_config/crawl_config.json` 来调整爬取参数：

```json
{
  "content_limits": {
    "markdown_display_limit": 3000,
    "word_count_threshold": 50
  },
  "quality_control": {
    "min_content_length": 100,
    "enable_content_filtering": true
  },
  "user_preferences": {
    "show_word_count": true,
    "show_crawl_info": true
  }
}
```

## 🎯 适用场景

- **学术研究**: 文献搜索、论文分析、引用追踪
- **市场调研**: 竞争分析、行业报告、趋势监控
- **技术文档**: API 文档整理、技术资料收集
- **内容创作**: 素材收集、事实核查、灵感发现

## 🔧 故障排除

### 常见问题

1. **找不到 mcp 命令**
   ```bash
   # 确保虚拟环境已激活
   source .venv/bin/activate
   which mcp
   ```

2. **路径配置错误**
   ```bash
   # 获取正确的绝对路径
   cd context-scraper-mcp-server
   pwd
   ```

3. **权限问题**
   ```bash
   # 检查文件权限
   ls -la ~/.aws/amazonq/mcp.json
   chmod 644 ~/.aws/amazonq/mcp.json
   ```

### 测试连接

```bash
# 直接运行服务器测试
cd context-scraper-mcp-server
source .venv/bin/activate
.venv/bin/mcp run server_v9.py
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 MIT 许可证。

## 🙏 致谢

- [Crawl4AI](https://github.com/unclecode/crawl4ai) - 强大的网页爬取库
- [Model Context Protocol](https://modelcontextprotocol.io/) - AI 工具集成标准

## 📚 相关链接

- [Crawl4AI 文档](https://docs.crawl4ai.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Amazon Q Developer](https://aws.amazon.com/q/developer/)
