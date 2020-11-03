import tkinter as tk
from tkinter import messagebox
import pickle

windows = tk.Tk()
windows.title('Welcome to you')
windows.geometry('450x300')

# welcom 界面
canvas = tk.Canvas(windows,height=200,width=500)
image_file = tk.PhotoImage(file='pictures/welcome.gif')
image = canvas.create_image(0,0,anchor='nw',image=image_file)
canvas.pack(side='top')

# user information
tk.Label(windows,text='User name:').place(x=50,y=150)
tk.Label(windows,text='Password:').place(x=50,y=190)

var_usr_name = tk.StringVar()
var_usr_name.set('example@python.com')
entry_usr_name = tk.Entry(windows,textvariable=var_usr_name)
entry_usr_name.place(x=160,y=150)
var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(windows,textvariable=var_usr_pwd,show='*')
entry_usr_pwd.place(x=160,y=190)

# login and sign up button
def usr_login():
    # 触发usr_login
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()

    try:
        with open('usrs_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        # 在没有读取到文件时，程序会创建该文件并将用户名和密码写入
        with open('usrs_info.pickle', 'wb') as usr_file:
            usrs_info = {'admin': 'admin'}  # 用户名为admin，密码为admin
            pickle.dump(usrs_info, usr_file)

    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            tk.messagebox.showinfo(title='Welcome', message='How are you?' + usr_name)
            windows.destroy()
        else:
            tk.messagebox.showerror(message='Error, your password is wrong, try again.')
    else:
        is_sign_up = tk.messagebox.askyesno('Welcom', 'You have not sign up yet.Sign up today?')
        if is_sign_up:
            usr_sign_up()

def usr_sign_up():
    def sign_to_Mofan_Python():
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        nn = new_name.get()

        with open('usrs_info.pickle','rb') as usr_file:
            exist_usr_info = pickle.load(usr_file)

        if np!=npf:
            tk.messagebox.showerror('Error','Password and confirm password must be the same')
        elif nn in exist_usr_info:
            tk.messagebox.showerror('Error','The user has already signed up!')
        else:
            exist_usr_info[nn] = np
            with open('usrs_info.pickle','wb') as usr_file:
                pickle.dump(exist_usr_info,usr_file)
            tk.messagebox.showinfo('Welcome','You have successfuly signed up!')

            window_sign_up.destroy()

    # usr_sign_up界面
    window_sign_up = tk.Toplevel(windows)
    window_sign_up.geometry('350x250')
    window_sign_up.title('Sign up window')

    new_name = tk.StringVar()
    new_name.set('example@python.com')
    tk.Label(window_sign_up, text='User name:').place(x=10, y=10)
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)
    entry_new_name.place(x=150, y=10)

    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='Password:').place(x=10, y=50)
    entry_user_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_user_pwd.place(x=150, y=50)

    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='Confirm password:').place(x=10, y=90)
    entry_user_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_user_pwd_confirm.place(x=150, y=90)

    btn_confirm_sign_up = tk.Button(window_sign_up, text='Sign up', command=sign_to_Mofan_Python)
    btn_confirm_sign_up.place(x=150, y=130)



btn_login = tk.Button(windows,text='Login',command=usr_login)
btn_login.place(x=170,y=230)
btn_sign_up = tk.Button(windows,text='Sign up',command=usr_sign_up)
btn_sign_up.place(x=270,y=230)

windows.mainloop()