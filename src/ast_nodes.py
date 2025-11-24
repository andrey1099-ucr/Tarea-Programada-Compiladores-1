from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Any


class Node:
    """Base AST node."""

    def print(self):
        """Debug helper to pretty-print this node."""
        print(self)


# ---------- Basic value/identifier nodes ----------


@dataclass
class Program(Node):
    body: List[Node] = field(default_factory=list)


@dataclass
class Name(Node):
    id: str


@dataclass
class Constant(Node):
    value: Any


# ---------- Parameters, functions, classes ----------


@dataclass
class Param(Node):
    """Function parameter. If default is None, it is required."""

    name: Name
    default: Optional[Node] = None


@dataclass
class Assign(Node):
    target: Node
    op: str  # '=', 'PLUS_EQUAL', etc.
    value: Node


@dataclass
class Return(Node):
    value: Optional[Node] = None


@dataclass
class Pass(Node):
    pass


@dataclass
class Break(Node):
    pass


@dataclass
class Continue(Node):
    pass


@dataclass
class If(Node):
    condition: Node
    body: List[Node] = field(default_factory=list)
    elifs: List["ElifClause"] = field(default_factory=list)
    orelse: List[Node] = field(default_factory=list)


@dataclass
class ElifClause(Node):
    condition: Node
    body: List[Node] = field(default_factory=list)


@dataclass
class While(Node):
    condition: Node
    body: List[Node] = field(default_factory=list)


@dataclass
class For(Node):
    target: Name
    iterable: Node
    body: List[Node] = field(default_factory=list)


@dataclass
class ClassDef(Node):
    """Python-like class definition with optional inheritance."""

    name: Name
    bases: List[Name] = field(default_factory=list)
    body: List[Node] = field(default_factory=list)


@dataclass
class FunctionDef(Node):
    name: Name
    params: List[Param] = field(default_factory=list)
    body: List[Node] = field(default_factory=list)


# ---------- Expressions ----------


@dataclass
class BinaryOp(Node):
    op: str  # 'ADD', 'MINUS', 'EQUAL_EQUAL', 'OR', etc.
    left: Node
    right: Node


@dataclass
class UnaryOp(Node):
    op: str  # 'NOT', unary minus, etc.
    operand: Node


@dataclass
class Call(Node):
    func: Node
    args: List[Node] = field(default_factory=list)


@dataclass
class Attribute(Node):
    value: Node
    attr: Name


@dataclass
class Index(Node):
    """Represents value[index], e.g. a[0] or a[i]."""

    value: Node
    index: Node


@dataclass
class ListLiteral(Node):
    elements: List[Node] = field(default_factory=list)


@dataclass
class TupleLiteral(Node):
    elements: List[Node] = field(default_factory=list)


@dataclass
class KeyValue(Node):
    key: Node
    value: Node


@dataclass
class DictLiteral(Node):
    pairs: List[KeyValue] = field(default_factory=list)
