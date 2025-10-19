# -*- coding: utf-8 -*-
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
from fractions import Fraction
import re

def parse_fraction(s):
	"""
	字符串转Fraction对象，支持2'3/5、3/5、2等格式。
	"""
	s = s.strip()
	if "'" in s:
		integer, frac = s.split("'")
		num, den = frac.split('/')
		return Fraction(int(integer)) + Fraction(int(num), int(den))
	elif '/' in s:
		num, den = s.split('/')
		return Fraction(int(num), int(den))
	else:
		return Fraction(int(s))


def tokenize(expr):
	"""将表达式字符串分解为 token 列表。"""
	token_spec = [
		('NUMBER', r"\d+'\d+/\d+|\d+/\d+|\d+"),
		('OP', r"[+\-×÷]"),
		('LPAREN', r"\("),
		('RPAREN', r"\)"),
		('SKIP', r"\s+"),
	]
	tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_spec)
	for mo in re.finditer(tok_regex, expr):
		kind = mo.lastgroup
		value = mo.group()
		if kind == 'SKIP':
			continue
		yield (kind, value)


def parse_expression(s):
	"""
	将表达式字符串解析成表达式树，节点形式为 (op, left, right)，数字为 Fraction。
	支持操作符 + - × ÷，括号，以及真分数格式（2'3/5）。
	优先级：× ÷ 高于 + -，均为左结合。
	"""
	tokens = list(tokenize(s))
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
		raise ValueError('Unexpected token in factor: %s' % (peek(),))

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
	# 如果还有剩余 token，可能是末尾的 '=' 或其他，忽略非数字/ops
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
