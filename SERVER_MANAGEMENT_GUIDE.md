# 🔧 MCP 服务器管理指南

## 🎯 快速操作流程

### 方法一：使用管理脚本（推荐）

```bash
# 1. 查看当前状态
python manage_server.py status

# 2. 一键升级到增强版
python manage_server.py upgrade

# 3. 按提示在新终端启动服务器
cd /Users/dpliu/EC2/context-scraper-mcp-server
uv run --with mcp mcp run server.py

# 4. 重启 Q Chat
```

### 方法二：手动操作

```bash
# 1. 停止当前服务器
python manage_server.py stop

# 2. 备份并替换
cp server.py server_backup.py
cp server_enhanced.py server.py

# 3. 启动新服务器
uv run --with mcp mcp run server.py

# 4. 重启 Q Chat
```

## 📋 详细命令说明

### 🔍 查看状态
```bash
python manage_server.py status
```
显示：
- 文件存在状态
- 进程运行状态  
- 当前版本信息

### 🛑 停止服务器
```bash
python manage_server.py stop
```
功能：
- 查找相关进程
- 优雅停止 (SIGTERM)
- 强制停止 (SIGKILL)
- 验证停止结果

### 🚀 升级服务器
```bash
python manage_server.py upgrade
```
流程：
1. 停止当前服务器
2. 备份原版文件
3. 部署增强版文件
4. 提示启动命令

### 🔄 恢复备份
```bash
python manage_server.py restore
```
用途：
- 如果增强版有问题
- 恢复到原版服务器
- 保持系统稳定

## 🎮 完整操作演示

### 第一次升级流程

```bash
# 步骤 1: 检查当前状态
$ python manage_server.py status
📊 MCP 服务器状态
========================================
📁 文件状态:
  server.py: ✅ 存在
  server_enhanced.py: ✅ 存在
  server_backup.py: ❌ 不存在
🔄 运行状态:
  ✅ 运行中 (1 个进程)
    PID 58630
  📦 版本: 原版

# 步骤 2: 升级到增强版
$ python manage_server.py upgrade
🚀 开始升级到增强版服务器...
🔍 查找运行中的 MCP 服务器...
📋 找到 1 个相关进程:
  PID 58630: /Users/dpliu/EC2/context-scraper-mcp-server/.venv/bin/python...
🛑 停止进程 58630...
✅ 成功停止 1 个服务器进程
💾 备份当前服务器文件...
✅ 备份保存到: server_backup.py
🚀 升级到增强版服务器...
✅ 增强版服务器已部署
✅ 升级完成！
🚀 启动 MCP 服务器...
📝 使用命令: uv run --with mcp mcp run server.py
💡 请在新的终端窗口中运行以下命令:
   cd /Users/dpliu/EC2/context-scraper-mcp-server
   uv run --with mcp mcp run server.py

🔄 然后重启 Q Chat 或重新连接 MCP 服务器

# 步骤 3: 在新终端启动服务器
$ cd /Users/dpliu/EC2/context-scraper-mcp-server
$ uv run --with mcp mcp run server.py

# 步骤 4: 重启 Q Chat
# 退出当前 Q Chat 会话，重新启动
```

## 🚨 故障排除

### 问题 1: 进程无法停止
```bash
# 查找所有相关进程
ps aux | grep -E "(server\.py|context-scraper)" | grep -v grep

# 手动强制停止
kill -9 <PID>
```

### 问题 2: 升级后有问题
```bash
# 恢复到原版
python manage_server.py restore

# 或手动恢复
cp server_backup.py server.py
```

### 问题 3: Q Chat 连接不上
```bash
# 检查服务器是否正常启动
python manage_server.py status

# 确保端口没有冲突
lsof -i :11235  # 如果使用特定端口

# 重启 Q Chat
# 完全退出 Q Chat，重新启动
```

## 📊 版本对比

| 特性 | 原版 | 增强版 |
|------|------|--------|
| 基础工具 | 4个 | 4个 (兼容) |
| 增强工具 | 0个 | 4个 (新增) |
| 智能提示 | 2个 | 9个 |
| 内容过滤 | ❌ | ✅ |
| 截图功能 | ❌ | ✅ |
| 动态内容 | ❌ | ✅ |
| 智能批量 | ❌ | ✅ |
| API依赖 | 无 | 无 |

## 🎉 升级后的新功能

### 新增工具
1. `crawl_clean` - 智能内容过滤
2. `crawl_with_screenshot` - 截图功能
3. `crawl_dynamic` - 动态内容处理
4. `crawl_smart_batch` - 智能批量处理

### 智能提示
- 自动选择最佳工具
- 内容类型识别
- 专业场景优化

### 使用示例
```
用户: "帮我爬取这个商品页面的信息"
Q: 自动选择 crawl_smart_batch + product 类型

用户: "这个网站内容很乱，帮我提取干净的内容"  
Q: 自动选择 crawl_clean

用户: "需要截图保存这个页面"
Q: 自动选择 crawl_with_screenshot
```

---

**💡 提示**: 升级是安全的，原版会自动备份，随时可以恢复！
