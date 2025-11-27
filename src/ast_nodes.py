from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Any


# Base class:
class Node:
    """Base AST node."""

    def print(self):
        """Debug helper to pretty-print this node."""
        print(self)


# Basic identifiers:

@dataclass
class Program(Node):
    body: List[Node] = field(default_factory=list)

@dataclass
class Name(Node):
    id: str

@dataclass
class Constant(Node):
    value: Any


# Parameters:
@dataclass
class Param(Node):
    name: Name
    default: Optional[Node] = None


# All assign types:
@dataclass
class Assign(Node):
    target: Node
    op: str  # =, +=...
    value: Node


# Reserved words:

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

# If clause:
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


# Loops:

@dataclass
class While(Node):
    condition: Node
    body: List[Node] = field(default_factory=list)

@dataclass
class For(Node):
    target: Name
    iterable: Node
    body: List[Node] = field(default_factory=list)


# Definitions:

@dataclass
class ClassDef(Node): # Not used
    name: Name
    bases: List[Name] = field(default_factory=list)
    body: List[Node] = field(default_factory=list)

@dataclass
class FunctionDef(Node):
    name: Name
    params: List[Param] = field(default_factory=list)
    body: List[Node] = field(default_factory=list)


# Expressions:

@dataclass
class BinaryOp(Node):
    op: str  # +, -, ==, or...
    left: Node
    right: Node

@dataclass
class UnaryOp(Node):
    op: str  # NOT, unary minus...
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
class Index(Node): # value[index]
    value: Node
    index: Node

@dataclass
class ListLiteral(Node): # [1, 2, 3]
    elements: List[Node] = field(default_factory=list)


@dataclass
class TupleLiteral(Node): # (1, 2, 3)
    elements: List[Node] = field(default_factory=list)


@dataclass
class KeyValue(Node): # "key1" : "FrontDoor"
    key: Node
    value: Node

@dataclass
class DictLiteral(Node):
    pairs: List[KeyValue] = field(default_factory=list)
