import logging #导入 Python 标准日志库。


def setup_logging() -> None: #定义一个函数，用来初始化日志配置。
    logging.basicConfig( #设置全局日志格式。
        level=logging.INFO, #表示记录 INFO 及以上级别日志：
        format="%(asctime)s %(levelname)s %(name)s %(message)s", #表示日志显示格式：时间 级别 logger名字 日志内容
    )