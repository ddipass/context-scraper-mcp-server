#!/usr/bin/env python3
"""
MCP 服务器管理脚本
用于启动、停止、重启和升级 Context Scraper MCP 服务器
"""
import os
import sys
import subprocess
import signal
import time
import shutil
from pathlib import Path

class MCPServerManager:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.server_file = self.project_dir / "server.py"
        self.enhanced_file = self.project_dir / "server_enhanced.py"
        self.backup_file = self.project_dir / "server_backup.py"
        
    def find_server_processes(self):
        """查找当前运行的服务器进程"""
        try:
            result = subprocess.run(
                ["ps", "aux"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            processes = []
            for line in result.stdout.split('\n'):
                if 'context-scraper-mcp-server' in line and 'server.py' in line:
                    parts = line.split()
                    if len(parts) > 1:
                        pid = parts[1]
                        processes.append({
                            'pid': pid,
                            'line': line.strip()
                        })
            
            return processes
        except subprocess.CalledProcessError:
            return []
    
    def stop_server(self):
        """停止当前运行的服务器"""
        print("🔍 查找运行中的 MCP 服务器...")
        processes = self.find_server_processes()
        
        if not processes:
            print("✅ 没有找到运行中的 Context Scraper MCP 服务器")
            return True
        
        print(f"📋 找到 {len(processes)} 个相关进程:")
        for proc in processes:
            print(f"  PID {proc['pid']}: {proc['line']}")
        
        # 停止进程
        stopped_count = 0
        for proc in processes:
            try:
                pid = int(proc['pid'])
                print(f"🛑 停止进程 {pid}...")
                os.kill(pid, signal.SIGTERM)
                stopped_count += 1
                time.sleep(0.5)  # 给进程时间优雅退出
            except (ValueError, ProcessLookupError, PermissionError) as e:
                print(f"⚠️ 无法停止进程 {pid}: {e}")
        
        # 等待进程完全停止
        time.sleep(2)
        
        # 验证是否停止成功
        remaining = self.find_server_processes()
        if remaining:
            print(f"⚠️ 仍有 {len(remaining)} 个进程在运行，尝试强制停止...")
            for proc in remaining:
                try:
                    pid = int(proc['pid'])
                    os.kill(pid, signal.SIGKILL)
                    print(f"💀 强制停止进程 {pid}")
                except:
                    pass
        
        print(f"✅ 成功停止 {stopped_count} 个服务器进程")
        return True
    
    def backup_current_server(self):
        """备份当前服务器文件"""
        if self.server_file.exists():
            print("💾 备份当前服务器文件...")
            shutil.copy2(self.server_file, self.backup_file)
            print(f"✅ 备份保存到: {self.backup_file}")
            return True
        else:
            print("⚠️ 当前服务器文件不存在，跳过备份")
            return False
    
    def upgrade_to_enhanced(self):
        """升级到增强版服务器"""
        if not self.enhanced_file.exists():
            print(f"❌ 增强版服务器文件不存在: {self.enhanced_file}")
            return False
        
        print("🚀 升级到增强版服务器...")
        
        # 备份当前版本
        self.backup_current_server()
        
        # 复制增强版
        shutil.copy2(self.enhanced_file, self.server_file)
        print("✅ 增强版服务器已部署")
        return True
    
    def restore_backup(self):
        """恢复备份的服务器"""
        if not self.backup_file.exists():
            print("❌ 没有找到备份文件")
            return False
        
        print("🔄 恢复备份的服务器...")
        shutil.copy2(self.backup_file, self.server_file)
        print("✅ 服务器已恢复到备份版本")
        return True
    
    def start_server(self):
        """启动服务器"""
        if not self.server_file.exists():
            print(f"❌ 服务器文件不存在: {self.server_file}")
            return False
        
        print("🚀 启动 MCP 服务器...")
        print("📝 使用命令: uv run --with mcp mcp run server.py")
        print("💡 请在新的终端窗口中运行以下命令:")
        print(f"   cd {self.project_dir}")
        print("   uv run --with mcp mcp run server.py")
        print()
        print("🔄 然后重启 Q Chat 或重新连接 MCP 服务器")
        return True
    
    def show_status(self):
        """显示服务器状态"""
        print("📊 MCP 服务器状态")
        print("=" * 40)
        
        # 检查文件状态
        print("📁 文件状态:")
        print(f"  server.py: {'✅ 存在' if self.server_file.exists() else '❌ 不存在'}")
        print(f"  server_enhanced.py: {'✅ 存在' if self.enhanced_file.exists() else '❌ 不存在'}")
        print(f"  server_backup.py: {'✅ 存在' if self.backup_file.exists() else '❌ 不存在'}")
        
        # 检查进程状态
        processes = self.find_server_processes()
        print(f"\n🔄 运行状态:")
        if processes:
            print(f"  ✅ 运行中 ({len(processes)} 个进程)")
            for proc in processes:
                print(f"    PID {proc['pid']}")
        else:
            print("  ❌ 未运行")
        
        # 检查版本
        if self.server_file.exists():
            try:
                with open(self.server_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'crawl_clean' in content:
                        print("  📦 版本: 增强版")
                    else:
                        print("  📦 版本: 原版")
            except:
                print("  📦 版本: 未知")

def main():
    """主函数"""
    manager = MCPServerManager()
    
    if len(sys.argv) < 2:
        print("🎯 MCP 服务器管理工具")
        print("=" * 30)
        print("用法:")
        print("  python manage_server.py <命令>")
        print()
        print("可用命令:")
        print("  status    - 显示服务器状态")
        print("  stop      - 停止服务器")
        print("  upgrade   - 升级到增强版")
        print("  restore   - 恢复备份版本")
        print("  start     - 启动服务器")
        print("  restart   - 重启服务器")
        print()
        print("示例:")
        print("  python manage_server.py status")
        print("  python manage_server.py upgrade")
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        manager.show_status()
    
    elif command == "stop":
        manager.stop_server()
    
    elif command == "upgrade":
        print("🚀 开始升级到增强版服务器...")
        manager.stop_server()
        if manager.upgrade_to_enhanced():
            print("✅ 升级完成！")
            manager.start_server()
        else:
            print("❌ 升级失败")
    
    elif command == "restore":
        print("🔄 开始恢复备份版本...")
        manager.stop_server()
        if manager.restore_backup():
            print("✅ 恢复完成！")
            manager.start_server()
        else:
            print("❌ 恢复失败")
    
    elif command == "start":
        manager.start_server()
    
    elif command == "restart":
        print("🔄 重启服务器...")
        manager.stop_server()
        time.sleep(2)
        manager.start_server()
    
    else:
        print(f"❌ 未知命令: {command}")
        print("使用 'python manage_server.py' 查看帮助")

if __name__ == "__main__":
    main()
