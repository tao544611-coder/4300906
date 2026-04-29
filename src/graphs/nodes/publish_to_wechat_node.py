import os
import json
import base64
import requests
from typing import Dict, List, Any
from datetime import datetime
from coze_workload_identity import Client
from cozeloop.decorator import observe
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context

from graphs.state import PublishToWeChatInput, PublishToWeChatOutput


def publish_to_wechat_node(
    state: PublishToWeChatInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> PublishToWeChatOutput:
    """
    title: 发布到公众号
    desc: 将分析后的新闻生成公众号文章并发布
    integrations: 微信公众号、图片生成
    """
    ctx = runtime.context
    
    client = Client()
    
    # 获取access_token
    def get_access_token():
        return client.get_integration_credential("integration-wechat-official-account")
    
    class WeChatOfficial:
        def __init__(self):
            self.access_token = get_access_token()
        
        def _is_base64(self, s: str) -> bool:
            t = s.strip().replace("\n", "")
            try:
                import base64
                base64.b64decode(t, validate=True)
                return True
            except Exception:
                return False
        
        def _prepare_media_files(self, image: Any):
            files = None
            f_to_close = None
            if isinstance(image, bytes):
                files = {"media": ("image.jpg", image)}
            elif isinstance(image, str):
                if image.startswith("http://") or image.startswith("https://"):
                    resp = requests.get(image, timeout=30)
                    resp.raise_for_status()
                    files = {"media": ("image.jpg", resp.content)}
                elif image.startswith("data:"):
                    import base64
                    b64 = image.split(",", 1)[1] if "," in image else ""
                    data = base64.b64decode(b64)
                    files = {"media": ("image.jpg", data)}
                elif self._is_base64(image):
                    import base64
                    data = base64.b64decode(image.strip().replace("\n", ""), validate=True)
                    files = {"media": ("image.jpg", data)}
            return files, f_to_close
        
        @observe
        def generate_image_by_prompt(self, prompt: str) -> str:
            """
            生成图片
            :param prompt: 图片描述
            :return: 图片url
            """
            base_url = os.getenv("COZE_INTEGRATION_BASE_URL")
            api_key = client.get_access_token()
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + api_key
            }
            request = {
                "model": "doubao-seedream-4-0-250828",
                "prompt": prompt,
            }
            response = None
            try:
                response = requests.post(f'{base_url}/api/v3/images/generations', json=request, headers=headers, timeout=30)
                response.raise_for_status()
                data = response.json()
                if "error" in data:
                    raise Exception(f"图片生成失败: status_code={response.status_code}, message={data['error']['message']}")
                img_list = []
                for item in data["data"]:
                    if "url" in item:
                        img_list.append(item["url"])
                if len(img_list) == 0:
                    raise Exception(f"图片生成失败: status_code={response.status_code}, message=无图片url")
                return img_list[0]
            except Exception as e:
                raise Exception(f"图片生成失败: {e}")
            finally:
                try:
                    if response is not None:
                        response.close()
                except Exception:
                    pass
        
        @observe
        def upload_permanent_image(self, image: Any) -> Dict[str, Any]:
            """上传永久图片"""
            token = self.access_token
            url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
            files, f_to_close = self._prepare_media_files(image)
            try:
                r = requests.post(url, files=files, timeout=30)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                raise Exception(f"上传永久图片异常: {e}")
            if data.get("errcode", 0) != 0:
                raise Exception(f"上传永久图片失败: {data}")
            return {"media_id": data.get("media_id"), "url": data.get("url")}
        
        def add_draft(self, articles: List[Dict[str, Any]]) -> str:
            """新增草稿"""
            if not articles:
                raise ValueError("articles不能为空")
            token = self.access_token
            url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
            try:
                json_data = json.dumps({"articles": articles}, ensure_ascii=False).encode("utf-8")
                r = requests.post(url, data=json_data, timeout=15)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                raise Exception(f"新增草稿异常: {e}")
            if data.get("errcode", 0) != 0:
                raise Exception(f"新增草稿失败: {data}")
            media_id = data.get("media_id")
            if not media_id:
                raise Exception(f"新增草稿失败: {data}")
            return media_id
    
    try:
        wechat = WeChatOfficial()

        # 生成封面图（带容错处理）
        thumb_media_id = ""
        cover_image_url = ""
        today = datetime.now().strftime("%Y年%m月%d日")

        try:
            # 尝试生成封面图
            cover_prompt = f"AI人工智能科技感封面图，现代简约风格，蓝色调，包含机器人、芯片、数据流等元素，适合公众号文章封面，高清，专业"
            cover_image_url = wechat.generate_image_by_prompt(cover_prompt)
            print(f"图片生成成功：{cover_image_url}")

            # 上传封面图获取media_id
            perm_result = wechat.upload_permanent_image(cover_image_url)
            thumb_media_id = perm_result["media_id"]
            print(f"封面图上传成功，media_id：{thumb_media_id}")

        except Exception as e:
            # 图片生成失败，尝试使用网络图片
            print(f"警告：封面图生成失败，尝试使用网络图片。错误：{str(e)}")

            try:
                # 使用 Unsplash 的免费科技感图片作为封面
                cover_image_url = "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=900&h=500&fit=crop"
                print(f"使用网络图片作为封面：{cover_image_url}")
                perm_result = wechat.upload_permanent_image(cover_image_url)
                thumb_media_id = perm_result["media_id"]
                print(f"网络图片上传成功，media_id：{thumb_media_id}")
            except Exception as e2:
                print(f"警告：无法上传网络图片，将尝试不使用封面图。错误：{str(e2)}")
                # thumb_media_id 保持为空字符串
                # 注意：微信公众号的草稿可能需要封面图，如果失败则无法创建草稿
            except Exception as e2:
                print(f"警告：无法上传占位图片，将尝试不使用封面图。错误：{str(e2)}")
                # thumb_media_id 保持为空字符串，创建草稿时可能需要封面，看微信要求
        
        # 构建文章内容
        title = f"AI早报 | {today} 最新AI行业资讯"
        
        # 构建HTML内容
        content_html = f'<p style="font-size: 16px; color: #333; line-height: 1.8;">今日AI行业要闻速览：</p>'
        
        for i, news in enumerate(state.analyzed_news, 1):
            content_html += f'''
<section style="margin: 20px 0; padding: 15px; background: #f5f7fa; border-radius: 8px;">
<h3 style="font-size: 18px; color: #2c3e50; margin: 0 0 10px 0;">{i}. {news.get("title", "")}</h3>
<p style="font-size: 14px; color: #7f8c8d; margin: 5px 0;">来源：{news.get("site_name", "")} | {news.get("publish_time", "")}</p>
<p style="font-size: 15px; color: #34495e; line-height: 1.6; margin: 10px 0;">{news.get("analysis", "")}</p>
<p style="font-size: 13px; color: #95a5a6;">链接：<a href="{news.get("url", "")}" style="color: #3498db;">阅读原文</a></p>
</section>
'''
        
        content_html += '''
<p style="font-size: 14px; color: #999; text-align: center; margin-top: 30px;">—— 完 ——</p>
<p style="font-size: 13px; color: #bdc3c7; text-align: center;">本文由AI智能生成，仅供参考</p>
'''
        
        # 构建文章对象
        article = {
            "title": title,
            "author": "AI助手",
            "digest": f"今日AI行业最新动态，精选{len(state.analyzed_news)}条重要资讯",
            "content": content_html,
            "thumb_media_id": thumb_media_id,
            "need_open_comment": 1,
            "only_fans_can_comment": 0
        }

        # 检查是否有有效的封面图
        if not thumb_media_id:
            return PublishToWeChatOutput(
                draft_media_id="",
                publish_status="发布失败: 无法获取有效的封面图，微信公众号草稿需要封面图。建议：1) 检查网络连接；2) 使用更稳定的图片源；3) 确认公众号有素材管理权限"
            )

        # 创建草稿
        draft_media_id = wechat.add_draft([article])
        print(f"草稿创建成功，media_id：{draft_media_id}")

        return PublishToWeChatOutput(
            draft_media_id=draft_media_id,
            publish_status="草稿已创建"
        )
    
    except Exception as e:
        return PublishToWeChatOutput(
            draft_media_id="",
            publish_status=f"发布失败: {str(e)}"
        )
