# ChangeKit
Change是一个系列，包含修改环境的一系列程序，每个软件使用方法完全一样
# 统一pyinstaller打包指令
```
pyinstaller --onefile --noconsole 文件名.py
```
## ChangeJava
一个用于更改Java环境的小工具

放置所有Java的安装目录下，程序会自动识别所有Java
#### pyinstaller打包指令
```
pyinstaller --onefile --noconsole ChangeJava.py
```
#### Fix
- [x] 修复无法永久修改环境变量的问题

## ChangeNet
一个用于更改.Net环境的小工具

放置所有.Net的安装目录下，程序会自动识别所有.Net
#### pyinstaller打包指令
```
pyinstaller --onefile --noconsole ChangeNet.py
```
