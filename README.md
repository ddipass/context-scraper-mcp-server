# Context Scraper MCP Server

一个基于 [Crawl4AI](https://github.com/unclecode/crawl4ai) 的增强版 Model Context Protocol (MCP) 服务器，为 Amazon Q Developer 和其他 AI 工具提供强大的网页爬取和内容提取功能。

## 🚀 功能特性

### 🧠 智能爬取能力
- **智能内容过滤**: 自动去除广告、导航等噪音内容
- **动态内容处理**: 支持 JavaScript 渲染和 SPA 应用
- **截图功能**: 生成网页截图并转换为 Base64 格式
- **内容类型识别**: 支持 15+ 种内容类型自动识别优化

### 🛠️ 核心工具 (8个)
#### 基础工具 (4个)
- `crawl` - 基础网页爬取，返回 Markdown 格式内容
- `crawl_with_selector` - 使用 CSS 选择器精确提取特定内容
- `crawl_multiple` - 批量爬取多个 URL，用逗号分隔
- `health_check` - 检查网站可访问性和基本信息

#### 增强工具 (4个)
- `crawl_clean` - 智能清理爬取，自动过滤噪音内容
- `crawl_with_screenshot` - 爬取网页并生成截图
- `crawl_dynamic` - 动态内容爬取，等待 JavaScript 渲染
- `crawl_smart_batch` - 智能批量爬取，根据内容类型优化策略

### 🎯 智能提示系统 (9个)
- `create_context_from_url` - 智能保存到 Amazon Q 上下文
- `research_with_sources` - 基于多个来源进行深度研究
- `extract_product_data` - 智能提取产品信息
- `monitor_site_content` - 设置网站内容监控基线
- `analyze_competitor_sites` - 竞争对手网站分析
- `capture_dynamic_content` - 捕获动态加载的内容
- `extract_structured_data` - 提取结构化数据
- `quick_site_audit` - 快速网站综合审计
- 各种专业场景的定制提示

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

### 方法二：从零开始创建

如果你想从头开始创建项目：

```bash
# 初始化项目
uv init context-scraper-mcp-server
cd context-scraper-mcp-server

# 安装依赖
uv add "mcp[cli]" crawl4ai

# 激活虚拟环境
source .venv/bin/activate

# 运行 Crawl4AI 后安装设置
crawl4ai-setup
```

### 方法三：使用传统 pip

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

## 🎮 服务器管理

项目提供了便捷的服务器管理工具：

```bash
# 查看服务器状态
python manage_server.py status

# 停止服务器
python manage_server.py stop

# 启动服务器
python manage_server.py start

# 重启服务器
python manage_server.py restart
```

详细管理指南请参考 [SERVER_MANAGEMENT_GUIDE.md](./SERVER_MANAGEMENT_GUIDE.md)

## 💡 使用示例

### 智能爬取（推荐）
让 Amazon Q 根据你的描述自动选择最佳工具：

```
"帮我爬取这个商品页面的价格信息"
"获取这几个新闻网站的文章内容，需要干净的格式"
"分析这个竞争对手的产品策略"
"这个网站是动态加载的，帮我处理一下"
```

### 直接调用工具

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

## 🧠 智能特性

### 内容类型识别
支持自动识别和优化处理以下内容类型：
- `article` - 文章内容
- `product` - 产品信息
- `news` - 新闻内容
- `blog` - 博客文章
- `contact` - 联系信息
- `pricing` - 价格信息
- `navigation` - 导航结构
- `form` - 表单内容
- `table` - 表格数据
- 等 15+ 种类型

### 智能选择器映射
每种内容类型都有优化的 CSS 选择器：
```css
article: "article, .article, .post, .entry, .content, main, [role='main']"
product: ".product, .item, [data-product], .product-card, .product-info"
news: ".news, .article, .story, .post, [data-article], .news-item"
```

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

- [使用指南](./USAGE_GUIDE.md) - 详细的功能使用说明
- [服务器管理指南](./SERVER_MANAGEMENT_GUIDE.md) - 服务器管理和故障排除

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
