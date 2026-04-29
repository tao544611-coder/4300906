#!/usr/bin/env python3
"""
深度诊断微信公众号集成问题
"""
import requests
import json

# 从截图中获取的 AppID
APP_ID = "wx6b8bd0ec095f3c88"

def test_wechat_api_direct():
    """直接测试微信 API（需要 AppSecret）"""
    print("=" * 60)
    print("微信公众号 API 直接测试")
    print("=" * 60)
    print()
    print(f"App ID: {APP_ID}")
    print()
    print("⚠️  注意：需要 AppSecret 才能测试")
    print()
    print("请按照以下步骤操作：")
    print()
    print("1. 登录 https://mp.weixin.qq.com/")
    print("2. 进入「开发」→「基本配置」")
    print("3. 查看或重置 AppSecret")
    print("4. 在 Coze 平台更新 AppSecret")
    print()
    print("=" * 60)
    print()

def check_wechat_permissions():
    """检查微信公众号权限"""
    print("=" * 60)
    print("微信公众号权限检查")
    print("=" * 60)
    print()
    print("请确认你的公众号具备以下权限：")
    print()
    print("必需权限：")
    print("  ✅ 草稿箱功能权限")
    print("  ✅ 素材管理权限")
    print("  ✅ 群发权限（如果要自动发布）")
    print()
    print("检查路径：")
    print("  微信公众平台 → 开发 → 接口权限")
    print()
    print("=" * 60)
    print()

def diagnose_500_error():
    """诊断 500 错误的可能原因"""
    print("=" * 60)
    print("500 错误可能原因诊断")
    print("=" * 60)
    print()
    print("集成 ID 存在，但获取凭证失败，可能原因：")
    print()
    print("1. AppSecret 配置错误")
    print("   - AppSecret 可能已过期")
    print("   - AppSecret 可能输入错误")
    print("   - 解决：重新获取并更新 AppSecret")
    print()
    print("2. 集成授权问题")
    print("   - 集成可能未授权到当前项目")
    print("   - 解决：在 Coze 平台重新授权")
    print()
    print("3. 微信公众号权限不足")
    print("   - 公众号类型可能不支持该功能")
    print("   - 解决：检查接口权限")
    print()
    print("4. 服务器内部错误")
    print("   - Coze 平台可能暂时不可用")
    print("   - 解决：稍后重试或联系技术支持")
    print()
    print("=" * 60)
    print()

def recommend_solutions():
    """推荐解决方案"""
    print("=" * 60)
    print("推荐解决方案（按优先级排序）")
    print("=" * 60)
    print()
    print("方案 1：重新配置 AppSecret（最可能）")
    print("-" * 60)
    print("1. 登录 https://mp.weixin.qq.com/")
    print("2. 进入「开发」→「基本配置」")
    print("3. 点击「重置」AppSecret")
    print("4. 复制新的 AppSecret（只显示一次）")
    print("5. 在 Coze 平台更新 AppSecret")
    print("6. 保存并测试")
    print()
    print("方案 2：检查集成授权")
    print("-" * 60)
    print("1. 登录 Coze 平台")
    print("2. 进入「集成管理」→「微信公众号」")
    print("3. 检查「授权项目」列表")
    print("4. 确认当前项目已授权")
    print("5. 如果未授权，点击「授权」")
    print()
    print("方案 3：验证微信公众号权限")
    print("-" * 60)
    print("1. 登录微信公众平台")
    print("2. 进入「开发」→「接口权限」")
    print("3. 确认必需权限已开启")
    print()
    print("方案 4：联系技术支持")
    print("-" * 60)
    print("如果以上方案都无效，请联系：")
    print("- Coze 平台技术支持")
    print("- 提供错误信息：Integration credential request failed with status 500")
    print()
    print("=" * 60)
    print()

def main():
    test_wechat_api_direct()
    check_wechat_permissions()
    diagnose_500_error()
    recommend_solutions()

if __name__ == "__main__":
    main()
