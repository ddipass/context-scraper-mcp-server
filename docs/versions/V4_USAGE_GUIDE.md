# Context Scraper MCP Server V4 使用指南

## 🚀 V4 新特性

### 核心改进
- **一个工具搞定所有研究** - `smart_research_assistant`
- **极简配置** - 只需配置3个参数
- **Claude 3.7集成** - 最强推理模型深度分析
- **深度网站爬取** - 自动发现相关页面
- **智能意图识别** - 自动选择最佳策略

## 📋 快速开始

### 1. 检查配置
```bash
# V4会自动创建config.json，包含默认的Bedrock Gateway配置
cat config.json
```

### 2. 测试连接
在Q CLI中运行：
```
test_claude_connection()
```

### 3. 开始研究
```
smart_research_assistant(
    "分析特斯拉的自动驾驶技术发展", 
    "https://tesla.com"
)
```

## 🎯 使用示例

### 基础研究
```
smart_research_assistant(
    "了解这家公司的主要业务",
    "https://example.com"
)
```

### 竞争分析
```
smart_research_assistant(
    "对比OpenAI和Anthropic的产品策略",
    "https://openai.com,https://anthropic.com"
)
```

### 深度研究
```
smart_research_assistant(
    "深入分析量子计算的商业应用前景",
    "https://ibm.com/quantum",
    "deep"
)
```

## 🔧 配置管理

### 查看当前配置
```
show_current_config()
```

### 更新Claude配置
```
update_claude_config(
    api_key="新的API密钥",
    base_url="新的API地址",
    model="新的模型名称"
)
```

### 测试连接
```
test_claude_connection()
```

## 🎛️ 智能策略

V4会根据你的问题自动选择策略：

| 关键词 | 策略 | 说明 |
|--------|------|------|
| "对比"、"竞争" | competitive | 并发爬取多个网站进行对比 |
| "深入"、"详细" | deep | 使用深度爬取发现更多内容 |
| "快速"、"简单" | quick | 高效爬取核心内容 |
| 其他 | standard | 标准智能爬取 |

## 📊 输出格式

V4生成结构化研究报告：

```markdown
# 🔬 智能研究报告: [你的问题]

## 📊 研究概览
- 研究类型、策略、时间等

## 🧠 Claude智能分析
- 核心发现
- 详细分析  
- 深度洞察
- 结论建议

## 📚 信息来源
- 完整的来源链接列表
```

## ⚠️ 注意事项

### 网站要求
- 必须提供目标网站URL
- 多个网站用逗号分隔
- 建议不超过5个网站

### 性能考虑
- 深度爬取可能需要15-25分钟
- 竞争分析通常10-15分钟
- 标准研究一般5-10分钟

### 错误处理
- Claude不可用时自动降级到基础分析
- 网站访问失败会尝试其他策略
- 所有V3功能保持可用

## 🆚 V3 vs V4

| 特性 | V3 | V4 |
|------|----|----|
| 工具数量 | 20+ 个独立工具 | 1个智能助手 + 配置工具 |
| 使用方式 | 需要选择具体工具 | 自然语言描述需求 |
| 分析能力 | 基础内容整理 | Claude 3.7深度分析 |
| 配置复杂度 | 硬编码 | 3参数配置文件 |
| 深度爬取 | 不支持 | 自动多层爬取 |

## 🔄 从V3迁移

V4完全兼容V3，你可以：

1. **继续使用V3工具** - 所有V3工具仍然可用
2. **逐步尝试V4** - 用`smart_research_assistant`处理复杂研究
3. **混合使用** - 简单任务用V3，复杂研究用V4

## 🐛 故障排除

### Claude连接失败
1. 检查网络连接
2. 验证API密钥
3. 确认Bedrock Gateway运行状态

### 爬取失败
1. 检查网站URL是否正确
2. 尝试使用V3的基础工具
3. 检查网站是否有反爬虫限制

### 配置问题
1. 删除config.json让系统重新创建
2. 使用`show_current_config()`检查配置
3. 手动编辑config.json文件

## 📞 获取帮助

1. **查看配置**: `show_current_config()`
2. **测试连接**: `test_claude_connection()`
3. **查看V4功能**: 使用`research_anything_v4`提示
4. **降级到V3**: 使用任何V3工具作为备选

---

**V4版本**: 2025-01-07  
**兼容性**: 完全向下兼容V3  
**推荐用法**: 复杂研究用V4，简单任务用V3
