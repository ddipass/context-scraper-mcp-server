# Context Scraper MCP Server - 项目结构

## 📁 当前项目结构

```
context-scraper-mcp-server/
├── 🚀 server.py                    # 主服务器 (V6)
├── 📖 README.md                    # 项目说明
├── ⚙️ pyproject.toml               # 项目配置
├── 🔒 uv.lock                      # 依赖锁定
├── 🚫 .gitignore                   # Git忽略规则
├── 📋 PROJECT_CLEANUP_SUMMARY.md   # 清理总结
├── 📊 PROJECT_STRUCTURE.md         # 本文件
│
├── 🧠 v6_core/                     # V6 核心模块
│   ├── config_manager.py           #   ⚙️ 统一配置管理
│   ├── intent_analyzer.py          #   🎯 无偏见意图分析
│   └── search_manager.py           #   🔍 多搜索引擎管理
│
├── 📋 v6_config/                   # V6 配置文件
│   ├── search_engines.json         #   🔧 搜索引擎配置
│   ├── user_preferences.json       #   👤 用户偏好设置
│   └── system_config.json          #   🖥️ 系统配置
│
├── 📚 docs/                        # 文档目录
│   ├── architecture/               #   🏗️ 架构文档
│   │   ├── DEPENDENCY_ANALYSIS.md  #     📊 依存关系分析
│   │   ├── DEPENDENCY_GRAPH.md     #     📈 依存关系图表
│   │   └── SEARCH_ENGINE_ANALYSIS.md #   🔍 搜索引擎分析
│   ├── development/                #   🔧 开发文档
│   │   ├── V6_UPGRADE_PLAN.md      #     📋 V6升级规划
│   │   ├── V6_UPGRADE_COMPLETE.md  #     ✅ V6升级完成
│   │   └── SEARCH_ENGINE_FIX_SUMMARY.md # 🔧 搜索引擎修复
│   └── versions/                   #   📋 版本文档
│       └── V5_USAGE_GUIDE.md       #     📖 V5使用指南
│
├── 🛠️ tools/                       # 管理工具
│   ├── manage_server.py            #   🎮 服务器管理工具
│   └── README.md                   #   📖 工具说明
│
├── 📦 legacy/                      # 历史版本
│   ├── servers/                    #   🗂️ 历史服务器文件
│   │   ├── server.py               #     V1 基础版本
│   │   ├── server_v2_enhanced.py  #     V2 增强版本
│   │   ├── server_v3_smart.py     #     V3 智能版本
│   │   ├── server_v4_simple.py    #     V4 研究版本
│   │   ├── server_v5.py           #     V5 分层版本
│   │   ├── server_v5_core.py      #     V5 核心引擎
│   │   ├── server_v6.py           #     V6 原始文件
│   │   ├── anti_detection.py      #     反爬虫模块
│   │   ├── smart_prompts.py       #     智能提示模块
│   │   ├── simple_config.py       #     简单配置管理
│   │   └── system_manager.py      #     系统管理模块
│   ├── tests/                     #   🧪 历史测试文件
│   │   ├── quick_test_v5.py       #     V5快速测试
│   │   ├── test_v6.py             #     V6综合测试
│   │   └── test_search_matching.py #     搜索匹配测试
│   ├── configs/                   #   ⚙️ 历史配置文件
│   │   └── config.json            #     旧版配置文件
│   └── README.md                  #   📖 Legacy说明
│
└── 🔧 其他文件
    ├── .amazonq/                  # Amazon Q 配置
    ├── .venv/                     # Python 虚拟环境
    └── __pycache__/               # Python 缓存
```

## 🎯 核心文件说明

### 🚀 主服务器
- **`server.py`** - 当前的主服务器，基于V6架构，提供完整的MCP服务

### 🧠 V6 核心模块
- **`v6_core/config_manager.py`** - 统一配置管理，支持分层配置和热更新
- **`v6_core/intent_analyzer.py`** - 无偏见意图分析，严格遵循用户指定
- **`v6_core/search_manager.py`** - 多搜索引擎管理，支持5大搜索引擎

### 📋 V6 配置
- **`v6_config/search_engines.json`** - 搜索引擎配置和优先级
- **`v6_config/user_preferences.json`** - 用户偏好和个性化设置
- **`v6_config/system_config.json`** - 系统级配置和性能参数

## 📊 版本演进历史

```
V1 → V2 → V3 → V4 → V5 → V6 (当前)
│     │     │     │     │     │
│     │     │     │     │     └── 多搜索引擎 + 无偏见分析
│     │     │     │     └────── 分层执行 + 实时进度
│     │     │     └─────────── 智能研究 + Claude集成
│     │     └───────────────── 智能提示 + 反爬虫
│     └─────────────────────── 增强爬取 (已废弃)
└───────────────────────────── 基础爬取
```

## 🔧 使用指南

### 启动服务器
```bash
# 使用主服务器
uv run --with mcp mcp run server.py
```

### 配置管理
```bash
# 服务器管理
python tools/manage_server.py status
python tools/manage_server.py start
python tools/manage_server.py stop
```

### 查看历史版本
```bash
# 查看所有历史版本
ls legacy/servers/

# 运行历史版本 (如果需要)
python legacy/servers/server_v5.py
```

## 📚 文档导航

### 🏗️ 架构文档
- [依存关系分析](docs/architecture/DEPENDENCY_ANALYSIS.md)
- [依存关系图表](docs/architecture/DEPENDENCY_GRAPH.md)
- [搜索引擎分析](docs/architecture/SEARCH_ENGINE_ANALYSIS.md)

### 🔧 开发文档
- [V6升级规划](docs/development/V6_UPGRADE_PLAN.md)
- [V6升级完成](docs/development/V6_UPGRADE_COMPLETE.md)
- [搜索引擎修复](docs/development/SEARCH_ENGINE_FIX_SUMMARY.md)

### 📋 版本文档
- [V5使用指南](docs/versions/V5_USAGE_GUIDE.md)

## 🎉 清理成果

### ✅ 结构优化
- 主服务器突出显示 (`server.py`)
- 历史版本完整保留 (`legacy/`)
- 文档分类清晰 (`docs/`)
- 工具独立管理 (`tools/`)

### ✅ 维护性提升
- 减少根目录文件数量
- 相关文件归类存放
- 版本历史清晰可追溯
- 配置管理统一化

### ✅ 用户体验改善
- 部署配置简化
- 文档查找便捷
- 功能使用直观
- 问题排查高效

这样的项目结构既保持了完整性，又提高了可维护性和专业性。
