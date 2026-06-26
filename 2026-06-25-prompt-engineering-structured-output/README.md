# 2026-06-25 Prompt Engineering 与结构化输出

这是 Prompt Engineering 与结构化输出学习项目，用于练习 Prompt 基础写法、任务模板、JSON 结构化输出、Pydantic 校验、JSON 修复和 Prompt 评测。

本项目重点不是搭建 API，而是通过独立脚本理解 LLM 应用开发中 prompt 如何被设计、约束、校验和评测。

## 学习目标

- 理解 Zero-shot、Instruction、Few-shot Prompt 的区别
- 设计问答、分类、抽取三类常见任务 prompt
- 理解角色设定、任务边界、输出格式约束
- 练习 Markdown 输出和 JSON 结构化输出
- 使用 `json.loads()` 解析模型 JSON 输出
- 使用 Pydantic 校验模型输出结构
- 处理模型输出不合法 JSON 的情况
- 使用修复 prompt 和 retry 流程提高稳定性
- 使用固定测试集评测 prompt 稳定性

## 项目结构

```text
2026-06-25-prompt-engineering-structured-output/
├── .env.example
├── README.md
├── prompt_compare.py
├── prompt_tasks.py
├── prompt_constraints.py
├── json_output_examples.py
├── json_repair_examples.py
└── prompt_eval_examples.py
```

## 文件说明

```text
prompt_compare.py
对比 Zero-shot、Instruction、Few-shot 三种 prompt 写法。

prompt_tasks.py
练习问答、分类、抽取三类常见 prompt 任务。

prompt_constraints.py
练习角色设定、任务边界、Markdown 输出和 JSON 输出约束。

json_output_examples.py
练习 JSON 结构化输出、json.loads() 解析和 Pydantic 校验。

json_repair_examples.py
练习 JSON 解析失败后的修复 prompt 和失败重试流程。

prompt_eval_examples.py
练习使用固定测试集评测 prompt，记录准确率、格式正确率和失败原因。
```

## 环境变量

本项目使用 `.env` 保存本地真实配置，但 `.env` 不提交到 GitHub。

`.env.example` 示例：

```env
AIHUBMIX_API_KEY=your-api-key-here
AIHUBMIX_BASE_URL=https://aihubmix.com/v1
AIHUBMIX_MODEL=deepseek-v4-flash
```

## 运行方式

进入项目目录：

```bash
cd /Users/xiongzehao/Desktop/python进阶/2026-06-study/2026-06-25-prompt-engineering-structured-output
```

运行任意练习脚本：

```bash
../.venv/bin/python prompt_compare.py
../.venv/bin/python prompt_tasks.py
../.venv/bin/python prompt_constraints.py
../.venv/bin/python json_output_examples.py
../.venv/bin/python json_repair_examples.py
../.venv/bin/python prompt_eval_examples.py
```

## 核心知识点

### Prompt 基础写法

```text
Zero-shot Prompt
不给示例，直接让模型完成任务，适合简单问答和快速测试。

Instruction Prompt
给出明确任务、规则和输出限制，适合控制输出格式。

Few-shot Prompt
给出示例，让模型模仿格式和判断标准，适合分类、抽取和固定格式输出。
```

更稳定的写法通常是：

```text
角色
任务
边界
输出格式
示例
输入
```

### 常见任务模板

```text
问答 Prompt
用于解释概念、总结知识、回答问题。

分类 Prompt
用于从固定标签中选择类别，类别必须提前给定。

抽取 Prompt
用于从文本中提取固定字段，字段名和缺失值处理规则必须明确。
```

### Markdown 与 JSON

```text
Markdown
适合给人阅读，比如学习笔记、README、报告总结。

JSON
适合给程序处理，比如接口返回、工具参数、信息抽取结果。
```

### Pydantic 校验

模型输出 JSON 后，不能直接相信。

推荐流程：

```text
模型输出 JSON 字符串
-> json.loads() 解析成 dict
-> Pydantic model_validate() 校验字段和值
-> 得到可控的数据对象
```

Pydantic 可以检查：

```text
字段是否存在
字段类型是否正确
字段值是否在允许范围内
```

### JSON 修复与重试

模型可能输出不合法 JSON，例如：

```text
缺少括号
字段名不一致
输出 Markdown 包裹 JSON
混入解释文字
```

处理流程：

```text
先 json.loads()
如果成功，直接使用
如果失败，调用修复 prompt
修复后再次 json.loads()
如果仍失败，继续 retry 或抛出异常
```

### Prompt 评测

Prompt 不能只看单次效果，需要用固定测试集评测。

本项目记录：

```text
准确率
格式正确率
失败原因
```

Prompt 评测的价值：

```text
发现边界样例
定位失败原因
对比不同 prompt 的稳定性
避免只凭一次输出判断效果
```

## 本阶段结论

```text
写 prompt 是第一步。
结构化输出是第二步。
校验和修复是第三步。
评测 prompt 才能知道它是否稳定。
```

这个项目为后续 RAG、Agent、工具调用打基础，因为 Agent 需要稳定地识别用户意图、选择工具、生成工具参数，并处理失败输出。
