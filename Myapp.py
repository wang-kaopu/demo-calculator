# -*- coding: utf-8 -*-
import argparse
import sys
from src import generator, grader

def main():
	parser = argparse.ArgumentParser(description='小学四则运算题目生成与判题程序')
	parser.add_argument('-n', type=int, help='生成题目的数量')
	parser.add_argument('-r', type=int, help='题目中数值的范围（不包括该值）')
	parser.add_argument('-e', type=str, help='题目文件路径')
	parser.add_argument('-a', type=str, help='答案文件路径')
	args = parser.parse_args()

	# 判题模式
	if args.e and args.a:
		grader.grade(args.e, args.a)
		return

	# 题目生成模式
	if args.n is not None and args.r is not None:
		generator.generate(args.n, args.r)
		return

	# 参数不足，输出帮助
	parser.print_help()
	sys.exit(1)

if __name__ == '__main__':
	main()
