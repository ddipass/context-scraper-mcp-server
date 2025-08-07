# v9_core/config_manager.py - V9 统一配置管理器
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class SearchEngine(Enum):
    """支持的搜索引擎"""
    GOOGLE = "google"
    BAIDU = "baidu"
    YAHOO = "yahoo"
    BING = "bing"
    DUCKDUCKGO = "duckduckgo"

@dataclass
class ClaudeConfig:
    """Claude API配置"""
    api_key: str = ""
    base_url: str = "http://Bedroc-Proxy-dZmq8lX6J5TY-92025060.us-west-2.elb.amazonaws.com/api/v1"
    model: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    enabled: bool = False
    timeout: int = 30
    max_tokens: int = 4000
    temperature: float = 0.7

@dataclass
class SearchEngineConfig:
    """搜索引擎配置"""
    name: str
    enabled: bool = True
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    timeout: int = 30
    priority: int = 1  # 1=最高优先级

@dataclass
class UserPreferences:
    """用户偏好配置"""
    default_search_engine: str = "google"
    respect_explicit_engine: bool = True  # 严格遵循用户指定的引擎
    auto_fallback: bool = True
    search_timeout: int = 30
    max_concurrent_searches: int = 3
    
    # 内容类型偏好
    chinese_content_engine: str = "baidu"
    academic_content_engine: str = "google"
    privacy_focused_engine: str = "duckduckgo"
    
    # 智能选择偏好
    enable_smart_engine_selection: bool = True
    learn_from_user_choices: bool = True

@dataclass
class SystemConfig:
    """系统配置"""
    version: str = "6.0.0"
    debug_mode: bool = False
    log_level: str = "INFO"
    cache_enabled: bool = True
    cache_ttl: int = 3600
    
    # 性能配置
    max_concurrent_requests: int = 10
    request_timeout: int = 60
    retry_attempts: int = 3
    
    # 安全配置
    enable_rate_limiting: bool = True
    max_requests_per_minute: int = 100

class V6ConfigManager:
    """V9 统一配置管理器"""
    
    def __init__(self, config_dir: str = "v9_config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        # 配置文件路径
        self.search_engines_file = self.config_dir / "search_engines.json"
        self.user_preferences_file = self.config_dir / "user_preferences.json"
        self.system_config_file = self.config_dir / "system_config.json"
        self.claude_config_file = self.config_dir / "claude_config.json"
        
        # 加载配置
        self.search_engines = self._load_search_engines()
        self.user_preferences = self._load_user_preferences()
        self.system_config = self._load_system_config()
        self.claude_config = self._load_claude_config()
    
    def _load_search_engines(self) -> Dict[str, SearchEngineConfig]:
        """加载搜索引擎配置"""
        if self.search_engines_file.exists():
            try:
                with open(self.search_engines_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return {
                    name: SearchEngineConfig(**config) 
                    for name, config in data.items()
                }
            except Exception as e:
                print(f"⚠️ 搜索引擎配置加载失败: {e}")
        
        # 返回默认配置
        return self._get_default_search_engines()
    
    def _get_default_search_engines(self) -> Dict[str, SearchEngineConfig]:
        """获取默认搜索引擎配置"""
        return {
            "google": SearchEngineConfig(
                name="Google",
                enabled=True,
                base_url="https://www.google.com/search",
                priority=1
            ),
            "baidu": SearchEngineConfig(
                name="百度",
                enabled=True,
                base_url="https://www.baidu.com/s",
                priority=2
            ),
            "bing": SearchEngineConfig(
                name="Bing",
                enabled=True,
                base_url="https://www.bing.com/search",
                priority=3
            ),
            "yahoo": SearchEngineConfig(
                name="Yahoo",
                enabled=True,
                base_url="https://search.yahoo.com/search",
                priority=4
            ),
            "duckduckgo": SearchEngineConfig(
                name="DuckDuckGo",
                enabled=True,
                base_url="https://duckduckgo.com/",
                priority=5
            )
        }
    
    def _load_user_preferences(self) -> UserPreferences:
        """加载用户偏好"""
        if self.user_preferences_file.exists():
            try:
                with open(self.user_preferences_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return UserPreferences(**data)
            except Exception as e:
                print(f"⚠️ 用户偏好加载失败: {e}")
        
        return UserPreferences()
    
    def _load_system_config(self) -> SystemConfig:
        """加载系统配置"""
        if self.system_config_file.exists():
            try:
                with open(self.system_config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return SystemConfig(**data)
            except Exception as e:
                print(f"⚠️ 系统配置加载失败: {e}")
        
        return SystemConfig()
    
    def _load_claude_config(self) -> ClaudeConfig:
        """加载Claude配置"""
        if self.claude_config_file.exists():
            try:
                with open(self.claude_config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                claude_data = data.get('claude_api', {})
                return ClaudeConfig(**claude_data)
            except Exception as e:
                print(f"⚠️ Claude配置加载失败: {e}")
        
        return ClaudeConfig()
    
    def save_all_configs(self):
        """保存所有配置"""
        self.save_search_engines()
        self.save_user_preferences()
        self.save_system_config()
        self.save_claude_config()
    
    def save_search_engines(self):
        """保存搜索引擎配置"""
        try:
            data = {
                name: asdict(config) 
                for name, config in self.search_engines.items()
            }
            with open(self.search_engines_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ 搜索引擎配置保存失败: {e}")
    
    def save_user_preferences(self):
        """保存用户偏好"""
        try:
            with open(self.user_preferences_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.user_preferences), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ 用户偏好保存失败: {e}")
    
    def save_system_config(self):
        """保存系统配置"""
        try:
            with open(self.system_config_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.system_config), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ 系统配置保存失败: {e}")
    
    def save_claude_config(self):
        """保存Claude配置"""
        try:
            data = {
                "claude_api": asdict(self.claude_config),
                "usage_notes": {
                    "description": "Claude API配置用于高级内容分析和智能研究功能",
                    "setup_instructions": [
                        "1. 将你的Claude API Key填入上面的api_key字段",
                        "2. 设置enabled为true启用Claude功能", 
                        "3. 根据需要调整model、timeout等参数",
                        "4. 重启服务器使配置生效"
                    ],
                    "security_note": "请妥善保管API Key，不要提交到版本控制系统"
                }
            }
            with open(self.claude_config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Claude配置保存失败: {e}")
    
    def get_enabled_search_engines(self) -> Dict[str, SearchEngineConfig]:
        """获取启用的搜索引擎"""
        return {
            name: config 
            for name, config in self.search_engines.items() 
            if config.enabled
        }
    
    def get_search_engine_by_priority(self) -> list[tuple[str, SearchEngineConfig]]:
        """按优先级获取搜索引擎"""
        enabled = self.get_enabled_search_engines()
        return sorted(
            enabled.items(), 
            key=lambda x: x[1].priority
        )
    
    def update_user_preference(self, key: str, value: Any):
        """更新用户偏好"""
        if hasattr(self.user_preferences, key):
            setattr(self.user_preferences, key, value)
            self.save_user_preferences()
        else:
            raise ValueError(f"未知的用户偏好: {key}")
    
    def enable_search_engine(self, engine_name: str):
        """启用搜索引擎"""
        if engine_name in self.search_engines:
            self.search_engines[engine_name].enabled = True
            self.save_search_engines()
    
    def disable_search_engine(self, engine_name: str):
        """禁用搜索引擎"""
        if engine_name in self.search_engines:
            self.search_engines[engine_name].enabled = False
            self.save_search_engines()
    
    def get_config_summary(self) -> Dict[str, Any]:
        """获取配置摘要"""
        enabled_engines = list(self.get_enabled_search_engines().keys())
        return {
            "version": self.system_config.version,
            "enabled_search_engines": enabled_engines,
            "default_search_engine": self.user_preferences.default_search_engine,
            "respect_explicit_engine": self.user_preferences.respect_explicit_engine,
            "debug_mode": self.system_config.debug_mode
        }

# 全局配置管理器实例
config_manager = V6ConfigManager()

# 便捷访问函数
def get_config() -> V6ConfigManager:
    """获取配置管理器实例"""
    return config_manager

def get_search_engines() -> Dict[str, SearchEngineConfig]:
    """获取搜索引擎配置"""
    return config_manager.search_engines

def get_user_preferences() -> UserPreferences:
    """获取用户偏好"""
    return config_manager.user_preferences

def get_claude_config() -> ClaudeConfig:
    """获取Claude配置"""
    return config_manager.claude_config

def get_system_config() -> SystemConfig:
    """获取系统配置"""
    return config_manager.system_config
