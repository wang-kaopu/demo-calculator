# -*- coding: utf-8 -*-
from fractions import Fraction
import re
from .errors import ExpressionParseError, ParameterValidationError


def format_fraction(frac):
	"""
	将Fraction对象格式化为真分数字符串，如3/5，2'3/8。
	"""
	if frac.denominator == 1:
		return str(frac.numerator)
	elif abs(frac.numerator) > frac.denominator:
		# 带整数部分的真分数
		integer = frac.numerator // frac.denominator
		remainder = abs(frac.numerator) % frac.denominator
		return f"{integer}'{remainder}/{frac.denominator}"
	else:
		return f"{frac.numerator}/{frac.denominator}"


def normalize_expr(expr):
	"""
	表达式规范化（用于去重），支持交换律和结合律。
	输入为表达式树（tuple/int/Fraction），输出为唯一字符串。
	"""
	def tree_key(e):
		if isinstance(e, (int, Fraction)):
			return str(Fraction(e))
		op, left, right = e
		# 交换律处理：+ ×
		if op in ['+', '×']:
			left_key = tree_key(left)
			right_key = tree_key(right)
			# 按字典序排列
			children = sorted([left_key, right_key])
			return f"{op}({children[0]},{children[1]})"
		else:
			return f"{op}({tree_key(left)},{tree_key(right)})"
	return tree_key(expr)


# 新增分数处理相关工具


def parse_fraction(s):
	"""
	字符串转Fraction对象，支持2'3/5、3/5、2等格式。
	在无法解析时抛出 ExpressionParseError 。
	"""
	if s is None:
		raise ExpressionParseError('空字符串不能解析为分数', text=str(s))
	ss = s.strip()
	try:
		if "'" in ss:
			parts = ss.split("'")
			if len(parts) != 2:
				raise ValueError('带整数部分的分数格式错误')
			integer, frac = parts
			num, den = frac.split('/')
			return Fraction(int(integer)) + Fraction(int(num), int(den))
		elif '/' in ss:
			num, den = ss.split('/')
			return Fraction(int(num), int(den))
		else:
			return Fraction(int(ss))
	except ValueError as e:
		raise ExpressionParseError(f'无法解析分数: {e}', text=s)


def tokenize(expr):
	"""
	将表达式字符串分解为 token 列表。
	在遇到无法匹配的字符时会触发 ExpressionParseError。
	"""
	if expr is None:
		raise ExpressionParseError('表达式为空', text=str(expr))
	token_spec = [
		('NUMBER', r"\d+'\d+/\d+|\d+/\d+|\d+"),
		('OP', r"[+\-×÷]"),
		('LPAREN', r"\("),
		('RPAREN', r"\)"),
		('SKIP', r"\s+"),
	]
	tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_spec)
	pos = 0
	for mo in re.finditer(tok_regex, expr):
		kind = mo.lastgroup
		value = mo.group()
		start = mo.start()
		if start != pos:
			# 说明有无法识别的字符
			raise ExpressionParseError(f'在位置 {pos} 发现无法识别的字符: {expr[pos:start]}', text=expr)
		pos = mo.end()
		if kind == 'SKIP':
			continue
		yield (kind, value)
	if pos != len(expr):
		# 尾部仍有无法识别字符
		raise ExpressionParseError(f'在位置 {pos} 发现无法识别的字符: {expr[pos:]}', text=expr)


def parse_expression(s):
	"""
	将表达式字符串解析成表达式树，遇到解析问题抛出 ExpressionParseError。
	"""
	try:
		tokens = list(tokenize(s))
	except ExpressionParseError:
		raise
	except Exception as e:
		raise ExpressionParseError(f'词法分析失败: {e}', text=s)

	pos = 0

	def peek():
		return tokens[pos] if pos < len(tokens) else (None, None)

	def consume(expected_kind=None):
		nonlocal pos
		if pos < len(tokens):
			tok = tokens[pos]
			pos += 1
			return tok
		return (None, None)

	def parse_factor():
		kind, val = peek()
		if kind == 'NUMBER':
			consume('NUMBER')
			return parse_fraction(val)
		if kind == 'LPAREN':
			consume('LPAREN')
			node = parse_expr()
			if peek()[0] == 'RPAREN':
				consume('RPAREN')
				return node
			raise ExpressionParseError('缺失右括号', text=s)
		raise ExpressionParseError(f'Unexpected token in factor: {peek()}', text=s)

	def parse_term():
		node = parse_factor()
		while True:
			kind, val = peek()
			if kind == 'OP' and val in ('×', '÷'):
				consume('OP')
				right = parse_factor()
				node = (val, node, right)
				continue
			break
		return node

	def parse_expr():
		node = parse_term()
		while True:
			kind, val = peek()
			if kind == 'OP' and val in ('+', '-'):
				consume('OP')
				right = parse_term()
				node = (val, node, right)
				continue
			break
		return node

	tree = parse_expr()
	return tree


def is_proper_fraction(frac):
	"""
	判断是否为真分数（分子小于分母，且为正分数）
	"""
	frac = Fraction(frac)
	return 0 < abs(frac.numerator) < frac.denominator


def fraction_add(a, b):
	return Fraction(a) + Fraction(b)


def fraction_sub(a, b):
	return Fraction(a) - Fraction(b)


def fraction_mul(a, b):
	return Fraction(a) * Fraction(b)


def fraction_div(a, b):
	if Fraction(b) == 0:
		raise ZeroDivisionError('分母为零')
	return Fraction(a) / Fraction(b)
