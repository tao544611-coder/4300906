#!/usr/bin/env python3
"""
测试不同的微信集成 ID
"""
import os
from coze_workload_identity import Client

# 可能的集成 ID 列表
POSSIBLE_INTEGRATION_IDS = [
    "integration-wechat-official-account",  # 当前代码使用的
    "wechat-official-account",
    "weixin-official-account",
    "wx-official-account",
    "wx-official",
    "wechat",
    "weixin",
]

def test_integration_id(integration_id: str) -> bool:
    """测试集成 ID 是否有效"""
    try:
        client = Client()
        token = client.get_integration_credential(integration_id)
        
        if token:
            print(f"✅ 集成 ID '{integration_id}' 成功！")
            print(f"   Access Token: {token[:20]}...")
            return True
        else:
            print(f"❌ 集成 ID '{integration_id}' 失败：返回空 token")
            return False
    except Exception as e:
        print(f"❌ 集成 ID '{integration_id}' 失败：{str(e)}")
        return False

def main():
    print("=" * 60)
    print("微信公众号集成 ID 检测工具")
    print("=" * 60)
    print()
    
    found = False
    for integration_id in POSSIBLE_INTEGRATION_IDS:
        print(f"正在测试: {integration_id}")
        if test_integration_id(integration_id):
            found = True
            print()
            print("=" * 60)
            print(f"✅ 找到正确的集成 ID: {integration_id}")
            print("=" * 60)
            break
        print()
    
    if not found:
        print("=" * 60)
        print("❌ 所有常见的集成 ID 都失败了！")
        print("=" * 60)
        print()
        print("请登录 Coze 平台查看集成详情页，找到正确的集成 ID")
        print("路径：项目 → 集成管理 → 微信公众号 → 集成详情")

if __name__ == "__main__":
    main()
