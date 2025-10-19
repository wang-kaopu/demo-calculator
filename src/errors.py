# -*- coding: utf-8 -*-
"""
自定义异常模块：定义项目中使用的异常类型。

异常层次：
- CalculatorError: 基类
- RuleViolationError: 规则检查失败（例如题目规则不满足）
- ExpressionParseError: 表达式解析失败
- FileOperationError: 文件读写错误封装
- ParameterValidationError: 参数验证失败（非法的 n/r/输入）
"""
from typing import Optional


class CalculatorError(Exception):
    """所有自定义异常的基类。"""
    pass


class RuleViolationError(CalculatorError):
    """当生成或判题时发现题目违反规则（例如负数、不符合真分数约束等）。"""
    pass


class ExpressionParseError(CalculatorError):
    """当解析表达式字符串失败时抛出，携带可选的位置信息或原始文本。"""
    def __init__(self, message: str, text: Optional[str] = None):
        super().__init__(message)
        self.text = text


class FileOperationError(CalculatorError):
    """封装文件 I/O 的错误，例如文件不存在或权限不足。"""
    def __init__(self, message: str, path: Optional[str] = None):
        super().__init__(message)
        self.path = path


class ParameterValidationError(CalculatorError):
    """当函数接收到不合法参数时抛出。"""
    pass
