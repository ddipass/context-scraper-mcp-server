#!/usr/bin/env python3
"""
爬取配置管理器
统一管理所有爬取相关的参数配置
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ContentLimits:
    """内容长度限制配置"""
    markdown_display_limit: int = 3000
    claude_preview_limit: int = 100
    basic_crawl_unlimited: bool = True

@dataclass
class QualityControl:
    """质量控制配置"""
    word_count_threshold: int = 50
    min_content_quality: str = "medium"

@dataclass
class TimingControl:
    """时间控制配置"""
    page_timeout_ms: int = 30000
    stealth_delay_seconds: int = 1
    dynamic_content_delay_seconds: int = 2
    default_delay_seconds: int = 0

@dataclass
class RetryControl:
    """重试控制配置"""
    max_retries: int = 3
    retry_backoff_factor: int = 2
    retry_max_delay_seconds: int = 10

@dataclass
class CacheControl:
    """缓存控制配置"""
    default_cache_mode: str = "BYPASS"
    enable_smart_caching: bool = False

@dataclass
class BrowserControl:
    """浏览器控制配置"""
    default_wait_until: str = "domcontentloaded"
    headless_mode: bool = True
    browser_type: str = "chromium"

@dataclass
class UserPreferences:
    """用户偏好设置"""
    show_detailed_logs: bool = True
    show_word_count: bool = True
    show_timing_info: bool = True
    compact_output: bool = False

@dataclass
class AdvancedSettings:
    """高级设置"""
    enable_content_optimization: bool = True
    enable_smart_analysis: bool = True
    auto_detect_dynamic_content: bool = True

class CrawlConfigManager:
    """爬取配置管理器"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径，如果为None则使用默认路径
        """
        if config_file is None:
            # 默认配置文件路径
            current_dir = Path(__file__).parent.parent
            config_file = current_dir / "v9_config" / "crawl_config.json"
        
        self.config_file = Path(config_file)
        self._config_data = {}
        self._load_config()
        
        # 初始化配置对象
        self.content_limits = self._create_content_limits()
        self.quality_control = self._create_quality_control()
        self.timing_control = self._create_timing_control()
        self.retry_control = self._create_retry_control()
        self.cache_control = self._create_cache_control()
        self.browser_control = self._create_browser_control()
        self.user_preferences = self._create_user_preferences()
        self.advanced_settings = self._create_advanced_settings()
    
    def _load_config(self):
        """加载配置文件"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self._config_data = json.load(f)
                print(f"✅ 爬取配置已加载: {self.config_file}")
            else:
                print(f"⚠️  配置文件不存在，使用默认配置: {self.config_file}")
                self._config_data = {}
        except Exception as e:
            print(f"❌ 配置文件加载失败: {e}")
            self._config_data = {}
    
    def _create_content_limits(self) -> ContentLimits:
        """创建内容限制配置"""
        config = self._config_data.get("content_limits", {})
        return ContentLimits(
            markdown_display_limit=config.get("markdown_display_limit", 3000),
            claude_preview_limit=config.get("claude_preview_limit", 100),
            basic_crawl_unlimited=config.get("basic_crawl_unlimited", True)
        )
    
    def _create_quality_control(self) -> QualityControl:
        """创建质量控制配置"""
        config = self._config_data.get("quality_control", {})
        return QualityControl(
            word_count_threshold=config.get("word_count_threshold", 50),
            min_content_quality=config.get("min_content_quality", "medium")
        )
    
    def _create_timing_control(self) -> TimingControl:
        """创建时间控制配置"""
        config = self._config_data.get("timing_control", {})
        return TimingControl(
            page_timeout_ms=config.get("page_timeout_ms", 30000),
            stealth_delay_seconds=config.get("stealth_delay_seconds", 1),
            dynamic_content_delay_seconds=config.get("dynamic_content_delay_seconds", 2),
            default_delay_seconds=config.get("default_delay_seconds", 0)
        )
    
    def _create_retry_control(self) -> RetryControl:
        """创建重试控制配置"""
        config = self._config_data.get("retry_control", {})
        return RetryControl(
            max_retries=config.get("max_retries", 3),
            retry_backoff_factor=config.get("retry_backoff_factor", 2),
            retry_max_delay_seconds=config.get("retry_max_delay_seconds", 10)
        )
    
    def _create_cache_control(self) -> CacheControl:
        """创建缓存控制配置"""
        config = self._config_data.get("cache_control", {})
        return CacheControl(
            default_cache_mode=config.get("default_cache_mode", "BYPASS"),
            enable_smart_caching=config.get("enable_smart_caching", False)
        )
    
    def _create_browser_control(self) -> BrowserControl:
        """创建浏览器控制配置"""
        config = self._config_data.get("browser_control", {})
        return BrowserControl(
            default_wait_until=config.get("default_wait_until", "domcontentloaded"),
            headless_mode=config.get("headless_mode", True),
            browser_type=config.get("browser_type", "chromium")
        )
    
    def _create_user_preferences(self) -> UserPreferences:
        """创建用户偏好配置"""
        config = self._config_data.get("user_preferences", {})
        return UserPreferences(
            show_detailed_logs=config.get("show_detailed_logs", True),
            show_word_count=config.get("show_word_count", True),
            show_timing_info=config.get("show_timing_info", True),
            compact_output=config.get("compact_output", False)
        )
    
    def _create_advanced_settings(self) -> AdvancedSettings:
        """创建高级设置配置"""
        config = self._config_data.get("advanced_settings", {})
        return AdvancedSettings(
            enable_content_optimization=config.get("enable_content_optimization", True),
            enable_smart_analysis=config.get("enable_smart_analysis", True),
            auto_detect_dynamic_content=config.get("auto_detect_dynamic_content", True)
        )
    
    def update_content_limits(self, **kwargs):
        """更新内容限制配置"""
        for key, value in kwargs.items():
            if hasattr(self.content_limits, key):
                setattr(self.content_limits, key, value)
        self._save_config()
    
    def update_quality_control(self, **kwargs):
        """更新质量控制配置"""
        for key, value in kwargs.items():
            if hasattr(self.quality_control, key):
                setattr(self.quality_control, key, value)
        self._save_config()
    
    def update_timing_control(self, **kwargs):
        """更新时间控制配置"""
        for key, value in kwargs.items():
            if hasattr(self.timing_control, key):
                setattr(self.timing_control, key, value)
        self._save_config()
    
    def update_user_preferences(self, **kwargs):
        """更新用户偏好配置"""
        for key, value in kwargs.items():
            if hasattr(self.user_preferences, key):
                setattr(self.user_preferences, key, value)
        self._save_config()
    
    def _save_config(self):
        """保存配置到文件"""
        try:
            # 确保目录存在
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 构建配置数据
            config_data = {
                "content_limits": {
                    "description": "内容长度限制配置",
                    "markdown_display_limit": self.content_limits.markdown_display_limit,
                    "claude_preview_limit": self.content_limits.claude_preview_limit,
                    "basic_crawl_unlimited": self.content_limits.basic_crawl_unlimited
                },
                "quality_control": {
                    "description": "爬取质量控制配置",
                    "word_count_threshold": self.quality_control.word_count_threshold,
                    "min_content_quality": self.quality_control.min_content_quality
                },
                "timing_control": {
                    "description": "时间控制配置",
                    "page_timeout_ms": self.timing_control.page_timeout_ms,
                    "stealth_delay_seconds": self.timing_control.stealth_delay_seconds,
                    "dynamic_content_delay_seconds": self.timing_control.dynamic_content_delay_seconds,
                    "default_delay_seconds": self.timing_control.default_delay_seconds
                },
                "retry_control": {
                    "description": "重试控制配置",
                    "max_retries": self.retry_control.max_retries,
                    "retry_backoff_factor": self.retry_control.retry_backoff_factor,
                    "retry_max_delay_seconds": self.retry_control.retry_max_delay_seconds
                },
                "cache_control": {
                    "description": "缓存控制配置",
                    "default_cache_mode": self.cache_control.default_cache_mode,
                    "enable_smart_caching": self.cache_control.enable_smart_caching
                },
                "browser_control": {
                    "description": "浏览器控制配置",
                    "default_wait_until": self.browser_control.default_wait_until,
                    "headless_mode": self.browser_control.headless_mode,
                    "browser_type": self.browser_control.browser_type
                },
                "user_preferences": {
                    "description": "用户偏好设置",
                    "show_detailed_logs": self.user_preferences.show_detailed_logs,
                    "show_word_count": self.user_preferences.show_word_count,
                    "show_timing_info": self.user_preferences.show_timing_info,
                    "compact_output": self.user_preferences.compact_output
                },
                "advanced_settings": {
                    "description": "高级设置",
                    "enable_content_optimization": self.advanced_settings.enable_content_optimization,
                    "enable_smart_analysis": self.advanced_settings.enable_smart_analysis,
                    "auto_detect_dynamic_content": self.advanced_settings.auto_detect_dynamic_content
                }
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 配置已保存: {self.config_file}")
            
        except Exception as e:
            print(f"❌ 配置保存失败: {e}")
    
    def get_config_summary(self) -> str:
        """获取配置摘要"""
        return f"""爬取配置摘要:
        
📄 内容限制:
  - Markdown显示限制: {self.content_limits.markdown_display_limit} 字符
  - Claude预览限制: {self.content_limits.claude_preview_limit} 字符
  - 基础爬取无限制: {self.content_limits.basic_crawl_unlimited}

🎯 质量控制:
  - 词数阈值: {self.quality_control.word_count_threshold} 词
  - 最小质量: {self.quality_control.min_content_quality}

⏱️ 时间控制:
  - 页面超时: {self.timing_control.page_timeout_ms}ms
  - 隐身延迟: {self.timing_control.stealth_delay_seconds}s
  - 动态内容延迟: {self.timing_control.dynamic_content_delay_seconds}s

🔄 重试控制:
  - 最大重试: {self.retry_control.max_retries} 次
  - 退避因子: {self.retry_control.retry_backoff_factor}

👤 用户偏好:
  - 详细日志: {self.user_preferences.show_detailed_logs}
  - 显示词数: {self.user_preferences.show_word_count}
  - 显示时间: {self.user_preferences.show_timing_info}
  - 紧凑输出: {self.user_preferences.compact_output}
"""

# 全局配置管理器实例
_config_manager = None

def get_crawl_config() -> CrawlConfigManager:
    """获取全局配置管理器实例"""
    global _config_manager
    if _config_manager is None:
        _config_manager = CrawlConfigManager()
    return _config_manager

def reload_crawl_config():
    """重新加载配置"""
    global _config_manager
    _config_manager = CrawlConfigManager()
    return _config_manager
