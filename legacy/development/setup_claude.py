#!/usr/bin/env python3
"""Claude 3.7 配置脚本"""

import json
import os
from pathlib import Path

def setup_claude_config():
    """配置Claude 3.7 API"""
    
    print("🚀 Claude 3.7 配置向导")
    print("=" * 50)
    
    # 获取API Key
    api_key = input("请输入你的Claude API Key: ").strip()
    
    if not api_key:
        print("❌ API Key不能为空")
        return False
    
    # 确认配置
    print(f"\n📋 配置确认:")
    print(f"   API Key: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else api_key}")
    print(f"   模型: us.anthropic.claude-3-7-sonnet-20250219-v1:0")
    print(f"   启用状态: True")
    
    confirm = input("\n确认配置? (y/N): ").strip().lower()
    
    if confirm != 'y':
        print("❌ 配置已取消")
        return False
    
    # 更新配置文件
    config_file = Path("v6_config/claude_config.json")
    
    try:
        # 读取现有配置
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = {"claude_api": {}}
        
        # 更新配置
        config["claude_api"].update({
            "api_key": api_key,
            "base_url": "http://Bedroc-Proxy-dZmq8lX6J5TY-92025060.us-west-2.elb.amazonaws.com/api/v1",
            "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            "enabled": True,
            "timeout": 30,
            "max_tokens": 4000,
            "temperature": 0.7
        })
        
        # 保存配置
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 配置已保存到 {config_file}")
        
        # 验证配置
        print("\n🔍 验证配置...")
        os.system("python3 verify_claude_config.py")
        
        print("\n🎉 Claude 3.7 配置完成！")
        print("💡 提示: 重启服务器使配置生效")
        print("   python tools/manage_server.py restart")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置保存失败: {e}")
        return False

if __name__ == "__main__":
    setup_claude_config()
