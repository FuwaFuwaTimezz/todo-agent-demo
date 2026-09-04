"""Todo 数据模型。"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Todo:
    """一条待办事项。

    Attributes:
        id: 唯一标识，由 TodoStore 自增分配。
        title: 待办内容。
        done: 是否已完成，默认 False。
        created_at: 创建时间。
    """

    id: int
    title: str
    done: bool = False
    created_at: datetime = field(default_factory=datetime.now)
