# -*- coding: utf-8 -*-
from src.utils import parse_fraction, format_fraction

def grade(exercise_file, answer_file):
	"""
	判定答案文件中的对错并输出统计结果到Grade.txt。
	"""
	# 读取标准答案
	with open('Answers.txt', 'r', encoding='utf-8') as f:
		std_answers = [line.strip() for line in f if line.strip()]
	# 读取用户答案
	with open(answer_file, 'r', encoding='utf-8') as f:
		user_answers = [line.strip() for line in f if line.strip()]
	correct = []
	wrong = []
	for idx, (std, user) in enumerate(zip(std_answers, user_answers), 1):
		try:
			if parse_fraction(std) == parse_fraction(user):
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
