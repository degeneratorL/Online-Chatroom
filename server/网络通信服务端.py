import socket
import threading
from socket import *
import tkinter
from tkinter import messagebox
from tkinter import *
import tkinter.font as tf
import json
import time
import client_draw
import tkinter.ttk
import os
import pyaudio
global filestate
global nfilestate
global state,state1
global audioflag
audioflag=1
filestate=1
nfilestate=1
state=1
state1=1
class chat(object):
    acs={}
    def connect(self):
        self.s=socket(AF_INET,SOCK_STREAM)
        self.s.connect(("47.106.178.71",30001))
        return self.s

    def recive(self,s):
        global nfilestate
        while 1:
            data=s.recv(1024).decode('utf-8')
            data_dict=json.loads(data)
            type=data_dict["type"]
            if type=="login":
                if data_dict["code"]=="0000":
                    nickname=data_dict["nickname"]
                    accounts=data_dict["accounts"]
                    accounts=json.loads(accounts)
                    chat.acs=accounts
                    chat.acs[nickname]="1"
                    self.chat_interface(nickname,chat.acs)
                else:
                    tkinter.messagebox.showinfo(title='登录提示',message=data_dict['msg'])
            elif type=="register":
                if data_dict["code"]=="0000":
                    nickname=data_dict["nickname"]
                    accounts = data_dict["accounts"]
                    accounts = json.loads(accounts)
                    chat.acs = accounts
                    tkinter.messagebox.showinfo(title='进入聊天室',message=data_dict['msg'])
                    self.chat_interface(nickname,chat.acs)
                else:
                    tkinter.messagebox.showinfo(title='注册提示', message=data_dict['msg'])
            elif type=="chat":
                message=data_dict["message"]
                nickname=data_dict["nickname"]
                ismy=data_dict["ismy"]
                gop = data_dict["gop"]
                self.message_text.config(state=NORMAL)
                self.message_text.tag_config('DimGray', foreground='#696969', font=("Times", "13"))
                times=" "+nickname+"\t"+time.strftime("%H:%M:%S",time.localtime())+ '\n'
                self.message_text.insert(tkinter.END,times,"DimGray")
                if ismy=="yes":
                    if gop=='g':
                        ft = tf.Font(family='微软雅黑', size=13)
                        self.message_text.tag_config("tag_4", foreground="#00BFFF", font=ft)
                        self.message_text.insert(END, message, 'tag_4')
                    else:
                        ft = tf.Font(family='微软雅黑', size=13)
                        self.message_text.tag_config("tag_5", foreground="#DC143C", font=ft)
                        self.message_text.insert(END, message, 'tag_5')
                else:
                    if gop=='g':
                        ft = tf.Font(family='微软雅黑', size=13)
                        self.message_text.tag_config("tag_6", foreground="#008000", font=ft)
                        self.message_text.insert(END, message, 'tag_6')
                    else:
                        ft = tf.Font(family='微软雅黑', size=13)
                        self.message_text.tag_config("tag_7", foreground="#DC143C", font=ft)
                        self.message_text.insert(END, message, 'tag_7')
                self.message_text.insert(END, "\n")
                self.message_text.config(state=DISABLED)
                self.message_text.see(END)
            elif type == "newcomer":
                nickname=data_dict["nickname"]
                chat.acs[nickname]="1"
                client_draw.refresh_friends(self,chat.acs)
            elif type=="filenameask":
                if data_dict["filename"]=="离线文件":
                    answer = messagebox.askyesno(title="请求提示", message="有离线文件上传，是否接收")
                    if answer == False:
                        data_d={}
                        data_d["type"] = "refuse"
                        data_d["filename"] ="离线文件"
                        data_d = json.dumps(data_d)
                        self.s.send(data_d.encode("utf-8"))
                        continue
                    else:
                        data_d = {}
                        data_d["type"] = "agree"
                        data_d["filename"] = "离线文件"
                        data_d["nickname"]=data_dict["nickname"]
                        data_d = json.dumps(data_d)
                        s1 = socket(AF_INET, SOCK_STREAM)
                        s1.connect(("47.106.178.71", 30001))
                        s1.send(data_d.encode("utf-8"))
                        threading.Thread(target=self.receivefile, args=(s1,"离线文件")).start()
                else:
                    answer = messagebox.askyesno(title="请求提示", message="%s请求向你发送文件%s" % (
                    data_dict["nickname"], data_dict["filename"]))
                    if answer == False:
                        data_d = {}
                        data_d["size"]=data_dict["size"]
                        data_d["type"] = "refuse"
                        data_d["nickname"] = data_dict["nickname"]
                        data_d["myname"] = data_dict["myname"]
                        data_d["filename"]=data_dict["filename"]
                        data_d = json.dumps(data_d)
                        self.s.send(data_d.encode("utf-8"))
                        continue
                    data_d = {}
                    if os.path.isfile(data_dict["filename"]):
                        data_d["location"]=os.stat(data_dict["filename"]).st_size
                    else:
                        data_d["location"]=0
                    data_d["size"] = data_dict["size"]
                    data_d["type"] = "agree"
                    data_d["nickname"] = data_dict["nickname"]
                    data_d["myname"]=data_dict["myname"]
                    data_d["filename"] = data_dict["filename"]
                    data_d = json.dumps(data_d)
                    self.s2 = socket(AF_INET, SOCK_STREAM)
                    self.s2.connect(("47.106.178.71", 30001))
                    time.sleep(1)
                    dataf={}
                    dataf["type"]="filecom"
                    dataf["nickname"]=data_dict["nickname"]
                    dataf["myname"] = data_dict["myname"]
                    dataf=json.dumps(dataf)
                    self.s2.send(dataf.encode("utf-8"))
                    t=threading.Thread(target=self.receivefile,args=(self.s2,data_dict["nickname"],))
                    time.sleep(1)
                    t.start()
                    self.s.send(data_d.encode("utf-8"))
            elif data_dict["type"] == "refuse":
                tkinter.messagebox.showinfo(title="发送提示", message="对方拒绝文件请求")
            elif data_dict["type"]=="agree":
                self.t1=threading.Thread(target=self.sendFile0, args=(data_dict["filename"], data_dict["size"],data_dict["location"], '1',))
                time.sleep(1)
                self.t1.start()
            elif data_dict["type"]=="stop":
                self.s2.close()
            elif type == "exit":
                chat.acs[data_dict["nickname"]]="0"
                client_draw.refresh_friends(self,chat.acs)
            elif type=="audioexit":
                global audioflag
                audioflag=0
                self.button10.destroy()
                self.child.destroy()
            elif type=="audio":
                self.audio(data_dict)
            elif type == "audiorefuse":
                tkinter.messagebox.showinfo(title="提示", message="语音聊天请求被拒绝")
            elif type=='SOR':
                nfilestate=1-nfilestate
            elif type == "audioag":
                t=threading.Thread(target=self.audioag,args=(data_dict,))
                time.sleep(1)
                t.start()

    def receivefile(self,s,nickname):
        global state
        child = tkinter.Toplevel(self.root)
        child.title = "发送文件提示"
        progressbarOne = tkinter.ttk.Progressbar(child, length=400, mode='determinate', orient=tkinter.HORIZONTAL)
        progressbarOne.pack(pady=20)
        button = tkinter.Button(child, text='SOR', command=lambda :self.changestate1(nickname))
        button.pack(pady=5)
        data = s.recv(1024).decode('utf-8')
        data_dict = json.loads(data)
        progressbarOne['value'] = data_dict["location"]
        fsize = data_dict["message"]
        progressbarOne['maximum'] = fsize
        filename = data_dict["filename"]
        state=0
        self.f = open(filename, 'ab')
        received_size = data_dict["location"]
        while received_size < fsize:
            if fsize - received_size > 1024:
                size = 1024
            else:
                size = fsize - received_size
            try:
                data = s.recv(size)
            except:
                break
            if not data:
                break
            data_len = len(data)
            received_size += data_len
            progressbarOne["value"] += data_len
            self.f.write(data)
        progressbarOne.destroy()
        child.destroy()
        if received_size==fsize:
            tkinter.messagebox.showinfo(title="下载提示", message="文件下载完毕")
            s.close()
        self.f.close()
        state=1

    def changestate1(self,nickname):
        data={}
        data["type"]="SOR"
        data["nickname"]=nickname
        data=json.dumps(data)
        self.s.send(data.encode("utf-8"))


    def audiocom(self):
        data={}
        data["type"]="audio"
        data["nickname"]=client_draw.gop
        if client_draw.gop == "g":
            tkinter.messagebox.showinfo(title="发送提示", message="请向用户单独请求语音通信")
            return
        if chat.acs[client_draw.gop]=="0":
            tkinter.messagebox.showinfo(title="发送提示", message="该用户为离线用户，不能语音通信")
            return
        data=json.dumps(data)
        self.s.send(data.encode('utf-8'))

    def audioag(self,data_dict):
        global audioflag
        audioflag=1
        self.child = tkinter.Toplevel(self.root)
        self.child.title = "语音通话"
        self.button10 = tkinter.Button(self.child, text='STOP',command=self.closeaudio)
        self.button10.pack(pady=5)
        s1 = socket(AF_INET, SOCK_STREAM)
        s1.connect(("47.106.178.71", 30001))
        data={}
        data["type"]="audiotry"
        data["myname"]=data_dict["myname"]
        data["nickname"]=data_dict["nickname"]
        data=json.dumps(data)
        s1.send(data.encode("utf-8"))
        chunk_size = 1024
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)
        threading.Thread(target=self.receive_data,args=(s1,)).start()
        self.send_data(s1)


    def closeaudio(self):
        global audioflag
        data={}
        data["type"]="audioexit"
        data["nickname"]=client_draw.gop
        data=json.dumps(data)
        self.s.send(data.encode("utf-8"))
        self.button10.destroy()
        self.child.destroy()
        audioflag=0

    def receive_data(self,s1):
        global audioflag
        while True:
            try:
                if audioflag==0:
                    break
                data = s1.recv(1024)
                self.playing_stream.write(data)
            except:
                pass
        self.playing_stream.close()
        try:
            s1.close()
        except:
            pass


    def send_data(self,s1):
        while True:
            try:
                if audioflag==0:
                    break
                data = self.recording_stream.read(1024)
                s1.sendall(data)
            except:
                pass
        self.recording_stream.close()
        try:
            s1.close()
        except:
            pass

    def audio(self,data_dict):
        answer=messagebox.askyesno(title="请求提示", message="%s请求与你语音通信"%data_dict["nickname"])
        if answer == False:
            data={}
            data["type"]="audiorefuse"
            data["nickname"]=data_dict["nickname"]
            data=json.dumps(data)
            self.s.send(data.encode("utf-8"))
        else:
            data={}
            data["type"]="audioag"
            data["nickname"]=data_dict["nickname"]
            data["myname"]=data_dict["myname"]
            data = json.dumps(data)
            self.s.send(data.encode("utf-8"))
            threading.Thread(target=self.audioag,args=(data_dict,)).start()


    def register_interface(self):
        client_draw.draw_register(self)

    def chat_interface(self,nickname,accounts):
        client_draw.draw_chat(self,nickname,accounts)

    def return_login_interface(self):
        self.label_nickname.destroy()
        self.input_nickname.destroy()
        self.label_password.destroy()
        self.input_password.destroy()
        client_draw.draw_login(self)

    def verify_register(self):
        account=self.input_account.get()
        password=self.input_password.get()
        nickname=self.input_nickname.get()
        register_data={}
        register_data["type"]="register"
        register_data["account"]=account
        register_data["password"]=password
        register_data["nickname"]=nickname
        data=json.dumps(register_data)
        self.s.send(data.encode('utf-8'))

    def verify_login(self):
        account=self.input_account.get()
        password=self.input_password.get()
        login_data={}
        login_data["type"]="login"
        login_data["account"]=account
        login_data["password"]=password
        data=json.dumps(login_data)
        self.s.send(data.encode('utf-8'))

    def sendMsg(self):
        message=self.send_text.get('0.0',tkinter.END).strip()
        if not message:
            tkinter.messagebox.showinfo(title="发送提示",message="发送内容不能为空")
            return
        self.send_text.delete('0.0',tkinter.END)
        chat_data={}
        chat_data["type"]="chat"
        chat_data["message"]=message
        chat_data["gop"] = client_draw.gop
        data = json.dumps(chat_data)
        self.s.send(data.encode('utf-8'))


    def sendFile0(self,filename,size,location,state):
        global state1
        global filestate
        global nfilestate
        filestate=1
        nfilestate=1
        state1=0
        self.s1=socket(AF_INET, SOCK_STREAM)
        self.s1.connect(("47.106.178.71", 30001))
        if state=="0":
            tkinter.messagebox.showinfo(title="发送提示", message="准备向对方发送离线文件")
        else:
            tkinter.messagebox.showinfo(title="发送提示", message="对方接受文件请求")
        child=tkinter.Toplevel(self.root)
        child.title="发送文件提示"
        progressbarOne = tkinter.ttk.Progressbar(child, length=400, mode='determinate', orient=tkinter.HORIZONTAL)
        progressbarOne.pack(pady=20)
        button = tkinter.Button(child, text='SOR',command=self.changestate)
        button.pack(pady=5)
        progressbarOne['maximum'] = size
        progressbarOne['value']=location
        chat_data={}
        chat_data["type"]="filename"
        chat_data["message"] = size
        chat_data["location"]=location
        chat_data["filename"]=filename
        chat_data["gop"] = client_draw.gop
        chat_data["state"] = chat.acs[client_draw.gop]
        data=json.dumps(chat_data)
        self.s1.send(data.encode('utf-8'))
        f=open(filename,'rb')
        f.seek(location)
        time.sleep(1)
        flag_exit=1
        while location<size:
            if filestate==0:
                while(filestate==0):
                    continue
            if nfilestate==0:
                while (nfilestate == 0):
                    continue
            if size-location>1024:
                ssize=1024
            else:
                ssize=size-location
            fidata=f.read(ssize)
            try:
                self.s1.send(fidata)
            except:
                flag_exit=0
                break
            progressbarOne["value"] += len(fidata)
            location+=len(fidata)
        if flag_exit==0:
            f.close()
            return
        progressbarOne.destroy()
        child.destroy()
        tkinter.messagebox.showinfo(title="发送提示", message="文件发送成功")
        f.close()
        self.s1.close()
        state1=1

    def changestate(self):
        global filestate
        filestate=1-filestate

    def sendFile(self):
        filename=self.send_text.get('0.0',tkinter.END).strip()
        if not filename:
            tkinter.messagebox.showinfo(title="发送提示",message="发送内容不能为空")
            return
        self.send_text.delete('0.0', tkinter.END)
        if os.path.isfile(filename):
            size = os.stat(filename).st_size
            chat_data={}
            chat_data["size"]=size
            chat_data["type"]="filenameask"
            chat_data["filename"]=filename
            chat_data["nickname"] = client_draw.gop
            if chat_data["nickname"]=="g":
                tkinter.messagebox.showinfo(title="发送提示", message="请向用户单独发送文件")
                return
            chat_data["state"]=chat.acs[client_draw.gop]
            data=json.dumps(chat_data)
            if chat_data["state"]=="1":
                self.s.send(data.encode('utf-8'))
            else:
                t=threading.Thread(target=self.sendFile0,args=(filename,size,0,chat_data["state"]))
                time.sleep(1)
                t.start()
        else:
            tkinter.messagebox.showinfo(title="发送提示", message="文件不存在")



    def sendMsgEvent(self,event):
        if event.keysym=="Return":
            self.sendMsg()



    def on_closing(self):
        global state
        global state1
        if messagebox.askokcancel("推出提示","是否离开聊天室"):
            exit_data = {}
            exit_data["type"] = "exit"
            data = json.dumps(exit_data)
            self.root.destroy()
            self.s.send(data.encode('utf-8'))
            if state1==0:
                data0= {}
                data0["type"]="stop"
                data0["nickname"]=client_draw.gop
                data0=json.dumps(data0)
                time.sleep(1)
                self.s.send(data0.encode("utf-8"))
                self.s1.close()
            if state==0:
                self.f.close()


if __name__=='__main__':
    chatroom=chat()
    client=chatroom.connect()
    t=threading.Thread(target=chatroom.recive,args=(client,))
    t.start()
    chatroom.root=tkinter.Tk()
    client_draw.draw_login(chatroom)
    tkinter.mainloop()





