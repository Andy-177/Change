import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
import sys
import subprocess

def run_as_admin(command):
    """以管理员身份运行指定的 CMD 命令"""
    try:
        subprocess.run(
            f"powershell Start-Process -FilePath 'cmd.exe' -ArgumentList '/c {command}' -Verb RunAs",
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except subprocess.CalledProcessError as e:
        messagebox.showerror("错误", f"命令执行失败: {e.stderr}")
    except Exception as e:
        messagebox.showerror("错误", f"发生未知错误: {str(e)}")

def get_base_path():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(os.path.realpath(sys.executable))
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return base_path

def check_dotnet():
    """检查当前目录下的 .NET 环境（仅检查根目录下是否有 dotnet.exe）"""
    base_path = get_base_path()
    all_folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    dotnet_marker_file = "dotnet.exe"
    dotnet_folders = []

    for folder in all_folders:
        folder_path = os.path.join(base_path, folder)
        marker_path = os.path.join(folder_path, dotnet_marker_file)
        if os.path.exists(marker_path):
            dotnet_folders.append(folder_path)

    return dotnet_folders

def set_dotnet_root(dotnet_path):
    if dotnet_path:
        run_as_admin(f"setx /M DOTNET_ROOT \"{dotnet_path}\"")
        messagebox.showinfo("更改完成", f"已更改 .NET 环境为\n{dotnet_path}\n\n请重新打开命令行或IDE使设置生效。")
    else:
        messagebox.showwarning("未选择 .NET", "未选择 .NET 环境，请选择一个 .NET 版本")

def get_selected_dotnet():
    selected_dotnet = dropdown.get()
    if selected_dotnet:
        set_dotnet_root(selected_dotnet)
    else:
        messagebox.showwarning("未选择 .NET", "未选择 .NET 环境，请选择一个 .NET 版本")

# 设置工作目录
os.chdir(get_base_path())

# --- UI 布局 ---
Window = tk.Tk()
style = ttk.Style()
style.theme_use("clam")
Window.title(".NET 环境切换")
Window.geometry("400x220")

# 禁止窗口最大化
Window.resizable(False, False)  # 第一个参数控制宽度是否可调整，第二个参数控制高度是否可调整

# 添加标题
title = tk.Label(Window, text="请选择 .NET 环境", font=("Arial", 16, "bold"))
title.pack(pady=(20, 5))

# 检测 .NET 环境
dotnet_versions = check_dotnet()

# 如果没有检测到任何环境，给出提示
if not dotnet_versions:
    no_env_label = ttk.Label(Window, text="未检测到任何 .NET 环境。\n请将 .NET 版本文件夹放在此程序目录下。", foreground="red")
    no_env_label.pack(pady=20)
else:
    # 创建下拉菜单
    dropdown = ttk.Combobox(Window, values=dotnet_versions, width=50, state="readonly")
    dropdown.pack(pady=10, padx=40)

    # 默认选择第一个
    dropdown.current(0)

    # 创建按钮
    change_button = ttk.Button(Window, text="更改 .NET 环境", command=get_selected_dotnet)
    change_button.pack(pady=(30, 20))

# 启动主循环
Window.mainloop()