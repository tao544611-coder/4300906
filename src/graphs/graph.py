from langgraph.graph import StateGraph, END

from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)
from graphs.nodes.search_news_node import search_news_node
from graphs.nodes.analyze_news_node import analyze_news_node
from graphs.nodes.publish_to_wechat_node import publish_to_wechat_node


# 创建状态图
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
builder.add_node("search_news", search_news_node)
builder.add_node("analyze_news", analyze_news_node, metadata={"type": "agent", "llm_cfg": "config/analyze_news_llm_cfg.json"})
builder.add_node("publish_to_wechat", publish_to_wechat_node)

# 设置入口点
builder.set_entry_point("search_news")

# 添加边
builder.add_edge("search_news", "analyze_news")
builder.add_edge("analyze_news", "publish_to_wechat")
builder.add_edge("publish_to_wechat", END)

# 编译图
main_graph = builder.compile()
