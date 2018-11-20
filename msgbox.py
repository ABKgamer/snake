from tkinter import Button, Tk, Label
from threading import *


class Mb(Thread):
    def showmsg(self, obj, titlemsg="Message Box" ,lablemsg="sample Text", leftbuttonmsg="left", rightbuttonmsg="right"):
        self.obj = obj
        self.choce = ""
        self.gui = Tk()
        self.gui.title(titlemsg)
        self.lab = Label(self.gui, text=lablemsg)
        self.lab.grid(columnspan=2, row=0)
        self.butleft = Button(self.gui, text=leftbuttonmsg, command=lambda args=(leftbuttonmsg):self.buttonclicked(args))
        self.butleft.grid(row=1,column=0)
        self.butright = Button(self.gui, text=rightbuttonmsg, command=lambda args=(rightbuttonmsg):self.buttonclicked(args))
        self.butright.grid(row=1,column=1)
        self.gui.resizable(width=False, height=False)
        self.gui.mainloop()
        return self.choce

    def buttonclicked(self,args):
        self.obj.run = args
        self.gui.quit()