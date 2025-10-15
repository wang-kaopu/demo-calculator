# -*- coding: utf-8 -*-
import random
from fractions import Fraction
from src.utils import format_fraction, normalize_expr

OPS = ['+', '-', '×', '÷']

def random_number(r):
	"""随机生成自然数或真分数，范围[0, r)"""
	if random.random() < 0.5:
		# 自然数
		return random.randint(0, r-1)
	else:
		# 真分数
		denominator = random.randint(2, r-1) if r > 2 else 2
		numerator = random.randint(1, denominator-1)
		integer = random.randint(0, r//2) if random.random() < 0.3 and r > 3 else 0
		if integer:
			return Fraction(integer * denominator + numerator, denominator)
		else:
			return Fraction(numerator, denominator)

def random_expr(r, max_ops=3):
	"""递归生成表达式，最多max_ops个运算符"""
	if max_ops == 0:
		return random_number(r)
	op = random.choice(OPS)
	if op in ['+', '×']:
		# 交换律，左右对称
		left_ops = random.randint(0, max_ops-1)
		right_ops = max_ops-1 - left_ops
	else:
		# 非交换律，左结合
		left_ops = max_ops-1
		right_ops = 0
	left = random_expr(r, left_ops)
	right = random_expr(r, right_ops)
	return (op, left, right)

def eval_expr(expr):
	"""递归计算表达式的值，返回Fraction"""
	if isinstance(expr, Fraction) or isinstance(expr, int):
		return Fraction(expr)
	op, left, right = expr
	l = eval_expr(left)
	r = eval_expr(right)
	if op == '+':
		return l + r
	elif op == '-':
		if l < r:
			raise ValueError('负数')
		return l - r
	elif op == '×':
		return l * r
	elif op == '÷':
		if r == 0:
			raise ValueError('除零')
		res = l / r
		if res.numerator >= res.denominator:
			raise ValueError('除法结果非真分数')
		return res

def expr_to_str(expr):
	"""表达式转字符串，带括号"""
	if isinstance(expr, Fraction) or isinstance(expr, int):
		return format_fraction(Fraction(expr))
	op, left, right = expr
	left_str = expr_to_str(left)
	right_str = expr_to_str(right)
	# 括号处理
	if isinstance(left, tuple):
		left_str = f'({left_str})'
	if isinstance(right, tuple):
		right_str = f'({right_str})'
	return f'{left_str} {op} {right_str}'

def generate(n, r):
	"""
	生成n道四则运算题目，数值范围[0, r)，并写入Exercises.txt和Answers.txt。
	"""
	questions = []
	answers = []
	expr_set = set()
	tries = 0
	while len(questions) < n and tries < n * 20:
		tries += 1
		try:
			ops = random.randint(1, 3)
			expr = random_expr(r, ops)
			val = eval_expr(expr)
			# 结果不能为负数，除法结果为真分数
			if val < 0:
				continue
			expr_str = expr_to_str(expr)
			norm = normalize_expr(expr_str)
			if norm in expr_set:
				continue
			expr_set.add(norm)
			questions.append(expr_str + ' =')
			answers.append(format_fraction(val))
		except Exception:
			continue
	# 写入文件
	with open('Exercises.txt', 'w', encoding='utf-8') as f:
		for q in questions:
			f.write(q + '\n')
	with open('Answers.txt', 'w', encoding='utf-8') as f:
		for a in answers:
			f.write(a + '\n')
	print(f"已生成{len(questions)}道题，写入Exercises.txt和Answers.txt")
