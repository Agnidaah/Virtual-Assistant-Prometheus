from pyttsx3 import init
from speech_recognition import Recognizer,Microphone
from datetime import datetime
from webbrowser import open_new_tab
from threading import Thread
from tkinter import *
from wikipedia import summary
from multiprocessing import Process
import sqlite3
from tkinter import messagebox
engine = init('sapi5');voices = engine.getProperty('voices');engine.setProperty('voice', voices[0].id);niklo=False
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def takeCommand(keptl='en-in'):
    #It takes microphone input from the user and returns string output
    r = Recognizer()
    with Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...") 
        query = r.recognize_google(audio,language=keptl)
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query
def downloader():
    from sys import exit
    r="360p";dir="";vidq=2;audq=2
    def re(event):
        nonlocal r
        cs = reso.curselection()
        try:
            r=reso.get(cs)
        except:
            pass
    def dow():
        nonlocal vidq
        b11['state']='disable'
        b1['text']='DOWNLOADING...'
        b1.configure(bg="red")
        from pytube import YouTube 
        try:
            video=YouTube(link.get())
            try:
                import os
                megatron=video.streams.filter(res=r,progressive=True,file_extension ='mp4').first().download(f"{dir}")
                messagebox.showinfo('information','DOWNLOAD COMPLETED')
            except Exception as e:
                messagebox.showwarning('warning','RESOLUTION NOT AVAILABLE')
            else:
                try:
                    base,ext=os.path.splitext(megatron)
                    new_file=base+'mp4' + '.mp4'
                    os.rename(megatron,new_file)
                except:
                    base,ext=os.path.splitext(megatron)
                    new_file=base+'mp4' +str(vidq)+ '.mp4';vidq+=1
                    os.rename(megatron,new_file)
        except:
            messagebox.showwarning('warning','LINK NOT GOOD')
        b11['state']='normal'
        b1['text']='DOWNLOAD'
        b1.configure(bg="blue") 
        exit()
    def dowmp3():
        nonlocal audq
        b1['state']='disable'
        import os
        from pytube import YouTube
        try:
            yt=YouTube(link.get())
        except:
            messagebox.showwarning('warning','LINK NOT GOOD')
            b1['state']='normal'
            return
        else:
            try:
                video = yt.streams.filter(only_audio=True).first()
            except Exception as e:
                print(e)
                messagebox.showwarning('warning','SOME PROBLEM OCCURRED')
                b1['state']='normal'
                return 
            else:
                try:
                    trion=video.download(output_path=dir)
                except:
                    messagebox.showwarning('warning',"CAN'T DOWNLOAD")
                    b1['state']='normal'
                    return 
        try:
            base,ext = os.path.splitext(trion)
            new_file = base+'mp3' + '.mp3'
            os.rename(trion,new_file)
        except Exception as e:
            base,ext = os.path.splitext(trion)
            new_file = base+'mp3' +str(audq)+ '.mp3';audq+=1
            os.rename(trion,new_file)
        b1['state']='normal'
        messagebox.showinfo('information','DOWNLOAD COMPLETED')
        exit()
    def reset():
        nonlocal r
        link.delete(0, 'end')
        reso.selection_clear(0, 'end')
        r="360p"
    def place():
        nonlocal dir
        from tkinter import filedialog
        dir = filedialog.askdirectory()
    a=Tk()
    a.geometry("600x650");a.resizable(False, False)
    a.title("YOUTUBE VIDEO DOWNLOADER")
    a.configure(bg='brown')
    Label(a,text="ENTER VIDEO LINK",font="Constantia 18 bold",relief=RIDGE,bd=5).pack(side=TOP,pady=5)
    url=StringVar();link=Entry(a,textvariable=url,width=40,font="18",relief=SUNKEN,bd=5,bg='red');link.pack(side=TOP,pady=5)
    Label(a,text="SET RESOLUTION",font="Constantia 18 bold",relief=RIDGE,bd=5).pack(side=TOP,pady=5)
    reso= Listbox(a,font="Arial 13 bold",relief=RAISED,bd=5,selectbackground="red")
    reso.configure(background="skyblue",fg="black",height=6,width=5,selectmode=SINGLE)
    reso.insert(0,"144p");reso.insert(1,"240p");reso.insert(2,"360p")
    reso.insert(3,"480p");reso.insert(4,"720p");reso.insert(5,"1080p")
    reso.bind('<<ListboxSelect>>',re);reso.pack(side=TOP,pady=5)
    def dstr():
        a.destroy()
    f1=Frame(a,bg="grey",relief=SUNKEN,bd=6);f1.pack(side=TOP,fill="both",padx=6,pady=6)
    b3=Button(f1,text='BROWSE TO SAVE',activebackground='violet',bg="skyblue",font="Constantia 18 bold",fg='green',bd=5,relief=RAISED,command=place)
    b3.pack(side=TOP,pady=5)
    b1=Button(f1,text='DOWNLOAD',activebackground='red',fg="lightgreen",font="Constantia 18 bold",bg='blue',bd=5,relief=RAISED,command=lambda :Thread(target=dow).start())
    b1.pack(side=TOP,pady=5)
    b11=Button(f1,text='⬇️MP3',activebackground='red',fg="lightgreen",font="Constantia 18 bold",bg='blue',bd=5,relief=RAISED,command=lambda :Thread(target=dowmp3).start())
    b11.pack(side=TOP,pady=5)
    b2=Button(f1,text='RESET',activebackground='red',fg="red",font="Constantia 18 bold",bg='yellow',bd=5,relief=RAISED,command=reset)
    b2.pack(side=TOP,pady=5)
    b4=Button(f1,text='CANCEL',activebackground='violet',fg="blue",font="Constantia 18 bold",bg='red',bd=5,relief=RAISED,command=dstr)
    b4.pack(side=RIGHT,pady=5)
    a.mainloop()
    exit()
def alarm(reminder):
    from winsound import Beep;from time import sleep
    for i in range(2):
        Beep(1000,500)
        sleep(1)
    speak(reminder)
def alarmclock(reminder):
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
                alarm(reminder)
                lis.remove(lis[0])
                if len(lis)!=0:
                    ze=d1[lis[0]]
            if(lock!=[] and de[0]==datetime.now().hour and
                de[1]==datetime.now().minute) :#FOR NEXT DAY ALARMS
                alarm(reminder)
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
def whatsapp():
    from subprocess import Popen;from time import sleep
    from psutil import process_iter
    if ("WhatsApp.exe" in (i.name() for i in process_iter()))==False:#WILL SEE IF IT IS STILL THERE
        try:
            Popen(["cmd", "/C", f"start whatsapp://"],shell=True)#send?phone=+917488091153^&text=
        except:
            speak('some problem occured sir...')#WILL OPEN WEB WHATSAPP THEN ( EXCEPTION JUST FOR ASSURITY)
            webwhat()
        else:
            sleep(3)
            if ("WhatsApp.exe" in (i.name() for i in process_iter()))==False:
                speak('whatsapp is not installed.....sir')#MOSTLY PROBABLE
                webwhat()
            else:
                sleep(12)
    else:
        from pygetwindow import getWindowsWithTitle
        win=getWindowsWithTitle("WhatsApp")[0];win.maximize()
def whatsapp2():
    from pygetwindow import getWindowsWithTitle;from time import sleep
    win=getWindowsWithTitle("WhatsApp")[0];win.maximize();sleep(1)#WILL WILL MAXIMZE THE WINDOW
    from pyautogui import locateOnScreen,click
    battery=locateOnScreen('checko.png')#IF SAW THAT RED BATERY ALERT THEN WILL CANCEL IT
    if battery!=None:
        click('checko.png')
    speak("tell me name sir")
    name=None
    while name=='None' or name==None:
        name=takeCommand()#KEEP ON ASKING NAME TILL GET 
    whatsapp3(name,yes=0)
def whatsapp3(name,yes):
    print(name)
    from time import sleep
    import pyautogui;pyautogui.FAILSAFE=False
    pyautogui.moveTo(375,150,duration=0.01);pyautogui.click()
    if yes==0:
        pyautogui.typewrite(name)
    else:
        from pyperclip import copy
        copy(name)
        pyautogui.hotkey('ctrl','v')
    pyautogui.press("enter");sleep(0.5)
    l = pyautogui.locateOnScreen('icheck.png')
    if(l!=None):
        sleep(4)#will do search whether the given name is in list or not
    lo = pyautogui.locateOnScreen('check.png')
    if(lo==None):
        pyautogui.moveTo(875,985,duration=0.01)
        pyautogui.click()
        speak("what to write sir");b='None'
        while b=='None':
            b= takeCommand()
        if b.lower()=='paste':
            pyautogui.hotkey('ctrl','v')
        else:
            pyautogui.typewrite(b)
        pyautogui.press("enter")
    else:
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.typewrite(['backspace'])
        hiname=translate(name)
        if yes==0:
            whatsapp3(hiname,yes=1)
        else:
            speak("name incorrect sir")
def translator():#GUI TRANSLATOR
    from tkinter import messagebox
    jek={'afrikaans':'af','albanian':'sq','amharic':'am','arabic':'ar','armenian':'hy','azerbaijani':'az','basque':'eu','belarusian':'be','bengali':'bn','bosnian':'bs','bulgarian':'bg','catalan':'ca','cebuano':'ceb','chichewa':'ny','chinese (simplified)':'zh-cn','chinese (traditional)':'zh-tw','corsican':'co','croatian':'hr','czech':'cs','danish':'da','dutch':'nl','english':'en','esperanto':'eo','estonian':'et','filipino':'tl','finnish':'fi','french':'fr','frisian':'fy','galician':'gl','georgian':'ka','german':'de','greek':'el','gujarati':'gu','haitian creole':'ht','hausa':'ha','hawaiian':'haw','hebrew':'iw','hebrew':'he','hindi':'hi','hmong':'hmn','hungarian':'hu','icelandic':'is','igbo':'ig','indonesian':'id','irish':'ga','italian':'it','japanese':'ja','javanese':'jw','kannada':'kn','kazakh':'kk','khmer':'km','korean':'ko','kurdish (kurmanji)':'ku','kyrgyz':'ky','lao':'lo','latin':'la','latvian':'lv','lithuanian':'lt','luxembourgish':'lb','macedonian':'mk','malagasy':'mg','malay':'ms','malayalam':'ml','maltese':'mt','maori':'mi','marathi':'mr','mongolian':'mn','myanmar (burmese)':'my','nepali':'ne','norwegian':'no','odia':'or','pashto':'ps','persian':'fa','polish':'pl','portuguese':'pt','punjabi':'pa','romanian':'ro','russian':'ru','samoan':'sm','scots gaelic':'gd','serbian':'sr','sesotho':'st','shona':'sn','sindhi':'sd','sinhala':'si','slovak':'sk','slovenian':'sl','somali':'so','spanish':'es','sundanese':'su','swahili':'sw','swedish':'sv','tajik':'tg','tamil':'ta','telugu':'te','thai':'th','turkish':'tr','ukrainian':'uk','urdu':'ur','uyghur':'ug','uzbek':'uz','vietnamese':'vi','welsh':'cy','xhosa':'xh','yiddish':'yi','yoruba':'yo','zulu':'zu'}
    import tkinter as tk
    za=tk.Tk();za.title('TRANSLATOR');za.geometry("1160x600");za.minsize(1160,600)
    za.configure(background='black')
    import googletrans
    l1=tk.Label(za,text="FROM",font="Constantia 18 bold",fg="yellow",bg="black",bd=5,relief="raised");l1.grid(row=0,column=0,padx=5,pady=5)
    l2=tk.Listbox(za,bg='black',width=2,selectmode='single',relief='raised',exportselection=False,height=19,bd=5)
    l2.configure(bg="black",font="Constantia 14 bold",fg="white",width=17)
    l2.grid(row=1,column=0,sticky='ne',padx=5,pady=5)
    for i in googletrans.LANGUAGES.values():
        l2.insert('end',i)
    l3=tk.Label(za,text="TO",font="Constantia 18 bold",fg="yellow",bg="black",bd=5,relief="raised");l3.grid(row=0,column=1,padx=5,pady=5)
    l4=tk.Listbox(za,bg='black',width=2,selectmode='single',relief='raised',exportselection=False,height=19,bd=5)
    l4.configure(bg="black",font="Constantia 14 bold",fg="white",width=17)
    l4.grid(row=1,column=1,sticky='ne',padx=5,pady=5)
    f1=tk.Frame(za,background='black');f1.grid(row=2,column=2)
    f2=tk.Frame(za,background='black');f2.grid(row=1,column=2)
    l5=tk.Label(za,text="ENTER TEXT",font="Constantia 18 bold",fg="yellow",bg="black",bd=5,relief="raised");l5.grid(row=0,column=2,padx=5,pady=5)
    for i in googletrans.LANGUAGES.values():
        l4.insert('end',i)
    text1= tk.Text(f2,font="lucida 13",relief='sunken',bd=5,height=12);text1.grid(row=0,column=0)
    text2= tk.Text(f2,font="lucida 13",relief='sunken',bd=5,height=12,state='normal');text2.grid(row=1,column=0)
    b10=tk.Button(f1,text="TRANSLATE",activebackground='red',font="Constantia 18 bold",fg="yellow",bg="black",bd=5,relief="raised",command=lambda:anab(text1));b10.grid(row=0,column=0,padx=5,pady=5)
    gotit=None;sec=""
    b11=tk.Button(f1,text="🎤",activebackground='red',font="Constantia 18 bold",fg="yellow",bg="black",bd=5,relief="raised",command=lambda:Thread(target=fake).start());b11.grid(row=0,column=2,padx=5,pady=5)
    def fake():
        b11['state']='disable'
        fema(gotit,sec)
        b11['state']='normal'
    def anab(text1):
        text1=text1.get('1.0','end');print(text1)
        nonlocal gotit,text2,sec
        if len(l2.curselection())==1:
            fir=jek[l2.get(l2.curselection()[0])]
        else:
            messagebox.showwarning('warning','No Source Language')
            return None
        if len(l4.curselection())==1:
            sec=jek[l4.get(l4.curselection()[0])]
        else:
            messagebox.showwarning('warning','No Destination Language')
            return None
        try:
            gotit=translate(text1,fir,sec)
        except Exception as e:
            messagebox.showwarning('warning','No Valid Text Input')
            return None
        text2.delete(1.0,"end")
        text2.insert(1.0,gotit)
    za.mainloop()
def translate(gtstr,src1='en',dest1='hi'):
    from googletrans import Translator 
    translator = Translator()
    result = translator.translate(gtstr, src=src1, dest=dest1)
    return result.text
def fema(strxx,langu):
    from gtts import gTTS
    from os import path,remove
    try:
        myobj = gTTS(text=strxx,lang=langu,slow=False)#makes obj of text 
    except:
        speak("destination language not supported sir")
    else:
        myobj.save("welcome.mp3")#saves it as mp3
    from playsound import playsound
    try:
        playsound('welcome.mp3')#plays it and you hear translation
    except Exception as e:
        pass
    if path.exists("welcome.mp3"):
        remove("welcome.mp3")#deletion
    else:
        print("The file does not exist")
def asks():
    zoya={'afrikaans':'af','albanian':'sq','amharic':'am','arabic':'ar','armenian':'hy','azerbaijani':'az','basque':'eu','belarusian':'be','bengali':'bn','bosnian':'bs','bulgarian':'bg','catalan':'ca','cebuano':'ceb','chichewa':'ny','chinese':'zh-cn','chinese simplified':'zh-cn','chinese traditional':'zh-tw','corsican':'co','croatian':'hr','czech':'cs','danish':'da','dutch':'nl','english':'en','esperanto':'eo','estonian':'et','filipino':'tl','finnish':'fi','french':'fr','frisian':'fy','galician':'gl','georgian':'ka','german':'de','greek':'el','gujarati':'gu','haitian creole':'ht','hausa':'ha','hawaiian':'haw','hebrew':'iw','hebrew':'he','hindi':'hi','hmong':'hmn','hungarian':'hu','icelandic':'is','igbo':'ig','indonesian':'id','irish':'ga','italian':'it','japanese':'ja','javanese':'jw','kannada':'kn','kazakh':'kk','khmer':'km','korean':'ko','kurdish':'ku','kyrgyz':'ky','lao':'lo','latin':'la','latvian':'lv','lithuanian':'lt','luxembourgish':'lb','macedonian':'mk','malagasy':'mg','malay':'ms','malayalam':'ml','maltese':'mt','maori':'mi','marathi':'mr','mongolian':'mn','burmese':'my','nepali':'ne','norwegian':'no','odia':'or','pashto':'ps','persian':'fa','polish':'pl','portuguese':'pt','punjabi':'pa','romanian':'ro','russian':'ru','samoan':'sm','scots gaelic':'gd','serbian':'sr','sesotho':'st','shona':'sn','sindhi':'sd','sinhala':'si','slovak':'sk','slovenian':'sl','somali':'so','spanish':'es','sundanese':'su','swahili':'sw','swedish':'sv','tajik':'tg','tamil':'ta','telugu':'te','thai':'th','turkish':'tr','ukrainian':'uk','urdu':'ur','uyghur':'ug','uzbek':'uz','vietnamese':'vi','welsh':'cy','xhosa':'xh','yiddish':'yi','yoruba':'yo','zulu':'zu'}
    speak("tell me source language sir");langu=None
    while langu==None:
        try:
            langu=zoya[takeCommand().lower()]#will keep on listening till get a language name
        except:
            speak('tell me again sir')
    speak("tell me destination language sir");langu1=None
    while langu1==None:
        try:
            langu1=zoya[takeCommand().lower()]#will keep on listening till get a language name
        except:
            speak('tell me again sir')
    speak("dictate sir")
    gtstr=takeCommand(langu)
    strxx=translate(gtstr,langu,langu1)#goes to tranlate
    fema(strxx,langu1)#then she speaks the translation
def search(query):
    from wikipedia import summary
    open_new_tab(f'http://www.google.com/search?btnG=1&q={query}')
    try:
        results = summary(query,sentences=2)
    except:
        speak("not much popular sir!")
    else:
        speak("According to Wikipedia")
        speak(results)
def chatbot(query):
    b=[['prometheus'],
    ['hello','hi there','hey'],
    ['how are you','you fine',"what's up"],
    ['who are you','what are you','about you','your name'],
    ['you do'],
    ['what is','who is'],
    ["i am fine","good",'great'],
    ['bad','worst','worse']]
    a=[['yes sir'],
    ['hello...how are you...',"it's a pleasure to meet you",'good to see you'],
    ["i'm fine.. what about you","i'm alright...tell me about you","i'm well.. say me about youself"],
    ["i'm a virtual assistant named prometheus of age-2","myself prometheus of age-2"],
    ['i can give you desktop assistance',"i do desktop chores for multitasking"],
    ['let me see'],
    ["that's great",'i always wish that'],
    ['oh...be calm',"well... turning worst into wonderful is what you should do"]]
    from random import choice
    for i,j in enumerate(b):
        if list(filter(lambda x:x in query,j)):
            return choice(a[i])
def webwhat():
    open_new_tab('https://web.whatsapp.com/')
def impdf():
    from tkinter import Tk 
    from tkinter import filedialog 
    from pathlib import Path
    Tk().withdraw()
    path=filedialog.askopenfiles(title="Select images",initialdir=str(Path.home()),filetypes=((["jpeg/png files", "*.jpg;*.png;*.jfif;*.jpeg"]),("all files", "*.*")))
    from PIL import Image
    khali=[];z=0;alpha=None#recipe variables
    for i in path:
        z+=1
        a=Image.open(i.name)
        i=a.convert('RGB')
        if z!=1:
            khali.append(i)#khali is list of image objects after the first image
        else:
            alpha=i#because first image is stored in alpha
    if alpha:
        dir = filedialog.askdirectory(title="save pdf")
        alpha.save(f"{dir}/myImages.pdf",save_all=True, append_images=khali)#saving will started with first image and will be appened using khali
        speak('pdf created sir')
def pdftext():#it helps in extracting text
    import PyPDF2#importing needed modules
    from tkinter import Tk 
    from tkinter import filedialog 
    from pathlib import Path
    Tk().withdraw()
    file= filedialog.askopenfilename(title="Select a PDF",initialdir=str(Path.home()), filetype=(("PDF    Files","*.pdf"),("All Files","*.*")))
    j=PyPDF2.PdfFileReader(file)#making object of pdf file
    take=""
    for i in range(j.getNumPages()):
        take+=j.getPage(i).extractText()#getting text from each page
    with open("new.txt",'w',encoding='utf-8') as f:
        f.write(take)
        speak("text extraction done sir")
def copytext():# it helps in extracting text just by taking a snip from screen
    x1,y1,x2,y2=None,None,None,None;from os import remove
    def getcord():#tkinter function
        op=Tk()
        op.geometry("1600x900");op.state('zoomed')#so that full screen will be covered
        op.overrideredirect(True);op.attributes('-topmost', True)#no button allowances
        op.attributes('-alpha', 0.2)#making translucent
        canvas = Canvas(op,cursor="cross")#canvas to draw rectangle
        canvas.pack( expand=True,fill=BOTH)
        rect = None
        start_x = None
        start_y = None#starting coords of rect
        def key_press(event):#recording starting coords
            nonlocal start_x,start_y,rect,x1,y1
            x1=event.x*(1920/1535);y1=event.y*(1080/864)
            start_x =canvas.canvasx(event.x)
            start_y =canvas.canvasy(event.y)
            rect=canvas.create_rectangle(start_x,start_y,start_x,start_y,outline='red',width=2)
        def press_move(event):#drawing rectangle
            curX = canvas.canvasx(event.x)
            curY = canvas.canvasy(event.y)
            canvas.coords(rect,start_x,start_y,curX,curY) 
        def key_released(event):#get last coords
            nonlocal x2,y2
            x2=event.x*(1920/1535);y2=event.y*(1080/864)
            op.destroy()   
        canvas.bind("<ButtonPress-1>",key_press)
        canvas.bind("<B1-Motion>",press_move)
        canvas.bind("<ButtonRelease-1>",key_released)
        op.mainloop()
    def gettext():#extracting text
        from PIL import ImageGrab,Image;from pytesseract import image_to_string,pytesseract
        try:#check each condition of rect drawing and take ss
            image=ImageGrab.grab(bbox=(x1,y1,x2,y2))
            image.save('sc.png')
        except:
            try:
                image=ImageGrab.grab(bbox=(x2,y1,x1,y2))
                image.save('sc.png')
            except:
                try:
                    image=ImageGrab.grab(bbox=(x2,y2,x1,y1))
                    image.save('sc.png')
                except:
                    image=ImageGrab.grab(bbox=(x1,y2,x2,y1))
                    image.save('sc.png')
        image=Image.open('sc.png')
        pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"#using tesseract
        image_to_text=image_to_string(image,lang='eng')
        remove("sc.png")
        from pyperclip import copy
        copy(image_to_text)
    getcord()
    try:
        gettext()
    except:
        from os import path#just a precaution that ss should not be left
        if path.exists("sc.png"):
            remove("sc.png")
        speak('try again sir')
        copytext()
def openit(query):
    from subprocess import Popen
    if 'notepad' in query:
        Popen('C:\\Windows\\System32\\Notepad.exe')
    elif 'wordpad' in query or 'wattpad' in query:
        Popen('C:\\Windows\\System32\\write.exe')
    elif 'calculator' in query:
        Popen('C:\\Windows\\System32\\calc.exe')
    elif 'ppt' in query or 'powerpoint' in query:
        Popen(r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE")
    elif 'excel' in query:
        Popen(r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE")
    elif 'ms word' in query:
        Popen(r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE")
    elif 'paint' in query:
        Popen(r"C:\Windows\System32\mspaint.exe")
    elif 'zero cross' in query:
        jab=False
        pe = Process(target=first)
        pe.start()
        if jab:
            import sys;sys.exit()
        if jab==True:
            jab=False
        else:
            jab=True
    else:
        speak("i can't.. do it sir")
def closit(query):
    from psutil import process_iter;from os import kill;from signal import SIGINT
    if 'notepad' in query:
        for pid in (process.pid for process in process_iter() if process.name()=="notepad.exe"):
            kill(pid,SIGINT)
    elif 'paint' in query:
        for pid in (process.pid for process in process_iter() if process.name()=="mspaint.exe"):
            kill(pid,SIGINT)
    elif 'calculator' in query:
        for pid in (process.pid for process in process_iter() if process.name()=="Calculator.exe"):
                kill(pid,SIGINT)
    elif 'ms word' in query:
        for pid in (process.pid for process in process_iter() if process.name()=="WINWORD.EXE"):
                kill(pid,SIGINT)
    elif 'ppt' in query or 'powerpoint' in query:
        for pid in (process.pid for process in process_iter() if process.name()=="POWERPNT.EXE"):
                kill(pid,SIGINT)
    elif 'excel' in query:
        for pid in (process.pid for process in process_iter() if process.name()=="EXCEL.EXE"):
                kill(pid,SIGINT)
    elif 'wordpad' in query or 'wattpad' in query:
        for pid in (process.pid for process in process_iter() if process.name()=="wordpad.exe"):
                kill(pid,SIGINT)
    else:
        speak("i can't.. do it sir")
def first():
    turn1='gu est1';turn2="gu est2"
    from tkinter import messagebox
    import chime
    a=Tk()
    a.geometry("650x650");a.resizable(False,False)
    a.configure(bg="black")
    count=0
    def turny(cbtn):
        nonlocal turn1,turn2
        if cbtn:
            turn2='gu est2';b16['state']='disable';b18['text']='WITH PROFILE'
        else:
            turn1='gu est1';b15['state']='disable';b17['text']='WITH PROFILE'
    def disble():
        b1['state']=b2['state']=b3['state']=b4['state']=b5['state']=b6['state']=b7['state']=b8['state']=b9['state']='disable'
    def anable():
        b10['state']=b11['state']=b13['state']=b15['state']=b16['state']=b17['state']=b18['state']=b23['state']='disable'
        chime.theme('zelda');chime.success()
        nonlocal count
        l1['text']='RESULT';count=0
        b1.configure(state='normal',text="  1  ");b2.configure(state='normal',text="  2  ");b3.configure(state='normal',text="  3  ")
        b4.configure(state='normal',text="  4  ");b5.configure(state='normal',text="  5  ");b6.configure(state='normal',text="  6  ")
        b7.configure(state='normal',text="  7  ");b8.configure(state='normal',text="  8  ");b9.configure(state='normal',text="  9  ")
    def work():
        z=0;nonlocal count
        if b1['text']==b2['text']==b3['text']:
            l1['text']=f"{b1['text']} WON";disble();z=1
        elif b1['text']==b5['text']==b9['text']:
            l1['text']=f"{b1['text']} WON";disble();z=1
        elif b1['text']==b4['text']==b7['text']:
            l1['text']=f"{b1['text']} WON";disble();z=1
        elif b2['text']==b5['text']==b8['text']:
            l1['text']=f"{b2['text']} WON";disble();z=1
        elif b3['text']==b6['text']==b9['text']:
            l1['text']=f"{b3['text']} WON";disble();z=1
        elif b4['text']==b5['text']==b6['text']:
            l1['text']=f"{b4['text']} WON";disble();z=1
        elif b7['text']==b8['text']==b9['text']:
            l1['text']=f"{b7['text']} WON";disble();z=1
        elif b3['text']==b5['text']==b7['text']:
            l1['text']=f"{b7['text']} WON";disble();z=1
        elif count==9:
            l1['text']="DRAW";z=1
        if(z==1):
            chime.theme('mario')
            chime.success()
            b10['text']='PLAY AGAIN'
            b10['state']=b11['state']=b13['state']=b17['state']=b18['state']=b23['state']='normal'
            if turn1!='gu est1':
                b15['state']='normal'
            if turn2!='gu est2':
                b16['state']='normal'
            if l1['text']==" X  WON": 
                mark('win')
            elif l1['text']==" O  WON":
                mark('loss')
            else:
                mark('draw')
    def mark(condition):
        nonlocal turn1,turn2
        if turn1!='gu est1':
            try:
                conn=sqlite3.connect('gfg.db')
                cursor = conn.execute(f"SELECT {condition} from {turn1} where serial=1;");point=cursor.fetchone()[0]
                conn.execute(f'''update {turn1} set {condition}={point+1} where serial=1;''')
                conn.commit()
                conn.close()
            except:
                turn1='gu est1';b15['state']='disable';b17['text']='WITH PROFILE'
        if condition=='loss':
            condition='win';print(condition)
        else:
            condition='loss'
        if turn2!='gu est2':
            try:
                conn=sqlite3.connect('gfg.db')
                cursor = conn.execute(f"SELECT {condition} from {turn2} where serial=1;");point=cursor.fetchone()[0]
                conn.execute(f'''update {turn2} set {condition}={point+1} where serial=1;''')
                conn.commit()
                conn.close()
            except:
                turn2='gu est2';b16['state']='disable';b18['text']='WITH PROFILE'
    def chng(b):
        nonlocal count
        if count%2==0:
            b['text']=" X ";count+=1
        else:
            b['text']=" O ";count+=1
        b['state']='disabled'
        chime.theme('chime')
        chime.info()
        if count>4:
            work()
    def credel(zero):
        if zero==True:
            adder=0
        else:
            adder=4
        def setnm():
            if ' ' in playername.get():
                messagebox.showinfo('information',"no space allowed in profile name!")
            elif playername.get()!="":
                try:
                    conn=sqlite3.connect('gfg.db')
                    if zero==True:
                        conn.execute(f'''CREATE TABLE {playername.get()}
                        (serial number(1),
                        WIN NUMBER(3),
                        LOSS NUMBER(3),
                        DRAW NUMBER(3));''')
                        conn.execute(f'''insert into {playername.get()} values(1,0,0,0);''')
                    else:
                        conn=sqlite3.connect('gfg.db')
                        conn.execute(f'''drop table {playername.get()};''')
                    conn.commit()
                    conn.close()
                except:
                    if zero==True:
                        messagebox.showwarning('warning',"profile already exists!choose another name.")
                    else:
                        messagebox.showwarning('warning',"profile doesn't exist!!!")
                else:
                    cncl()
                    if zero==True:
                        messagebox.showinfo('information','profile created!')
                    else:
                        messagebox.showinfo('information','profile deleted!')
            else:
                messagebox.showwarning('warning',"Enter name first")
        def cncl():
            stnm.destroy()
            b12.destroy()
            b14.destroy()
            b23['state']='normal'
            b11['state']='normal'
            b13['state']='normal'
            b17['state']='normal'
            b18['state']='normal'
            b10['state']='normal'
        playername=StringVar();stnm=Entry(f2,textvariable=playername,font="12",relief='sunken',bd=5,bg='red');stnm.grid(row=2+adder,column=0)
        b12=Button(f2,text="SET NAME",activebackground='red',font="Constantia 18 bold",fg="yellow",bg="black",bd=5,relief="raised",command=setnm);b12.grid(row=3+adder,column=0)
        b14=Button(f2,text="CANCEL",activebackground='red',font="Constantia 18 bold",fg="yellow",bg="black",bd=5,relief="raised",command=cncl);b14.grid(row=4+adder,column=0)
        b23['state']='disable'
        b10['state']='disable'
        b11['state']='disable'
        b13['state']='disable'
        b17['state']='disable'
        b18['state']='disable'
    def see(gtro):
        def setnm():
            nonlocal turn1,turn2
            if turn1==player_name.get() or turn2==player_name.get():
                messagebox.showwarning('warning',"can't set same name!!!")
            elif ' ' in player_name.get():
                messagebox.showinfo('information',"no space allowed in profile name!")
            elif player_name.get()!="":
                try:
                    conn=sqlite3.connect('gfg.db')
                    conn.execute(f'''select * from {player_name.get()};''')
                    conn.commit()
                    conn.close()
                except:
                    if gtro==0:
                        turn1='gu est1'
                    else:
                        turn2="gu est2"
                    messagebox.showwarning('warning',"profile doesn't exist!!!")
                else:
                    if gtro==0:
                        turn1=player_name.get()
                    else:
                        turn2=player_name.get()
                    cncl()
                    if gtro==0:
                        b17['text']=player_name.get()[0:12]
                    else:
                        b18['text']=player_name.get()[0:12]
                    messagebox.showinfo('information','got profile!')
                    if gtro==0:
                        b15['state']='normal'
                    else:
                        b16['state']='normal'
            else:
                messagebox.showwarning('warning',"set name first")
        def cncl():
            stnm_.destroy()
            b19.destroy()
            b20.destroy()
            b23['state']='normal'
            b11['state']='normal'
            b13['state']='normal'
            b17['state']='normal'
            b18['state']='normal'
            b10['state']='normal'
        player_name=StringVar();stnm_=Entry(f4,textvariable=player_name,font="12",relief='sunken',bd=5,bg='red');stnm_.grid(row=3,column=gtro)
        b19=Button(f4,text="ENTER",activebackground='red',font="Constantia 18 bold",fg="yellow",bg="black",bd=5,relief="raised",command=setnm);b19.grid(row=4,column=gtro)
        b20=Button(f4,text="CANCEL",activebackground='red',font="Constantia 18 bold",fg="yellow",bg="black",bd=5,relief="raised",command=cncl);b20.grid(row=5,column=gtro)
        b23['state']='disable'
        b10['state']='disable'
        b11['state']='disable'
        b13['state']='disable'
        b17['state']='disable'
        b18['state']='disable'
    def stats():
        def tknm():
            if ' ' in player_nam.get():
                messagebox.showinfo('information',"no space allowed in profile name!")
            elif player_nam.get()!="":
                try:
                    conn=sqlite3.connect('gfg.db')
                    cursor=conn.execute(f'''select * from {player_nam.get()};''');p=cursor.fetchone()
                    pstat=f"WIN:{p[1]} LOSS:{p[2]} DRAW:{p[3]}"
                    conn.commit()
                    conn.close()
                except:
                    messagebox.showwarning('warning',"profile doesn't exist!!!")
                else:
                    cncl()
                    messagebox.showinfo('information',f'{pstat}')
            else:
                messagebox.showwarning('warning',"set name first")
        def cncl():
            stnm_.destroy()
            b21.destroy()
            b22.destroy()
            b23['state']='normal'
            b11['state']='normal'
            b13['state']='normal'
            b17['state']='normal'
            b18['state']='normal'
            b10['state']='normal'
        player_nam=StringVar();stnm_=Entry(f4,textvariable=player_nam,font="12",relief='sunken',bd=5,bg='red');stnm_.grid(row=1,column=2)
        b21=Button(f4,text="ENTER",activebackground='red',font="Constantia 18 bold",fg="yellow",bg="black",bd=5,relief="raised",command=tknm);b21.grid(row=2,column=2)
        b22=Button(f4,text="CANCEL",activebackground='red',font="Constantia 18 bold",fg="yellow",bg="black",bd=5,relief="raised",command=cncl);b22.grid(row=3,column=2)
        b23['state']='disable'
        b10['state']='disable'
        b11['state']='disable'
        b13['state']='disable'
        b17['state']='disable'
        b18['state']='disable'
    fl=Frame(a,bg="black");fl.grid(row=0,column=0)
    fa=Frame(fl,relief="sunken",bd=5,bg="blue");fa.grid(row=0,column=0,padx=5,pady=5)
    f1=Frame(fa,relief="sunken",bd=5,bg="blue");f1.grid(row=0,column=0,padx=5,pady=5)
    b1=Button(f1,text="  1  ",font="Constantia 24 bold",fg="green",bg="black",bd=5,state='disable',relief="raised",command=lambda :chng(b1));b1.grid(row=0,column=0)
    b2=Button(f1,text="  2  ",font="Constantia 24 bold",fg="green",bg="black",bd=5,state='disable',relief="raised",command=lambda :chng(b2));b2.grid(row=0,column=1)
    b3=Button(f1,text="  3  ",font="Constantia 24 bold",fg="green",bg="black",bd=5,state='disable',relief="raised",command=lambda :chng(b3));b3.grid(row=0,column=2)
    b4=Button(f1,text="  4  ",font="Constantia 24 bold",fg="green",bg="black",bd=5,state='disable',relief="raised",command=lambda :chng(b4));b4.grid(row=1,column=0)
    b5=Button(f1,text="  5  ",font="Constantia 24 bold",fg="green",bg="black",bd=5,state='disable',relief="raised",command=lambda :chng(b5));b5.grid(row=1,column=1)
    b6=Button(f1,text="  6  ",font="Constantia 24 bold",fg="green",bg="black",bd=5,state='disable',relief="raised",command=lambda :chng(b6));b6.grid(row=1,column=2)
    b7=Button(f1,text="  7  ",font="Constantia 24 bold",fg="green",bg="black",bd=5,state='disable',relief="raised",command=lambda :chng(b7));b7.grid(row=2,column=0)
    b8=Button(f1,text="  8  ",font="Constantia 24 bold",fg="green",bg="black",bd=5,state='disable',relief="raised",command=lambda :chng(b8));b8.grid(row=2,column=1)
    b9=Button(f1,text="  9  ",font="Constantia 24 bold",fg="green",bg="black",bd=5,state='disable',relief="raised",command=lambda :chng(b9));b9.grid(row=2,column=2)
    l1=Label(fa,text="RESULT",fg="red",font="Constantia 24 bold",bg="black",bd=5,relief="flat");l1.grid(row=1,column=0)
    f2=Frame(fl,relief="sunken",bd=5,bg="black");f2.grid(row=0,column=1,padx=5,pady=5)
    b10=Button(f2,text="PLAY",activebackground='red',font="Constantia 24 bold",fg="yellow",bg="black",bd=5,relief="raised",command=anable);b10.grid(row=0,column=0)
    b11=Button(f2,text="CREATE PROFILE",activebackground='red',font="Constantia 18 bold",fg="yellow",bg="black",bd=5,relief="raised",command=lambda :credel(True));b11.grid(row=1,column=0)
    b13=Button(f2,text="DELETE PROFILE",activebackground='red',font="Constantia 18 bold",fg="yellow",bg="black",bd=5,relief="raised",command=lambda :credel(False));b13.grid(row=5,column=0)
    f4=Frame(a,bg="black");f4.grid(row=1,column=0)
    l2=Label(f4,text="PLAYER X",fg="red",font="Constantia 24 bold",bg="black",bd=5,relief="flat");l2.grid(row=0,column=0)
    l3=Label(f4,text="PLAYER O",fg="red",font="Constantia 24 bold",bg="black",bd=5,relief="flat");l3.grid(row=0,column=1)
    b15=Button(f4,text="AS GUEST",activebackground='red',font="Constantia 18 bold",fg="yellow",bg="black",bd=5,relief="raised",command=lambda :turny(False));b15.grid(row=1,column=0)
    b16=Button(f4,text="AS GUEST",activebackground='red',font="Constantia 18 bold",fg="yellow",bg="black",bd=5,relief="raised",command=lambda :turny(True));b16.grid(row=1,column=1)
    b17=Button(f4,text="WITH PROFILE",activebackground='red',font="Constantia 18 bold",fg="yellow",bg="black",bd=5,relief="raised",command=lambda :see(0));b17.grid(row=2,column=0)
    b18=Button(f4,text="WITH PROFILE",activebackground='red',font="Constantia 18 bold",fg="yellow",bg="black",bd=5,relief="raised",command=lambda :see(1));b18.grid(row=2,column=1)
    b23=Button(f4,text="PLAYER STATS",activebackground='red',font="Constantia 18 bold",fg="yellow",bg="black",bd=5,relief="raised",command=stats);b23.grid(row=0,column=2)
    a.mainloop()
def bmit():
    mainWin = Tk()
    mainWin.title("BMI Calculator")
    engine.setProperty('voice', voices[1].id)
    Label(mainWin, text="**************** Welcome To BMI Calculator ****************",font="Constantia 18 bold").grid(row=0, column = 0, columnspan=2)
    Label(mainWin,text="Enter your weight in Kilograms : ",font="Constantia 18 bold" ).grid(row=2,column=0,sticky=W)
    Label(mainWin,text="Enter your height in Meters : ",font="Constantia 18 bold").grid(row=3,column=0, sticky=W)
    w = Entry(mainWin,width=20,font="18",borderwidth=5)
    w.grid(row=2,column=1)
    h= Entry(mainWin,width=20,font="18",borderwidth=5)
    h.grid(row=3,column=1)
    def BMI():
        #Calculating the BMI 
        try:
            madhu=w.get()
            sudan=h.get()
            BMI=float(madhu)/float(sudan)**2
        except :
            kash['state']='disable'
            speak('Enter correct values first')
            kash['state']='normal'
        else:
            #Evaluating the BMI condition
            if BMI < 18.5:
                messagebox.showinfo("Your status","Oh no! Underweight, Your BMI : "+ str(BMI))
            elif BMI >= 18.5 and BMI < 25:
                messagebox.showinfo("Your status","Wow! Normal, Your BMI : "+ str(BMI))
            elif BMI >=25 and BMI < 30:
                messagebox.showinfo("Your status","Ops! Overweight, Your BMI : "+ str(BMI))
            else:
                messagebox.showinfo("Your status","OMG! Obesity, Your BMI : "+ str(BMI))
        exit()
    kash=Button(mainWin, text="Calculate", bg="#bbfa1b", activebackground="orange",font="Constantia 18 bold",command=lambda :Thread(target=BMI).start())
    kash.grid(row=4,column = 0, columnspan=2)
    speak('Welcome To BMI Calculator')
    mainWin.mainloop()
    exit()
def logo(man,eye):
    # import turtle library
    import turtle       
    my_window = turtle.Screen() ;my_window.title("AGE-2")
    my_window.bgcolor("#000000")       # creates a graphics window
    def left():
        my1= turtle.Turtle()
        my1.fillcolor(man)
        my1.begin_fill()
        my1.pensize(2)
        my1.color(man)
        my1.speed(10)
        my1.right(90)
        my1.forward(200)
        my1.right(150) 
        my1.forward(200)
        my1.left(15)
        my1.forward(200)
        my1.right(15) 
        my1.forward(200)
        my1.goto(0,0)
        my1.end_fill()
    def right():
        my= turtle.Turtle()  
        my.pensize(2)
        my.color(man)
        my.speed(10)    
        my.right(90) 
        my.forward(200)    
        my.left(150) 
        my.forward(200)
        my.right(15)    
        my.forward(200)
        my.left(15) 
        my.forward(200)
        my.goto(0,0)
    def reye():
        a= turtle.Turtle() 
        a.pensize(2)
        a.color(man)
        a.speed(10)
        a.right(15)
        a.forward(103.527618) 
        a.right(15)
        a.pencolor(eye)
        for i in range(0,5,2):
            a.fillcolor(man)
            a.begin_fill()
            a.forward(50-i)
            a.left(120)
            a.forward(70-i)
            a.left(135)
            a.forward(60-i)
            a.left(105)
            a.end_fill()
    def leye():
        b= turtle.Turtle() 
        b.pensize(2)
        b.color("black")
        b.speed(10)
        b.right(165)
        b.forward(103.527618) 
        b.left(15)
        b.pencolor(eye)
        for i in range(0,5,2):
            b.forward(50-i)
            b.right(120)
            b.forward(70-i)
            b.right(135)
            b.forward(60-i)
            b.right(105)
    left();right();reye();leye()
    speak('this ..is..')
    yes=turtle.Turtle();yes.speed(10)
    yes.left(90)
    yes.forward(200);yes.pencolor("grey")
    yes.write("PROMETHEUS", align="center", font=("Wide Latin", 25, "italic"));speak('prometheus')
    exit()
def key():
    from keyboard import is_pressed;from time import sleep
    while True:
        # It records all the keys until escape is pressed
        sleep(0.2)
        if niklo==True:
            print(niklo)
            import sys;sys.exit()
        if is_pressed('c+t'):
            copytext()
def exer():
    from time import sleep;from winsound import Beep;l=0
    while True:
        sleep(60);l+=1
        speak(f"{l}minutes completed sir")
if __name__ == "__main__":
    #first()
    speak('hello sir')#;exer()
    an=Thread(target=key);an.start()
    try:
        loh=Process(target=logo,args=("red","yellow"));loh.start()
    except:
        pass
    while True:
        query = takeCommand().lower()
        if 'search' in query:
            search(query.replace("search",""))
        elif 'voice reminder' in query or 'fix reminder' in query:
            speak("set voice command sir")
            reminder = takeCommand()
            pui = Process(target=alarmclock,args=(reminder,))
            pui.start()
        elif 'eye exercise' in query:
            speak('improve eyesight sir')
            exer()
        elif 'open task manager' in query:
            from os import system;jab=False
            dr=Process(target=system,args=("C:\Windows\System32\Taskmgr.exe",));dr.start()
            if jab:
                import sys;sys.exit()
            if jab==True:
                jab=False
            else:
                jab=True
        elif 'open bmi' in query:
            p = Process(target=bmit)
            p.start()
        elif 'youtube downloader' in query:
            p = Process(target=downloader)
            p.start()
        elif 'open youtube' in query:
            try:
                open_new_tab('http://www.youtube.com')
            except:
                speak('some problem occurred sir')
        elif 'open google' in query:
            try:
                open_new_tab('http://www.google.com')
            except:
                speak('some problem occurred sir')
        elif 'the time' in query:
            strTime = datetime.now().strftime("%H:%M:%S")   
            speak(f"Sir, the time is {strTime}")
        elif 'translate' in query:
            asks()
        elif 'open whatsapp' in query:
            whatsapp()
        elif 'send message on whatsapp' in query:
            from psutil import process_iter
            if ("WhatsApp.exe" in (i.name() for i in process_iter()))==False:
                whatsapp()
            try:
                whatsapp2()
            except:
                webwhat()
        elif 'translator' in query:
            translator()
        elif 'terminate yourself' in query or 'terminator yourself' in query:
            niklo=True
            speak('ok... bye sir... have a nice day')
            try:
                loh=Process(target=logo,args=("grey","#6699CC"));loh.start()
            except:
                pass
            exit()
        elif 'image to pdf' in query:
            impdf()
        elif 'copy text' in query:
            copytext()
        elif 'pdf text extractor' in query:
            try:
                pdftext()
            except:
                pass
        elif 'close' in query:
            speak('it will not save ..the work...sir...are you sure')
            permi=takeCommand().lower()
            if 'ofcourse' in permi or 'yes' in permi or 'why not' in permi:
                closit(query)
            else:
                speak('okay... i will not close')
        elif 'open' in query:
            openit(query)
        elif 'day name' in query or 'what day is today' in query or 'what is the day' in query:
            now=datetime.now()
            speak(now.strftime("%A"))
        else:
            if said:=chatbot(query):
                speak(said)
            if said=='let me see':
                if 'what is' in query or 'who is' in query:
                    try:
                        speak(summary(query[(query.find('is')+3):],sentences=2))
                    except:
                        speak('not able to find sir')
