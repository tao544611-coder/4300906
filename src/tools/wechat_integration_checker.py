"""
微信公众号集成诊断工具
用于排查微信集成配置问题
"""
import os
from coze_workload_identity import Client


def check_wechat_integration():
    """检查微信公众号集成配置"""
    print("=" * 60)
    print("微信公众号集成诊断工具")
    print("=" * 60)

    client = Client()

    # 检查集成 ID
    integration_id = "integration-wechat-official-account"
    print(f"\n1. 检查集成 ID: {integration_id}")

    try:
        # 尝试获取凭证
        print("   正在尝试获取集成凭证...")
        credential = client.get_integration_credential(integration_id)

        print(f"   ✅ 成功获取凭证！")
        print(f"   凭证类型: {type(credential)}")
        print(f"   凭证内容: {credential}")

        if credential:
            print("\n✅ 集成配置正确！")
            return True
        else:
            print("\n❌ 错误：凭证为空")
            return False

    except Exception as e:
        print(f"\n❌ 获取凭证失败！")
        print(f"   错误类型: {type(e).__name__}")
        print(f"   错误信息: {str(e)}")

        # 常见错误诊断
        error_msg = str(e)
        if "500" in error_msg:
            print("\n🔍 诊断结果：")
            print("   - 错误码 500 表示集成服务请求失败")
            print("   - 可能原因：")
            print("     1. 集成 ID 不正确")
            print("     2. 集成未正确授权到当前项目")
            print("     3. AppID 和 AppSecret 配置错误")
            print("     4. 微信公众号服务器 IP 白名单未配置")
            print("\n💡 解决方案：")
            print("   1. 检查 Coze 平台上的集成 ID 是否为: integration-wechat-official-account")
            print("   2. 确认集成已授权到当前项目")
            print("   3. 验证 AppID 和 AppSecret 是否正确")
            print("   4. 在微信公众平台配置服务器 IP 白名单")

        elif "404" in error_msg:
            print("\n🔍 诊断结果：")
            print("   - 集成 ID 不存在")
            print("\n💡 解决方案：")
            print("   - 检查 Coze 平台上的集成 ID 是否正确")
            print("   - 确认是否已创建微信公众号集成")

        elif "403" in error_msg:
            print("\n🔍 诊断结果：")
            print("   - 集成未授权到当前项目")
            print("\n💡 解决方案：")
            print("   - 在 Coze 平台将集成授权到当前项目")

        return False


if __name__ == "__main__":
    success = check_wechat_integration()

    if not success:
        print("\n" + "=" * 60)
        print("📞 需要帮助？")
        print("=" * 60)
        print("如果以上方案无法解决问题，请检查：")
        print("1. Coze 平台集成管理页面")
        print("2. 微信公众平台开发配置")
        print("3. 联系技术支持")
