import os
import json
from jinja2 import Template
from coze_coding_dev_sdk import LLMClient
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context

from graphs.state import AnalyzeNewsInput, AnalyzeNewsOutput


def analyze_news_node(
    state: AnalyzeNewsInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> AnalyzeNewsOutput:
    """
    title: 新闻分析
    desc: 从搜索结果中筛选5-8条最有价值的AI新闻，并进行分析
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    # 读取配置文件
    cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config['metadata']['llm_cfg'])
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        llm_cfg = json.load(fd)
    
    # 提取配置
    model_config = llm_cfg.get("config", {})
    system_prompt = llm_cfg.get("sp", "")
    user_prompt_template = llm_cfg.get("up", "")
    
    # 渲染用户提示词
    tpl = Template(user_prompt_template)
    user_prompt = tpl.render(
        news_count=state.news_count,
        search_results=state.search_results
    )
    
    # 创建LLM客户端
    client = LLMClient(ctx=ctx)
    
    # 构建消息
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    # 调用大模型
    response = client.invoke(
        messages=messages,
        model=model_config.get("model", "doubao-seed-2-0-lite-260215"),
        temperature=model_config.get("temperature", 0.7),
        top_p=model_config.get("top_p", 0.9),
        max_completion_tokens=model_config.get("max_completion_tokens", 4000),
        thinking=model_config.get("thinking", "disabled")
    )
    
    # 解析响应
    content = response.content
    if isinstance(content, list):
        content = " ".join(item.get("text", "") if isinstance(item, dict) else str(item) for item in content)
    
    # 提取JSON部分
    try:
        # 尝试直接解析
        result = json.loads(content)
        analyzed_news = result.get("news_list", [])
    except json.JSONDecodeError:
        # 如果直接解析失败，尝试提取JSON代码块
        import re
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            try:
                result = json.loads(json_match.group())
                analyzed_news = result.get("news_list", [])
            except json.JSONDecodeError:
                # 如果仍然失败，返回空列表
                analyzed_news = []
        else:
            analyzed_news = []
    
    return AnalyzeNewsOutput(analyzed_news=analyzed_news)
