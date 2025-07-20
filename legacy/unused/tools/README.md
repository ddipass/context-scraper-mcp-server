# Tools - 工具集

这个目录包含了 Context Scraper MCP Server 的管理和维护工具。

## 📁 工具列表

### `manage_server.py` - 服务器管理工具
MCP 服务器的启动、停止、重启和升级管理脚本。

#### 功能
- 🚀 启动服务器
- 🛑 停止服务器  
- 🔄 重启服务器
- 📊 查看服务器状态
- 🔧 服务器进程管理

#### 使用方法
```bash
# 查看服务器状态
python tools/manage_server.py status

# 启动服务器
python tools/manage_server.py start

# 停止服务器
python tools/manage_server.py stop

# 重启服务器
python tools/manage_server.py restart
```

## 🔧 开发工具

如需添加新的管理工具，请：

1. 在此目录创建新的 Python 文件
2. 遵循现有的代码风格
3. 添加适当的文档说明
4. 更新此 README 文件

## 📋 工具开发规范

### 命名规范
- 使用描述性的文件名
- 使用下划线分隔单词
- 添加 `.py` 扩展名

### 代码规范
- 添加文件头注释说明功能
- 使用 argparse 处理命令行参数
- 提供 `--help` 选项
- 包含错误处理

### 文档规范
- 在文件开头添加功能说明
- 提供使用示例
- 说明依赖关系

## 🚀 快速开始

```bash
# 进入工具目录
cd tools

# 查看可用工具
ls -la

# 运行服务器管理工具
python manage_server.py --help
```
