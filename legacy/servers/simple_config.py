# simple_config.py - 极简配置管理器
# V4专用：只管理最核心的Claude LLM配置

import json
import os
from pathlib import Path

class SimpleConfig:
    """极简配置管理 - 只管理最核心的LLM配置"""
    
    def __init__(self):
        self.config_file = Path("config.json")
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置，如果不存在就创建默认配置"""
        if not self.config_file.exists():
            print("📝 配置文件不存在，创建默认配置...")
            self.create_default_config()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                print(f"✅ 配置已加载: {self.config_file}")
                return config_data
        except Exception as e:
            print(f"⚠️ 配置文件读取失败，使用默认配置: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        """默认配置 - 使用Bedrock Gateway"""
        return {
            "llm": {
                "api_key": "cbN4Vd270Ku3pq2dVh+8rICNqa2RsPvxyiW1bEDrG1o=",
                "base_url": "http://Bedroc-Proxy-dZmq8lX6J5TY-92025060.us-west-2.elb.amazonaws.com/api/v1",
                "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
            }
        }
    
    def create_default_config(self):
        """创建默认配置文件"""
        default_config = self.get_default_config()
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            print(f"✅ 已创建配置文件: {self.config_file}")
        except Exception as e:
            print(f"❌ 创建配置文件失败: {e}")
    
    def get_llm_config(self):
        """获取LLM配置"""
        llm = self.config.get('llm', {})
        return {
            'api_key': llm.get('api_key'),
            'base_url': llm.get('base_url'),
            'model': llm.get('model')
        }
    
    def update_llm_config(self, api_key=None, base_url=None, model=None):
        """更新LLM配置"""
        updated = False
        
        if api_key:
            self.config['llm']['api_key'] = api_key
            updated = True
            
        if base_url:
            self.config['llm']['base_url'] = base_url
            updated = True
            
        if model:
            self.config['llm']['model'] = model
            updated = True
        
        if updated:
            try:
                # 保存到文件
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
                print("✅ 配置已更新并保存")
            except Exception as e:
                print(f"❌ 配置保存失败: {e}")
        else:
            print("ℹ️ 没有配置需要更新")
    
    def reload_config(self):
        """重新加载配置文件"""
        self.config = self.load_config()
        return self.config
    
    def validate_config(self):
        """验证配置完整性"""
        llm_config = self.get_llm_config()
        
        issues = []
        if not llm_config.get('api_key'):
            issues.append("缺少API密钥")
        if not llm_config.get('base_url'):
            issues.append("缺少API地址")
        if not llm_config.get('model'):
            issues.append("缺少模型名称")
        
        if issues:
            return False, issues
        else:
            return True, ["配置验证通过"]

# 全局配置实例
config = SimpleConfig()

# 测试函数
def test_config():
    """测试配置系统"""
    print("🧪 测试配置系统...")
    
    # 测试加载
    llm_config = config.get_llm_config()
    print(f"LLM配置: {llm_config}")
    
    # 测试验证
    is_valid, messages = config.validate_config()
    print(f"配置验证: {'✅' if is_valid else '❌'} - {messages}")
    
    return is_valid

if __name__ == "__main__":
    test_config()
