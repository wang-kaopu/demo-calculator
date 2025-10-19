# demo-calculator

小学四则运算题目生成与判题程序

运行示例：

生成题目：

```powershell
python Myapp.py -n 10 -r 10
```

判题：

```powershell
python Myapp.py -e Exercises.txt -a Answers.txt
```

打包为单文件 exe（Windows，已安装 Python 环境）:

```powershell
python -m pip install -r requirements.txt
pyinstaller --onefile Myapp.py
# 生成的可执行文件在 dist\\Myapp.exe
```