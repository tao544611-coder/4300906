from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class GlobalState(BaseModel):
    """全局状态定义"""
    search_results: List[Dict] = Field(default=[], description="搜索到的AI新闻列表")
    analyzed_news: List[Dict] = Field(default=[], description="分析后的新闻列表（5-8条）")
    draft_media_id: str = Field(default="", description="公众号草稿ID")
    publish_status: str = Field(default="", description="发布状态")


class GraphInput(BaseModel):
    """工作流的输入"""
    query: str = Field(default="AI行业最新新闻", description="搜索关键词")
    count: int = Field(default=15, description="搜索新闻数量")
    news_count: int = Field(default=6, description="最终提取的新闻数量")


class GraphOutput(BaseModel):
    """工作流的输出"""
    draft_media_id: str = Field(..., description="公众号草稿ID")
    publish_status: str = Field(..., description="发布状态：草稿已创建/已发布/失败")


class SearchNewsInput(BaseModel):
    """新闻搜索节点的输入"""
    query: str = Field(..., description="搜索关键词")
    count: int = Field(default=15, description="搜索数量")


class SearchNewsOutput(BaseModel):
    """新闻搜索节点的输出"""
    search_results: List[Dict] = Field(..., description="搜索到的新闻列表")


class AnalyzeNewsInput(BaseModel):
    """新闻分析节点的输入"""
    search_results: List[Dict] = Field(..., description="搜索到的新闻列表")
    news_count: int = Field(default=6, description="需要提取的新闻数量")


class AnalyzeNewsOutput(BaseModel):
    """新闻分析节点的输出"""
    analyzed_news: List[Dict] = Field(..., description="分析后的新闻列表")


class PublishToWeChatInput(BaseModel):
    """公众号发布节点的输入"""
    analyzed_news: List[Dict] = Field(..., description="分析后的新闻列表")


class PublishToWeChatOutput(BaseModel):
    """公众号发布节点的输出"""
    draft_media_id: str = Field(..., description="草稿ID")
    publish_status: str = Field(..., description="发布状态")
