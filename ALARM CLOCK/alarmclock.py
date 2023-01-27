from winsound import Beep
from datetime import datetime
from threading import Thread
from tkinter import *
def alarmclock():
    #from winsound import Beep
    from time import sleep
    hr=min=zone=None;brak=False;jj=0;from sys import exit;thradkill=False
    d1={};ttl=None;lis=[];lock=[]
    def worker():
        nonlocal brak,jj,thradkill,lis,lock
        if jj!=0:
            brak=True 
        else:
            jj=1
        while brak==True:#WILL CONTAIN THREAD BEFORE THE THREAD IN LOOP EXITS
            pass
        ze=de=[]
        if len(lis)!=0:
            ze=d1[lis[0]]
        if len(lock)!=0:
            de=d1[lock[0]]
        while(1 == 1):#WILL KEEP ON CHECKING
            print(lis,'lis');print(lock,'lock')
            if(brak==True):
                break
            if(lis!=[] and ze[0]==datetime.now().hour and
                ze[1]==datetime.now().minute) :#FOR UPCOMING ALARMS
                Beep(1000,1000)
                lis.remove(lis[0])
                if len(lis)!=0:
                    ze=d1[lis[0]]
            if(lock!=[] and de[0]==datetime.now().hour and
                de[1]==datetime.now().minute) :#FOR NEXT DAY ALARMS
                Beep(1000,1000)
                lock.remove(lock[0])
                if len(lock)!=0:
                    de=d1[lock[0]]
            if lis==[] and lock==[]:
                jj=0;break
            sleep(1)
            if thradkill==True:
                thradkill=False#SO THAT NEXT NEW THREAD DON'T EXIT
                exit()
            if (24==datetime.now().hour and 0==datetime.now().minute and(0==datetime.now().second or 1==datetime.now().second or 2==datetime.now().second)):
                lis=lock;lock=[]
        brak=False
        exit()        
    def stslr():
        b1['state']='disabled'
        def ampm():
            if(b2['text']=='AM'):
                b2['text']='PM' 
            else:
                b2['text']='AM'
        def destroy():
            b1.config(state=NORMAL)
            a.destroy()
        def func(l2_,l1_,b2_):
            nonlocal hr,min,zone,lis,lock
            hr=l2_.get(ANCHOR)
            min=l1_.get(ANCHOR)
            zone=b2_['text']
            b1.config(state=NORMAL)
            lb1=Label(b,text=f"{hr}:{min} {zone}",bg="black",font="Constantia 18 bold",fg="white",relief=RAISED,bd=5);lb1.pack(side=TOP)
            if(zone=="PM"):
                if(hr!=12):
                    hr=hr+12
            elif(zone=="AM" and hr==12):
                hr+=12
            ttl=hr*60+min
            if ttl>(datetime.now().hour*60 +datetime.now().minute):
                lis.append(ttl);lis.sort()#KEEP ON SORTING AS PER ALARM PRIORITY AND SAME IN ELSE
            else:
                lock.append(ttl);lock.sort()
            d1[ttl]=[hr,min]
            t=Thread(target=worker);t.setDaemon(True);t.start()#THREAD FOR NEW AND UPCOMING ALARMS
            a.destroy()
        a=Tk()
        a.overrideredirect(True)
        a.geometry("330x378");a.resizable(False,False)
        a.configure(bg='black')
        b2=Button(a,text="AM",activebackground="grey",font="Constantia 18 bold",bg='black',fg='blue',bd=10,relief=RAISED,command=ampm);b2.grid(column=0,row=1)
        la1=Label(a,text="HR",bg="black",font="Constantia 18 bold",fg="white",relief=RAISED,bd=5);la1.grid(row=0,column=1)
        la2=Label(a,text="MIN",bg="black",font="Constantia 18 bold",fg="white",relief=RAISED,bd=5);la2.grid(row=0,column=2)
        l2=Listbox(a,bg='black',width=2,selectmode=SINGLE,relief=RAISED,exportselection=False,height=5,bd=5)
        l2.configure(bg="black",font="Constantia 28 bold",fg="white",width=2,selectmode=SINGLE,relief=RAISED)
        l2.grid(row=1,column=1, sticky='sw')
        for values in range(1,13):
            l2.insert(END, values)
        l1=Listbox(a,bg='black',width=2,selectmode=SINGLE,relief=RAISED,exportselection=False,height=5,bd=5)
        l1.configure(bg="black",font="Constantia 28 bold",fg="white",width=2,selectmode=SINGLE,relief=RAISED)
        l1.grid(row=1,column=2,sticky='sw')
        for values in range(60):
            l1.insert(END, values)
        b3=Button(a,text="SET",activebackground="grey",font="Constantia 18 bold",bg='black',fg='blue',bd=10,relief=RAISED,command=lambda:func(l2,l1,b2));b3.grid(column=3,row=1)
        b4=Button(a,text="CANCEL",activebackground="grey",font="Constantia 18 bold",bg='black',fg='blue',bd=10,relief=RAISED,command=destroy);b4.grid(column=0,sticky='s')
        a.mainloop()
    def dest():
        nonlocal thradkill;thradkill=True
        b.destroy()
        exit()
    b=Tk()
    b.geometry("600x550");b.resizable(False, False)
    b.title("ALARM CLOCK")
    b.configure(bg='black')
    bsd=Button(b,text="CANCEL",activebackground="grey",font="Constantia 18 bold",bg='black',fg='blue',bd=10,relief=RAISED,command=dest);bsd.pack(side=BOTTOM)
    b1=Button(b,text="+",activebackground="grey",font="Constantia 18 bold",bg='black',fg='blue',bd=10,relief=RAISED,command=stslr);b1.pack(side=BOTTOM)
    b.mainloop()
    exit()
alarmclock()