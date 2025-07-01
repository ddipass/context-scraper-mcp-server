# anti_detection.py - 反爬虫检测增强模块
import random
import time
import asyncio
from typing import Optional, List, Dict, Any
from crawl4ai import *
from crawl4ai.user_agent_generator import ValidUAGenerator, UserAgentGenerator

class EnhancedAntiDetection:
    """增强反爬虫检测功能"""
    
    def __init__(self):
        self.ua_generator = UserAgentGenerator()
        self.valid_ua_generator = ValidUAGenerator()
        self.used_agents = set()
        
    def get_random_user_agent_with_hints(self) -> tuple[str, str]:
        """生成随机 User Agent 和匹配的 Client Hints"""
        user_agent, client_hints = self.ua_generator.generate_with_client_hints(
            device_type="desktop",
            browser_type=random.choice(["chrome", "edge"]),
            num_browsers=3
        )
        
        # 避免重复使用相同的 UA（最多记录50个）
        while user_agent in self.used_agents and len(self.used_agents) < 50:
            user_agent, client_hints = self.ua_generator.generate_with_client_hints(
                device_type="desktop",
                browser_type=random.choice(["chrome", "edge"]),
                num_browsers=3
            )
        
        self.used_agents.add(user_agent)
        if len(self.used_agents) > 100:  # 清理旧记录
            self.used_agents = set(list(self.used_agents)[-50:])
            
        return user_agent, client_hints
    
    def get_stealth_headers(self, client_hints: str) -> Dict[str, str]:
        """生成隐身请求头"""
        return {
            "sec-ch-ua": client_hints,
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "accept-encoding": "gzip, deflate, br",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "dnt": "1"
        }
    
    def get_random_viewport(self) -> tuple[int, int]:
        """生成随机视窗大小"""
        common_resolutions = [
            (1920, 1080), (1366, 768), (1536, 864), (1440, 900),
            (1280, 720), (1600, 900), (1920, 1200), (2560, 1440)
        ]
        return random.choice(common_resolutions)
    
    def get_stealth_browser_config(self, randomize_viewport: bool = True) -> BrowserConfig:
        """获取隐身浏览器配置"""
        user_agent, client_hints = self.get_random_user_agent_with_hints()
        headers = self.get_stealth_headers(client_hints)
        
        if randomize_viewport:
            viewport_width, viewport_height = self.get_random_viewport()
        else:
            viewport_width, viewport_height = 1920, 1080
            
        return BrowserConfig(
            headless=True,
            user_agent=user_agent,
            headers=headers,
            viewport_width=viewport_width,
            viewport_height=viewport_height,
            java_script_enabled=True,
            ignore_https_errors=True,
            extra_args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                "--disable-field-trial-config",
                "--disable-back-forward-cache",
                "--disable-background-networking",
                "--disable-default-apps",
                "--disable-extensions",
                "--disable-sync",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-infobars",
                "--disable-blink-features=AutomationControlled",
                f"--window-size={viewport_width},{viewport_height}",
                "--disable-automation",
                "--exclude-switches=enable-automation",
                "--disable-client-side-phishing-detection"
            ]
        )

class GeolocationSpoofer:
    """地理位置伪装"""
    
    @staticmethod
    def get_random_location() -> GeolocationConfig:
        """获取随机地理位置"""
        locations = [
            {"name": "New York", "lat": 40.7128, "lng": -74.0060},
            {"name": "London", "lat": 51.5074, "lng": -0.1278},
            {"name": "Tokyo", "lat": 35.6762, "lng": 139.6503},
            {"name": "Sydney", "lat": -33.8688, "lng": 151.2093},
            {"name": "Paris", "lat": 48.8566, "lng": 2.3522},
            {"name": "Berlin", "lat": 52.5200, "lng": 13.4050},
            {"name": "Toronto", "lat": 43.6532, "lng": -79.3832},
            {"name": "Singapore", "lat": 1.3521, "lng": 103.8198}
        ]
        location = random.choice(locations)
        return GeolocationConfig(
            latitude=location["lat"],
            longitude=location["lng"],
            accuracy=random.uniform(10, 100)
        )

class RetryManager:
    """重试管理器"""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    async def execute_with_retry(self, crawler, url: str, config: CrawlerRunConfig):
        """带重试的执行"""
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                result = await crawler.arun(url=url, config=config)
                if result.success:
                    return result
                else:
                    last_error = result.error_message
                    if attempt < self.max_retries:
                        delay = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
                        await asyncio.sleep(delay)
            except Exception as e:
                last_error = str(e)
                if attempt < self.max_retries:
                    delay = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
                    await asyncio.sleep(delay)
        
        # 返回失败结果
        from crawl4ai.models import AsyncCrawlResponse
        return AsyncCrawlResponse(
            url=url,
            success=False,
            error_message=f"Failed after {self.max_retries + 1} attempts. Last error: {last_error}"
        )

class ConcurrencyManager:
    """并发管理器"""
    
    def __init__(self, max_concurrent: int = 5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.max_concurrent = max_concurrent
    
    async def execute_with_limit(self, coro):
        """限制并发执行"""
        async with self.semaphore:
            return await coro

# 工厂函数
def create_stealth_config() -> BrowserConfig:
    """创建隐身配置"""
    detector = EnhancedAntiDetection()
    return detector.get_stealth_browser_config()

def create_geo_spoofed_config(location: Optional[str] = None) -> tuple[BrowserConfig, GeolocationConfig]:
    """创建地理位置伪装配置"""
    detector = EnhancedAntiDetection()
    spoofer = GeolocationSpoofer()
    
    browser_config = detector.get_stealth_browser_config()
    geo_config = spoofer.get_random_location()
    
    return browser_config, geo_config

def create_retry_manager(max_retries: int = 3) -> RetryManager:
    """创建重试管理器"""
    return RetryManager(max_retries=max_retries)

def create_concurrency_manager(max_concurrent: int = 5) -> ConcurrencyManager:
    """创建并发管理器"""
    return ConcurrencyManager(max_concurrent=max_concurrent)
