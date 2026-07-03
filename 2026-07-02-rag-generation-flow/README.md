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