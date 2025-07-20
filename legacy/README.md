# Legacy Files - 历史版本文件

这个目录包含了 Context Scraper MCP Server 的历史版本文件和相关资源。

## 📁 目录结构

### `servers/` - 历史版本服务器
- `server.py` - V1 基础版本
- `server_v2_enhanced.py` - V2 增强版本 (已废弃)
- `server_v3_smart.py` - V3 智能版本
- `server_v4_simple.py` - V4 研究版本
- `server_v5.py` - V5 分层版本
- `server_v5_core.py` - V5 核心引擎
- `server_v6.py` - V6 多搜索引擎版本

### `servers/` - 支持模块
- `anti_detection.py` - 反爬虫检测模块
- `smart_prompts.py` - 智能提示模块
- `simple_config.py` - 简单配置管理
- `system_manager.py` - 系统管理模块

### `tests/` - 历史测试文件
- `quick_test_v5.py` - V5 快速测试
- `test_v6.py` - V6 综合测试
- `test_search_matching.py` - 搜索引擎匹配测试

### `configs/` - 历史配置文件
- `config.json` - 旧版配置文件

## 🔄 版本演进历史

```
V1 (server.py)
├── 基础网页爬取功能
└── 简单的 MCP 工具集成

V2 (server_v2_enhanced.py) - 已废弃
├── 增强的爬取功能
└── 反爬虫检测

V3 (server_v3_smart.py)
├── 智能提示路由
├── 反爬虫检测增强
└── 口语化需求理解

V4 (server_v4_simple.py)
├── 智能研究助手
├── Claude API 集成
└── 意图分析器

V5 (server_v5.py + server_v5_core.py)
├── 分层执行引擎
├── 实时进度反馈
├── 4种研究模式
└── 性能优化

V6 (server_v6.py) → 现在的 server.py
├── 多搜索引擎支持
├── 无偏见意图分析
├── 统一配置管理
└── 用户意图至上
```

## 📋 依赖关系

### V3 依赖
- `anti_detection.py`
- `smart_prompts.py`

### V4 依赖
- V3 的所有依赖
- `simple_config.py`

### V5 依赖
- V4 的所有依赖
- `server_v5_core.py`

### V6 依赖
- 独立的 `v6_core/` 模块
- 不再依赖历史版本

## ⚠️ 使用说明

这些历史版本文件仅供参考和学习使用，不建议在生产环境中使用。

如需使用历史版本功能，请：
1. 查看对应版本的文档
2. 确认依赖关系
3. 注意兼容性问题

## 🚀 迁移到当前版本

如果你正在使用历史版本，建议迁移到当前的主版本 (`server.py`)：

1. **从 V5 迁移**：
   - V6 完全兼容 V5 的所有功能
   - 额外获得多搜索引擎支持

2. **从 V4 迁移**：
   - 保留所有研究功能
   - 获得分层执行和搜索引擎支持

3. **从 V3 迁移**：
   - 保留智能提示功能
   - 获得研究助手和搜索引擎功能

## 📚 相关文档

- [架构文档](../docs/architecture/) - 系统架构分析
- [开发文档](../docs/development/) - 开发历程和升级记录
- [版本文档](../docs/versions/) - 各版本详细说明
