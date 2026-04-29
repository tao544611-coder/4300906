# 微信公众号集成问题排查指南

## 🔍 问题描述

**错误信息**: `Integration credential request failed with status 500`

**症状**: 工作流在发布到公众号节点失败，无法获取微信公众号集成凭证

---

## ✅ 排查步骤

### 步骤 1: 检查 Coze 平台集成配置 ⭐ 最重要

#### 1.1 登录 Coze 平台
1. 访问 https://www.coze.cn/
2. 进入你的项目

#### 1.2 查看集成列表
1. 找到「集成管理」或「Integrations」页面
2. 查看已安装的集成列表
3. 确认是否有「微信公众号」集成

#### 1.3 检查集成 ID
1. 点击「微信公众号」集成进入配置页
2. 查看集成详情
3. **关键**：记下集成 ID（可能是 `integration-wechat-official-account` 或其他）

#### 1.4 确认集成授权
1. 在集成详情页，查看「授权项目」列表
2. 确认当前项目是否在授权列表中
3. 如果不在，点击「授权」按钮

#### 1.5 验证 AppID 和 AppSecret
1. 在集成配置页，检查 AppID 和 AppSecret
2. 确认这两个值是否正确填写
3. 如果不确定，重新获取：
   - 登录 https://mp.weixin.qq.com/
   - 进入「开发」→「基本配置」
   - 复制 AppID
   - 重置 AppSecret（只显示一次，务必保存）

### 步骤 2: 检查代码中的集成 ID

#### 2.1 查看代码中的集成 ID
代码中使用的集成 ID：
```python
# 文件: src/graphs/nodes/publish_to_wechat_node.py
# 第 31 行
integration_id = "integration-wechat-official-account"
```

#### 2.2 比对集成 ID
- ✅ 如果 Coze 平台上的集成 ID 是 `integration-wechat-official-account`，无需修改
- ❌ 如果不同，需要修改代码中的集成 ID

#### 2.3 如何修改集成 ID（如果需要）

如果 Coze 平台上的集成 ID 不同，按以下步骤修改：

1. 找到 Coze 平台上的正确集成 ID
2. 修改代码：

```bash
# 编辑文件
vi src/graphs/nodes/publish_to_wechat_node.py

# 找到第 31 行
return client.get_integration_credential("integration-wechat-official-account")

# 将引号中的值改为 Coze 平台上的集成 ID
# 例如：
return client.get_integration_credential("weixin-official-account-xxx")
```

3. 保存文件并提交

### 步骤 3: 检查微信公众号配置

#### 3.1 检查公众号类型
- ✅ 订阅号：可以发送 1 次/天
- ✅ 服务号：可以发送 4 次/月
- ✅ 认证服务号：功能最全

#### 3.2 检查 API 权限
登录微信公众平台：
1. 进入「开发」→「接口权限」
2. 确认以下权限已开启：
   - ✅ 草稿箱功能权限
   - ✅ 素材管理权限
   - ✅ 群发权限（如果要自动发布）

#### 3.3 配置服务器 IP 白名单（重要）
1. 在微信公众平台，进入「开发」→「基本配置」
2. 找到「服务器配置」或「IP 白名单」
3. 添加 Coze 平台的服务器 IP
4. 如果不知道具体 IP，可以先临时允许所有 IP（仅测试用）

### 步骤 4: 验证集成配置

#### 4.1 在 Coze 平台测试集成
1. 进入集成管理页面
2. 找到「微信公众号」集成
3. 点击「测试」或「验证」按钮
4. 查看测试结果

#### 4.2 查看集成日志
1. 在 Coze 平台查看集成日志
2. 检查是否有错误信息

---

## 🛠️ 常见问题与解决方案

### 问题 1: 集成 ID 不匹配

**症状**: 500 错误
**原因**: 代码中的集成 ID 与 Coze 平台不一致
**解决**:
1. 在 Coze 平台查找正确的集成 ID
2. 修改代码中的集成 ID
3. 重新部署

### 问题 2: 集成未授权到项目

**症状**: 500 错误
**原因**: 集成创建后未授权到当前项目
**解决**:
1. 在 Coze 平台进入集成详情
2. 找到「授权项目」
3. 点击「授权」按钮，选择当前项目

### 问题 3: AppID 或 AppSecret 错误

**症状**: 500 错误或 401 错误
**原因**: AppID 或 AppSecret 填写错误
**解决**:
1. 重新从微信公众平台获取 AppID 和 AppSecret
2. 在 Coze 平台更新配置
3. 保存并测试

### 问题 4: 公众号权限不足

**症状**: 创建草稿失败，提示权限不足
**原因**: 公众号未开启必要权限
**解决**:
1. 在微信公众平台开启草稿箱、素材管理等权限
2. 确认公众号类型是否满足需求

### 问题 5: IP 白名单限制

**症状**: 500 错误或连接超时
**原因**: Coze 服务器 IP 未加入白名单
**解决**:
1. 在微信公众平台配置 IP 白名单
2. 临时方案：先允许所有 IP（仅测试用）

---

## 📝 修改集成 ID 的步骤（如果需要）

假设 Coze 平台上的集成 ID 是 `weixin-official-account-12345`：

### 方法 1: 使用 sed 命令

```bash
# 备份原文件
cp src/graphs/nodes/publish_to_wechat_node.py src/graphs/nodes/publish_to_wechat_node.py.bak

# 替换集成 ID
sed -i 's/integration-wechat-official-account/weixin-official-account-12345/g' \
  src/graphs/nodes/publish_to_wechat_node.py

# 验证修改
grep "get_integration_credential" src/graphs/nodes/publish_to_wechat_node.py
```

### 方法 2: 手动编辑

```bash
# 使用 vi 编辑
vi src/graphs/nodes/publish_to_wechat_node.py

# 找到第 31 行，修改为正确的集成 ID
# 保存并退出
```

### 修改后提交

```bash
# 查看修改
git diff src/graphs/nodes/publish_to_wechat_node.py

# 提交修改
git add src/graphs/nodes/publish_to_wechat_node.py
git commit -m "fix: 修正微信公众号集成ID"
git push
```

---

## 🧪 修改后重新测试

### 1. 提交代码

```bash
git add .
git commit -m "fix: 更新微信公众号集成配置"
git push
```

### 2. 在 Coze 平台重新部署

1. 进入你的项目
2. 找到工作流
3. 点击「重新部署」或「刷新代码」
4. 等待部署完成

### 3. 手动测试

1. 在 Coze 平台点击「运行」
2. 输入测试参数：
```json
{
  "query": "AI人工智能测试",
  "count": 5,
  "news_count": 3
}
```
3. 查看执行结果

---

## 📞 仍然无法解决？

如果以上步骤都无法解决问题，请收集以下信息：

1. **Coze 平台信息**:
   - 项目 ID
   - 集成 ID（完整的集成标识）
   - 集成状态截图

2. **微信公众号信息**:
   - 公众号类型（订阅号/服务号）
   - AppID（脱敏）
   - 已开启的 API 权限截图

3. **错误信息**:
   - 完整的错误日志
   - 执行时间
   - 工作流 ID

4. **联系技术支持**:
   - Coze 平台客服
   - 微信公众平台客服

---

## ✅ 成功标志

当问题解决后，你会看到：

1. ✅ 日志中不再出现 500 错误
2. ✅ publish_to_wechat 节点成功执行
3. ✅ 返回草稿 ID（draft_media_id 不为空）
4. ✅ 发布状态显示"草稿已创建"
5. ✅ 微信公众号草稿箱中出现新文章

---

## 🎯 快速检查清单

在排查前，快速检查以下项目：

- [ ] Coze 平台上已创建微信公众号集成
- [ ] 集成已授权到当前项目
- [ ] AppID 和 AppSecret 已正确填写
- [ ] 代码中的集成 ID 与 Coze 平台一致
- [ ] 公众号具备必要 API 权限
- [ ] IP 白名单已配置（如有需要）
- [ ] 代码已修改并提交到 GitHub
- [ ] Coze 平台工作流已重新部署

---

**希望这份排查指南能帮助你解决问题！** 🚀
