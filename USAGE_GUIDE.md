# Context Scraper MCP Server - 使用指南

## 🚀 快速开始

### 启动服务器
```bash
python server.py
```

### 在 Amazon Q 中配置
```json
{
  "mcpServers": {
    "context-scraper": {
      "command": "python",
      "args": ["/path/to/context-scraper-mcp-server/server.py"]
    }
  }
}
```

## 🔧 功能详解

### 1. 基础爬取 - `crawl(url)`
**用途**: 爬取单个网页，返回 Markdown 格式内容
**示例**:
```
crawl("https://docs.crawl4ai.com")
```

### 2. 选择器爬取 - `crawl_with_selector(url, css_selector)`
**用途**: 使用 CSS 选择器精确提取特定内容
**示例**:
```
# 只提取文章内容
crawl_with_selector("https://blog.example.com/post", "article")

# 提取所有产品卡片
crawl_with_selector("https://shop.example.com", ".product-card")

# 提取导航链接
crawl_with_selector("https://example.com", "nav a")
```

**常用选择器**:
- `article` - 文章内容
- `.content, .main-content` - 主要内容区域
- `h1, h2, h3` - 标题
- `.product, .item` - 产品信息
- `nav a` - 导航链接
- `.post, .blog-post` - 博客文章

### 3. 批量爬取 - `crawl_multiple(urls_str)`
**用途**: 同时爬取多个 URL，用逗号分隔
**示例**:
```
crawl_multiple("https://site1.com,https://site2.com,https://site3.com")
```

### 4. 健康检查 - `health_check(url)`
**用途**: 检查网站是否可访问
**示例**:
```
health_check("https://example.com")
```

## 📝 提示功能

### 1. 创建上下文 - `create_context_from_url(url)`
**用途**: 将网页内容保存到 Amazon Q 的上下文规则中
**示例**:
```
create_context_from_url("https://docs.crawl4ai.com/installation")
```

### 2. 研究文档 - `create_research_context(topic, urls)`
**用途**: 从多个 URL 创建研究文档
**示例**:
```
create_research_context("AI Web Scraping", "https://crawl4ai.com,https://docs.crawl4ai.com")
```

### 3. 特定内容提取 - `extract_specific_content(url, content_type)`
**用途**: 提取特定类型的内容
**示例**:
```
extract_specific_content("https://news.site.com", "articles")
extract_specific_content("https://shop.site.com", "products")
```

**支持的内容类型**:
- `articles` - 文章内容
- `products` - 产品信息
- `links` - 链接
- `headings` - 标题
- `images` - 图片
- `navigation` - 导航
- `forms` - 表单
- `tables` - 表格

## 💡 实用场景

### 场景 1: 技术文档整理
```
# 爬取多个文档页面
crawl_multiple("https://docs.example.com/guide1,https://docs.example.com/guide2,https://docs.example.com/guide3")

# 或使用研究文档功能
create_research_context("API Documentation", "https://docs.example.com/api,https://docs.example.com/sdk")
```

### 场景 2: 竞品分析
```
# 提取产品信息
extract_specific_content("https://competitor.com/products", "products")

# 健康检查竞品网站
health_check("https://competitor.com")
```

### 场景 3: 新闻聚合
```
# 只提取新闻文章内容
crawl_with_selector("https://news.site.com/article", "article")

# 批量爬取多个新闻源
crawl_multiple("https://news1.com/today,https://news2.com/today,https://news3.com/today")
```

### 场景 4: 学术研究
```
# 创建研究主题文档
create_research_context("Machine Learning", "https://arxiv.org/paper1,https://arxiv.org/paper2")

# 提取论文标题和摘要
crawl_with_selector("https://arxiv.org/abs/2301.00001", ".title, .abstract")
```

## 🔧 高级技巧

### 1. CSS 选择器组合
```
# 多个选择器
crawl_with_selector("https://example.com", "h1, h2, .important")

# 层级选择器
crawl_with_selector("https://example.com", ".content article p")

# 属性选择器
crawl_with_selector("https://example.com", "a[href*='download']")
```

### 2. 批量处理优化
```
# 相关页面一起处理（更高效）
crawl_multiple("https://docs.site.com/page1,https://docs.site.com/page2")

# 不同域名分开处理
crawl_multiple("https://site1.com/page1,https://site1.com/page2")
crawl_multiple("https://site2.com/page1,https://site2.com/page2")
```

### 3. 错误处理
```
# 先检查网站可用性
health_check("https://example.com")

# 再进行爬取
crawl("https://example.com")
```

## 🚨 注意事项

1. **尊重网站规则**: 遵守 robots.txt 和网站使用条款
2. **合理频率**: 不要过于频繁地请求同一网站
3. **错误处理**: 使用 health_check 先验证网站可用性
4. **选择器准确性**: 使用浏览器开发者工具确认 CSS 选择器
5. **内容长度**: 批量爬取时注意内容总长度

## 🔍 故障排除

### 问题 1: 爬取失败
**解决方案**:
1. 使用 `health_check()` 检查网站可用性
2. 检查网络连接
3. 确认 URL 格式正确

### 问题 2: CSS 选择器无效
**解决方案**:
1. 使用浏览器开发者工具验证选择器
2. 尝试更通用的选择器
3. 检查页面是否为动态加载内容

### 问题 3: 内容为空
**解决方案**:
1. 检查选择器是否匹配到元素
2. 尝试不使用选择器的基础爬取
3. 确认页面内容不是 JavaScript 动态生成

## 📞 获取帮助

如果遇到问题，可以：
1. 查看错误信息
2. 运行 `python demo.py` 测试基础功能
3. 检查 Crawl4AI 文档: https://docs.crawl4ai.com/
4. 提交 Issue 到项目仓库
