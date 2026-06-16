# 2026-06-04 Python Advanced Basics

这个目录是 Python 进阶语法练习，重点学习装饰器和上下文管理器。

这两个概念后续会在 FastAPI、数据库连接、日志、测试和 Agent 工具封装中反复出现。

## 学习目标

- 理解装饰器的基本结构
- 使用 `*args` 和 `**kwargs` 包装函数调用
- 使用 `functools.wraps` 保留原函数信息
- 实现日志装饰器和计时装饰器
- 理解上下文管理器的 `__enter__` 和 `__exit__`
- 理解 `with` 语句如何自动管理资源

## 项目结构

```text
2026-06-04-study/
├── context_manager_demo.py
├── decorator_demo.py
└── README.md
```

## 核心文件

### `decorator_demo.py`

这个文件练习装饰器。

实现了两个装饰器：

- `log_call`
- `timer`

`log_call` 用来记录函数调用信息：

```text
函数名
位置参数
关键字参数
返回值
```

`timer` 用来记录函数执行耗时。

练习中还把两个装饰器叠加使用：

```python
@log_call
@timer
def create_task(...):
    ...
```

这有助于理解装饰器如何包装原函数，以及多个装饰器的执行顺序。

### `context_manager_demo.py`

这个文件练习上下文管理器。

实现了两个类：

- `FileManager`
- `DatabaseConnection`

`FileManager` 模拟文件打开和关闭：

```python
with FileManager("demo.txt", "w") as file:
    file.write("hello context manager")
```

`DatabaseConnection` 模拟数据库连接和关闭：

```python
with DatabaseConnection("task_db") as db:
    result = db.query("select * from tasks")
```

重点理解：

```text
__enter__
进入 with 代码块时执行

__exit__
离开 with 代码块时执行
```

## 运行方式

在本目录执行：

```bash
../.venv/bin/python decorator_demo.py
```

或者：

```bash
../.venv/bin/python context_manager_demo.py
```

## 和后续学习的关系

装饰器后续会帮助理解：

- FastAPI 路由装饰器
- 日志包装
- 权限校验
- 计时统计
- 工具函数增强

上下文管理器后续会帮助理解：

- 文件读写
- 数据库连接
- SQLAlchemy session 生命周期
- 测试资源清理

## 一句话总结

这个练习通过装饰器和上下文管理器，理解 Python 如何在不改变核心业务代码的情况下，增加日志、计时和资源自动管理能力。
