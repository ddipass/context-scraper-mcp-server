# Context Scraper MCP Server - 依存关系可视化图

## 🎯 核心依存关系图

```mermaid
graph TD
    %% 主服务器文件
    A[server.py<br/>基础版本] --> A1[独立运行<br/>无内部依赖]
    
    B[server_v3_smart.py<br/>智能版本] --> C[anti_detection.py<br/>反爬虫模块]
    B --> D[smart_prompts.py<br/>智能提示模块]
    
    E[server_v4_simple.py<br/>研究版本] --> B
    E --> F[simple_config.py<br/>配置管理]
    
    G[server_v5.py<br/>分层版本] --> E
    G --> H[server_v5_core.py<br/>V5核心引擎]
    
    %% 工具文件
    I[system_manager.py<br/>系统管理] --> I1[独立工具<br/>无内部依赖]
    J[manage_server.py<br/>服务器管理] --> J1[独立工具<br/>无内部依赖]
    K[quick_test_v5.py<br/>V5测试] --> H
    
    %% 样式定义
    classDef serverFile fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef coreModule fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef toolFile fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef independent fill:#fff3e0,stroke:#e65100,stroke-width:2px
    
    %% 应用样式
    class A,B,E,G serverFile
    class C,D,F,H coreModule
    class I,J,K toolFile
    class A1,I1,J1 independent
```

## 🔄 版本演进流程图

```mermaid
graph LR
    V1[V1 基础版<br/>server.py] --> V2[V2 增强版<br/>已废弃]
    V2 --> V3[V3 智能版<br/>server_v3_smart.py]
    V3 --> V4[V4 研究版<br/>server_v4_simple.py]
    V4 --> V5[V5 分层版<br/>server_v5.py]
    
    %% 模块依赖
    V3 -.-> M1[anti_detection.py]
    V3 -.-> M2[smart_prompts.py]
    V4 -.-> M3[simple_config.py]
    V5 -.-> M4[server_v5_core.py]
    
    %% 样式
    classDef version fill:#bbdefb,stroke:#1976d2,stroke-width:2px
    classDef module fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    classDef deprecated fill:#ffcdd2,stroke:#d32f2f,stroke-width:2px
    
    class V1,V3,V4,V5 version
    class V2 deprecated
    class M1,M2,M3,M4 module
```

## 📊 模块功能分布图

```mermaid
pie title 文件功能分布
    "主服务器" : 4
    "核心模块" : 4
    "工具管理" : 4
```

## 🏗️ 架构层次图

```mermaid
graph TB
    subgraph "应用层"
        APP[Amazon Q Developer]
        MCP[MCP Protocol]
    end
    
    subgraph "服务层"
        V5[server_v5.py<br/>分层执行引擎]
        V4[server_v4_simple.py<br/>智能研究助手]
        V3[server_v3_smart.py<br/>智能提示路由]
    end
    
    subgraph "核心模块层"
        CORE[server_v5_core.py<br/>分层引擎]
        CONFIG[simple_config.py<br/>配置管理]
        ANTI[anti_detection.py<br/>反爬虫]
        PROMPT[smart_prompts.py<br/>智能提示]
    end
    
    subgraph "基础设施层"
        CRAWL[Crawl4AI<br/>爬取引擎]
        BROWSER[Browser<br/>浏览器]
    end
    
    subgraph "工具层"
        MGR[manage_server.py<br/>服务器管理]
        SYS[system_manager.py<br/>系统管理]
        TEST[quick_test_v5.py<br/>测试工具]
    end
    
    %% 连接关系
    APP --> MCP
    MCP --> V5
    V5 --> V4
    V4 --> V3
    V5 --> CORE
    V4 --> CONFIG
    V3 --> ANTI
    V3 --> PROMPT
    V5 --> CRAWL
    CRAWL --> BROWSER
    
    %% 样式
    classDef app fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef service fill:#f1f8e9,stroke:#558b2f,stroke-width:2px
    classDef core fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef infra fill:#fff8e1,stroke:#f57c00,stroke-width:2px
    classDef tool fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    
    class APP,MCP app
    class V5,V4,V3 service
    class CORE,CONFIG,ANTI,PROMPT core
    class CRAWL,BROWSER infra
    class MGR,SYS,TEST tool
```

## 🔍 详细依赖分析

### 直接依赖关系

| 文件 | 直接依赖 | 依赖类型 |
|------|----------|----------|
| `server_v5.py` | `server_v4_simple.py` | 完全导入 (`import *`) |
| `server_v5.py` | `server_v5_core.py` | 选择导入 |
| `server_v4_simple.py` | `server_v3_smart.py` | 完全导入 (`import *`) |
| `server_v4_simple.py` | `simple_config.py` | 选择导入 |
| `server_v3_smart.py` | `anti_detection.py` | 选择导入 |
| `server_v3_smart.py` | `smart_prompts.py` | 选择导入 |
| `quick_test_v5.py` | `server_v5_core.py` | 测试导入 |

### 间接依赖关系

```
server_v5.py
├── server_v4_simple.py
│   ├── server_v3_smart.py
│   │   ├── anti_detection.py
│   │   └── smart_prompts.py
│   └── simple_config.py
└── server_v5_core.py
```

## 🚨 潜在问题和建议

### 1. 循环依赖风险
- ✅ **当前状态**: 无循环依赖
- 🔍 **监控点**: V5 核心模块保持独立

### 2. 导入链过长
- ⚠️ **问题**: V5 → V4 → V3 → 模块，导入链较长
- 💡 **建议**: 考虑直接导入核心模块

### 3. 配置文件不一致
- ⚠️ **问题**: README 中使用 `server.py`，但最新功能在 `server_v5.py`
- 💡 **建议**: 更新配置指向 V5

### 4. 测试覆盖
- ✅ **优点**: V5 有专门测试文件
- 💡 **建议**: 增加 V3/V4 的测试覆盖

## 🎯 优化建议

### 短期优化
1. **更新主入口**: 将 `server.py` 重命名为 `server_v1.py`，`server_v5.py` 重命名为 `server.py`
2. **配置更新**: 更新 README 和配置文件指向最新版本
3. **文档同步**: 确保文档与实际使用的版本一致

### 长期优化
1. **模块重构**: 考虑将核心功能提取到独立包
2. **版本管理**: 建立更清晰的版本管��策略
3. **测试完善**: 建立完整的测试体系

## 📋 维护检查清单

- [ ] 检查所有 import 语句是否正确
- [ ] 验证版本间的兼容性
- [ ] 确保配置文件指向正确版本
- [ ] 测试所有依赖模块的功能
- [ ] 检查是否有未使用的文件
- [ ] 验证工具文件的独立性
