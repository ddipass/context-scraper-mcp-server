#!/usr/bin/env python3
"""验证Claude配置脚本"""

try:
    from v6_core.config_manager import get_claude_config
    
    print("🔍 检查Claude配置...")
    claude_config = get_claude_config()
    
    print(f"✅ 配置加载成功")
    print(f"📊 配置详情:")
    print(f"   启用状态: {claude_config.enabled}")
    print(f"   模型: {claude_config.model}")
    print(f"   API Key: {'已配置' if claude_config.api_key else '❌ 未配置'}")
    print(f"   Base URL: {claude_config.base_url}")
    print(f"   超时时间: {claude_config.timeout}秒")
    print(f"   最大Token: {claude_config.max_tokens}")
    print(f"   温度: {claude_config.temperature}")
    
    if claude_config.enabled and claude_config.api_key:
        print("\n🎉 Claude 3.7 配置完成，可以使用！")
    elif not claude_config.api_key:
        print("\n⚠️ 请填入API Key")
    elif not claude_config.enabled:
        print("\n⚠️ 请设置enabled为true")
    else:
        print("\n❌ 配置有问题，请检查")
        
except Exception as e:
    print(f"❌ 配置验证失败: {e}")
