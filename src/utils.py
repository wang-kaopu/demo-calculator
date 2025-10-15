# -*- coding: utf-8 -*-
from fractions import Fraction

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
	表达式规范化（用于去重），如交换律、括号等。
	这里只做简单字符串排序，复杂情况可用表达式树。
	"""
	# TODO: 可扩展为表达式树的规范化
	return ''.join(sorted(expr.replace(' ', '')))
