# -*- coding: utf-8 -*-
from src.utils import parse_fraction, format_fraction, parse_expression
from src.generator import eval_expr

def grade(exercise_file, answer_file):
	"""
	判定答案文件中的对错并输出统计结果到Grade.txt。
	"""
	# 读取题目与用户答案
	with open(exercise_file, 'r', encoding='utf-8') as f:
		exercises = [line.strip() for line in f if line.strip()]
	with open(answer_file, 'r', encoding='utf-8') as f:
		user_answers = [line.strip() for line in f if line.strip()]
	correct = []
	wrong = []
	for idx, (ex_line, user) in enumerate(zip(exercises, user_answers), 1):
		try:
			# 去掉末尾等号和空格
			expr_text = ex_line.rstrip().rstrip('=')
			tree = parse_expression(expr_text)
			std_val = eval_expr(tree)
			if parse_fraction(user) == std_val:
				correct.append(idx)
			else:
				wrong.append(idx)
		except Exception:
			wrong.append(idx)
	# 输出统计
	with open('Grade.txt', 'w', encoding='utf-8') as f:
		f.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
		f.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")
	print(f"判题完成，正确{len(correct)}题，错误{len(wrong)}题，结果写入Grade.txt")
