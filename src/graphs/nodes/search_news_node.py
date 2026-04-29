import json
from typing import Dict, List
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context

from graphs.state import SearchNewsInput, SearchNewsOutput


def search_news_node(
    state: SearchNewsInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> SearchNewsOutput:
    """
    title: 多渠道搜索AI新闻
    desc: 从36氪、虎嗅、IT之家、InfoQ、GitHub、arXiv等多个渠道搜索最新的AI新闻、论文和开源项目
    integrations: web-search
    """
    ctx = runtime.context

    # 定义多渠道搜索关键词
    search_queries = [
        f"{state.query} site:36kr.com",  # 36氪
        f"{state.query} site:huxiu.com",  # 虎嗅
        f"{state.query} site:ithome.com",  # IT之家
        f"{state.query} site:infoq.cn",  # InfoQ
        "AI 开源项目 site:github.com",  # GitHub开源项目
        "AI 人工智能论文 site:arxiv.org",  # arXiv学术论文
    ]

    # 创建搜索客户端
    search_ctx = new_context(method="search.web")
    client = SearchClient(ctx=search_ctx)

    # 存储所有搜索结果
    all_search_results = []

    # 对每个渠道进行搜索
    for query in search_queries:
        try:
            response = client.web_search(
                query=query,
                count=5,  # 每个渠道取5条
                need_summary=True
            )

            # 提取搜索结果
            if response.web_items:
                for item in response.web_items:
                    all_search_results.append({
                        "title": item.title,
                        "url": item.url,
                        "site_name": item.site_name,
                        "snippet": item.snippet or "",
                        "summary": item.summary or "",
                        "publish_time": item.publish_time or ""
                    })
        except Exception as e:
            # 单个渠道搜索失败不影响其他渠道
            print(f"搜索失败 {query}: {str(e)}")
            continue

    # 去重（基于URL）
    seen_urls = set()
    unique_results = []
    for result in all_search_results:
        if result["url"] not in seen_urls:
            seen_urls.add(result["url"])
            unique_results.append(result)

    # 根据用户要求的数量返回结果
    return SearchNewsOutput(search_results=unique_results[:state.count])
