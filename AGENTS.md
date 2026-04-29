## 项目概述
- **名称**: AI新闻推送工作流
- **功能**: 每天自动抓取AI行业新闻，提取5-8条重要资讯并进行分析，发布到微信公众号

### 节点清单
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| search_news | `nodes/search_news_node.py` | task | 搜索AI新闻 | - | - |
| analyze_news | `nodes/analyze_news_node.py` | agent | 分析并筛选新闻 | - | `config/analyze_news_llm_cfg.json` |
| publish_to_wechat | `nodes/publish_to_wechat_node.py` | task | 发布到公众号 | - | - |

**类型说明**: task(task节点) / agent(大模型) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

## 子图清单
无子图

## 技能使用
- 节点 `search_news` 使用技能 `web-search`：搜索AI行业最新新闻
- 节点 `analyze_news` 使用技能 `llm`：使用大语言模型分析并筛选新闻
- 节点 `publish_to_wechat` 使用技能 `wechat-official-account` 和 `image-generation`：生成封面图并发布到微信公众号

## 工作流说明
1. **新闻搜索**: 使用网络搜索功能获取最新的AI行业新闻（默认15条）
2. **新闻分析**: 使用大语言模型从搜索结果中筛选5-8条最有价值的新闻，并生成简要分析
3. **公众号发布**: 自动生成封面图，构建公众号文章内容，创建草稿

## 输入参数
- `query`: 搜索关键词（默认：AI行业最新新闻）
- `count`: 搜索新闻数量（默认：15）
- `news_count`: 最终提取的新闻数量（默认：6）

## 输出参数
- `draft_media_id`: 公众号草稿ID
- `publish_status`: 发布状态

## 注意事项
- 使用前需要配置微信公众号集成凭证
- 发布的草稿需要在微信公众号后台手动审核和发布
- 封面图由AI自动生成
