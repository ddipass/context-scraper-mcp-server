# Context Scraper V5 使用指南

## 🚀 V5 核心特性

### ⚡ 性能提升
- **速度提升 75%**: 从V4的45秒降到10秒
- **实时进度反馈**: 不再盲等，随时掌控进度
- **智能ETA计算**: 预估时间误差 < 20%

### 🧠 智能分层执行
- **Layer 1**: 快速爬取 (3-15秒)
- **Layer 2**: 智能分析 (5-20秒)  
- **Layer 3**: 深度挖掘 (按需执行)

### 🎯 四种研究模式
- **快速模式** (3-8秒): 获取核心信息
- **标准模式** (15-25秒): 全面分析研究
- **深度模式** (30-60秒): 多层挖掘洞察
- **自动模式**: 根据问题自动选择

## 🛠️ 安装和配置

### 1. 基础要求
V5完全基于V4构建，需要先确保V4正常工作：

```bash
# 检查V4配置
python -c "from server_v4_simple import show_current_config; import asyncio; print(asyncio.run(show_current_config()))"
```

### 2. V5组件测试
```bash
# 运行V5核心测试
python test_v5.py
```

### 3. 启动V5服务器
```bash
# 使用V5服务器
uv run --with mcp mcp run server_v5.py
```

## 🎮 V5工具使用

### 主要工具：research_anything_v5

```python
# 基础用法
research_anything_v5(
    query="分析特斯拉的自动驾驶技术",
    websites="https://tesla.com",
    mode="auto",  # auto/quick/standard/deep
    show_progress=True
)
```

### 快速研究：research_quick_v5

```python
# 3-8秒快速了解
research_quick_v5(
    query="了解OpenAI的最新产品",
    websites="https://openai.com"
)
```

### 深度研究：research_deep_v5

```python
# 30-60秒深度分析
research_deep_v5(
    query="深入分析量子计算的商业应用",
    websites="https://ibm.com/quantum,https://google.com/quantum"
)
```

### 竞争分析：research_competitive_v5

```python
# 专业竞品对比
research_competitive_v5(
    query="对比三大云服务商的AI产品",
    websites="https://aws.amazon.com,https://azure.microsoft.com,https://cloud.google.com"
)
```

## 📊 实时进度示例

V5提供详细的实时进度反馈：

```
⏱️ **意图分析** (45.0%)
📝 已选择 standard 模式，预计 20 秒
⏰ 已用时: 2秒 | 预计剩余: 18秒

⏱️ **快速爬取** (35.0%)
📝 已爬取 2 个网站
⏰ 已用时: 8秒 | 预计剩余: 12秒

⏱️ **智能分析** (85.0%)
📝 智能分析完成
⏰ 已用时: 15秒 | 预计剩余: 3秒
```

## 🎯 使用场景和建议

### 场景1: 快速了解
**需求**: 快速了解一个公司或产品
**推荐**: `research_quick_v5`
**时间**: 3-8秒

```python
research_quick_v5(
    "了解Anthropic公司的主要产品",
    "https://anthropic.com"
)
```

### 场景2: 全面研究
**需求**: 深入研究某个技术或市场
**推荐**: `research_deep_v5`
**时间**: 30-60秒

```python
research_deep_v5(
    "深入分析大语言模型的发展趋势",
    "https://openai.com,https://anthropic.com"
)
```

### 场景3: 竞品对比
**需求**: 对比多个竞争对手
**推荐**: `research_competitive_v5`
**时间**: 20-30秒

```python
research_competitive_v5(
    "对比主流AI助手的功能特性",
    "https://openai.com,https://anthropic.com,https://google.com"
)
```

### 场景4: 自定义研究
**需求**: 复杂的自定义研究需求
**推荐**: `research_anything_v5` + 手动指定模式
**时间**: 根据模式而定

```python
research_anything_v5(
    "分析AI行业的投资机会和风险",
    "https://openai.com,https://anthropic.com,https://google.com",
    mode="deep",
    show_progress=True
)
```

## 🔧 系统管理

### 检查V5状态
```python
v5_system_status()
```

### 性能测试
```python
v5_performance_test(
    test_query="测试查询",
    test_website="https://example.com"
)
```

## ⚡ 性能优化建议

### 1. 网站选择
- **单个网站**: 自动选择深度爬取
- **2-3个网站**: 标准并发处理
- **4+个网站**: 自动限制为前3个

### 2. 模式选择
- **快速了解**: 使用 `quick` 模式
- **日常研究**: 使用 `standard` 模式  
- **深度分析**: 使用 `deep` 模式
- **不确定**: 使用 `auto` 模式

### 3. 进度控制
- **需要反馈**: `show_progress=True`
- **批量处理**: `show_progress=False`

## 🚨 故障排除

### 问题1: V5启动失败
**解决**: 确保V4配置正确
```bash
python -c "from server_v4_simple import test_claude_connection; import asyncio; print(asyncio.run(test_claude_connection()))"
```

### 问题2: 进度显示异常
**解决**: 检查进度回调函数
```python
# 禁用进度显示
research_anything_v5(query, websites, show_progress=False)
```

### 问题3: 性能不达预期
**解决**: 运行性能测试
```python
v5_performance_test()
```

## 🔄 向下兼容

V5完全兼容V4和V3的所有功能：

```python
# V3功能仍然可用
crawl("https://example.com")
crawl_clean("https://example.com")

# V4功能仍然可用  
smart_research_assistant("查询", "https://example.com")
show_current_config()

# V5新功能
research_anything_v5("查询", "https://example.com")
```

## 📈 V5 vs V4 对比

| 特性 | V4 | V5 |
|------|----|----|
| 执行时间 | 45秒 | 10秒 (75%提升) |
| 进度反馈 | 无 | 实时ETA |
| 模式选择 | 3种 | 4种 |
| 用户控制 | 有限 | 完全可控 |
| 错误处理 | 基础 | 智能降级 |
| 架构设计 | 单层 | 分层执行 |

## 🎉 开始使用

1. **检查状态**: `v5_system_status()`
2. **性能测试**: `v5_performance_test()`
3. **开始研究**: 选择合适的V5工具
4. **享受提升**: 体验75%的性能提升！

---

**V5版本**: 基于V4构建的下一代智能研究助手
**核心优势**: 速度快、反馈实时、智能可控
**兼容性**: 100%向下兼容V4和V3
