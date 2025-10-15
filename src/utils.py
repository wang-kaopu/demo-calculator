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
	表达式规范化（用于去重），如交换律、括号等。
	这里只做简单字符串排序，复杂情况可用表达式树。
	"""
	# TODO: 可扩展为表达式树的规范化
	return ''.join(sorted(expr.replace(' ', '')))

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
