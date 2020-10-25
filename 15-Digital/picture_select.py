import tkinter as tk
from tkinter.filedialog import askdirectory,askopenfilename
from run_game import *
import usr_login as ul

windows = tk.Tk()
windows.title("选择一张图片")
windows.geometry('280x200')

def select_path():
    path = askopenfilename(title='选择一个图片',
                           initialdir='/',filetypes=[('Pictures source file','*.jpeg')])
    src_picture.set(path)
    windows.destroy()

src_picture = tk.StringVar()
tk.Label(windows,text='图片路径：').grid(row=0,column=0)
entry_src_picture = tk.Entry(windows,textvariable=src_picture)
entry_src_picture.grid(row=0,column=1)
tk.Button(windows,text = "路径选择",command=select_path).grid(row=0,column=2)
windows.mainloop()

src = src_picture.get()
if image(src)==None:
    run_game()