# 🚀 Context Scraper MCP Server - 增强功能指南

## 📋 功能概览

### 原有功能（保持不变）
- **4个基础工具**: `crawl`, `crawl_with_selector`, `crawl_multiple`, `health_check`
- **4个增强工具**: `crawl_clean`, `crawl_with_screenshot`, `crawl_dynamic`, `crawl_smart_batch`

### 🆕 新增反爬虫工具（4个）
- **`crawl_stealth`**: 隐身爬取，使用随机UA和反检测技术
- **`crawl_with_geolocation`**: 地理位置伪装爬取
- **`crawl_with_retry`**: 自动重试机制
- **`crawl_concurrent_optimized`**: 智能并发控制

### 🧠 新增智能提示（6个）
- **`stealth_research`**: 隐身研究提示
- **`competitive_intelligence`**: 竞争情报收集
- **`market_monitoring_setup`**: 市场监控设置
- **`anti_detection_audit`**: 反检测审计
- **`data_extraction_optimization`**: 数据提取优化
- **原有9个提示**: 保持不变

## 🛠️ 新工具详细说明

### 1. crawl_stealth - 隐身爬取
```python
# 使用随机User Agent、浏览器指纹伪装
result = await crawl_stealth("https://example.com")
```

**特性:**
- 随机生成真实浏览器User Agent
- 自动匹配Client Hints头
- 随机视窗大小
- JavaScript反检测
- 禁用自动化标识

**适用场景:**
- 严格反爬虫的网站
- 需要模拟真实用户访问
- 避免被识别为爬虫

### 2. crawl_with_geolocation - 地理位置伪装
```python
# 模拟不同地理位置访问
result = await crawl_with_geolocation("https://example.com", "random")
```

**特性:**
- 随机选择全球8个主要城市位置
- 纬度、经度、精度伪装
- 结合隐身技术

**适用场景:**
- 地理位置限制的网站
- 需要测试不同地区内容
- 绕过IP地理限制

### 3. crawl_with_retry - 重试爬取
```python
# 自动重试失败请求
result = await crawl_with_retry("https://unstable-site.com", max_retries=3)
```

**特性:**
- 指数退避重试策略
- 随机延迟避免检测
- 详细错误报告

**适用场景:**
- 不稳定的网站
- 网络环境不佳
- 提高成功率

### 4. crawl_concurrent_optimized - 并发优化
```python
# 智能并发控制批量爬取
result = await crawl_concurrent_optimized("url1,url2,url3", max_concurrent=5)
```

**特性:**
- 信号量控制并发数
- 结合重试机制
- 异常处理和统计

**适用场景:**
- 大量URL批量处理
- 提升爬取效率
- 避免过载目标服务器

## 🎯 智能提示使用指南

### 1. stealth_research - 隐身研究
```
使用提示: stealth_research("AI技术趋势", "https://site1.com,https://site2.com")
```
**自动执行:**
- 隐身爬取避免检测
- 地理位置切换
- 重试机制保证数据完整
- 生成综合研究报告

### 2. competitive_intelligence - 竞争情报
```
使用提示: competitive_intelligence("competitor1.com,competitor2.com", "产品定价策略")
```
**自动执行:**
- 并发高效爬取
- 隐身技术避免识别
- 多地区访问对比
- 生成竞争分析矩阵

### 3. market_monitoring_setup - 市场监控
```
使用提示: market_monitoring_setup("target-sites.com", "daily")
```
**自动执行:**
- 建立监控基线
- 截图记录视觉状态
- 设置变化检测规则
- 创建自动化脚本

### 4. anti_detection_audit - 反检测审计
```
使用提示: anti_detection_audit("https://target-site.com")
```
**自动执行:**
- 测试多种爬取方式
- 分析检测机制
- 评估绕过成功率
- 推荐最佳策略

### 5. data_extraction_optimization - 数据提取优化
```
使用提示: data_extraction_optimization("https://site.com", "产品信息")
```
**自动执行:**
- 针对数据类型优化
- 选择最佳提取策略
- 质量评估和报告
- 结构化数据输出

## 🔧 部署和使用

### 1. 文件结构
```
context-scraper-mcp-server/
├── server.py                    # 原版服务器（保持不变）
├── server_v2_enhanced.py        # 增强版服务器
├── anti_detection.py            # 反爬虫模块
└── ENHANCED_FEATURES_GUIDE.md   # 本指南
```

### 2. 启动增强版服务器
```bash
# 使用增强版服务器
uv run --with mcp mcp run server_v2_enhanced.py
```

### 3. MCP 配置更新

#### 方法一：仅使用增强版（推荐）
在 `.amazonq/mcp.json` 文件中配置：

```json
{
    "mcpServers": {
        "ContextScraperPro": {
            "command": "uv",
            "args": ["run", "--with", "mcp", "mcp", "run", "server_v2_enhanced.py"],
            "cwd": "/Users/dpliu/EC2/context-scraper-mcp-server"
        }
    }
}
```

#### 方法二：替换现有配置
如果你已经有原版配置，直接替换文件名即可：

```json
{
    "mcpServers": {
        "ContextScraper": {
            "command": "uv",
            "args": ["run", "--with", "mcp", "mcp", "run", "server_v2_enhanced.py"],
            "cwd": "/Users/dpliu/EC2/context-scraper-mcp-server"
        }
    }
}
```

#### ⚠️ 重要：避免同时运行两个版本
**不要同时运行原版和增强版**，因为：
- 工具名称重复（如 `crawl`, `crawl_clean` 等8个相同工具）
- Amazon Q 会混淆，不知道调用哪个版本
- 可能导致不可预期的行为和错误

#### 正确的版本管理方式
- **生产使用**: 选择一个版本，配置后重启 Amazon Q
- **测试切换**: 修改配置文件中的 `server.py` → `server_v2_enhanced.py`
- **备份保留**: 保留原版文件作为备份，但不要同时运行

#### 配置验证步骤

1. **停止现有服务器**：
   ```bash
   python manage_server.py stop
   ```

2. **更新配置文件**：
   修改 `.amazonq/mcp.json` 使用上述任一配置

3. **重启 Amazon Q Developer**

4. **验证新功能**：
   ```bash
   # 检查服务器状态
   python manage_server.py status
   
   # 应该看到增强版服务器运行
   ```

5. **测试工具**：
   - 基础测试: "爬取 https://example.com"
   - 隐身测试: "使用隐身模式爬取严格的网站"
   - 地理测试: "模拟不同地区访问这个网站"

#### 功能对比表

| 功能 | 原版 server.py | 增强版 server_v2_enhanced.py |
|------|----------------|------------------------------|
| 基础工具 | 8个 | 8个（相同） |
| 反爬虫工具 | ❌ | 4个新增 |
| 智能提示 | 9个 | 15个 |
| 成功率 | 标准 | 显著提升 |
| 推荐使用 | 兼容性测试 | 生产环境 |
# 在 Amazon Q 中输入: "使用隐身模式爬取 https://example.com"
```

## 🎨 使用场景示例

### 场景1: 严格反爬虫网站
```
"这个网站有严格的反爬虫机制，帮我获取产品信息"
→ AI会自动选择 crawl_stealth 或相关提示
```

### 场景2: 地理限制内容
```
"这个网站在我的地区无法访问，帮我看看内容"
→ AI会使用 crawl_with_geolocation 切换地理位置
```

### 场景3: 大规模数据收集
```
"我需要分析50个竞争对手网站的定价策略"
→ AI会使用 competitive_intelligence 提示和并发优化工具
```

### 场景4: 不稳定网站
```
"这个网站经常访问失败，但我需要监控它的更新"
→ AI会使用 crawl_with_retry 和 market_monitoring_setup
```

## ⚡ 性能优化建议

### 1. 并发控制
- 默认并发数: 5
- 可根据目标网站调整
- 避免过高并发导致封IP

### 2. 重试策略
- 默认重试3次
- 指数退避: 1s, 2s, 4s
- 随机延迟避免检测

### 3. 缓存策略
- 隐身模式默认绕过缓存
- 普通模式启用缓存提升效率
- 根据需求选择缓存模式

### 4. 资源管理
- 自动清理User Agent历史
- 限制并发连接数
- 优化内存使用

## 🛡️ 使用注意事项

### 1. 合规使用
- 遵守目标网站的robots.txt
- 尊重网站使用条款
- 避免过度频繁访问

### 2. 技术限制
- 某些高级反爬虫可能仍然有效
- 地理位置伪装不是100%可靠
- 重试机制有次数限制

### 3. 性能考虑
- 隐身模式会增加延迟
- 并发过高可能影响稳定性
- 重试会增加总体时间

## 🔄 版本兼容性

- **向后兼容**: 所有原有功能保持不变
- **渐进升级**: 可以逐步从原版切换到增强版
- **配置独立**: 两个版本可以并存使用

## 📞 技术支持

如果遇到问题或需要定制功能，请参考：
1. 检查依赖是否正确安装
2. 确认网络连接正常
3. 查看错误日志定位问题
4. 根据目标网站调整策略参数
