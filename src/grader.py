# -*- coding: utf-8 -*-
from src.utils import parse_fraction, format_fraction, parse_expression
from src.generator import eval_expr
from src.errors import FileOperationError, ExpressionParseError

import logging

def grade(exercise_file, answer_file):
	"""
	判定答案文件中的对错并输出统计结果到Grade.txt。
	"""
	# 读取题目与用户答案，捕获文件 I/O 错误并包装
	try:
		with open(exercise_file, 'r', encoding='utf-8') as f:
			exercises = [line.strip() for line in f if line.strip()]
	except FileNotFoundError as e:
		raise FileOperationError('读取题目文件失败，文件不存在', path=exercise_file)
	except PermissionError as e:
		raise FileOperationError('读取题目文件失败，权限被拒绝', path=exercise_file)

	try:
		with open(answer_file, 'r', encoding='utf-8') as f:
			user_answers = [line.strip() for line in f if line.strip()]
	except FileNotFoundError as e:
		raise FileOperationError('读取答案文件失败，文件不存在', path=answer_file)
	except PermissionError as e:
		raise FileOperationError('读取答案文件失败，权限被拒绝', path=answer_file)
	correct = []
	wrong = []
	for idx, (ex_line, user) in enumerate(zip(exercises, user_answers), 1):
		try:
			# 去掉末尾等号和空格
			expr_text = ex_line.rstrip().rstrip('=')
			try:
				tree = parse_expression(expr_text)
			except ExpressionParseError as e:
				logging.debug(f'表达式解析失败，第%d题: %s; 错误: %s', idx, expr_text, e)
				wrong.append(idx)
				continue
			std_val = eval_expr(tree)
			try:
				user_val = parse_fraction(user)
			except Exception:
				# 用户答案无法解析为分数，判为错误
				wrong.append(idx)
				continue
			if user_val == std_val:
				correct.append(idx)
			else:
				wrong.append(idx)
		except Exception as e:
			logging.exception('判题时发生未处理异常')
			wrong.append(idx)
	# 输出统计
	try:
		with open('Grade.txt', 'w', encoding='utf-8') as f:
			f.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
			f.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")
	except Exception as e:
		raise FileOperationError('写入 Grade.txt 失败', path='Grade.txt')
	print(f"判题完成，正确{len(correct)}题，错误{len(wrong)}题，结果写入Grade.txt")
