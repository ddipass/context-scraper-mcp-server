# system_manager.py - MCP项目管理模块
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Tuple
import psutil

class MCPProjectManager:
    """MCP项目管理器 - 专注于Context Scraper MCP项目的状态和存储管理"""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.project_name = "Context Scraper MCP Server"
        
        # MCP项目相关的垃圾文件路径
        self.mcp_junk_patterns = {
            "Python缓存": [
                "__pycache__",
                "*.pyc", 
                "*.pyo",
                ".pytest_cache"
            ],
            "Crawl4AI缓存": [
                ".crawl4ai",
                "browser-profile-*",
                "chrome_*",
                "firefox_*"
            ],
            "MCP日志": [
                "*.log",
                "crawl4ai.log",
                "mcp.log"
            ],
            "临时文件": [
                "*.tmp",
                "*.temp",
                ".DS_Store"
            ]
        }
        
        # 用户缓存目录
        self.user_cache_dirs = [
            Path.home() / ".cache" / "crawl4ai",
            Path.home() / ".crawl4ai",
            Path(tempfile.gettempdir()) / "browser-profile-*",
            Path(tempfile.gettempdir()) / "crawl4ai*"
        ]
    
    def get_mcp_server_status(self) -> Dict:
        """获取Context Scraper MCP服务器状态"""
        try:
            result = subprocess.run(
                ["python", "manage_server.py", "status"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # 解析输出，提取关键信息
            status_info = {
                "success": result.returncode == 0,
                "raw_output": result.stdout,
                "error": result.stderr,
                "project_name": self.project_name,
                "project_path": str(self.project_root),
                "parsed_info": {}
            }
            
            if result.returncode == 0:
                status_info["parsed_info"] = self._parse_status_output(result.stdout)
            
            return status_info
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "raw_output": "",
                "error": "MCP服务器状态检查超时",
                "project_name": self.project_name,
                "project_path": str(self.project_root),
                "parsed_info": {}
            }
        except Exception as e:
            return {
                "success": False,
                "raw_output": "",
                "error": f"检查MCP服务器状态时出错: {str(e)}",
                "project_name": self.project_name,
                "project_path": str(self.project_root),
                "parsed_info": {}
            }
    
    def _parse_status_output(self, output: str) -> Dict:
        """解析状态输出"""
        parsed = {
            "files": {},
            "processes": [],
            "version": "未知"
        }
        
        lines = output.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if "文件状态:" in line:
                current_section = "files"
            elif "运行状态:" in line:
                current_section = "processes"
            elif "版本:" in line:
                parsed["version"] = line.split("版本:")[-1].strip()
            elif current_section == "files" and ":" in line:
                parts = line.split(":")
                if len(parts) >= 2:
                    filename = parts[0].strip()
                    status = parts[1].strip()
                    parsed["files"][filename] = status
            elif current_section == "processes" and "PID" in line:
                pid = line.replace("PID", "").strip()
                if pid.isdigit():
                    parsed["processes"].append(int(pid))
        
        return parsed
    
    def scan_mcp_junk_files(self) -> Dict:
        """扫描MCP项目相关的垃圾文件"""
        junk_info = {
            "total_size": 0,
            "total_files": 0,
            "categories": {},
            "file_details": [],
            "scan_locations": []
        }
        
        # 扫描项目目录
        scan_location = f"项目目录: {self.project_root}"
        junk_info["scan_locations"].append(scan_location)
        self._scan_mcp_directory(self.project_root, junk_info)
        
        # 扫描用户缓存目录
        for cache_dir in self.user_cache_dirs:
            if "*" in str(cache_dir):
                # 处理通配符路径
                parent_dir = cache_dir.parent
                pattern = cache_dir.name
                if parent_dir.exists():
                    for match_dir in parent_dir.glob(pattern):
                        if match_dir.exists():
                            scan_location = f"用户缓存: {match_dir}"
                            junk_info["scan_locations"].append(scan_location)
                            self._scan_mcp_directory(match_dir, junk_info, prefix="用户缓存-")
            else:
                if cache_dir.exists():
                    scan_location = f"用户缓存: {cache_dir}"
                    junk_info["scan_locations"].append(scan_location)
                    self._scan_mcp_directory(cache_dir, junk_info, prefix="用户缓存-")
        
        return junk_info
    
    def _scan_mcp_directory(self, directory: Path, junk_info: Dict, prefix: str = ""):
        """扫描指定目录中的MCP相关垃圾文件"""
        try:
            for category, patterns in self.mcp_junk_patterns.items():
                category_name = f"{prefix}{category}"
                if category_name not in junk_info["categories"]:
                    junk_info["categories"][category_name] = {"size": 0, "files": 0, "paths": []}
                
                for pattern in patterns:
                    if "*" in pattern:
                        # 通配符匹配文件
                        for file_path in directory.rglob(pattern):
                            if file_path.is_file():
                                self._add_junk_file(file_path, category_name, junk_info)
                    else:
                        # 目录匹配
                        for dir_path in directory.rglob(pattern):
                            if dir_path.is_dir():
                                self._add_junk_directory(dir_path, category_name, junk_info)
                                
        except Exception as e:
            print(f"扫描目录 {directory} 时出错: {e}")
    
    def _add_junk_file(self, file_path: Path, category: str, junk_info: Dict):
        """添加垃圾文件到统计"""
        try:
            size = file_path.stat().st_size
            junk_info["total_size"] += size
            junk_info["total_files"] += 1
            junk_info["categories"][category]["size"] += size
            junk_info["categories"][category]["files"] += 1
            junk_info["categories"][category]["paths"].append(str(file_path))
            
            junk_info["file_details"].append({
                "path": str(file_path),
                "size": size,
                "category": category,
                "modified": file_path.stat().st_mtime,
                "type": "file"
            })
        except Exception:
            pass
    
    def _add_junk_directory(self, dir_path: Path, category: str, junk_info: Dict):
        """添加垃圾目录到统计"""
        try:
            dir_size = self._get_directory_size(dir_path)
            file_count = sum(1 for _ in dir_path.rglob("*") if _.is_file())
            
            junk_info["total_size"] += dir_size
            junk_info["total_files"] += file_count
            junk_info["categories"][category]["size"] += dir_size
            junk_info["categories"][category]["files"] += file_count
            junk_info["categories"][category]["paths"].append(str(dir_path))
            
            junk_info["file_details"].append({
                "path": str(dir_path),
                "size": dir_size,
                "category": category,
                "modified": dir_path.stat().st_mtime,
                "type": "directory"
            })
        except Exception:
            pass
    
    def _get_directory_size(self, directory: Path) -> int:
        """获取目录大小"""
        total_size = 0
        try:
            for file_path in directory.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except Exception:
            pass
        return total_size
    
    def clean_mcp_junk_files(self, categories: List[str] = None, max_age_days: int = 7) -> Dict:
        """清理MCP项目相关的垃圾文件"""
        if categories is None:
            categories = ["Python缓存", "Crawl4AI缓存", "临时文件"]
        
        junk_info = self.scan_mcp_junk_files()
        cleaned_info = {
            "success": True,
            "cleaned_size": 0,
            "cleaned_files": 0,
            "errors": [],
            "cleaned_details": [],
            "skipped_details": []
        }
        
        current_time = time.time()
        max_age_seconds = max_age_days * 24 * 3600
        
        for item in junk_info["file_details"]:
            # 检查类别
            item_category = item["category"].replace("用户缓存-", "")
            if item_category not in categories:
                continue
            
            # 检查文件年龄
            if current_time - item["modified"] < max_age_seconds:
                cleaned_info["skipped_details"].append({
                    "path": item["path"],
                    "reason": f"文件太新 (小于{max_age_days}天)"
                })
                continue
            
            try:
                file_path = Path(item["path"])
                if file_path.exists():
                    if item["type"] == "directory":
                        shutil.rmtree(file_path)
                    else:
                        file_path.unlink()
                    
                    cleaned_info["cleaned_size"] += item["size"]
                    cleaned_info["cleaned_files"] += 1
                    cleaned_info["cleaned_details"].append({
                        "path": item["path"],
                        "size": item["size"],
                        "category": item["category"]
                    })
            except Exception as e:
                cleaned_info["errors"].append({
                    "path": item["path"],
                    "error": str(e)
                })
        
        if cleaned_info["errors"]:
            cleaned_info["success"] = len(cleaned_info["errors"]) < len(cleaned_info["cleaned_details"])
        
        return cleaned_info
    
    def get_mcp_system_info(self) -> Dict:
        """获取MCP项目相关的系统信息"""
        try:
            # 磁盘使用情况
            disk_usage = shutil.disk_usage(self.project_root)
            
            # 内存使用情况
            memory = psutil.virtual_memory()
            
            # CPU 使用情况
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 项目目录大小
            project_size = self._get_directory_size(self.project_root)
            
            return {
                "project_info": {
                    "name": self.project_name,
                    "path": str(self.project_root),
                    "size": project_size
                },
                "disk": {
                    "total": disk_usage.total,
                    "used": disk_usage.used,
                    "free": disk_usage.free,
                    "percent": (disk_usage.used / disk_usage.total) * 100
                },
                "memory": {
                    "total": memory.total,
                    "used": memory.used,
                    "free": memory.available,
                    "percent": memory.percent
                },
                "cpu": {
                    "percent": cpu_percent,
                    "count": psutil.cpu_count()
                }
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def format_size(size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"

# 全局管理器实例
mcp_manager = MCPProjectManager()
