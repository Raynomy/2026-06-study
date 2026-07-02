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