## RAG 生成回答流程

本项目在文档上传和向量检索的基础上，新增了基于上下文生成回答的能力。

完整流程：

```text
用户上传文档
-> 文档切分成 chunks
-> chunks 转成 embedding
-> chunks 写入 Qdrant 向量库
-> 用户提出问题
-> 问题转成 embedding
-> 从 Qdrant 检索相关 chunks
-> 根据相似度阈值过滤低相关 chunks
-> 将高相关 chunks 拼接成 context
-> 将 context 和 question 组成 prompt
-> 调用 LLM 生成回答
-> 返回 answer 和 sources
```

## 新增接口

### POST /documents/answer

作用：

```text
根据已上传文档回答用户问题。
```

请求示例：

```json
{
  "question": "FastAPI 怎么实现登录鉴权？",
  "top_k": 3
}
```

响应示例：

```json
{
  "question": "FastAPI 怎么实现登录鉴权？",
  "answer": "FastAPI 可以结合 JWT 实现用户登录和接口鉴权，但资料中没有提供具体实现方法。",
  "sources": [
    {
      "chunk_id": "fastapi_notes.md-1-a11a46b7",
      "source": "fastapi_notes.md",
      "paragraph": 1,
      "score": 0.841,
      "text": "FastAPI 是一个现代 Python Web 框架..."
    }
  ]
}
```

## 有资料问题测试

问题：

```text
FastAPI 怎么实现登录鉴权？
```

结果：

```text
系统检索到 FastAPI 相关 chunk，并基于该 chunk 生成回答。
```

说明：

```text
RAG 回答不是直接让模型自由发挥，而是先检索资料，再让模型基于资料回答。
```

## 无资料问题测试

问题：

```text
Django 的 ORM 怎么使用？
```

结果：

```json
{
  "question": "Django 的 ORM 怎么使用？",
  "answer": "我没有在已上传的资料中找到相关内容。",
  "sources": []
}
```

说明：

```text
当检索结果相似度低于阈值时，系统不会把无关资料交给模型回答。
```

## 相似度阈值

本项目在 `rag_service.py` 中加入了：

```python
MIN_RELEVANCE_SCORE = 0.6
```

作用：

```text
过滤低相关 chunk，避免向量库把“最相似但不相关”的内容传给 LLM。
```

为什么需要它：

```text
向量库总会返回 top-k 中最相似的内容。
但最相似不代表真的相关。
如果不加阈值，无关问题也可能带着错误上下文进入 prompt。
```

## 本阶段核心理解

RAG 的核心不是简单地“把文档丢给模型”，而是：

```text
先检索
再筛选
再拼接上下文
最后让模型基于上下文回答
```

一个基础 RAG 系统通常包含：

```text
文档处理
chunk 切分
embedding
向量库
top-k 检索
相似度过滤
prompt 构造
LLM 生成
source 返回
```

## 当前限制

```text
Qdrant 仍然使用内存模式，服务重启后数据会丢失。
只支持手动上传文本，不支持真实文件上传。
chunk 切分策略仍然比较简单。
相似度阈值是经验值，还没有系统评测。
还没有加入 RAG 回答质量评测。
```

## 后续可优化方向

```text
使用持久化 Qdrant
支持真实文件上传
支持 PDF / Markdown 解析
优化 chunk size 和 overlap
加入 rerank
加入引用编号
加入 RAG 评测集
记录命中率、无答案拒答率和答案准确率
```


## Grounding 约束

Grounding 指的是让模型的回答严格基于给定资料，而不是依赖模型自己的通用知识自由发挥。

在 RAG 项目中，grounding 的核心是：

```text
先检索资料
再把资料拼成 context
最后要求模型只能根据 context 回答
```

## 为什么需要 Grounding

如果没有 grounding 约束，模型可能会：

```text
使用自己的背景知识补充答案
回答资料中没有出现的内容
在资料不足时仍然给出看似合理的回答
产生幻觉
```

例如用户问：

```text
Django 的 ORM 怎么使用？
```

如果资料中没有 Django ORM，模型本身其实知道 Django ORM 的用法。  
但在 RAG 系统里，它不应该直接回答，因为当前知识库没有提供这个依据。

正确行为是：

```text
资料中没有提到。
```

或者：

```text
我没有在已上传的资料中找到相关内容。
```

## 本项目中的 Grounding Prompt

本项目在 `rag_service.py` 中使用了更严格的 prompt：

```text
你是一个严格遵守 grounding 规则的中文 RAG 助手。

你的任务：
只根据【资料】回答【问题】。

Grounding 规则：
1. 只能使用【资料】中明确出现的信息
2. 不能使用你自己的背景知识补充答案
3. 不能推测、扩展或编造资料外的信息
4. 如果【资料】不足以回答问题，必须回答“资料中没有提到”
5. 如果只能回答一部分，就只回答资料能支持的部分
6. 回答要简洁清楚
```

这段 prompt 的作用是：

```text
限制模型只能使用检索结果
阻止模型根据通用知识扩展答案
资料不足时让模型拒答
减少幻觉
```

## 有资料问题测试

问题：

```text
FastAPI 登录后客户端应该怎么携带 token？
```

资料中包含：

```text
用户登录成功后，后端生成 token，客户端后续请求时在 Authorization header 中携带 token。
```

模型回答：

```text
根据【资料】，客户端后续请求时在 Authorization header 中携带 token。
```

说明：

```text
回答中的关键信息可以在资料中找到。
模型没有额外补充资料中没有的实现细节。
```

## 无资料问题测试

问题：

```text
Django 的 ORM 怎么使用？
```

当前资料中没有 Django ORM 相关内容。

模型回答：

```text
我没有在已上传的资料中找到相关内容。
```

说明：

```text
模型没有使用自己的背景知识解释 Django ORM。
当资料不足时，系统选择拒答。
```

## 幻觉案例记录

潜在幻觉案例：

```text
问题：Django 的 ORM 怎么使用？
资料：只有 FastAPI、JWT、pytest、Docker 相关内容
```

如果没有 grounding，模型可能会回答：

```text
Django ORM 可以通过定义 Model 类、执行迁移、使用 objects 查询数据库。
```

这个回答本身可能是正确的，但它不来自当前资料，所以在 RAG 系统里属于不可信回答。

加入 grounding 后，系统应该回答：

```text
资料中没有提到。
```

这就是 grounding 的价值：

```text
不是让模型展示自己知道多少，
而是让模型只回答当前资料能支持的内容。
```

## Grounding 和 Sources 的关系

Grounding 约束回答内容，sources 提供答案依据。

两者配合使用：

```text
grounding：限制模型只能基于资料回答
sources：告诉用户答案来自哪些资料
```

一个可信的 RAG 回答应该满足：

```text
answer 中的关键信息能在 sources.text 中找到
sources.source 来自正确文件
sources.score 足够高
资料不足时不强行回答
```

## 核心结论

```text
Grounding 是 RAG 减少幻觉的关键。
RAG 不是让模型自由回答，而是让模型基于检索资料回答。
资料不足时，拒答比编造更可靠。
answer + sources + grounding 共同构成可信 RAG 回答。
```

## RAG 调参记录

本次主要观察两个参数：

```text
chunk_size：每个 chunk 的文本长度
top_k：每次检索返回多少个 chunk
```

## chunk_size 对召回的影响

### chunk_size = 120, overlap = 20

测试问题：

```text
客户端登录后怎么携带 token？
```

召回结果中命中了相关内容：

```text
Authorization header 中携带 token
```

但问题是 chunk 开头出现了：

```text
续请求时...
```

说明句子被切断了。

结论：

```text
chunk_size 太小，容易把完整语义切碎。
虽然能命中局部关键词，但上下文不完整。
```

### chunk_size = 180, overlap = 40

调整后，同样的问题召回结果中包含更完整的信息：

```text
用户登录成功后，后端可以生成 JWT token，客户端后续请求时在 Authorization header 中携带 token。
```

结论：

```text
chunk_size 变大后，语义更完整，句子被切断的问题减少。
但一个 chunk 里也可能混入 pytest、Docker 等弱相关内容。
```

## top_k 对召回的影响

### top_k = 1

结果：

```text
只返回最相关的 1 个 chunk。
```

优点：

```text
上下文更干净。
较少引入无关内容。
```

缺点：

```text
如果相关信息分散在多个 chunk 中，可能漏掉上下文。
```

### top_k = 3

结果：

```text
返回前 3 个相似 chunk。
```

优点：

```text
召回内容更多。
更可能补齐前后文。
```

缺点：

```text
容易带入弱相关 chunk。
可能让 prompt 中混入噪声。
```

## 本次召回失败原因

本次观察到的主要问题：

```text
固定字符切分可能切断句子。
chunk 太小会导致上下文不完整。
chunk 太大会混入无关内容。
top_k 太大会带入弱相关资料。
```

对应解决思路：

```text
适当增大 chunk_size
设置合理 overlap
使用相似度阈值过滤低相关 chunk
后续可以改成按段落或 Markdown 标题切分
必要时加入 rerank
```

## 当前推荐配置

当前项目暂时使用：

```python
chunk_size = 180
overlap = 40
top_k = 1 或 3
MIN_RELEVANCE_SCORE = 0.75
```

理解：

```text
chunk_size=180：保证基本语义完整
overlap=40：减少切断句子的影响
top_k=1：适合来源干净的问答
top_k=3：适合需要更多上下文的问题
相似度阈值：过滤掉弱相关资料
```

## 核心结论

RAG 调参没有一个永远正确的固定值。

需要根据：

```text
文档长度
文档结构
问题类型
答案需要的上下文范围
召回结果是否干净
```

不断观察和调整。

调参目标不是让返回内容越多越好，而是：

```text
召回足够相关的资料
减少无关资料进入 prompt
让 LLM 基于更干净的 context 回答
```
#### RAG 评测表

##### 评测目标
本次评测用于检查 RAG 系统在固定测试问题下的表现，重点关注：

- 回答是否基于已上传资料
- 回答是否准确
- `sources` 是否真实引用了检索结果
- 资料不足时是否能够正确拒答
- 失败时是检索问题、生成问题，还是引用问题

##### 评测结论
- 总测试数：20
- 通过数：11
- 失败数：9
- 分类/回答准确率：55%
- 引用正确率：通过样例中较稳定
- 主要失败原因：检索召回不稳定，导致相关 chunk 没有被召回或召回不完整

##### 评测维度
- 回答准确性：回答内容是否和资料一致
- 引用质量：`sources` 是否真的来自检索结果
- Grounding：回答是否只基于资料，不胡编
- 失败处理：资料不足时是否返回“未找到相关内容”
- 稳定性：同类问题多次测试时结果是否一致

##### 典型通过样例
- 问题：FastAPI 登录后客户端应该怎么携带 token？
- 结果：回答正确，明确说明客户端应在 `Authorization` header 中携带 token
- 引用：只引用了相关的 FastAPI JWT chunk
- 结论：回答与资料一致，引用也正确

- 问题：FastAPI 如何实现用户登录鉴权？
- 结果：回答正确，说明可以结合 JWT 实现登录鉴权
- 引用：引用了包含 JWT 鉴权说明的 chunk
- 结论：属于标准 grounded answer

- 问题：Django 的 ORM 怎么使用？
- 结果：资料中没有相关内容
- 结论：应返回“我没有在已上传的资料中找到相关内容”，并且 `sources` 为空

##### 典型失败样例
- 失败类型：检索召回不足
- 表现：问题本身是资料里有的，但没有把最相关 chunk 召回出来
- 影响：回答可能变空、答偏，或引用了不够相关的 chunk

- 失败类型：引用不够干净
- 表现：召回结果里混入了相关性较弱的 chunk
- 影响：虽然答案大致正确，但 `sources` 质量下降

- 失败类型：资料不足时处理不稳定
- 表现：有时会硬答，有时会正确拒答
- 影响：说明提示词和检索阈值还可以继续优化

##### 失败原因归纳
1. 检索阶段
- chunk 切分粒度可能还不够理想
- top-k 结果里相关 chunk 排名不稳定
- query 与 chunk 的语义匹配不总是稳定

2. 生成阶段
- prompt 对“只能基于资料回答”的约束还可以更强
- 资料不足时的拒答语气和格式还可以统一

3. 引用阶段
- `sources` 应优先返回真正支持回答的 chunk
- 无关 chunk 不应该混入最终引用列表

##### 可以继续优化的方向
- 调整 chunk size 和 overlap
- 优化 top-k 和相似度阈值
- 强化 prompt 中的 grounding 约束
- 对“资料不足”增加统一拒答模板
- 在返回结果里继续保留 `sources`，方便追溯

##### 本阶段收获
- 明白了 RAG 评测不只是看“答对没”，还要看“有没有依据”
- 明白了检索质量直接决定最终回答质量
- 明白了 `sources` 是判断 RAG 是否可靠的重要证据
- 明白了 grounding 的核心是“只基于资料回答，不补编”

##### 下一步
- 继续优化检索召回
- 继续补充测试样例
- 进一步整理 RAG 项目结构和 README
- 为后续完整项目积累可写进简历的成果