# 🚀 Context Scraper MCP Server - 项目总览

## 📁 项目结构

```
context-scraper-mcp-server/
├── 🔧 核心服务器文件
│   ├── server.py                    # V1 原版 (8工具 + 8提示)
│   ├── server_v2_enhanced.py        # V2 技术增强版 (12工具 + 13提示)
│   └── server_v3_smart.py          # V3 智能口语版 (12工具 + 5口语提示)
│
├── 🧩 功能模块
│   ├── anti_detection.py            # 反爬虫检测模块
│   └── smart_prompts.py            # 智能提示路由模块
│
├── 📚 文档指南
│   ├── README.md                    # 项目介绍
│   ├── USAGE_GUIDE.md              # 使用指南
│   ├── ENHANCED_FEATURES_GUIDE.md  # V2增强功能指南
│   ├── V3_SMART_UPGRADE_GUIDE.md   # V3智能版升级指南
│   ├── SERVER_MANAGEMENT_GUIDE.md  # 服务器管理指南
│   └── PROJECT_OVERVIEW.md         # 本文档
│
├── 🛠️ 管理工具
│   └── manage_server.py            # 服务器管理脚本
│
└── ⚙️ 配置文件
    ├── pyproject.toml              # 项目配置
    ├── .python-version             # Python版本
    └── .amazonq/                   # Amazon Q 配置目录
```

## 🎯 版本对比

| 特性 | V1 原版 | V2 技术增强版 | V3 智能口语版 |
|------|---------|---------------|---------------|
| **文件名** | `server.py` | `server_v2_enhanced.py` | `server_v3_smart.py` |
| **工具数量** | 8个 | 12个 | **17个** |
| **提示数量** | 8个 | 13个 | **6个** |
| **反爬虫能力** | 基础 | 高级 | 高级 |
| **系统管理** | ❌ | ❌ | **✅** |
| **用户体验** | 技术化 | 技术化 | 口语化 |
| **适用人群** | 开发者 | 高级用户 | 所有用户 |
| **学习成本** | 中等 | 较高 | 很低 |

## 🛠️ 核心工具对比

### 基础工具 (所有版本都有)
| 工具名 | 功能描述 |
|--------|----------|
| `crawl` | 基础网页爬取 |
| `crawl_with_selector` | CSS选择器精确提取 |
| `crawl_multiple` | 批量URL爬取 |
| `health_check` | 网站可访问性检查 |
| `crawl_clean` | 智能内容过滤 |
| `crawl_with_screenshot` | 截图功能 |
| `crawl_dynamic` | 动态内容处理 |
| `crawl_smart_batch` | 智能批量处理 |

### 反爬虫工具 (V2/V3 独有)
| 工具名 | 功能描述 |
|--------|----------|
| `crawl_stealth` | 隐身爬取 (UA轮换+指纹伪装) |
| `crawl_with_geolocation` | 地理位置伪装 |
| `crawl_with_retry` | 自动重试机制 |
| `crawl_concurrent_optimized` | 智能并发控制 |

### 系统管理工具 (V3 独有)
| 工具名 | 功能描述 |
|--------|----------|
| `check_server_status` | 检查服务器运行状态 |
| `manage_server` | 服务器管理 (启动/停止/重启) |
| `scan_junk_files` | 扫描垃圾文件和缓存 |
| `clean_junk_files` | 清理垃圾文件 |
| `get_system_info` | 系统资源监控 |

## 🎨 提示系统对比

### V1/V2 技术化提示 (13个)
- `create_context_from_url` - 保存到上下文
- `research_with_sources` - 多源研究
- `extract_product_data` - 产品信息提取
- `monitor_site_content` - 内容监控
- `analyze_competitor_sites` - 竞争对手分析
- `capture_dynamic_content` - 动态内容捕获
- `extract_structured_data` - 结构化数据提取
- `quick_site_audit` - 快速审计
- `stealth_research` - 隐身研究 (V2独有)
- `competitive_intelligence` - 竞争情报 (V2独有)
- `market_monitoring_setup` - 市场监控 (V2独有)
- `anti_detection_audit` - 反检测审计 (V2独有)
- `data_extraction_optimization` - 数据提取优化 (V2独有)

### V3 口语化提示 (6个)
- `help_me_crawl` - 万能助手 ("帮我爬网站")
- `help_me_research` - 研究助手 ("帮我研究一下")
- `help_me_get_data` - 数据提取 ("帮我抓数据")
- `help_me_monitor` - 监控助手 ("帮我盯着看")
- `help_me_check` - 网站体检 ("帮我看看这网站")
- `help_me_manage_system` - 系统管理 ("帮我管理系统") 🆕

## 🚀 使用场景推荐

### 🎯 V1 原版适合
- ✅ 学习和了解基础功能
- ✅ 稳定性要求高的环境
- ✅ 简单的爬取需求
- ✅ 作为备份方案

### 🔧 V2 技术增强版适合
- ✅ 面对严格反爬虫的网站
- ✅ 需要精确控制爬取策略
- ✅ 大规模数据收集项目
- ✅ 技术用户和开发者

### 🤖 V3 智能口语版适合
- ✅ 日常使用，追求简单易用
- ✅ 非技术用户
- ✅ 自然语言交互偏好
- ✅ 移动端或语音输入
- ✅ **系统管理和维护** 🆕
- ✅ **一站式解决方案** 🆕

## 📋 部署配置

### MCP 配置示例

#### 单版本部署 (推荐)
```json
{
    "mcpServers": {
        "ContextScraper": {
            "command": "uv",
            "args": ["run", "--with", "mcp", "mcp", "run", "server_v3_smart.py"],
            "cwd": "/Users/dpliu/EC2/context-scraper-mcp-server"
        }
    }
}
```

#### 多版本并存 (测试用)
```json
{
    "mcpServers": {
        "ContextScraperV1": {
            "command": "uv",
            "args": ["run", "--with", "mcp", "mcp", "run", "server.py"],
            "cwd": "/Users/dpliu/EC2/context-scraper-mcp-server"
        },
        "ContextScraperV2": {
            "command": "uv",
            "args": ["run", "--with", "mcp", "mcp", "run", "server_v2_enhanced.py"],
            "cwd": "/Users/dpliu/EC2/context-scraper-mcp-server"
        },
        "ContextScraperV3": {
            "command": "uv",
            "args": ["run", "--with", "mcp", "mcp", "run", "server_v3_smart.py"],
            "cwd": "/Users/dpliu/EC2/context-scraper-mcp-server"
        }
    }
}
```

## 🔄 版本升级路径

### 保守升级
```
V1 原版 → 测试 V2 → 确认后切换到 V2
```

### 激进升级
```
V1 原版 → 直接升级到 V3 智能版
```

### 渐进升级 (推荐)
```
V1 原版 → 并行测试 V2/V3 → 选择最适合的版本
```

## 💡 最佳实践

### 1. 版本选择
- **生产环境**: V3 智能版 (用户体验最佳)
- **开发测试**: V2 技术版 (功能最全面)
- **应急备份**: V1 原版 (最稳定)

### 2. 配置建议
- 使用单一版本，避免工具名称冲突
- 定期备份配置文件
- 根据目标网站选择合适的反爬虫策略

### 3. 使用技巧
- V3版本：用自然语言描述需求
- V2版本：选择具体的技术工具
- V1版本：使用基础功能组合

## 🎉 项目亮点

1. **渐进式架构**: 三个版本并存，满足不同需求
2. **向后兼容**: 新版本不影响旧版本使用
3. **模块化设计**: 功能模块独立，易于维护
4. **用户体验优化**: 从技术化到口语化的演进
5. **反爬虫能力**: 业界领先的反检测技术
6. **智能化**: 自动意图识别和工具选择

这个项目真正实现了从"**让人适应工具**"到"**让工具理解人**"的转变！🚀
