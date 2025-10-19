# -*- coding: utf-8 -*-
import argparse
import sys
import logging
from src import generator, grader
from src.errors import (
	CalculatorError,
	FileOperationError,
	ExpressionParseError,
	ParameterValidationError,
)

def main():
	# 简单日志配置
	logging.basicConfig(level=logging.INFO)

	parser = argparse.ArgumentParser(description='小学四则运算题目生成与判题程序')
	parser.add_argument('-n', type=int, help='生成题目的数量')
	parser.add_argument('-r', type=int, help='题目中数值的范围（不包括该值）')
	parser.add_argument('-e', type=str, help='题目文件路径')
	parser.add_argument('-a', type=str, help='答案文件路径')
	try:
		args = parser.parse_args()
	except SystemExit:
		raise
	except Exception as e:
		print(f"解析参数时发生错误: {e}", file=sys.stderr)
		sys.exit(1)

	# 判题模式 / 题目生成模式放在同一异常处理块中
	try:
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
	except FileOperationError as e:
		print(f"文件操作失败: {e} 路径={getattr(e, 'path', None)}", file=sys.stderr)
		logging.exception('文件操作失败')
		sys.exit(2)
	except ParameterValidationError as e:
		print(f"参数校验失败: {e}", file=sys.stderr)
		sys.exit(3)
	except ExpressionParseError as e:
		print(f"表达式解析失败: {e}", file=sys.stderr)
		sys.exit(4)
	except CalculatorError as e:
		print(f"处理失败: {e}", file=sys.stderr)
		logging.exception('处理失败')
		sys.exit(5)
	except Exception as e:
		print(f"发生未知错误: {e}", file=sys.stderr)
		logging.exception('未知错误')
		sys.exit(99)

if __name__ == '__main__':
	main()
