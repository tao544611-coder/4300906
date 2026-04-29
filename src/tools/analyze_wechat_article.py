#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
分析微信公众号文章的排版结构
"""
import json
from coze_coding_dev_sdk.fetch import FetchClient

def analyze_wechat_article(url):
    """获取并分析微信文章的排版结构"""
    print("=" * 80)
    print(f"正在获取文章: {url}")
    print("=" * 80)

    # 不使用 Context，使用默认配置
    client = FetchClient()

    try:
        response = client.fetch(url=url)

        if response.status_code != 0:
            print(f"❌ 获取失败: {response.status_message}")
            return

        print(f"\n📌 标题: {response.title}")
        print(f"📅 发布时间: {response.publish_time}")
        print(f"🔗 URL: {response.url}")
        print(f"\n{'=' * 80}")
        print("📄 内容结构分析:")
        print("=" * 80)

        # 统计各类型内容
        type_counts = {}
        content_structure = []

        for idx, item in enumerate(response.content):
            content_type = item.type
            type_counts[content_type] = type_counts.get(content_type, 0) + 1

            if content_type == "text":
                text = item.text.strip()
                if text:
                    content_structure.append({
                        "序号": len(content_structure) + 1,
                        "类型": "文本",
                        "内容": text[:100] + "..." if len(text) > 100 else text,
                        "字数": len(text)
                    })

            elif content_type == "image":
                image = item.image
                content_structure.append({
                    "序号": len(content_structure) + 1,
                    "类型": "图片",
                    "尺寸": f"{image.width}x{image.height}",
                    "URL": image.display_url[:60] + "..." if len(image.display_url) > 60 else image.display_url
                })

            elif content_type == "link":
                content_structure.append({
                    "序号": len(content_structure) + 1,
                    "类型": "链接",
                    "URL": item.url[:100] + "..." if len(item.url) > 100 else item.url
                })

        # 打印统计信息
        print(f"\n📊 内容统计:")
        print(f"  - 文本段落: {type_counts.get('text', 0)} 个")
        print(f"  - 图片: {type_counts.get('image', 0)} 张")
        print(f"  - 链接: {type_counts.get('link', 0)} 个")
        print(f"  - 总内容项: {len(response.content)} 个")

        # 打印详细结构
        print(f"\n{'=' * 80}")
        print("📋 详细内容结构:")
        print("=" * 80)

        for item in content_structure[:30]:  # 只显示前30项
            print(f"\n【{item['序号']}】{item['类型']}")
            for key, value in item.items():
                if key != "序号":
                    print(f"  {key}: {value}")

        # 分析排版特点
        print(f"\n{'=' * 80}")
        print("🎨 排版特点分析:")
        print("=" * 80)

        # 检查是否有标题、段落分隔等
        text_items = [item for item in response.content if item.type == "text"]
        if text_items:
            avg_length = sum(len(item.text) for item in text_items) // len(text_items)
            print(f"  - 平均段落长度: {avg_length} 字")

            # 检查是否有短文本（可能是标题或重点）
            short_texts = [item.text for item in text_items if len(item.text) < 50]
            if short_texts:
                print(f"  - 检测到 {len(short_texts)} 个短文本段落（可能是标题/重点）:")
                for i, text in enumerate(short_texts[:5]):
                    print(f"    {i+1}. {text}")

        # 保存到文件
        output_file = "/tmp/wechat_article_analysis.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({
                "title": response.title,
                "publish_time": response.publish_time,
                "url": response.url,
                "type_counts": type_counts,
                "content_structure": content_structure,
                "total_items": len(response.content)
            }, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 分析完成！")
        print(f"📁 详细数据已保存到: {output_file}")

    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    article_url = "https://mp.weixin.qq.com/s/LZ46hjBiTrfipbb_ZUEduA"
    analyze_wechat_article(article_url)
