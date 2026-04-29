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
    title: 搜索AI新闻
    desc: 使用网络搜索功能获取最新的AI行业新闻
    integrations: web-search
    """
    ctx = runtime.context
    
    # 创建搜索客户端
    search_ctx = new_context(method="search.web")
    client = SearchClient(ctx=search_ctx)
    
    # 执行搜索
    response = client.web_search(
        query=state.query,
        count=state.count,
        need_summary=True
    )
    
    # 提取搜索结果
    search_results = []
    if response.web_items:
        for item in response.web_items:
            search_results.append({
                "title": item.title,
                "url": item.url,
                "site_name": item.site_name,
                "snippet": item.snippet or "",
                "summary": item.summary or "",
                "publish_time": item.publish_time or ""
            })
    
    return SearchNewsOutput(search_results=search_results)
