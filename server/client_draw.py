import tkinter
from tkinter import *
from tkinter import messagebox
global gop
gop='g'
def draw_login(self): #登录页面
    self.root.title("聊天室登录页面")  # 给主窗口设置标题内容
    self.root.geometry('450x300') # 设置主窗口大小
    self.canvas = tkinter.Canvas(self.root, height=200, width=500)  # 创建画布
    self.label_account = tkinter.Label(self.root, text='账 号')  # 创建一个`Label`名为`账 号: `
    self.label_password = tkinter.Label(self.root, text='密 码')  # 创建一个`Label`名为`密 码: `
    self.input_account = tkinter.Entry(self.root, width=30)  # 创建一个账号输入框,并设置尺寸
    self.input_password = tkinter.Entry(self.root, show='*', width=30)  # 创建一个密码输入框,并设置尺寸
    self.login_button = tkinter.Button(self.root, command=self.verify_login, text="登 录", width=10) #登录按钮
    self.register_button = tkinter.Button(self.root, command=self.register_interface, text="注 册", width=10) #注册按钮

    # 登录页面各个控件进行布局
    self.label_account.place(x=90, y=70)
    self.label_password.place(x=90, y=150)
    self.input_account.place(x=135, y=70)
    self.input_password.place(x=135, y=150)
    self.login_button.place(x=120, y=235)
    self.register_button.place(x=250, y=235)


def draw_register(self): #注册页面控件创
    self.login_button.destroy()
    self.register_button.destroy()
    self.root.title("聊天室注册页面")
    self.root.geometry('450x300') # 设置主窗口大小
    self.canvas = tkinter.Canvas(self.root, height=200, width=500)  # 创建画布
    self.label_nickname = tkinter.Label(self.root, text='昵 称')  # 创建一个"Label",名为："昵 称"
    self.input_nickname = tkinter.Entry(self.root, width=30)  # 创建一个昵称输入框,并设置尺寸
    self.register_submit_button = tkinter.Button(self.root, command=self.verify_register, text="提交注册", width=10) #创建注册按钮
    self.return_login_button = tkinter.Button(self.root, command=self.return_login_interface, text="返回登录",width=10)  # 创建注册按钮

    # 注册页面各个控件进行布局
    self.label_account.place(x=90, y=70)
    self.label_password.place(x=90, y=130)
    self.input_account.place(x=135, y=70)
    self.input_password.place(x=135, y=130)
    self.label_nickname.place(x=90, y=190)
    self.input_nickname.place(x=135, y=190)
    self.register_submit_button.place(x=120, y=235)
    self.return_login_button.place(x=250, y=235)



def draw_chat(self,nickname,accounts):
    global i
    self.root.title("【%s】的聊天室页面" %nickname)
    self.root.configure(background="white")
    width=1300
    height=700
    screen_width=self.root.winfo_screenwidth()
    screen_height=self.root.winfo_screenheight()
    gm_str = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2,(screen_height - 1.2 * height) / 2)
    self.root.geometry(gm_str)
    self.root.resizable(width=False,height=False)
    self.label1 = tkinter.Label(self.root, text=" 在线用户 python聊天室欢迎您：" + nickname + " "+" ",font=("黑体",20),bg="#00BFFF",fg="white")
    self.label1.grid(row=0, column=0, ipady=0, padx=0, columnspan=3, sticky=E+W)
    friend_list_var=tkinter.StringVar()
    self.friend_list=Listbox(self.root,listvariable=friend_list_var,bg="#F8F8FF", fg="#00BFFF", font=("宋体", 14),highlightcolor="white", selectbackground="#00BFFF")
    self.friend_list.grid(row=1, column=0, rowspan=3, sticky=tkinter.N + tkinter.S, padx=0, pady=(0, 0))
    refresh_friends(self,accounts)
    b = Button(self.root, command=lambda: private_talk(self, nickname), text="切换聊天目标", bg="#00BFFF",
               fg="white", width=13, height=1, font=('黑体', 12), )
    b.place(x=0, y=0)
    self.root.rowconfigure(1,weight=1)
    self.root.columnconfigure(1,weight=1)
    sc_bar = tkinter.Scrollbar(self.root, activebackground='red')
    sc_bar.grid(row=1, column=0, sticky=tkinter.N + tkinter.S + tkinter.E, rowspan=3, pady=(0, 3))
    sc_bar['command']=self.friend_list.yview
    self.friend_list['yscrollcommand'] = sc_bar.set
    msg_sc_bar = tkinter.Scrollbar(self.root)
    msg_sc_bar.grid(row=1, column=1, sticky=tkinter.E + tkinter.N + tkinter.S, padx=(0, 1), pady=1)
    self.message_text = tkinter.Text(self.root, bg="white", height=1,highlightcolor="white", highlightthickness=1)
    self.message_text.config(state=tkinter.DISABLED)
    self.message_text.grid(row=1, column=1, sticky=W + E + N + S, padx=(0, 15), pady=(0, 27))
    msg_sc_bar["command"] = self.message_text.yview
    self.message_text["yscrollcommand"] = msg_sc_bar.set
    send_sc_bar = Scrollbar(self.root)
    send_sc_bar.grid(row=2, column=1, sticky=E + N + S, padx=(0, 1), pady=1)
    self.send_text = Text(self.root, bg="white", height=11, highlightcolor="white",
                          highlightbackground="#444444", highlightthickness=0)
    self.send_text.see(END)
    self.send_text.grid(row=2, column=1, sticky=W + E + N + S, padx=(0, 15), pady=0)
    send_sc_bar["command"] = self.send_text.yview
    self.send_text["yscrollcommand"] = send_sc_bar.set
    self.root.bind("<KeyPress-Return>", self.sendMsgEvent)
    button1 = Button(self.root, command=self.sendMsg, text="发送", bg="#00BFFF",
                     fg="white", width=13, height=2, font=('黑体', 12), )
    button1.place(x=650, y=640)
    button = Button(self.root, command=self.sendFile, text="发送文件", bg="#00BFFF",
                     fg="white", width=13, height=2, font=('黑体', 12), )
    button.place(x=770, y=640)
    button4 = Button(self.root, command=self.audiocom, text="语音通话", bg="#00BFFF",
                     fg="white", width=13, height=2, font=('黑体', 12), )
    button4.place(x=890, y=640)
    button2 = Button(self.root, text="关闭", bg="white", fg="black", width=13, height=2,
                     font=('黑体', 12), command=self.on_closing)
    button2.place(x=530, y=640)
    self.root.protocol('WM_DELETE_WINDOW', self.on_closing)

def private_talk(self,nickname):
    global chat_user  # 生命全局变量，方便再其他函数中使用
    global gop
    indexs = self.friend_list.curselection()
    index = indexs[0]
    if index > 0:
        chat_user = self.friend_list.get(index)
        if chat_user == '【群聊】':
            title = " 在线用户 python聊天室欢迎您：" + nickname + " " + \
                    " "
            change_title(self,title)
            gop = 'g'
        elif chat_user =='在线好友列表:':
            messagebox.showwarning(title="提示", message="不能点击此栏目!")
        elif chat_user =='离线好友列表:':
            messagebox.showwarning(title="提示", message="不能点击此栏目!")
        elif chat_user == nickname:
            messagebox.showwarning(title="提示", message="自己不能和自己进行对话!")
            chat_user = '【群聊】'  # 把聊天对象改为群聊
        else:  # 否则改为下面标题
            title = " " + nickname + " 私聊 -> " + chat_user + \
                    " "
            change_title(self,title)
            gop=chat_user

def refresh_friends(self, accounts):
    self.friend_list.delete(0, END)
    self.friend_list.insert(END, "在线好友列表:")
    self.friend_list.insert(END, "【群聊】")
    for account in accounts.keys():
        if accounts[account]=="1":
            self.friend_list.insert(END, account)
    self.friend_list.insert(END, "离线好友列表:")
    for account in accounts.keys():
        if accounts[account]=="0":
            self.friend_list.insert(END, account)
    self.friend_list.itemconfig(0, fg="#00BFFF")

def change_title(self, title):
    self.label1['text'] = title



